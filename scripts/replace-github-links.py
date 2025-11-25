#!/usr/bin/env python3
"""
Script pour remplacer tous les liens GitHub wiki par des liens Confluence
"""

import os
import requests
import re


def replace_github_links():
    """Remplace tous les liens GitHub wiki par des liens Confluence"""
    
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Content-Type': 'application/json'
    }
    
    # Mapping des URLs GitHub → titres Confluence
    link_mapping = {
        'https://github.com/michel-heon/uqam-gpt-docs/wiki': 'Documentation Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Home': 'Documentation Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Politique-de-Confidentialite': 'Politique de confidentialité - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Conditions-Utilisation': "Conditions d'utilisation - Agent Postdoc",
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Guide-Demarrage-Rapide': 'Guide de démarrage rapide - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/FAQ': 'FAQ - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Support': 'Support - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Signalement-Problemes': 'Signalement des problèmes - Agent Postdoc',
    }
    
    print("🔗 Remplacement des liens GitHub wiki par des liens Confluence")
    print("=" * 80)
    
    # Page à corriger
    page_id = 337576942
    page_title = 'Configuration URLs et Manifest - Agent Postdoc'
    
    # Récupérer la page
    url = f'{confluence_url}/rest/api/content/{page_id}'
    params = {'expand': 'body.storage,version'}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Erreur de récupération: {response.status_code}")
        return
    
    page_data = response.json()
    content = page_data['body']['storage']['value']
    version = page_data['version']['number']
    
    print(f"\n📄 {page_title} (version {version})")
    
    original_content = content
    replacements = 0
    
    # Remplacer chaque lien GitHub
    for github_url, confluence_title in link_mapping.items():
        # Pattern: <a href="github_url">texte</a>
        # On garde le texte du lien original
        pattern = rf'<a href="{re.escape(github_url)}"([^>]*)>([^<]+)</a>'
        
        def replace_link(match):
            nonlocal replacements
            attrs = match.group(1)  # Attributs supplémentaires (ex: class, target)
            link_text = match.group(2)  # Texte du lien
            
            # Créer le lien Confluence
            confluence_link = f'<ac:link><ri:page ri:content-title="{confluence_title}" /><ac:plain-text-link-body><![CDATA[{link_text}]]></ac:plain-text-link-body></ac:link>'
            
            replacements += 1
            return confluence_link
        
        content = re.sub(pattern, replace_link, content)
    
    if content == original_content:
        print("   ⏭️  Aucun lien à remplacer")
        return
    
    print(f"   🔧 {replacements} lien(s) à remplacer...")
    
    # Mettre à jour la page
    update_url = f'{confluence_url}/rest/api/content/{page_id}'
    update_data = {
        'version': {'number': version + 1},
        'title': page_title,
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
        new_version = response.json()['version']['number']
        print(f"   ✅ Page mise à jour (version {new_version})")
    else:
        print(f"   ❌ Erreur de mise à jour: {response.status_code}")
        print(f"   {response.text[:300]}")
    
    print("\n" + "=" * 80)
    print("✨ Terminé!")
    print("=" * 80)


if __name__ == '__main__':
    replace_github_links()
