#!/usr/bin/env python3
"""
Script pour lire le contenu d'une page Confluence et analyser sa structure
"""

import os
import sys
import requests
import json


def get_page_content(page_id: str):
    """Récupère et affiche le contenu d'une page Confluence"""
    
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    
    if not confluence_url or not confluence_token:
        print("❌ Variables d'environnement manquantes!")
        return None
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Accept': 'application/json'
    }
    
    # Récupérer la page avec tous les détails
    url = f"{confluence_url}/rest/api/content/{page_id}"
    params = {
        'expand': 'body.storage,version,space,ancestors,children.page'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code}: {response.text[:200]}")
        return None
    
    return response.json()


def analyze_page_structure(page_data):
    """Analyse la structure de la page"""
    
    print("📊 Analyse de la page Confluence")
    print("=" * 80)
    
    # Informations de base
    print(f"\n📄 Titre: {page_data.get('title', 'N/A')}")
    print(f"🔑 ID: {page_data.get('id', 'N/A')}")
    print(f"🏷️  Type: {page_data.get('type', 'N/A')}")
    print(f"📦 Espace: {page_data.get('space', {}).get('name', 'N/A')} ({page_data.get('space', {}).get('key', 'N/A')})")
    print(f"🔢 Version: {page_data.get('version', {}).get('number', 'N/A')}")
    
    # Ancêtres (hiérarchie)
    ancestors = page_data.get('ancestors', [])
    if ancestors:
        print(f"\n📂 Hiérarchie:")
        for i, ancestor in enumerate(ancestors):
            indent = "  " * i
            print(f"{indent}└─ {ancestor.get('title', 'N/A')} (ID: {ancestor.get('id', 'N/A')})")
        print(f"{'  ' * len(ancestors)}└─ 📍 {page_data.get('title', 'N/A')} (page actuelle)")
    
    # Pages enfants
    children = page_data.get('children', {}).get('page', {})
    if children and 'results' in children:
        child_pages = children['results']
        print(f"\n👶 Pages enfants ({len(child_pages)}):")
        for child in child_pages:
            print(f"  • {child.get('title', 'N/A')} (ID: {child.get('id', 'N/A')})")
    elif children:
        print(f"\n👶 Pages enfants: {children.get('size', 0)}")
    
    # Contenu (extrait)
    body = page_data.get('body', {}).get('storage', {}).get('value', '')
    if body:
        # Extraire les titres principaux du contenu HTML
        import re
        headings = re.findall(r'<h[12]>(.*?)</h[12]>', body)
        if headings:
            print(f"\n📋 Sections principales:")
            for heading in headings[:10]:  # Limiter à 10
                # Nettoyer les balises HTML
                clean_heading = re.sub(r'<[^>]+>', '', heading)
                print(f"  • {clean_heading}")
    
    # URL de la page
    page_url = f"{os.getenv('CONFLUENCE_URL')}/pages/viewpage.action?pageId={page_data.get('id')}"
    print(f"\n🔗 URL: {page_url}")
    
    return page_data


def get_all_pages_in_space(space_key: str):
    """Liste toutes les pages de l'espace"""
    
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {confluence_token}',
        'Accept': 'application/json'
    }
    
    url = f"{confluence_url}/rest/api/content"
    params = {
        'spaceKey': space_key,
        'type': 'page',
        'expand': 'ancestors',
        'limit': 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code}")
        return []
    
    return response.json().get('results', [])


if __name__ == '__main__':
    page_id = sys.argv[1] if len(sys.argv) > 1 else "255301983"
    
    print(f"🔍 Lecture de la page ID: {page_id}")
    print()
    
    page_data = get_page_content(page_id)
    
    if page_data:
        analyze_page_structure(page_data)
        
        # Lister toutes les pages de l'espace
        space_key = page_data.get('space', {}).get('key', 'UQAMGPT')
        print(f"\n\n📚 Structure complète de l'espace {space_key}")
        print("=" * 80)
        
        all_pages = get_all_pages_in_space(space_key)
        
        # Organiser par hiérarchie
        root_pages = [p for p in all_pages if not p.get('ancestors')]
        
        print(f"\n📑 Pages racines ({len(root_pages)}):")
        for page in root_pages:
            print(f"  📄 {page.get('title', 'N/A')} (ID: {page.get('id', 'N/A')})")
        
        # Pages avec parents
        child_pages = [p for p in all_pages if p.get('ancestors')]
        if child_pages:
            print(f"\n📑 Pages avec parents ({len(child_pages)}):")
            for page in child_pages:
                parent = page.get('ancestors', [])[-1] if page.get('ancestors') else None
                parent_title = parent.get('title', 'N/A') if parent else 'N/A'
                print(f"  └─ {page.get('title', 'N/A')} (parent: {parent_title})")
