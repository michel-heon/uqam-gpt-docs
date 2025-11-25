# Guide d'utilisation du Makefile - Wiki Confluence UQAM-GPT

Ce Makefile automatise toutes les opérations de gestion du wiki Confluence pour le projet UQAM-GPT.

## 🚀 Démarrage rapide

### Première utilisation

```bash
# 1. Installation complète
make setup

# 2. Mise à jour du wiki
make update
```

### Utilisation quotidienne

```bash
# Mettre à jour le wiki après avoir modifié les fichiers markdown
make update
```

## 📋 Commandes principales

### Installation et configuration

- `make install` - Installer l'environnement Python et les dépendances
- `make setup` - Configuration complète (installation + vérification)
- `make check` - Vérifier la configuration
- `make test-connection` - Tester la connexion à Confluence

### Mise à jour du wiki

- `make update` - **Commande principale** : mise à jour complète (francisation + contenu + liens)
- `make migrate` - Migration complète depuis zéro
- `make update-content` - Mettre à jour uniquement le contenu des pages
- `make franciser` - Remplacer les anglicismes par des termes français

### Corrections spécifiques

- `make fix-links` - Corriger les liens internes et remplacer les liens GitHub
- `make fix-code-blocks` - Corriger les blocs de code

### Validation

- `make verify` - Vérifier l'état complet des pages (liens, anglicismes, versions)
- `make list-pages` - Lister toutes les pages du wiki

### Opérations avancées

```bash
# Lire une page spécifique
make read-page PAGE_ID=337576935

# Supprimer une page (avec confirmation)
make delete-page PAGE_ID=337576935
```

### Maintenance

- `make clean` - Nettoyer les fichiers temporaires
- `make clean-all` - Supprimer l'environnement virtuel
- `make info` - Afficher les informations sur le projet

## 📖 Workflows typiques

### Workflow 1 : Modification de contenu

Lorsque vous modifiez un fichier markdown dans `postdoc/`:

```bash
# 1. Modifier les fichiers (ex: postdoc/Support.md)
vim postdoc/Support.md

# 2. Mettre à jour le wiki
make update

# 3. Vérifier le résultat
make verify
```

### Workflow 2 : Première installation sur une nouvelle machine

```bash
# 1. Cloner le repo
git clone <repo-url>
cd uqam-gpt-docs.wiki

# 2. Créer le fichier de configuration
cat > scripts/.env << 'EOF'
export CONFLUENCE_URL="https://wiki.uqam.ca"
export CONFLUENCE_TOKEN="votre_token_ici"
export CONFLUENCE_SPACE="UQAMGPT"
EOF

# 3. Installation et configuration
make setup

# 4. Première migration
make migrate
```

### Workflow 3 : Diagnostic de problèmes

```bash
# 1. Vérifier la configuration
make check

# 2. Tester la connexion
make test-connection

# 3. Vérifier l'état des pages
make verify

# 4. Lire une page spécifique pour diagnostiquer
make read-page PAGE_ID=337576935
```

## 🔧 Configuration requise

### Fichier `.env`

Créez le fichier `scripts/.env` avec :

```bash
export CONFLUENCE_URL="https://wiki.uqam.ca"
export CONFLUENCE_TOKEN="votre_personal_access_token"
export CONFLUENCE_SPACE="UQAMGPT"
```

### Obtenir un Personal Access Token

1. Allez sur : https://wiki.uqam.ca/plugins/personalaccesstokens/usertokens.action
2. Créez un nouveau token avec les permissions :
   - Read
   - Write
3. Copiez le token dans `scripts/.env`

⚠️ **Important** : Ne committez jamais le fichier `.env` dans Git!

## 📊 Structure des pages

Le wiki contient 8 pages principales :

| Page ID   | Titre                              | Fichier source                      |
|-----------|------------------------------------|-------------------------------------|
| 337576935 | Documentation Agent Postdoc        | postdoc/Home.md                     |
| 337576936 | Guide de démarrage rapide          | postdoc/Guide-Demarrage-Rapide.md   |
| 337576937 | FAQ                                | postdoc/FAQ.md                      |
| 337576938 | Support                            | postdoc/Support.md                  |
| 337576939 | Signalement des problèmes          | postdoc/Signalement-Problemes.md    |
| 337576940 | Politique de confidentialité       | postdoc/Politique-de-Confidentialite.md |
| 337576941 | Conditions d'utilisation           | postdoc/Conditions-Utilisation.md   |
| 337576942 | Configuration URLs et Manifest     | postdoc/Configuration-URLs-Manifest.md |

## 🎯 Que fait chaque commande ?

### `make update` (recommandé)

Cette commande exécute dans l'ordre :

1. **Francisation** : Remplace les termes anglais par des équivalents français
   - Troubleshooting → Dépannage
   - Feedback → Retour/Commentaire
   - Support → Assistance technique

2. **Mise à jour du contenu** : Envoie le contenu modifié à Confluence

3. **Correction des liens** : 
   - Convertit les liens HTML en format Confluence natif
   - Remplace les liens GitHub wiki par des liens Confluence

### `make migrate` (première fois)

Migration complète depuis zéro :

1. Francisation des sources
2. Conversion markdown → Confluence
3. Création/mise à jour des pages
4. Correction des liens
5. Correction des blocs de code

### `make verify`

Vérifie :
- ✅ Versions des pages
- ✅ Absence de liens GitHub wiki
- ✅ Absence d'anglicismes majeurs
- ✅ État de la connexion

## 🐛 Résolution de problèmes

### Erreur : "Environnement virtuel manquant"

```bash
make install
```

### Erreur : "Fichier de configuration manquant"

Créez le fichier `scripts/.env` avec vos credentials Confluence.

### Erreur : "Authentification échouée"

Vérifiez que votre Personal Access Token est valide et a les bonnes permissions.

### Les modifications ne sont pas visibles

```bash
# Forcer la mise à jour
make update

# Vérifier l'état
make verify

# Lire la page directement
make read-page PAGE_ID=337576935
```

### Blocs de code vides

```bash
make fix-code-blocks
```

### Liens brisés

```bash
make fix-links
```

## 📝 Bonnes pratiques

1. **Toujours franciser avant de migrer** : Le Makefile le fait automatiquement avec `make update`

2. **Vérifier après chaque mise à jour** : Utilisez `make verify`

3. **Tester localement** : Les scripts Python peuvent être exécutés directement pour des tests

4. **Sauvegarder votre token** : Conservez votre Personal Access Token en lieu sûr

5. **Ne pas committer `.env`** : Le fichier contient des secrets

## 🔗 Liens utiles

- **Wiki UQAM-GPT** : https://wiki.uqam.ca/spaces/UQAMGPT
- **Page principale** : https://wiki.uqam.ca/pages/viewpage.action?pageId=337576935
- **Tokens** : https://wiki.uqam.ca/plugins/personalaccesstokens/usertokens.action
- **API Confluence** : https://developer.atlassian.com/server/confluence/confluence-rest-api-examples/

## 💡 Aide

Pour afficher l'aide intégrée du Makefile :

```bash
make help
```

Pour des informations sur le projet :

```bash
make info
```

---

**Auteur** : Michel Héon  
**Date** : Novembre 2025  
**Projet** : UQAM-GPT Documentation Wiki
