#!/usr/bin/env python3
"""
Script pour corriger les liens internes dans les pages Confluence
Remplace les liens <a href="Page-Name"> par des liens Confluence natifs
"""

import os
import requests
import re


def get_page_id_by_title(confluence_url, headers, space_key, title):
    """Récupère l'ID d'une page par son titre"""
    url = f"{confluence_url}/rest/api/content"
    params = {
        'spaceKey': space_key,
        'title': title,
        'expand': 'version'
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]['id']
    return None


def fix_page_links(confluence_url, headers, space_key, page_id, page_map):
    """Corrige les liens d'une page"""
    
    # Récupérer le contenu actuel
    url = f"{confluence_url}/rest/api/content/{page_id}"
    params = {'expand': 'body.storage,version'}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return False, "Erreur de récupération"
    
    page_data = response.json()
    title = page_data['title']
    content = page_data['body']['storage']['value']
    version = page_data['version']['number']
    
    # Mapping des liens internes (slug markdown → titre Confluence complet)
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
    
    original_content = content
    replacements = 0
    
    # Remplacer chaque type de lien
    for md_link, confluence_title in link_mapping.items():
        if confluence_title not in page_map:
            continue
        
        target_page_id = page_map[confluence_title]
        
        # Pattern 1: <a href="Page-Name">texte</a>
        pattern1 = rf'<a href="{md_link}">([^<]+)</a>'
        replacement1 = f'<ac:link><ri:page ri:content-title="{confluence_title}" /><ac:plain-text-link-body><![CDATA[\\1]]></ac:plain-text-link-body></ac:link>'
        new_content = re.sub(pattern1, replacement1, content)
        if new_content != content:
            count = len(re.findall(pattern1, content))
            replacements += count
            content = new_content
        
        # Pattern 2: <a href="Page-Name.md">texte</a>
        pattern2 = rf'<a href="{md_link}\.md">([^<]+)</a>'
        replacement2 = f'<ac:link><ri:page ri:content-title="{confluence_title}" /><ac:plain-text-link-body><![CDATA[\\1]]></ac:plain-text-link-body></ac:link>'
        new_content = re.sub(pattern2, replacement2, content)
        if new_content != content:
            count = len(re.findall(pattern2, content))
            replacements += count
            content = new_content
        
        # Pattern 3: <a href="Page-Name.md#anchor">texte</a>
        pattern3 = rf'<a href="{md_link}\.md#([^"]+)">([^<]+)</a>'
        replacement3 = f'<ac:link ac:anchor="\\1"><ri:page ri:content-title="{confluence_title}" /><ac:plain-text-link-body><![CDATA[\\2]]></ac:plain-text-link-body></ac:link>'
        new_content = re.sub(pattern3, replacement3, content)
        if new_content != content:
            count = len(re.findall(pattern3, content))
            replacements += count
            content = new_content
    
    if content == original_content:
        return True, "Aucun changement"
    
    # Mettre à jour la page
    update_url = f"{confluence_url}/rest/api/content/{page_id}"
    update_data = {
        'version': {'number': version + 1},
        'title': title,
        'type': 'page',
        'body': {
            'storage': {
                'value': content,
                'representation': 'storage'
            }
        }
    }
    
    response = requests.put(update_url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        return True, f"{replacements} liens corrigés"
    else:
        return False, f"Erreur {response.status_code}: {response.text[:200]}"


def main():
    """Corrige les liens de toutes les pages"""
    
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    confluence_space = os.getenv('CONFLUENCE_SPACE')
    
    if not all([confluence_url, confluence_token, confluence_space]):
        print("❌ Variables d'environnement manquantes!")
        return
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Content-Type': 'application/json'
    }
    
    print("🔗 Correction des liens internes")
    print("=" * 80)
    
    # Liste des pages à corriger
    pages = [
        'Documentation Agent Postdoc',
        'Guide de démarrage rapide - Agent Postdoc',
        'FAQ - Agent Postdoc',
        'Support - Agent Postdoc',
        'Signalement des problèmes - Agent Postdoc',
        'Politique de confidentialité - Agent Postdoc',
        "Conditions d'utilisation - Agent Postdoc",
        'Configuration URLs et Manifest - Agent Postdoc'
    ]
    
    # Construire la map titre → ID
    print("\n📚 Récupération des IDs de pages...")
    page_map = {}
    for title in pages:
        page_id = get_page_id_by_title(confluence_url, headers, confluence_space, title)
        if page_id:
            page_map[title] = page_id
            print(f"   ✅ {title}: {page_id}")
        else:
            print(f"   ❌ {title}: non trouvée")
    
    print(f"\n🔧 Correction des liens dans {len(page_map)} pages...")
    
    success_count = 0
    error_count = 0
    
    for title in pages:
        if title not in page_map:
            continue
        
        page_id = page_map[title]
        print(f"\n   📄 {title}...")
        
        success, message = fix_page_links(confluence_url, headers, confluence_space, page_id, page_map)
        
        if success:
            print(f"      ✅ {message}")
            success_count += 1
        else:
            print(f"      ❌ {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print("✨ Terminé!")
    print(f"   • Pages mises à jour: {success_count}")
    if error_count > 0:
        print(f"   • Erreurs: {error_count}")
    print("=" * 80)


if __name__ == '__main__':
    main()
