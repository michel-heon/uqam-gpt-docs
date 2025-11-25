#!/usr/bin/env python3
"""
Script pour ajuster les liens internes dans les pages Confluence
Convertit les liens markdown vers des liens Confluence
"""

import os
import sys
import re
import requests
from pathlib import Path


def get_all_migrated_pages(confluence_url: str, token: str, parent_id: str):
    """Récupère toutes les pages migrées sous le parent"""
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    # Récupérer la page parent avec ses enfants
    url = f"{confluence_url}/rest/api/content/{parent_id}/child/page"
    params = {'expand': 'children.page', 'limit': 100}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code}")
        return {}
    
    results = response.json().get('results', [])
    
    # Créer un mapping titre → ID
    page_map = {}
    for page in results:
        page_map[page['title']] = page['id']
        
        # Récupérer les enfants de "Documentation Agent Postdoc"
        if 'Documentation Agent Postdoc' in page['title']:
            child_url = f"{confluence_url}/rest/api/content/{page['id']}/child/page"
            child_response = requests.get(child_url, headers=headers, params={'limit': 100})
            if child_response.status_code == 200:
                children = child_response.json().get('results', [])
                for child in children:
                    page_map[child['title']] = child['id']
    
    return page_map


def update_page_links(confluence_url: str, token: str, page_id: str, page_map: dict, space_key: str):
    """Met à jour les liens dans une page Confluence"""
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Récupérer le contenu actuel
    url = f"{confluence_url}/rest/api/content/{page_id}"
    params = {'expand': 'body.storage,version'}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return False
    
    page_data = response.json()
    title = page_data['title']
    content = page_data['body']['storage']['value']
    version = page_data['version']['number']
    
    # Mapping des liens internes (format markdown → titre Confluence)
    link_mapping = {
        'Guide-Demarrage-Rapide': 'Guide de démarrage rapide - Agent Postdoc',
        'FAQ': 'FAQ - Agent Postdoc',
        'Support': 'Support - Agent Postdoc',
        'Home': 'Documentation Agent Postdoc',
        'Politique-de-Confidentialite': 'Politique de confidentialité - Agent Postdoc',
        'Signalement-Problemes': 'Signalement des problèmes - Agent Postdoc',
        'Conditions-Utilisation': "Conditions d'utilisation - Agent Postdoc",
        'Configuration-URLs-Manifest': 'Configuration URLs et Manifest - Agent Postdoc'
    }
    
    # Trouver et remplacer les liens
    original_content = content
    updated = False
    
    # Pattern pour les liens wiki markdown: [texte](Page-Name) ou [texte](Page-Name.md)
    for md_link, confluence_title in link_mapping.items():
        if confluence_title not in page_map:
            continue
        
        target_page_id = page_map[confluence_title]
        
        # Patterns à remplacer
        patterns = [
            # [texte](Page-Name)
            (rf'<a href="{md_link}"([^>]*)>([^<]+)</a>',
             rf'<ac:link><ri:page ri:content-title="{confluence_title}" /><ac:plain-text-link-body><![CDATA[\2]]></ac:plain-text-link-body></ac:link>'),
            
            # Liens simples dans le texte HTML
            (rf'href="{md_link}"',
             f'href="/pages/viewpage.action?pageId={target_page_id}"'),
            
            # Liens avec .md
            (rf'href="{md_link}\.md"',
             f'href="/pages/viewpage.action?pageId={target_page_id}"'),
            
            # Liens avec ancres (Support.md#troubleshooting)
            (rf'href="{md_link}\.md#([^"]+)"',
             f'href="/pages/viewpage.action?pageId={target_page_id}#\\1"'),
        ]
        
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                content = new_content
                updated = True
    
    if not updated:
        return None  # Aucune modification
    
    # Mettre à jour la page
    update_data = {
        'id': page_id,
        'type': 'page',
        'title': title,
        'space': {'key': space_key},
        'body': {
            'storage': {
                'value': content,
                'representation': 'storage'
            }
        },
        'version': {
            'number': version + 1,
            'message': 'Mise à jour des liens internes'
        }
    }
    
    response = requests.put(url, json=update_data, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print(f"❌ Erreur mise à jour {title}: {response.status_code}")
        print(response.text[:500])
        return False


def main():
    """Point d'entrée"""
    
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    space_key = os.getenv('CONFLUENCE_SPACE', 'UQAMGPT')
    
    if not confluence_url or not confluence_token:
        print("❌ Variables d'environnement manquantes!")
        return 1
    
    print("🔗 Ajustement des liens internes dans Confluence")
    print("=" * 80)
    
    # ID de la page "08 - UQAM-GPT: Support et Maintenance"
    parent_id = "255302222"
    
    print(f"\n📚 Récupération de la liste des pages...")
    page_map = get_all_migrated_pages(confluence_url, confluence_token, parent_id)
    
    print(f"✅ {len(page_map)} pages trouvées:")
    for title, page_id in page_map.items():
        print(f"   • {title} (ID: {page_id})")
    
    print(f"\n🔧 Mise à jour des liens internes...")
    
    updated_count = 0
    skipped_count = 0
    
    for title, page_id in page_map.items():
        if 'Agent Postdoc' not in title:
            continue  # Ignorer les autres pages
        
        print(f"\n   📄 {title}...")
        result = update_page_links(confluence_url, confluence_token, page_id, page_map, space_key)
        
        if result is True:
            print(f"      ✅ Liens mis à jour")
            updated_count += 1
        elif result is None:
            print(f"      ⏭️  Aucun lien à ajuster")
            skipped_count += 1
        else:
            print(f"      ❌ Échec")
    
    print("\n" + "=" * 80)
    print(f"✨ Terminé!")
    print(f"   • Pages mises à jour: {updated_count}")
    print(f"   • Pages sans modification: {skipped_count}")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
