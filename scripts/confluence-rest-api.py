#!/usr/bin/env python3
"""
Script de migration de documentation markdown vers Confluence Server
Utilise l'API REST de Confluence Server (wiki.uqam.ca)

Prérequis:
- Python 3.7+
- pip install requests markdown beautifulsoup4

Configuration:
1. Créer un Personal Access Token dans Confluence:
   - Aller sur https://wiki.uqam.ca/plugins/personalaccesstokens/usertokens.action
   - Cliquer sur "Create token"
   - Copier le token généré

2. Définir les variables d'environnement:
   export CONFLUENCE_URL="https://wiki.uqam.ca"
   export CONFLUENCE_TOKEN="votre_token"
   export CONFLUENCE_SPACE="UQAMGPT"
"""

import os
import sys
import json
import requests
import markdown
from pathlib import Path
from typing import Dict, List, Optional
from bs4 import BeautifulSoup


class ConfluenceServerAPI:
    """Client pour l'API REST de Confluence Server"""
    
    def __init__(self, base_url: str, token: str, space_key: str):
        self.base_url = base_url.rstrip('/')
        self.space_key = space_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get_space(self) -> Optional[Dict]:
        """Récupère les informations de l'espace"""
        url = f"{self.base_url}/rest/api/space/{self.space_key}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        print(f"Erreur lors de la récupération de l'espace: {response.status_code}")
        print(response.text)
        return None
    
    def find_page_by_title(self, title: str) -> Optional[Dict]:
        """Cherche une page par titre dans l'espace"""
        url = f"{self.base_url}/rest/api/content"
        params = {
            'title': title,
            'spaceKey': self.space_key,
            'expand': 'version,body.storage'
        }
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            return results[0] if results else None
        return None
    
    def create_page(self, title: str, content: str, parent_id: Optional[str] = None) -> Optional[Dict]:
        """Crée une nouvelle page dans Confluence"""
        url = f"{self.base_url}/rest/api/content"
        
        data = {
            'type': 'page',
            'title': title,
            'space': {'key': self.space_key},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }
        
        if parent_id:
            data['ancestors'] = [{'id': parent_id}]
        
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        
        print(f"Erreur lors de la création de la page '{title}': {response.status_code}")
        print(response.text)
        return None
    
    def update_page(self, page_id: str, title: str, content: str, version: int) -> Optional[Dict]:
        """Met à jour une page existante"""
        url = f"{self.base_url}/rest/api/content/{page_id}"
        
        data = {
            'id': page_id,
            'type': 'page',
            'title': title,
            'space': {'key': self.space_key},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            },
            'version': {
                'number': version + 1
            }
        }
        
        response = self.session.put(url, json=data)
        if response.status_code == 200:
            return response.json()
        
        print(f"Erreur lors de la mise à jour de la page '{title}': {response.status_code}")
        print(response.text)
        return None


