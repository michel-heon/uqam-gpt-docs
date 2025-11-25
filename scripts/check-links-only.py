#!/usr/bin/env python3
"""
Script SIMPLIFIÉ pour corriger uniquement les liens internes cassés
Ne modifie une page que si elle contient réellement des liens HTML à corriger
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
    
    print("🔗 Vérification des liens internes")
    print("=" * 80)
    print("\n⏱️  Cette opération peut prendre quelques secondes...\n")
    
    # Liste des pages
    pages = [
        (337576935, 'Documentation Agent Postdoc'),
        (337576936, 'Guide de démarrage rapide - Agent Postdoc'),
        (337576937, 'FAQ - Agent Postdoc'),
        (337576938, 'Support - Agent Postdoc'),
        (337576939, 'Signalement des problèmes - Agent Postdoc'),
        (337576940, 'Politique de confidentialité - Agent Postdoc'),
        (337576941, "Conditions d'utilisation - Agent Postdoc"),
        (337576942, 'Configuration URLs et Manifest - Agent Postdoc')
    ]
    
    pages_with_html_links = 0
    pages_checked = 0
    
    for page_id, page_title in pages:
        pages_checked += 1
        
        # Récupérer la page
        response = requests.get(
            f'{confluence_url}/rest/api/content/{page_id}',
            headers=headers,
            params={'expand': 'body.storage,version'},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ {page_title}: Erreur de récupération")
            continue
        
        data = response.json()
        content = data['body']['storage']['value']
        version = data['version']['number']
        
        # Vérifier s'il y a des liens HTML internes (mauvais format)
        # Chercher <a href="..."> qui ne sont PAS des liens Confluence
        html_links = re.findall(r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', content)
        
        # Filtrer pour garder seulement les liens internes (pas http://, pas #)
        internal_html_links = [
            link for link, text in html_links 
            if not link.startswith('http') and not link.startswith('#') and not link.startswith('mailto:')
        ]
        
        if internal_html_links:
            pages_with_html_links += 1
            print(f"⚠️  {page_title} (v{version})")
            print(f"    Trouvé {len(internal_html_links)} lien(s) HTML interne(s)")
            for link in set(internal_html_links[:5]):  # Max 5 exemples
                print(f"      • {link}")
        else:
            print(f"✅ {page_title} (v{version}) - OK")
    
    print("\n" + "=" * 80)
    print(f"📊 Résumé:")
    print(f"   • Pages vérifiées: {pages_checked}")
    print(f"   • Pages avec liens HTML: {pages_with_html_links}")
    
    if pages_with_html_links == 0:
        print("\n✅ Tous les liens sont déjà au format Confluence!")
        print("   Aucune action nécessaire.")
    else:
        print(f"\n⚠️  {pages_with_html_links} page(s) nécessitent une correction")
        print("   💡 Note: Les liens HTML dans les blocs de code sont normaux")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
