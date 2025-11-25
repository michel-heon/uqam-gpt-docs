#!/bin/bash
# Script de vérification rapide pour le wiki Confluence
# Usage: ./quick-check.sh

set -e

echo "════════════════════════════════════════════════════════════════════"
echo "  🔍 Vérification rapide du wiki UQAM-GPT"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Vérifier que Make est installé
if ! command -v make &> /dev/null; then
    echo "❌ Make n'est pas installé!"
    echo "   Installez-le avec: sudo apt-get install make (Ubuntu/Debian)"
    exit 1
fi

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé!"
    exit 1
fi

echo "✅ Make et Python sont installés"
echo ""

# Vérifier l'environnement virtuel
if [ ! -d ".venv" ]; then
    echo "⚠️  Environnement virtuel manquant"
    echo "   Exécutez: make install"
    exit 1
fi

echo "✅ Environnement virtuel trouvé"
echo ""

# Vérifier le fichier de configuration
if [ ! -f "scripts/.env" ]; then
    echo "❌ Fichier de configuration manquant!"
    echo ""
    echo "📝 Créez le fichier scripts/.env avec:"
    echo ""
    echo "   export CONFLUENCE_URL=\"https://wiki.uqam.ca\""
    echo "   export CONFLUENCE_TOKEN=\"votre_token\""
    echo "   export CONFLUENCE_SPACE=\"UQAMGPT\""
    echo ""
    echo "💡 Vous pouvez copier scripts/.env.example et le modifier"
    exit 1
fi

echo "✅ Fichier de configuration trouvé"
echo ""

# Tester la connexion
echo "🔌 Test de connexion à Confluence..."
if make test-connection > /dev/null 2>&1; then
    echo "✅ Connexion Confluence OK"
else
    echo "❌ Échec de connexion à Confluence"
    echo "   Vérifiez votre token et votre connexion réseau"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  ✨ Système prêt! Vous pouvez utiliser:"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "  make update      # Mettre à jour le wiki"
echo "  make verify      # Vérifier l'état des pages"
echo "  make help        # Voir toutes les commandes"
echo ""
echo "════════════════════════════════════════════════════════════════════"
