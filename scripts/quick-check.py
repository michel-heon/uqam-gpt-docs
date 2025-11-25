#!/usr/bin/env python3
"""
Script de vérification rapide de l'état du wiki
Affiche un résumé des pages et détecte les problèmes potentiels
"""
import os
import sys
import requests
import re

def quick_check():
    """Vérification rapide de l'état du wiki"""
    
    # Charger les variables d'environnement
    env_file = 'scripts/.env'
    if not os.path.exists(env_file):
        print('❌ Fichier scripts/.env manquant!')
        print('💡 Copiez scripts/.env.example et configurez vos credentials')
        sys.exit(1)
    
    # Charger les variables
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                if 'export' in line:
                    line = line.replace('export ', '')
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"').strip("'")
    
    confluence_url = os.environ.get('CONFLUENCE_URL')
    confluence_token = os.environ.get('CONFLUENCE_TOKEN')
    
    if not confluence_url or not confluence_token:
        print('❌ Configuration incomplète!')
        sys.exit(1)
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Content-Type': 'application/json'
    }
    
    pages = [
        (337576935, 'Documentation Agent Postdoc'),
        (337576936, 'Guide de démarrage rapide'),
        (337576937, 'FAQ'),
        (337576938, 'Support'),
        (337576939, 'Signalement des problèmes'),
        (337576940, 'Politique de confidentialité'),
        (337576941, "Conditions d'utilisation"),
        (337576942, 'Configuration URLs et Manifest')
    ]
    
    print('🔍 Vérification rapide du wiki UQAM-GPT')
    print('=' * 80)
    print()
    
    # Test de connexion
    try:
        response = requests.get(
            f'{confluence_url}/rest/api/space/UQAMGPT',
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print('✅ Connexion à Confluence OK')
        else:
            print(f'❌ Erreur de connexion (HTTP {response.status_code})')
            sys.exit(1)
    except Exception as e:
        print(f'❌ Impossible de se connecter: {e}')
        sys.exit(1)
    
    print()
    print('📄 État des pages:')
    print('-' * 80)
    
    issues = []
    total_github_links = 0
    total_anglicisms = 0
    
    # Pages où les liens GitHub sont normaux (documentation de configuration)
    config_pages = ['Configuration URLs et Manifest', 'Politique de confidentialité']
    
    for page_id, title in pages:
        try:
            response = requests.get(
                f'{confluence_url}/rest/api/content/{page_id}',
                headers=headers,
                params={'expand': 'body.storage,version'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                version = data['version']['number']
                content = data['body']['storage']['value'].lower()
                
                # Vérifier les problèmes
                github_links = len(re.findall(r'github\.com/michel-heon/uqam-gpt-docs', content))
                has_troubleshooting = 'troubleshooting' in content
                has_feedback_loop = 'feedback loop' in content
                
                # Ignorer les liens GitHub dans les pages de configuration (ce sont des exemples)
                is_config_page = any(config_page in title for config_page in config_pages)
                
                if not is_config_page:
                    total_github_links += github_links
                
                if has_troubleshooting or has_feedback_loop:
                    total_anglicisms += 1
                
                status = '✅'
                notes = []
                
                if github_links > 0 and not is_config_page:
                    status = '⚠️'
                    notes.append(f'{github_links} lien(s) GitHub')
                    issues.append(f'{title}: {github_links} lien(s) GitHub wiki')
                
                if has_troubleshooting:
                    status = '⚠️'
                    notes.append('anglicisme "troubleshooting"')
                    issues.append(f'{title}: contient "troubleshooting"')
                
                if has_feedback_loop:
                    status = '⚠️'
                    notes.append('anglicisme "feedback loop"')
                    issues.append(f'{title}: contient "feedback loop"')
                
                note_str = f' ({", ".join(notes)})' if notes else ''
                print(f'{status} {title:<45} v{version}{note_str}')
            else:
                print(f'❌ {title:<45} Erreur HTTP {response.status_code}')
                issues.append(f'{title}: erreur de lecture')
        
        except Exception as e:
            print(f'❌ {title:<45} Erreur: {e}')
            issues.append(f'{title}: exception {e}')
    
    print('-' * 80)
    print()
    
    # Résumé
    print('📊 Résumé:')
    print(f'   • Pages vérifiées: {len(pages)}')
    print(f'   • Liens GitHub wiki: {total_github_links}')
    print(f'   • Pages avec anglicismes: {total_anglicisms}')
    print()
    
    if issues:
        print('⚠️  Problèmes détectés:')
        for issue in issues:
            print(f'   • {issue}')
        print()
        print('💡 Actions recommandées:')
        if total_github_links > 0:
            print('   → make fix-links')
        if total_anglicisms > 0:
            print('   → make franciser && make update-content')
        print()
        sys.exit(1)
    else:
        print('✅ Aucun problème détecté!')
        print()
        print(f'🔗 Wiki: {confluence_url}/spaces/UQAMGPT/pages/337576935')
        print()
        sys.exit(0)

if __name__ == '__main__':
    quick_check()
