# Makefile pour la gestion du wiki Confluence UQAM-GPT
# Auteur: Michel Héon
# Date: 2025-11-25

.PHONY: help install setup check migrate update-content fix-links fix-code-blocks franciser test-connection clean

# Variables
PYTHON := .venv/bin/python
PIP := .venv/bin/pip
SCRIPTS_DIR := scripts
ENV_FILE := $(SCRIPTS_DIR)/.env

# Couleurs pour l'affichage
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ Aide

help: ## Afficher cette aide
	@echo "$(BLUE)════════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Makefile - Gestion du Wiki Confluence UQAM-GPT$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make $(YELLOW)<target>$(NC)\n\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } \
		/^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════════$(NC)"

##@ Installation et Configuration

install: ## Installer l'environnement Python et les dépendances
	@echo "$(BLUE)📦 Installation de l'environnement Python...$(NC)"
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "$(GREEN)✅ Environnement virtuel créé$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Environnement virtuel déjà existant$(NC)"; \
	fi
	@$(PIP) install --upgrade pip
	@$(PIP) install -r $(SCRIPTS_DIR)/requirements.txt
	@echo "$(GREEN)✅ Dépendances installées$(NC)"

setup: install ## Configuration complète (installation + vérification)
	@echo "$(BLUE)⚙️  Vérification de la configuration...$(NC)"
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "$(RED)❌ Fichier $(ENV_FILE) manquant!$(NC)"; \
		echo "$(YELLOW)💡 Créez le fichier avec:$(NC)"; \
		echo "   export CONFLUENCE_URL=\"https://wiki.uqam.ca\""; \
		echo "   export CONFLUENCE_TOKEN=\"votre_token\""; \
		echo "   export CONFLUENCE_SPACE=\"UQAMGPT\""; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ Configuration OK$(NC)"
	@make test-connection

check: ## Vérifier la configuration et la connexion
	@echo "$(BLUE)🔍 Vérification de la configuration...$(NC)"
	@if [ ! -d ".venv" ]; then \
		echo "$(RED)❌ Environnement virtuel manquant$(NC)"; \
		echo "$(YELLOW)💡 Exécutez: make install$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "$(RED)❌ Fichier de configuration manquant$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ Configuration valide$(NC)"
	@make test-connection

##@ Tests et Diagnostic

test-connection: check ## Tester la connexion à Confluence
	@echo "$(BLUE)🔌 Test de connexion à Confluence...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) $(SCRIPTS_DIR)/test-confluence-connection.py

quick-check: check ## Vérification rapide de l'état du wiki (recommandé)
	@$(PYTHON) $(SCRIPTS_DIR)/quick-check.py

##@ Migration et Mise à Jour

migrate: check franciser ## Migration complète (franciser + migrer le contenu)
	@echo "$(BLUE)🚀 Migration complète du contenu...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) $(SCRIPTS_DIR)/confluence-rest-api.py
	@make fix-links
	@make fix-code-blocks
	@echo "$(GREEN)✨ Migration terminée avec succès!$(NC)"

update-content: check franciser ## Mettre à jour uniquement le contenu des pages
	@echo "$(BLUE)📝 Mise à jour du contenu des pages...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) $(SCRIPTS_DIR)/update-code-blocks.py
	@echo "$(GREEN)✅ Contenu mis à jour$(NC)"

franciser: ## Franciser le contenu (remplacer les anglicismes)
	@echo "$(BLUE)🇫🇷 Francisation du contenu...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/franciser-texte.py
	@echo "$(GREEN)✅ Contenu francisé$(NC)"

check-links: check ## Vérifier l'état des liens internes (recommandé avant fix-links)
	@echo "$(BLUE)🔗 Vérification des liens internes...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) $(SCRIPTS_DIR)/check-links-only.py

fix-links: check ## ⚠️  Corriger les liens internes (EXPÉRIMENTAL - utilisez avec précaution)
	@echo "$(RED)⚠️  ATTENTION: Cette commande est expérimentale$(NC)"
	@echo "$(YELLOW)   Recommandation: utilisez 'make check-links' pour vérifier d'abord$(NC)"
	@echo "$(YELLOW)   Les liens GitHub dans les pages de configuration sont normaux$(NC)"
	@read -p "Continuer? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		. $(ENV_FILE) && $(PYTHON) $(SCRIPTS_DIR)/fix-links-v2.py; \
	else \
		echo "$(YELLOW)Annulé$(NC)"; \
	fi

