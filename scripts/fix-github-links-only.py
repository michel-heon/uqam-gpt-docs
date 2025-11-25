#!/usr/bin/env python3
"""
Script optimisé pour remplacer UNIQUEMENT les liens GitHub par des liens Confluence
Ne modifie que les pages qui contiennent réellement des liens GitHub
"""

import os
import requests
import re


def main():
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    
    if not all([confluence_url, confluence_token]):
        print("❌ Variables d'environnement manquantes!")
        return
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Content-Type': 'application/json'
    }
    
    print("🔗 Remplacement des liens GitHub uniquement")
    print("=" * 80)
    
    # Mapping des liens GitHub vers les pages Confluence
    github_to_confluence = {
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Home': 'Documentation Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/': 'Documentation Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki': 'Documentation Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Guide-Demarrage-Rapide': 'Guide de démarrage rapide - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/FAQ': 'FAQ - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Support': 'Support - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Signalement-Problemes': 'Signalement des problèmes - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Politique-de-Confidentialite': 'Politique de confidentialité - Agent Postdoc',
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Conditions-Utilisation': "Conditions d'utilisation - Agent Postdoc",
        'https://github.com/michel-heon/uqam-gpt-docs/wiki/Configuration-URLs-Manifest': 'Configuration URLs et Manifest - Agent Postdoc'
    }
    
    # Pages à vérifier (seulement celles identifiées avec des liens GitHub)
    pages_to_check = [
        (337576940, 'Politique de confidentialité - Agent Postdoc'),
        (337576942, 'Configuration URLs et Manifest - Agent Postdoc')
    ]
    
    updated = 0
    
    for page_id, page_title in pages_to_check:
        print(f"\n📄 Vérification: {page_title}")
        
        # Récupérer la page
        response = requests.get(
            f'{confluence_url}/rest/api/content/{page_id}',
            headers=headers,
            params={'expand': 'body.storage,version'}
        )
        
        if response.status_code != 200:
            print(f"   ❌ Erreur de récupération")
            continue
        
        data = response.json()
        content = data['body']['storage']['value']
        version = data['version']['number']
        
        # Vérifier s'il y a des liens GitHub
        has_github = 'github.com/michel-heon/uqam-gpt-docs' in content
        
        if not has_github:
            print(f"   ⏭️  Aucun lien GitHub, page ignorée")
            continue
        
        # Compter les liens avant
        github_count_before = len(re.findall(r'github\.com/michel-heon/uqam-gpt-docs', content))
        print(f"   🔍 {github_count_before} lien(s) GitHub trouvé(s)")
        
        # Remplacer tous les liens GitHub
        original_content = content
        replacements = 0
        
        for github_url, confluence_title in github_to_confluence.items():
            if github_url in content:
                # Créer le lien Confluence
                confluence_link = f'<ac:link><ri:page ri:content-title="{confluence_title}" /><ac:plain-text-link-body><![CDATA[{confluence_title}]]></ac:plain-text-link-body></ac:link>'
                
                # Remplacer toutes les occurrences
                count = content.count(github_url)
                if count > 0:
                    content = content.replace(github_url, confluence_link)
                    replacements += count
                    print(f"   ✓ {github_url} → {confluence_title} ({count}x)")
        
        if replacements == 0:
            print(f"   ⚠️  Aucun remplacement effectué (peut-être des URLs différentes)")
            continue
        
        # Mettre à jour la page
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
        
        response = requests.put(
            f'{confluence_url}/rest/api/content/{page_id}',
            headers=headers,
            json=update_data
        )
        
        if response.status_code == 200:
            print(f"   ✅ Page mise à jour (v{version} → v{version + 1})")
            print(f"   📊 {replacements} lien(s) remplacé(s)")
            updated += 1
        else:
            print(f"   ❌ Erreur de mise à jour: {response.status_code}")
            print(f"      {response.text[:200]}")
    
    print("\n" + "=" * 80)
    print(f"✨ Terminé: {updated} page(s) mise(s) à jour")
    print("=" * 80)


if __name__ == '__main__':
    main()
