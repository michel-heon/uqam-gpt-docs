#!/usr/bin/env python3
"""
Script pour remplacer les anglicismes par des termes français
"""

import os
from pathlib import Path

# Mapping des anglicismes → termes français
replacements = {
    # Troubleshooting
    'Troubleshooting': 'Dépannage',
    'troubleshooting': 'dépannage',
    
    # Support (quand c'est un titre de section)
    '# Support -': '# Assistance technique -',
    '## Contact Support': '## Contact Assistance',
    '### Équipe de Support': "### Équipe d'assistance",
    'Contact Support': 'Contact Assistance',
    
    # Feedback
    'Feedback et Suggestions': 'Commentaires et suggestions',
    'feedback': 'retour',
    'Adaptive Card feedback': 'Carte adaptative de retour',
    'Boutons de feedback': 'Boutons de retour',
    
    # Logs (usage technique acceptable, mais on peut franciser)
    # On garde "logs" dans les contextes techniques comme "logs d'audit"
    
    # Debug (moins courant, à franciser)
    'debug': 'débogage',
    'Debug': 'Débogage',
}

def replace_in_file(file_path, replacements):
    """Remplace les anglicismes dans un fichier"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    for english, french in replacements.items():
        if english in content:
            count = content.count(english)
            content = content.replace(english, french)
            changes.append(f"  • {english} → {french} ({count}x)")
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, []


def main():
    """Remplace les anglicismes dans tous les fichiers markdown"""
    
    print("🇫🇷 Remplacement des anglicismes par des termes français")
    print("=" * 80)
    
    workspace_root = Path(__file__).parent.parent
    postdoc_dir = workspace_root / 'postdoc'
    
    # Fichiers à traiter
    files_to_process = [
        'Home.md',
        'Guide-Demarrage-Rapide.md',
        'FAQ.md',
        'Support.md',
        'Signalement-Problemes.md',
        'Politique-de-Confidentialite.md',
        'Conditions-Utilisation.md',
        'Configuration-URLs-Manifest.md'
    ]
    
    total_files_changed = 0
    
    for filename in files_to_process:
        file_path = postdoc_dir / filename
        
        if not file_path.exists():
            print(f"\n⚠️  {filename} - Fichier non trouvé")
            continue
        
        print(f"\n📄 {filename}...")
        changed, changes = replace_in_file(file_path, replacements)
        
        if changed:
            print("   ✅ Modifié:")
            for change in changes:
                print(change)
            total_files_changed += 1
        else:
            print("   ⏭️  Aucun anglicisme trouvé")
    
    print("\n" + "=" * 80)
    print(f"✨ Terminé! {total_files_changed} fichier(s) modifié(s)")
    print("=" * 80)
    print("\n💡 Prochaine étape: Re-migrer le contenu vers Confluence")
    print("   Commande: source scripts/.env && .venv/bin/python scripts/update-code-blocks.py")


if __name__ == '__main__':
    main()