fix-code-blocks: check ## Corriger les blocs de code
	@echo "$(BLUE)💻 Correction des blocs de code...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) $(SCRIPTS_DIR)/update-code-blocks.py
	@echo "$(GREEN)✅ Blocs de code corrigés$(NC)"

##@ Mise à Jour Rapide

update: check franciser update-content ## Mise à jour rapide (contenu uniquement, sans correction de liens)
	@echo "$(GREEN)════════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✨ Mise à jour complète terminée!$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)📊 Pages mises à jour:$(NC)"
	@. $(ENV_FILE) && $(PYTHON) -c "import requests, os; \
		r = requests.get(f\"{os.getenv('CONFLUENCE_URL')}/rest/api/content\", \
		headers={'Authorization': f\"Bearer {os.getenv('CONFLUENCE_TOKEN')}\"}, \
		params={'spaceKey': os.getenv('CONFLUENCE_SPACE'), 'title': 'Documentation Agent Postdoc', 'expand': 'version'}); \
		print(f\"   • Documentation Agent Postdoc (v{r.json()['results'][0]['version']['number']})\") if r.status_code == 200 else None"
	@echo "$(BLUE)🔗 Accès:$(NC) https://wiki.uqam.ca/spaces/UQAMGPT/pages/337576935"

##@ Opérations Avancées

read-page: check ## Lire une page Confluence (usage: make read-page PAGE_ID=337576935)
	@if [ -z "$(PAGE_ID)" ]; then \
		echo "$(RED)❌ Erreur: PAGE_ID requis$(NC)"; \
		echo "$(YELLOW)Usage: make read-page PAGE_ID=337576935$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)📖 Lecture de la page $(PAGE_ID)...$(NC)"
	@. $(ENV_FILE) && PAGE_ID=$(PAGE_ID) $(PYTHON) $(SCRIPTS_DIR)/read-page.py

delete-page: check ## Supprimer une page Confluence (usage: make delete-page PAGE_ID=337576935)
	@if [ -z "$(PAGE_ID)" ]; then \
		echo "$(RED)❌ Erreur: PAGE_ID requis$(NC)"; \
		echo "$(YELLOW)Usage: make delete-page PAGE_ID=337576935$(NC)"; \
		exit 1; \
	fi
	@echo "$(RED)⚠️  ATTENTION: Suppression de la page $(PAGE_ID)$(NC)"
	@read -p "Êtes-vous sûr? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		. $(ENV_FILE) && PAGE_ID=$(PAGE_ID) $(PYTHON) $(SCRIPTS_DIR)/delete-page.py; \
	else \
		echo "$(YELLOW)Annulé$(NC)"; \
	fi

##@ Validation et Vérification

