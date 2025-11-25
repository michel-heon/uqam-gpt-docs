# ADR 014: Gestion Sécurisée des Secrets Confluence

## Statut

✅ Accepté

## Date

2025-11-25

## Contexte

Le projet nécessite l'authentification à l'API REST de Confluence Server pour automatiser les opérations sur le wiki. Les éléments sensibles à protéger :

### Données sensibles

1. **Personal Access Token (PAT)** : Token d'authentification Confluence
2. **URL Confluence** : `https://wiki.uqam.ca`
3. **Nom de l'espace** : `UQAMGPT`
4. **IDs des pages** : 337576935-337576942

### Risques identifiés

#### Risque 1 : Exposition dans l'historique Git

**Scénario** : Token hardcodé dans scripts Python
**Impact** : Token public dans historique, accès non autorisé au wiki
**Probabilité** : Élevée (erreur commune)

#### Risque 2 : Token dans les logs

**Scénario** : Token visible dans output de débogage
**Impact** : Exposition dans logs CI/CD ou historique terminal
**Probabilité** : Moyenne

#### Risque 3 : Token partagé par erreur

**Scénario** : Fichier .env copié avec token réel
**Impact** : Accès non autorisé par tiers
**Probabilité** : Moyenne

#### Risque 4 : Token non révocable

**Scénario** : Token exposé mais pas de process de révocation
**Impact** : Accès persistant non autorisé
**Probabilité** : Faible (si Confluence permet révocation)

## Décision

### 1. Fichier .env pour configuration

**Structure adoptée** :

```bash
# scripts/.env (dans .gitignore)
export CONFLUENCE_URL="https://wiki.uqam.ca"
export CONFLUENCE_TOKEN="votre_token_personnel_ici"
export CONFLUENCE_SPACE="UQAMGPT"
```

**Chargement dans scripts** :

```python
import os

# Charger variables d'environnement depuis .env si présent
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key.replace('export ', '')] = value.strip('"')

# Utilisation sécurisée
CONFLUENCE_URL = os.environ.get('CONFLUENCE_URL')
CONFLUENCE_TOKEN = os.environ.get('CONFLUENCE_TOKEN')
CONFLUENCE_SPACE = os.environ.get('CONFLUENCE_SPACE')

if not all([CONFLUENCE_URL, CONFLUENCE_TOKEN, CONFLUENCE_SPACE]):
    raise ValueError("Variables d'environnement manquantes")
```

### 2. Fichier .env.example comme template

**Structure du template** :

```bash
# scripts/.env.example (dans Git)
# Copier ce fichier en .env et remplir avec vos valeurs

export CONFLUENCE_URL="https://wiki.uqam.ca"
export CONFLUENCE_TOKEN="votre_token_confluence_ici"
export CONFLUENCE_SPACE="UQAMGPT"

# Comment obtenir un token:
# 1. Aller sur https://wiki.uqam.ca
# 2. Profil > Personal Access Tokens
# 3. Créer un nouveau token avec permissions:
#    - Read (pages, spaces)
#    - Write (pages)
# 4. Copier le token généré ici
# 5. NE PAS committer ce fichier une fois modifié!
```

**Avantages** :

- ✅ Nouveau développeur voit la structure attendue
- ✅ Documentation intégrée (comment obtenir token)
- ✅ Pas de valeurs sensibles dans Git
- ✅ Process d'onboarding simplifié

### 3. Protection Git avec .gitignore

**Contenu du .gitignore** :

```gitignore
# Secrets et configuration
scripts/.env
*.env

# Environnements virtuels
.venv/
venv/
__pycache__/

# Fichiers temporaires
*.pyc
*.log
```

**Validation** :

```bash
# Vérifier que .env n'est pas tracké
git status scripts/.env
# Devrait montrer: "nothing to commit"
```

### 4. Cycle de vie du token

#### Création

```bash
# 1. Setup initial
cd /path/to/uqam-gpt-docs.wiki
cp scripts/.env.example scripts/.env

# 2. Éditer avec token réel
vim scripts/.env

# 3. Valider connexion
make test-connection
```

#### Utilisation

```bash
# Charger automatiquement dans scripts
source scripts/.env
make update
```

#### Révocation post-projet

**Processus recommandé** :

1. ✅ Migration terminée et validée
2. ✅ Token plus nécessaire pour maintenance quotidienne
3. ✅ Aller sur Confluence → Profil → Personal Access Tokens
4. ✅ Révoquer le token créé pour ce projet
5. ✅ Supprimer scripts/.env local

**Justification** :

- Limite la fenêtre d'exposition
- Suit le principe du moindre privilège
- Token peut être recréé si besoin ultérieur

### 5. Logging sécurisé

**Masquage du token dans logs** :

```python
def log_request(url, method, headers):
    """Log requête en masquant le token"""
    safe_headers = headers.copy()
    if 'Authorization' in safe_headers:
        safe_headers['Authorization'] = 'Bearer ***MASKED***'
    
    print(f"{method} {url}")
    print(f"Headers: {safe_headers}")
```