class MarkdownToConfluence:
    """Convertit le Markdown en format Confluence Storage"""
    
    def __init__(self, space_key: str):
        self.space_key = space_key
    
    def convert(self, md_content: str) -> str:
        """
        Convertit le Markdown en HTML Confluence Storage Format
        """
        # Conversion Markdown → HTML
        html = markdown.markdown(
            md_content,
            extensions=[
                'extra',
                'codehilite',
                'tables',
                'toc',
                'fenced_code'
            ]
        )
        
        # Nettoyage et adaptation pour Confluence
        soup = BeautifulSoup(html, 'html.parser')
        
        # Convertir les blocs de code
        for code_block in soup.find_all('pre'):
            code = code_block.find('code')
            if code:
                language = ''
                # Extraire le langage des classes
                classes = code.get('class', [])
                for cls in classes:
                    if cls.startswith('language-'):
                        language = cls.replace('language-', '')
                        break
                
                # Obtenir le contenu du code (texte brut)
                code_content = code.get_text()
                
                # Créer la macro Confluence manuellement (BeautifulSoup ne gère pas bien CDATA)
                macro_xml = f'<ac:structured-macro ac:name="code" ac:schema-version="1">'
                
                if language:
                    macro_xml += f'<ac:parameter ac:name="language">{language}</ac:parameter>'
                
                # Échapper le contenu pour XML
                code_escaped = (code_content
                    .replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;'))
                
                macro_xml += f'<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>'
                macro_xml += '</ac:structured-macro>'
                
                # Créer un nouveau tag à partir du XML
                from bs4 import BeautifulSoup as BS
                macro_soup = BS(macro_xml, 'html.parser')
                code_block.replace_with(macro_soup)
        
        # Convertir les tableaux (Confluence supporte les tables HTML basiques)
        # Pas de conversion nécessaire pour les tables simples
        
        # Convertir les liens relatifs en liens Confluence
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.endswith('.md'):
                # Lien vers un fichier markdown → lien Confluence
                page_title = href.replace('.md', '').replace('-', ' ').title()
                link['href'] = f'/spaces/{self.space_key}/pages/viewpage.action?title={page_title}'
        
        return str(soup)


def migrate_documentation(confluence_api: ConfluenceServerAPI, docs_path: Path):
    """
    Migre toute la documentation vers Confluence
    
    Structure des pages sous "08 - UQAM-GPT: Support et Maintenance":
    - Documentation Agent Postdoc (parent)
      - Guide de démarrage rapide
      - FAQ
      - Support
      - Signalement des problèmes
      - Politique de confidentialité
      - Conditions d'utilisation
      - Configuration URLs et Manifest
    """
    
    converter = MarkdownToConfluence(confluence_api.space_key)
    
    # Trouver l'ID de la page "08 - UQAM-GPT: Support et Maintenance"
    print("🔍 Recherche de la page parent '08 - UQAM-GPT: Support et Maintenance'...")
    parent_section = confluence_api.find_page_by_title('08 - UQAM-GPT: Support et Maintenance')
    
    if not parent_section:
        print("❌ Page parent '08 - UQAM-GPT: Support et Maintenance' introuvable!")
        print("💡 Vérifiez que cette page existe dans Confluence")
        return
    
    parent_section_id = parent_section['id']
    print(f"✅ Page parent trouvée (ID: {parent_section_id})")
    
    # Mapping fichiers → titres Confluence
    pages_to_migrate = [
        {
            'file': 'postdoc/Home.md',
            'title': 'Documentation Agent Postdoc',
            'parent': '08 - UQAM-GPT: Support et Maintenance',
            'parent_id': parent_section_id
        },
        {
            'file': 'postdoc/Guide-Demarrage-Rapide.md',
            'title': 'Guide de démarrage rapide - Agent Postdoc',
            'parent': 'Documentation Agent Postdoc'
        },
        {
            'file': 'postdoc/FAQ.md',
            'title': 'FAQ - Agent Postdoc',
            'parent': 'Documentation Agent Postdoc'
        },
        {
            'file': 'postdoc/Support.md',
            'title': 'Support - Agent Postdoc',
            'parent': 'Documentation Agent Postdoc'
        },
        {
            'file': 'postdoc/Signalement-Problemes.md',
            'title': 'Signalement des problèmes - Agent Postdoc',
            'parent': 'Documentation Agent Postdoc'
        },
        {
            'file': 'postdoc/Politique-de-Confidentialite.md',
            'title': 'Politique de confidentialité - Agent Postdoc',
            'parent': 'Documentation Agent Postdoc'
        },
        {
            'file': 'postdoc/Conditions-Utilisation.md',
            'title': "Conditions d'utilisation - Agent Postdoc",
            'parent': 'Documentation Agent Postdoc'
        },
        {
            'file': 'postdoc/Configuration-URLs-Manifest.md',
            'title': 'Configuration URLs et Manifest - Agent Postdoc',
            'parent': 'Documentation Agent Postdoc'
        }
    ]
    
    # Cache des IDs de pages créées
    page_ids = {}
    
    for page_info in pages_to_migrate:
        file_path = docs_path / page_info['file']
        
        if not file_path.exists():
            print(f"⚠️  Fichier introuvable: {file_path}")
            continue
        
        print(f"\n📄 Traitement: {page_info['title']}...")
        
        # Lire le contenu markdown
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convertir en format Confluence
        confluence_content = converter.convert(md_content)
        
        # Déterminer le parent ID si nécessaire
        parent_id = page_info.get('parent_id')  # ID explicite fourni
        if not parent_id and page_info.get('parent'):
            parent_id = page_ids.get(page_info['parent'])
            if not parent_id:
                print(f"⚠️  Parent '{page_info['parent']}' non trouvé, page créée à la racine")
        
        # Vérifier si la page existe déjà
        existing_page = confluence_api.find_page_by_title(page_info['title'])
        
        if existing_page:
            print(f"   Page existante trouvée (ID: {existing_page['id']})")
            result = confluence_api.update_page(
                page_id=existing_page['id'],
                title=page_info['title'],
                content=confluence_content,
                version=existing_page['version']['number']
            )
            if result:
                print(f"✅ Page mise à jour: {page_info['title']}")
                page_ids[page_info['title']] = existing_page['id']
        else:
            result = confluence_api.create_page(
                title=page_info['title'],
                content=confluence_content,
                parent_id=parent_id
            )
            if result:
                print(f"✅ Page créée: {page_info['title']} (ID: {result['id']})")
                page_ids[page_info['title']] = result['id']
    
    print("\n" + "="*60)
    print(f"✨ Migration terminée! {len(page_ids)} pages traitées.")
    print("="*60)


def main():
    """Point d'entrée principal"""
    
    # Charger les variables depuis .env si le fichier existe
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        print(f"📝 Chargement de la configuration depuis {env_file}")
        # Note: Les variables doivent être sourcées dans le shell avant d'exécuter ce script
        # Exemple: source scripts/.env && python3 scripts/confluence-rest-api.py
    
    # Vérifier les variables d'environnement
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    space_key = os.getenv('CONFLUENCE_SPACE', 'UQAMGPT')
    
    if not confluence_url or not confluence_token:
        print("❌ Erreur: Variables d'environnement manquantes!")
        print("\nVeuillez définir:")
        print("  export CONFLUENCE_URL='https://wiki.uqam.ca'")
        print("  export CONFLUENCE_TOKEN='votre_token'")
        print("  export CONFLUENCE_SPACE='UQAMGPT'  # (optionnel)")
        print("\nPour créer un token:")
        print("  https://wiki.uqam.ca/plugins/personalaccesstokens/usertokens.action")
        sys.exit(1)
    
    # Initialiser l'API
    api = ConfluenceServerAPI(confluence_url, confluence_token, space_key)
    
    # Vérifier l'accès à l'espace
    print(f"🔍 Vérification de l'espace '{space_key}'...")
    space_info = api.get_space()
    if not space_info:
        print(f"❌ Impossible d'accéder à l'espace '{space_key}'")
        sys.exit(1)
    
    print(f"✅ Espace trouvé: {space_info.get('name', space_key)}")
    
    # Déterminer le chemin de la documentation
    docs_path = Path(__file__).parent.parent
    print(f"📁 Dossier de documentation: {docs_path}")
    
    # Lancer la migration
    migrate_documentation(api, docs_path)


if __name__ == '__main__':
    main()
