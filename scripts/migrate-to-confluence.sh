#!/bin/bash

# Script de migration de la documentation UQAM-GPT vers Confluence
# Utilise le serveur MCP Atlassian pour créer les pages

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}  Migration UQAM-GPT Docs → Confluence${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

# Vérification des prérequis
echo -e "${YELLOW}Vérification des prérequis...${NC}"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js n'est pas installé${NC}"
    echo "Installez Node.js v18+ depuis https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}❌ Node.js version 18+ requis (version actuelle: $(node -v))${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node -v)${NC}"

# Vérifier npx
if ! command -v npx &> /dev/null; then
    echo -e "${RED}❌ npx n'est pas disponible${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npx disponible${NC}"

echo ""
echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${YELLOW}Étape 1 : Authentification Atlassian${NC}"
echo -e "${BLUE}--------------------------------------------------${NC}"
echo ""
echo "Une fenêtre de navigateur va s'ouvrir pour l'authentification OAuth."
echo "Connectez-vous avec vos identifiants Atlassian et approuvez les permissions."
echo ""
read -p "Appuyez sur Entrée pour continuer..."

# Lancer l'authentification
npx -y mcp-remote https://mcp.atlassian.com/v1/sse

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Échec de l'authentification${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Authentification réussie${NC}"
echo ""

echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${YELLOW}Étape 2 : Configuration de l'espace Confluence${NC}"
echo -e "${BLUE}--------------------------------------------------${NC}"
echo ""

# Demander les informations de l'espace Confluence
read -p "Nom de votre site Atlassian (ex: uqam.atlassian.net) : " CONFLUENCE_SITE
read -p "Clé de l'espace Confluence (ex: UQAMGPT) : " SPACE_KEY
read -p "Nom de l'espace (ex: UQAM-GPT Documentation) : " SPACE_NAME

echo ""
echo -e "${YELLOW}Configuration :${NC}"
echo "  Site : $CONFLUENCE_SITE"
echo "  Clé : $SPACE_KEY"
echo "  Nom : $SPACE_NAME"
echo ""

read -p "Ces informations sont-elles correctes ? (o/n) : " CONFIRM
if [ "$CONFIRM" != "o" ] && [ "$CONFIRM" != "O" ]; then
    echo -e "${RED}Migration annulée${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${YELLOW}Étape 3 : Liste des pages à migrer${NC}"
echo -e "${BLUE}--------------------------------------------------${NC}"
echo ""

# Fichiers à migrer
PAGES=(
    "Home.md|Home|Page d'accueil de l'écosystème UQAM-GPT"
    "README.md|À propos du projet|Description du projet UQAM-GPT"
    "postdoc/Home.md|Postdoc - Home|Documentation UQAM-GPT Postdoc"
    "postdoc/Guide-Demarrage-Rapide.md|Guide de Démarrage Rapide|Installation et première utilisation"
    "postdoc/FAQ.md|FAQ - Questions Fréquentes|Réponses aux questions courantes"
    "postdoc/Support.md|Support|Assistance technique et dépannage"
    "postdoc/Signalement-Problemes.md|Signalement de Problèmes|Processus de signalement"
    "postdoc/Politique-de-Confidentialite.md|Politique de Confidentialité|Protection des données personnelles"
    "postdoc/Conditions-Utilisation.md|Conditions d'Utilisation|Licence et conditions"
    "postdoc/Configuration-URLs-Manifest.md|Configuration Technique|Configuration URLs manifest"
)

echo "Pages à migrer :"
for page in "${PAGES[@]}"; do
    IFS='|' read -r file title desc <<< "$page"
    echo "  - $title ($file)"
done

TOTAL_PAGES=${#PAGES[@]}
echo ""
echo -e "${GREEN}Total : $TOTAL_PAGES pages${NC}"
echo ""

read -p "Commencer la migration ? (o/n) : " START_MIGRATION
if [ "$START_MIGRATION" != "o" ] && [ "$START_MIGRATION" != "O" ]; then
    echo -e "${RED}Migration annulée${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${YELLOW}Étape 4 : Migration des pages${NC}"
echo -e "${BLUE}--------------------------------------------------${NC}"
echo ""

# Note : Cette partie nécessite l'API Confluence ou l'utilisation de GitHub Copilot
echo -e "${YELLOW}⚠️  ATTENTION${NC}"
echo ""
echo "La migration automatique des pages nécessite :"
echo "1. L'API REST Confluence configurée, OU"
echo "2. L'utilisation de GitHub Copilot avec MCP Atlassian"
echo ""
echo -e "${GREEN}Méthode recommandée :${NC}"
echo ""
echo "Utilisez GitHub Copilot dans VS Code avec les commandes suivantes :"
echo ""

COUNT=1
for page in "${PAGES[@]}"; do
    IFS='|' read -r file title desc <<< "$page"
    echo "# Page $COUNT/$TOTAL_PAGES"
    echo -e "${BLUE}Copilot :${NC} Crée une page Confluence dans l'espace $SPACE_KEY"
    echo "          Titre : \"$title\""
    echo "          Contenu : Fichier $file"
    echo ""
    ((COUNT++))
done

echo ""
echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${YELLOW}Étape 5 : Instructions de migration manuelle${NC}"
echo -e "${BLUE}--------------------------------------------------${NC}"
echo ""

cat << 'EOF'
Pour chaque fichier, dans VS Code avec Copilot :

1. Ouvrez le fichier .md à migrer
2. Utilisez la commande :
   
   "@workspace Crée une page Confluence dans l'espace [CLÉ_ESPACE]
   avec le titre '[TITRE]' et le contenu de ce fichier"

3. Copilot utilisera le serveur MCP pour créer la page
4. Vérifiez la page créée dans Confluence
5. Passez au fichier suivant

Exemple concret :

@workspace Crée une page Confluence dans l'espace UQAMGPT
avec le titre 'Guide de Démarrage Rapide' et le contenu 
du fichier postdoc/Guide-Demarrage-Rapide.md
EOF

echo ""
echo -e "${GREEN}✓ Configuration terminée${NC}"
echo ""
echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${YELLOW}Prochaines étapes${NC}"
echo -e "${BLUE}--------------------------------------------------${NC}"
echo ""
echo "1. Ouvrez VS Code"
echo "2. Rechargez la configuration MCP (Cmd+Shift+P > Reload Window)"
echo "3. Utilisez GitHub Copilot pour créer les pages"
echo "4. Vérifiez les pages dans Confluence : https://$CONFLUENCE_SITE/wiki/spaces/$SPACE_KEY"
echo ""
echo -e "${GREEN}Documentation complète : .vscode/confluence-migration-guide.md${NC}"
echo ""

# Créer un fichier de log avec les informations
LOG_FILE=".vscode/confluence-migration.log"
cat > "$LOG_FILE" << EOF
Migration UQAM-GPT Docs vers Confluence
========================================

Date : $(date)
Site : $CONFLUENCE_SITE
Espace : $SPACE_KEY ($SPACE_NAME)

Pages à migrer : $TOTAL_PAGES

Liste des pages :
EOF

for page in "${PAGES[@]}"; do
    IFS='|' read -r file title desc <<< "$page"
    echo "- [ ] $title ($file)" >> "$LOG_FILE"
done

echo "" >> "$LOG_FILE"
echo "Instructions :" >> "$LOG_FILE"
echo "Utilisez GitHub Copilot avec les commandes décrites dans confluence-migration-guide.md" >> "$LOG_FILE"

echo -e "${GREEN}✓ Log créé : $LOG_FILE${NC}"
echo ""
