#!/usr/bin/env python3
"""
Script de test de connexion à Confluence Server
Vérifie l'authentification et l'accès à l'espace UQAMGPT
"""

import os
import sys
import requests
from pathlib import Path

# Ajouter le dossier parent au path pour importer le module
sys.path.insert(0, str(Path(__file__).parent))

def test_connection():
    """Teste la connexion à Confluence"""
    
    print("🔍 Test de connexion à Confluence Server")
    print("=" * 60)
    
    # Récupérer les variables d'environnement
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    space_key = os.getenv('CONFLUENCE_SPACE', 'UQAMGPT')
    
    # Vérifier les variables
    print("\n📋 Configuration:")
    print(f"   URL: {confluence_url or '❌ Non définie'}")
    print(f"   Token: {'✅ Défini' if confluence_token else '❌ Non défini'}")
    print(f"   Espace: {space_key}")
    
    if not confluence_url or not confluence_token:
        print("\n❌ Variables d'environnement manquantes!")
        print("\nDéfinissez-les avec:")
        print('   export CONFLUENCE_URL="https://wiki.uqam.ca"')
        print('   export CONFLUENCE_TOKEN="votre_token"')
        print('   export CONFLUENCE_SPACE="UQAMGPT"')
        print("\n💡 Pour créer un token:")
        print("   https://wiki.uqam.ca/plugins/personalaccesstokens/usertokens.action")
        return False
    
    # Tester la connexion
    print(f"\n🔌 Test de connexion à {confluence_url}...")
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Accept': 'application/json'
    }
    
    try:
        # Test 1: Vérifier l'API
        print("\n   1️⃣ Test de l'API REST...")
        response = requests.get(f'{confluence_url}/rest/api/space', headers=headers, timeout=10)
        
        if response.status_code == 401:
            print("   ❌ Authentification échouée (401)")
            print("   💡 Vérifiez votre token ou créez-en un nouveau")
            return False
        elif response.status_code == 403:
            print("   ❌ Accès refusé (403)")
            print("   💡 Vérifiez vos permissions dans Confluence")
            return False
        elif response.status_code != 200:
            print(f"   ❌ Erreur {response.status_code}: {response.text[:200]}")
            return False
        
        print("   ✅ API accessible")
        
        # Test 2: Vérifier l'espace
        print(f"\n   2️⃣ Test d'accès à l'espace '{space_key}'...")
        response = requests.get(
            f'{confluence_url}/rest/api/space/{space_key}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 404:
            print(f"   ❌ Espace '{space_key}' introuvable")
            print("   💡 Vérifiez la clé de l'espace dans Confluence")
            return False
        elif response.status_code != 200:
            print(f"   ❌ Erreur {response.status_code}: {response.text[:200]}")
            return False
        
        space_data = response.json()
        print(f"   ✅ Espace trouvé: {space_data.get('name', space_key)}")
        print(f"   📝 Type: {space_data.get('type', 'unknown')}")
        
        # Test 3: Vérifier les permissions d'écriture
        print(f"\n   3️⃣ Test des permissions...")
        response = requests.get(
            f'{confluence_url}/rest/api/content',
            headers=headers,
            params={'spaceKey': space_key, 'limit': 1},
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ Permissions de lecture OK")
            pages = response.json().get('results', [])
            if pages:
                print(f"   📄 Exemple de page: {pages[0].get('title', 'Sans titre')}")
        else:
            print(f"   ⚠️  Avertissement: {response.status_code}")
        
        # Résumé
        print("\n" + "=" * 60)
        print("✨ Connexion réussie!")
        print("=" * 60)
        print("\n🚀 Vous pouvez maintenant:")
        print("   1. Tester avec une page: python3 scripts/test-create-page.py")
        print("   2. Lancer la migration complète: python3 scripts/confluence-rest-api.py")
        
        return True
        
    except requests.exceptions.Timeout:
        print("   ❌ Timeout - Le serveur ne répond pas")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erreur inattendue: {e}")
        return False


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
