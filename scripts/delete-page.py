#!/usr/bin/env python3
"""
Script pour supprimer une page de Confluence
"""

import os
import sys
import requests
from pathlib import Path


def delete_page(page_id: str):
    """Supprime une page de Confluence"""
    
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    
    if not confluence_url or not confluence_token:
        print("❌ Variables d'environnement manquantes!")
        print("Exécutez: source scripts/.env")
        return False
    
    print(f"🗑️  Suppression de la page ID: {page_id}")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Accept': 'application/json'
    }
    
    # Récupérer d'abord les infos de la page
    url = f"{confluence_url}/rest/api/content/{page_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        print(f"❌ Page {page_id} introuvable")
        return False
    elif response.status_code != 200:
        print(f"❌ Erreur {response.status_code}: {response.text[:200]}")
        return False
    
    page_data = response.json()
    page_title = page_data.get('title', 'Sans titre')
    
    print(f"📄 Page trouvée: {page_title}")
    print(f"🔗 URL: {confluence_url}/pages/viewpage.action?pageId={page_id}")
    
    # Confirmation
    print(f"\n⚠️  Êtes-vous sûr de vouloir supprimer cette page ?")
    print(f"   Tapez 'oui' pour confirmer: ", end='')
    
    confirmation = input().strip().lower()
    if confirmation not in ['oui', 'yes', 'y', 'o']:
        print("❌ Suppression annulée")
        return False
    
    # Supprimer la page
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        print("\n✅ Page supprimée avec succès!")
        return True
    else:
        print(f"\n❌ Erreur lors de la suppression: {response.status_code}")
        print(response.text)
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/delete-page.py <page_id>")
        print("\nExemple: python3 scripts/delete-page.py 337576930")
        sys.exit(1)
    
    page_id = sys.argv[1]
    success = delete_page(page_id)
    sys.exit(0 if success else 1)
