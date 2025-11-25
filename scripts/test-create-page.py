#!/usr/bin/env python3
"""
Script de test - Création d'une page de test dans Confluence
"""

import os
import sys
import importlib.util
from pathlib import Path

# Charger le module depuis le fichier
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location(
    "confluence_rest_api",
    script_dir / "confluence-rest-api.py"
)
confluence_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(confluence_module)

ConfluenceServerAPI = confluence_module.ConfluenceServerAPI
MarkdownToConfluence = confluence_module.MarkdownToConfluence


def create_test_page():
    """Crée une page de test simple dans Confluence"""
    
    print("🧪 Test de création de page dans Confluence")
    print("=" * 60)
    
    # Récupérer la configuration
    confluence_url = os.getenv('CONFLUENCE_URL')
    confluence_token = os.getenv('CONFLUENCE_TOKEN')
    space_key = os.getenv('CONFLUENCE_SPACE', 'UQAMGPT')
    
    if not confluence_url or not confluence_token:
        print("❌ Variables d'environnement manquantes!")
        print("Exécutez: source scripts/.env")
        return False
    
    # Initialiser l'API
    api = ConfluenceServerAPI(confluence_url, confluence_token, space_key)
    converter = MarkdownToConfluence(space_key)
    
    # Contenu de test en Markdown
    test_content_md = """# Test de Migration - UQAM-GPT

## Introduction

Ceci est une page de **test** pour valider la migration de documentation depuis Markdown vers Confluence.

## Fonctionnalités testées

### 1. Formatage de base
- **Gras**
- *Italique*
- `Code inline`

### 2. Listes

#### Liste à puces
- Premier élément
- Deuxième élément
  - Sous-élément A
  - Sous-élément B
- Troisième élément

#### Liste numérotée
1. Étape un
2. Étape deux
3. Étape trois

### 3. Bloc de code

```python
def hello_confluence():
    print("Hello from UQAM-GPT!")
    return True
```

### 4. Tableau

| Fonctionnalité | Status | Notes |
|---------------|--------|-------|
| Connexion API | ✅ | Fonctionne |
| Authentification | ✅ | Token OK |
| Création page | 🧪 | En test |

### 5. Citations

> Ceci est une citation de test pour valider le formatage dans Confluence.

### 6. Liens

- [Documentation Confluence](https://wiki.uqam.ca)
- [UQAM](https://uqam.ca)

## Conclusion

Si vous voyez cette page correctement formatée dans Confluence, la migration fonctionne ! ✨

---

*Page créée automatiquement par le script de test - {}*
""".format("25 novembre 2025")
    
    # Convertir en format Confluence
    print("\n📝 Conversion Markdown → Confluence Storage Format...")
    confluence_content = converter.convert(test_content_md)
    
    # Titre de la page de test
    test_page_title = "🧪 Test Migration - Script Automatique"
    
    # Vérifier si la page existe déjà
    print(f"\n🔍 Recherche de la page '{test_page_title}'...")
    existing_page = api.find_page_by_title(test_page_title)
    
    if existing_page:
        print(f"   ℹ️  Page existante trouvée (ID: {existing_page['id']})")
        print(f"   🔄 Mise à jour de la page...")
        
        result = api.update_page(
            page_id=existing_page['id'],
            title=test_page_title,
            content=confluence_content,
            version=existing_page['version']['number']
        )
        
        if result:
            page_id = existing_page['id']
            print(f"\n✅ Page mise à jour avec succès!")
        else:
            print("\n❌ Échec de la mise à jour")
            return False
    else:
        print("   ℹ️  Page non trouvée, création d'une nouvelle page...")
        
        result = api.create_page(
            title=test_page_title,
            content=confluence_content,
            parent_id=None
        )
        
        if result:
            page_id = result['id']
            print(f"\n✅ Page créée avec succès!")
        else:
            print("\n❌ Échec de la création")
            return False
    
    # Afficher le lien vers la page
    page_url = f"{confluence_url}/pages/viewpage.action?pageId={page_id}"
    print("\n" + "=" * 60)
    print("🎉 Test réussi!")
    print("=" * 60)
    print(f"\n🔗 Lien vers la page:")
    print(f"   {page_url}")
    print(f"\n💡 Vérifiez que le formatage est correct dans Confluence")
    print(f"   puis lancez la migration complète:\n")
    print(f"   source scripts/.env && .venv/bin/python scripts/confluence-rest-api.py")
    
    return True


if __name__ == '__main__':
    success = create_test_page()
    sys.exit(0 if success else 1)
