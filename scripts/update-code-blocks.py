#!/usr/bin/env python3
"""
Script pour mettre à jour le contenu des pages avec les blocs de code corrigés
"""

import os
import sys
import importlib.util
from pathlib import Path

# Charger le module confluence-rest-api.py
spec = importlib.util.spec_from_file_location(
    "confluence_rest_api",
    Path(__file__).parent / "confluence-rest-api.py"
)
confluence_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(confluence_module)

ConfluenceServerAPI = confluence_module.ConfluenceServerAPI
MarkdownToConfluence = confluence_module.MarkdownToConfluence


def update_pages_content():
    """Met à jour le contenu des pages existantes avec les blocs de code corrigés"""
    
    # Configuration depuis les variables d'environnement
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    confluence_space = os.getenv('CONFLUENCE_SPACE')
    
    if not all([confluence_url, confluence_token, confluence_space]):
        print("❌ Variables d'environnement manquantes!")
        print("   Assurez-vous que CONFLUENCE_URL, CONFLUENCE_TOKEN et CONFLUENCE_SPACE sont définis")
        return
    
    # Initialiser l'API
    api = ConfluenceServerAPI(confluence_url, confluence_token, confluence_space)
    converter = MarkdownToConfluence(confluence_space)
    
    print("🔧 Mise à jour du contenu des pages avec blocs de code corrigés")
    print("=" * 80)
    
    # Mapping des pages à mettre à jour
    pages_to_update = [
        {
            'title': 'Documentation Agent Postdoc',
            'file': 'postdoc/Home.md'
        },
        {
            'title': 'Guide de démarrage rapide - Agent Postdoc',
            'file': 'postdoc/Guide-Demarrage-Rapide.md'
        },
        {
            'title': 'FAQ - Agent Postdoc',
            'file': 'postdoc/FAQ.md'
        },
        {
            'title': 'Support - Agent Postdoc',
            'file': 'postdoc/Support.md'
        },
        {
            'title': 'Signalement des problèmes - Agent Postdoc',
            'file': 'postdoc/Signalement-Problemes.md'
        },
        {
            'title': 'Politique de confidentialité - Agent Postdoc',
            'file': 'postdoc/Politique-de-Confidentialite.md'
        },
        {
            'title': 'Conditions d\'utilisation - Agent Postdoc',
            'file': 'postdoc/Conditions-Utilisation.md'
        },
        {
            'title': 'Configuration URLs et Manifest - Agent Postdoc',
            'file': 'postdoc/Configuration-URLs-Manifest.md'
        }
    ]
    
    updated_count = 0
    error_count = 0
    
    workspace_root = Path(__file__).parent.parent
    
    for page_info in pages_to_update:
        title = page_info['title']
        file_path = workspace_root / page_info['file']
        
        print(f"\n   📄 {title}...")
        
        # Vérifier que le fichier existe
        if not file_path.exists():
            print(f"      ⚠️  Fichier non trouvé: {file_path}")
            error_count += 1
            continue
        
        # Lire le contenu markdown
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convertir en format Confluence
        confluence_content = converter.convert(md_content)
        
        # Récupérer la page existante
        existing_page = api.find_page_by_title(title)
        if not existing_page:
            print(f"      ⚠️  Page non trouvée dans Confluence")
            error_count += 1
            continue
        
        # Mettre à jour la page
        updated_page = api.update_page(
            page_id=existing_page['id'],
            title=title,
            content=confluence_content,
            version=existing_page['version']['number']
        )
        
        if updated_page:
            print(f"      ✅ Contenu mis à jour (version {updated_page['version']['number']})")
            updated_count += 1
        else:
            print(f"      ❌ Erreur lors de la mise à jour")
            error_count += 1
    
    # Résumé
    print("\n" + "=" * 80)
    print("✨ Mise à jour terminée!")
    print(f"   • Pages mises à jour: {updated_count}")
    if error_count > 0:
        print(f"   • Erreurs: {error_count}")
    print("=" * 80)


if __name__ == '__main__':
    update_pages_content()