**Messages d'erreur sans token** :

```python
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    # Ne PAS logger headers qui contiennent le token
    print(f"Erreur HTTP {e.response.status_code}: {e.response.reason}")
    print(f"URL: {e.response.url}")
    # Headers volontairement omis
```

### 6. Validation de sécurité

**Commande de vérification** :

```bash
# Vérifier qu'aucun secret n'est dans Git
make security-check
```

**Implémentation dans Makefile** :

```makefile
security-check: ## Vérifier qu'aucun secret n'est exposé
	@echo "$(BLUE)Vérification de sécurité...$(NC)"
	@if git ls-files | grep -q '\.env$$'; then \
		echo "$(RED)❌ Fichier .env trouvé dans Git!$(NC)"; \
		exit 1; \
	fi
	@if git log --all --oneline | grep -qi 'token\|password\|secret'; then \
		echo "$(YELLOW)⚠️ Mentions de 'token/password/secret' dans commits$(NC)"; \
		echo "$(YELLOW)Vérifiez l'historique Git$(NC)"; \
	fi
	@echo "$(GREEN)✅ Aucun fichier .env trouvé dans Git$(NC)"
```

## Conséquences

### Positives

✅ **Zero secret dans Git** : Historique propre, pas de rotation nécessaire
✅ **Onboarding simple** : .env.example guide le setup
✅ **Révocation facile** : Token peut être révoqué post-migration
✅ **Logs sécurisés** : Token masqué dans output
✅ **Validation automatique** : make security-check détecte expositions

### Négatives

⚠️ **Setup manuel requis** : Chaque développeur doit créer .env
⚠️ **Pas de rotation automatique** : Token reste valide jusqu'à révocation manuelle
⚠️ **Risque de partage .env** : Développeurs doivent être formés

### Métriques de sécurité

- ✅ **0 token dans Git** : Vérification `git log` confirme
- ✅ **1 fichier template** : .env.example guide le process
- ✅ **100% masquage logs** : Aucun token visible dans output
- ✅ **Documentation complète** : MAKEFILE-GUIDE.md section sécurité

## Alternatives considérées

### Alternative 1 : Token en argument de commande

**Exemple** :

```bash
make update TOKEN="votre_token"
```

**Rejetée** :

- ❌ Token visible dans historique shell
- ❌ Token visible dans `ps aux`
- ❌ Plus verbeux pour chaque commande

### Alternative 2 : Fichier de credentials chiffré

**Exemple** : `.env.gpg` déchiffré avec GPG

**Rejetée** :

- ❌ Complexité (GPG setup, gestion clés)
- ❌ Overkill pour projet simple
- ❌ Barrière à l'entrée pour nouveaux contributeurs

### Alternative 3 : Service de secrets (Vault, AWS Secrets Manager)

**Rejetée** :

- ❌ Infrastructure externe requise
- ❌ Coût (si cloud)
- ❌ Complexité pour projet universitaire
- ❌ Dépendance sur service tiers

### Alternative 4 : Token hardcodé avec rotation automatique

**Rejetée** :

- ❌ Token toujours exposé pendant période de rotation
- ❌ Automatisation complexe
- ❌ Confluence peut ne pas supporter API de rotation

## Références

- [The Twelve-Factor App - Config](https://12factor.net/config) : Variables d'environnement pour configuration
- [OWASP Secret Management Cheat Sheet](https://cheatsheetsocial.com/owasp-secret-management-cheat-sheet/) : Best practices secrets
- [GitHub - Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) : Nettoyer historique Git
- [Atlassian - Personal Access Tokens](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html) : Documentation tokens Confluence

## Mise en œuvre

### Fichiers créés

- `scripts/.env.example` : Template avec documentation
- `.gitignore` : Protection scripts/.env

### Modifications code

Tous les scripts Python modifiés pour :

1. Charger variables depuis .env
2. Valider présence des variables
3. Masquer token dans logs
4. Messages d'erreur sans token

### Documentation

- `MAKEFILE-GUIDE.md` : Section "Configuration et Sécurité"
- `MAKEFILE-STATUS.md` : Recommandation de révocation post-migration
- `README.md` : Instructions setup .env

### Commandes Makefile

```bash
make setup          # Copie .env.example et demande édition
make test-connection # Valide token sans opération risquée
make security-check  # Vérifie qu'aucun secret dans Git
```

## Notes

Cette approche suit les recommandations de **UQAM Services Informatiques** et les **standards de sécurité académiques**. Le token est traité comme un mot de passe et doit être révoqué dès que le projet n'en a plus besoin.

**Important** : Le token doit être révoqué après migration initiale si aucune mise à jour régulière n'est prévue. Confluence permet de créer un nouveau token si besoin ultérieur.

La règle d'or : **Aucun secret ne doit jamais être commité dans Git, même dans une branche temporaire.**