verify: check ## Vérifier l'état des pages (liens, anglicismes, etc.)
	@echo "$(BLUE)🔍 Vérification de l'état des pages...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) -c "import requests, os, re; \
		url = os.getenv('CONFLUENCE_URL'); token = os.getenv('CONFLUENCE_TOKEN'); space = os.getenv('CONFLUENCE_SPACE'); \
		headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}; \
		pages = [(337576935, 'Documentation Agent Postdoc'), (337576936, 'Guide de démarrage rapide'), \
		         (337576937, 'FAQ'), (337576938, 'Support'), (337576939, 'Signalement des problèmes'), \
		         (337576940, 'Politique de confidentialité'), (337576941, 'Conditions d\\'utilisation'), \
		         (337576942, 'Configuration URLs et Manifest')]; \
		print('\\n$(GREEN)Pages Confluence:$(NC)'); \
		for page_id, title in pages: \
			r = requests.get(f'{url}/rest/api/content/{page_id}', headers=headers, params={'expand': 'version'}); \
			if r.status_code == 200: \
				v = r.json()['version']['number']; \
				print(f'  ✅ {title} (v{v})');"
	@echo ""
	@echo "$(BLUE)🔗 Vérification des liens GitHub...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) -c "import requests, os, re; \
		url = os.getenv('CONFLUENCE_URL'); token = os.getenv('CONFLUENCE_TOKEN'); \
		headers = {'Authorization': f'Bearer {token}'}; \
		pages = [337576935, 337576936, 337576937, 337576938, 337576939, 337576940, 337576941, 337576942]; \
		total = 0; \
		for page_id in pages: \
			r = requests.get(f'{url}/rest/api/content/{page_id}', headers=headers, params={'expand': 'body.storage'}); \
			if r.status_code == 200: \
				links = re.findall(r'github\.com/michel-heon/uqam-gpt-docs', r.json()['body']['storage']['value']); \
				total += len(links); \
		print(f'  {\"✅ Aucun lien GitHub wiki\" if total == 0 else f\"⚠️ {total} lien(s) GitHub trouvé(s)\"}');"
	@echo ""
	@echo "$(BLUE)🇫🇷 Vérification des anglicismes...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) -c "import requests, os; \
		url = os.getenv('CONFLUENCE_URL'); token = os.getenv('CONFLUENCE_TOKEN'); \
		headers = {'Authorization': f'Bearer {token}'}; \
		pages = [337576935, 337576936, 337576937, 337576938, 337576939, 337576940, 337576941, 337576942]; \
		found = False; \
		for page_id in pages: \
			r = requests.get(f'{url}/rest/api/content/{page_id}', headers=headers, params={'expand': 'body.storage'}); \
			if r.status_code == 200: \
				content = r.json()['body']['storage']['value'].lower(); \
				if 'troubleshooting' in content or 'feedback loop' in content: \
					found = True; \
		print('  ✅ Aucun anglicisme majeur' if not found else '  ⚠️ Anglicismes détectés');"
	@echo ""

##@ Maintenance

clean: ## Nettoyer les fichiers temporaires
	@echo "$(BLUE)🧹 Nettoyage des fichiers temporaires...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

clean-all: clean ## Nettoyer tout (y compris l'environnement virtuel)
	@echo "$(RED)⚠️  Suppression de l'environnement virtuel...$(NC)"
	@rm -rf .venv
	@echo "$(GREEN)✅ Environnement virtuel supprimé$(NC)"

##@ Documentation

list-pages: check ## Lister toutes les pages du wiki
	@echo "$(BLUE)📋 Liste des pages Confluence...$(NC)"
	@. $(ENV_FILE) && $(PYTHON) -c "import requests, os; \
		url = os.getenv('CONFLUENCE_URL'); token = os.getenv('CONFLUENCE_TOKEN'); space = os.getenv('CONFLUENCE_SPACE'); \
		r = requests.get(f'{url}/rest/api/content', \
			headers={'Authorization': f'Bearer {token}'}, \
			params={'spaceKey': space, 'limit': 100, 'expand': 'version'}); \
		if r.status_code == 200: \
			for page in r.json()['results']: \
				if 'Postdoc' in page['title']: \
					print(f\"  • {page['title']} (ID: {page['id']}, v{page['version']['number']})\");"

info: ## Afficher les informations sur le projet
	@echo "$(BLUE)════════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Projet: UQAM-GPT Documentation Wiki$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(YELLOW)Confluence:$(NC)  https://wiki.uqam.ca/spaces/UQAMGPT"
	@echo "$(YELLOW)Page principale:$(NC) https://wiki.uqam.ca/pages/viewpage.action?pageId=337576935"
	@echo "$(YELLOW)Espace:$(NC)      UQAMGPT"
	@echo "$(YELLOW)Section:$(NC)     08 - UQAM-GPT: Support et Maintenance"
	@echo ""
	@echo "$(BLUE)Pages migrées:$(NC)"
	@echo "  • Documentation Agent Postdoc (337576935)"
	@echo "  • Guide de démarrage rapide (337576936)"
	@echo "  • FAQ (337576937)"
	@echo "  • Support (337576938)"
	@echo "  • Signalement des problèmes (337576939)"
	@echo "  • Politique de confidentialité (337576940)"
	@echo "  • Conditions d'utilisation (337576941)"
	@echo "  • Configuration URLs et Manifest (337576942)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════════$(NC)"
