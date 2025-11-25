# ADR-007 : Sécurité des Secrets dans l'Historique Git

## Statut

⚪ Supersédé par [ADR 006 - Gestion Sécurisée Secrets](./006-gestion-securisee-secrets.md)

**Note** : Cet ADR reste comme exemple et référence historique. Pour le projet wiki, voir ADR 006.

## Date

2025-11-18 (Création)  
2025-11-25 (Supersédé par ADR 014)

## Contexte

**Auteur** : Architecture Team  
**Tags** : `security`, `git`, `credentials`, `azure`, `best-practices`  
**Projet d'origine** : UQAM-GPT Teams Application (exemple)

### Problème identifié

Un audit de sécurité de l'historique Git complet a révélé **2 clés API Azure Search exposées** dans plusieurs commits :

#### 🔴 Clés API exposées

| Clé API (tronquée) | Service Azure | Commits affectés | Statut |
|-------------------|---------------|------------------|---------|
| `9XLQVHdI...bjZ` | uqam-gpt-search-01 | df8f9b7, 3ea3262, 46cec31, c4844b9 | ✅ Masquée (9d11892) |
| `RpUK43RW...A5L` | uqam-gpt-search-02 | c4844b9 (main) | ❌ Non masquée |

#### 📍 Fichiers compromis

```
src/prompts/chat/config.json          (commits historiques)
OBSELETE/config.json                   (commit 46cec31)
OBSELETE/config-2.json                 (commit 46cec31)
docs/guides/CONFIGURATION.md           (commit df8f9b7)
env/.env.local.user.example            (commit df8f9b7)
```

#### 🔍 Méthodologie d'audit

```bash
# Recherche de patterns de secrets
git log --all --full-history -p | grep -E "(SECRET_|API_KEY|PASSWORD|crypto_|[0-9a-zA-Z]{40,})"

# Recherche spécifique par clé
git log --all -p -S "9XLQVHdIoBT" --source --all
git log --all -p -S "RpUK43RWI15" --source --all

# Vérification des commits récents
git log --oneline | head -20
```

### Causes racines

1. **Documentation avec exemples réels** : Fichiers de documentation utilisant des clés réelles au lieu de placeholders
2. **Fichiers de configuration obsolètes** : Anciens fichiers `config.json` commités avec credentials
3. **Absence de validation pré-commit** : Aucun hook Git pour détecter les secrets avant commit
4. **Templates sans masquage** : Fichiers `.example` créés initialement avec vraies valeurs

### Impact

- ✅ **Exposition confirmée** mais **clés non compromises** (confirmé par l'utilisateur)
- ⚠️ **Risque potentiel** : Clés accessibles dans l'historique Git public/privé
- 🔒 **Conformité** : Non-respect des best practices de sécurité Microsoft/Azure
- 📚 **Précédent dangereux** : Risque de répétition si non documenté

---

## 🎯 Décision

### Stratégie de remédiation adoptée

#### 1️⃣ **Remédiation immédiate** (Déjà effectuée)

**Commit 9d11892** : Masquage de la clé `9XLQVHdI...bjZ`

```bash
# Fichiers corrigés
docs/guides/CONFIGURATION.md          (2 occurrences)
env/.env.local.user.example            (1 occurrence)

# Remplacement
9XLQVHdIoBT2YgN7RENSZ4c0Had9jfWQgwOjf17UW8AzSeBMzbjZ
    ↓
<VOTRE_CLE_AZURE_SEARCH>
```

**Status** : ✅ Pushed to `origin/michel-heon/teams-agent-implementation`

#### 2️⃣ **Actions immédiates requises**

##### A. Rotation des clés API Azure

```bash
# Azure Portal → Azure AI Search → Keys → Regenerate

Service: uqam-gpt-search-01
├─ Primary Key (9XLQVHdI...bjZ)    → RÉGÉNÉRER ✅
└─ Secondary Key                    → GARDER (fallback)

Service: uqam-gpt-search-02
├─ Primary Key (RpUK43RW...A5L)    → RÉGÉNÉRER ✅
└─ Secondary Key                    → GARDER (fallback)
```

**Procédure** :
1. Régénérer les Primary Keys dans Azure Portal
2. Mettre à jour `env/.env.*.user` avec nouvelles clés
3. Redéployer les environnements (local, playground, dev)
4. Vérifier que l'application fonctionne
5. Marquer les anciennes clés comme révoquées dans la documentation

##### B. Nettoyage de l'historique Git (OPTIONNEL - Non recommandé)

⚠️ **Décision** : **NE PAS nettoyer l'historique Git**

**Raisons** :
- Les clés ne sont **pas compromises** (confirmé par l'utilisateur)
- Le repository est **privé** (UQAM-RECHERCHE/uqam-gpt-postdoc-teams)
- Risque de **casser les branches** et pull requests existants
- **Rotation des clés** est suffisante et moins risquée

**Alternative si nécessaire** (pour référence future) :

```bash
# Option 1: BFG Repo-Cleaner (recommandé)
java -jar bfg.jar --replace-text secrets.txt uqam-gpt-postdoc-teams.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Option 2: git-filter-repo (moderne)
git filter-repo --replace-text secrets.txt

# Option 3: git filter-branch (legacy)
git filter-branch --tree-filter 'git ls-files -z *.json | xargs -0 sed -i "s/9XLQVHdI...bjZ/<MASKED>/g"' -- --all
```

**⚠️ Avertissement** : Ces commandes réécrivent l'historique Git et nécessitent un `git push --force`, ce qui peut **casser les forks et clones existants**.

#### 3️⃣ **Mesures préventives** (À implémenter)

##### A. Pre-commit hooks avec git-secrets

**Installation** :

```bash
# macOS
brew install git-secrets

# Linux (Ubuntu/Debian)
sudo apt-get install git-secrets

# Ou via npm (cross-platform)
npm install -g git-secrets
```

**Configuration** :

```bash
# Initialiser git-secrets dans le repo
git secrets --install

# Ajouter patterns Azure
git secrets --add '(SECRET_|API_KEY|PASSWORD)=[A-Za-z0-9+/]{40,}'
git secrets --add '[A-Za-z0-9]{52}'  # Azure Search keys (52 chars)
git secrets --add 'crypto_[A-Za-z0-9]{40,}'

# Scanner l'historique existant
git secrets --scan-history
```

**Fichier `.git-secrets` à créer** :

```bash
# Azure API Keys
[A-Za-z0-9]{52}

# Generic secrets
(SECRET_|API_KEY|PASSWORD|TOKEN)=[A-Za-z0-9+/=]{20,}

# Teams Toolkit encrypted values
crypto_[A-Za-z0-9]{40,}

# Azure Connection Strings
AccountKey=[A-Za-z0-9+/=]{40,}

# Exclude false positives
!.*\.example$
!.*\/docs\/.*\.md$  # Docs avec placeholders OK
```

##### B. GitHub Actions / CI validation

**Fichier `.github/workflows/security-scan.yml`** :

```yaml
name: Security Scan

on:
  pull_request:
    branches: [main, dev, michel-heon/*]
  push:
    branches: [main, dev]

jobs:
  scan-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history
      
      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --debug --only-verified
      
      - name: GitLeaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

##### C. `.gitignore` renforcé

**Ajouts recommandés** :

```gitignore
# ============================================================================
# SECRETS ET CREDENTIALS (NE JAMAIS COMMITER)
# ============================================================================

# Environment files avec secrets
.env
.env.*
!.env.*.example
env/.env.*
!env/.env.*.example

# Teams Toolkit runtime configs
.localConfigs
.localConfigs.*

# Azure credentials
azure-credentials.json
service-principal.json

# SSH keys
*.pem
*.key
id_rsa*

# Backup files pouvant contenir secrets
*.bak
*.backup
*.old
*_backup.*

# Configuration files avec API keys
config.local.json
appsettings.local.json
secrets.json

# ============================================================================
# FICHIERS OBSOLÈTES (À EXCLURE SI CONTIENNENT SECRETS)
# ============================================================================
OBSELETE/
*.obsolete
```

##### D. Template files sécurisés

**Convention stricte** :

```bash
# ✅ BON : Fichiers .example avec placeholders
env/.env.local.user.example           → <VOTRE_CLE_AZURE_SEARCH>
env/.env.dev.user.example             → crypto_PLACEHOLDER_40_CHARS
config/appsettings.example.json       → "apiKey": "<YOUR_API_KEY>"

# ❌ INTERDIT : Fichiers avec vraies valeurs
env/.env.local.user                   → 9XLQVHdIoBT2YgN7...  (gitignored)
env/.env.dev.user                     → crypto_23cff1791...  (gitignored)
config/appsettings.json               → (gitignored)
```

**Script de validation** (`scripts/validate-templates.sh`) :

```bash
#!/bin/bash
set -e

echo "🔍 Validation des fichiers templates..."

# Patterns à détecter (secrets réels)
PATTERNS=(
    "[A-Za-z0-9]{52}"                      # Azure Search keys
    "crypto_[A-Za-z0-9]{40,}"              # Teams Toolkit encrypted
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}"  # GUIDs réels
)

# Fichiers à vérifier
FILES=(
    "env/.env.local.user.example"
    "env/.env.dev.user.example"
    "env/.env.playground.user.example"
    "docs/guides/CONFIGURATION.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        for pattern in "${PATTERNS[@]}"; do
            if grep -qE "$pattern" "$file"; then
                echo "❌ SECRET TROUVÉ dans $file"
                grep -E "$pattern" "$file"
                exit 1
            fi
        done
        echo "✅ $file OK"
    fi
done

echo "✅ Tous les templates sont sécurisés"
```

##### E. Azure Key Vault (Recommandé pour production)

**Migration des secrets** :

```javascript
// src/config.js (AVANT - Non sécurisé)
const azureSearchKey = process.env.SECRET_AZURE_SEARCH_KEY;

// src/config.js (APRÈS - Avec Key Vault)
const { DefaultAzureCredential } = require('@azure/identity');
const { SecretClient } = require('@azure/keyvault-secrets');

const credential = new DefaultAzureCredential();
const vaultUrl = `https://${process.env.KEY_VAULT_NAME}.vault.azure.net`;
const client = new SecretClient(vaultUrl, credential);

const azureSearchKey = await client.getSecret('azure-search-api-key');
```

**Avantages** :
- ✅ **Rotation automatique** des clés
- ✅ **Audit trail** complet (qui a accédé à quelle clé)
- ✅ **Managed Identity** (pas de secrets dans le code)
- ✅ **Conformité** SOC 2, ISO 27001

##### F. Managed Identity pour Azure Services (Idéal)

**Configuration** :

```javascript
// src/app/azureAISearchDataSource.js (AVANT)
const searchClient = new SearchClient(
    endpoint,
    indexName,
    new AzureKeyCredential(apiKey)  // ❌ Clé API en dur
);

// src/app/azureAISearchDataSource.js (APRÈS)
const { DefaultAzureCredential } = require('@azure/identity');

const searchClient = new SearchClient(
    endpoint,
    indexName,
    new DefaultAzureCredential()  // ✅ Managed Identity
);
```

**Setup Azure** :

```bash
# 1. Activer Managed Identity sur l'App Service
az webapp identity assign \
    --name <app-service-name> \
    --resource-group <resource-group>

# 2. Accorder les permissions Azure Search
az role assignment create \
    --assignee <managed-identity-principal-id> \
    --role "Search Index Data Reader" \
    --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Search/searchServices/<search-service>
```

**Avantages** :
- ✅ **Zéro secrets** dans le code ou configuration
- ✅ **Rotation automatique** (géré par Azure)
- ✅ **Audit intégré** (Azure Monitor)
- ✅ **Best practice** Microsoft

---

## 📊 Conséquences

### ✅ Avantages

1. **Sécurité renforcée** :
   - Secrets jamais exposés dans Git
   - Rotation des clés facilitée
   - Audit trail complet

2. **Conformité** :
   - Respect des standards Azure Security Benchmark
   - Conformité OWASP Top 10 (A07:2021 – Identification and Authentication Failures)
   - Alignement avec Microsoft Security Development Lifecycle (SDL)

3. **Automatisation** :
   - Pre-commit hooks détectent secrets avant push
   - CI/CD valide chaque PR
   - Pas de dépendance à la vigilance humaine

4. **Traçabilité** :
   - Historique des rotations de clés
   - Audit des accès (Key Vault / Managed Identity)
   - Documentation des incidents

### ⚠️ Inconvénients / Trade-offs

1. **Setup initial** :
   - Installation de git-secrets sur chaque machine dev
   - Configuration des GitHub Actions
   - Migration vers Key Vault/Managed Identity (optionnel)

2. **Faux positifs** :
   - Pre-commit hooks peuvent bloquer commits légitimes
   - Nécessite configuration de patterns d'exclusion

3. **Complexité** :
   - Courbe d'apprentissage pour nouveaux développeurs
   - Documentation supplémentaire nécessaire

4. **Performance** :
   - Scan de sécurité ajoute ~10-20s au CI/CD
   - Appels Key Vault ajoutent latence au démarrage (~200ms)

### 🎯 Métriques de succès

| Métrique | Avant | Objectif | Mesure |
|----------|-------|----------|--------|
| Secrets dans commits récents | 3 clés exposées (df8f9b7) | 0 | `git secrets --scan` |
| Temps de détection | Post-commit (manuel) | Pre-commit (auto) | Hook execution time |
| Coverage templates | 0% masqués | 100% masqués | Script validation |
| False positives CI | N/A | < 5% | GitHub Actions logs |
| Rotation des clés | Manuelle (ad-hoc) | Automatique (90j) | Key Vault policy |

---

## 🔄 Alternatives considérées

### Alternative 1 : Nettoyage historique Git (Rejeté)

**Approche** : `git filter-branch` ou `BFG Repo-Cleaner`

**Avantages** :
- Suppression complète des secrets de l'historique
- Conformité stricte (aucune trace)

**Inconvénients** :
- ❌ **Force push** nécessaire (casse les forks/clones)
- ❌ **Risque élevé** de perdre l'historique
- ❌ **Coordination complexe** avec l'équipe
- ❌ **Non nécessaire** si clés rotées et repo privé

**Décision** : ❌ **REJETÉ** - Rotation des clés + mesures préventives suffisent

### Alternative 2 : Secrets chiffrés dans Git (Rejeté)

**Approche** : `git-crypt` ou `ansible-vault`

**Avantages** :
- Secrets commités mais chiffrés
- Pas de fichiers `.user` à gérer

**Inconvénients** :
- ❌ **Clé de chiffrement** à distribuer (nouveau secret)
- ❌ **Complexité** pour onboarding
- ❌ **Rotation difficile** (re-chiffrer tout l'historique)

**Décision** : ❌ **REJETÉ** - Key Vault / Managed Identity est supérieur

### Alternative 3 : Environnement centralisé (Rejeté pour dev local)

**Approche** : Tous les secrets dans Azure uniquement, pas de `.env`

**Avantages** :
- Centralisation totale
- Audit complet

**Inconvénients** :
- ❌ **Dev local impossible** sans connexion Azure
- ❌ **Friction développement** (lenteur, dépendance réseau)
- ❌ **Coûts** (requêtes Key Vault en développement)

**Décision** : ❌ **REJETÉ pour local** - Mais ✅ **RECOMMANDÉ pour DEV/PROD**

---

## 📚 Références

### Standards et guidelines

- [OWASP Top 10 - A07:2021 Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [Microsoft Security Development Lifecycle (SDL)](https://www.microsoft.com/en-us/securityengineering/sdl)
- [Azure Security Benchmark - IM-1: Use centralized identity and authentication system](https://learn.microsoft.com/en-us/security/benchmark/azure/security-controls-v3-identity-management#im-1-use-centralized-identity-and-authentication-system)
- [CIS Azure Foundations Benchmark](https://www.cisecurity.org/benchmark/azure)

### Outils de sécurité

- [git-secrets (AWS Labs)](https://github.com/awslabs/git-secrets)
- [TruffleHog (TruffleSecure)](https://github.com/trufflesecurity/trufflehog)
- [GitLeaks](https://github.com/gitleaks/gitleaks)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [git-filter-repo](https://github.com/newren/git-filter-repo)

### Azure documentation

- [Azure Key Vault - Best Practices](https://learn.microsoft.com/en-us/azure/key-vault/general/best-practices)
- [Managed Identity for Azure Resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
- [Azure AI Search - Authentication](https://learn.microsoft.com/en-us/azure/search/search-security-api-keys)
- [Azure App Service - Managed Identity](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity)

### GitHub Security

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)
- [GitHub Actions - Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

### ADRs liés

- [ADR-006 : Gestion de AZURE_SEARCH_INDEX_NAME](./006-gestion-azure-search-index-name.md)
- [ADR-001 : Stratégie de branches Git](./001-strategie-branches-git.md)

---

## 🚀 Plan d'action (Roadmap)

### ✅ Phase 1 : Remédiation immédiate (COMPLÉTÉ)

- [x] Masquer clé `9XLQVHdI...bjZ` dans documentation (commit 9d11892)
- [x] Créer ADR-007 sur sécurité Git

### 🔴 Phase 2 : Actions urgentes (À FAIRE IMMÉDIATEMENT)

- [ ] **Régénérer clés API Azure Search** :
  - [ ] uqam-gpt-search-01 (Primary Key)
  - [ ] uqam-gpt-search-02 (Primary Key)
- [ ] **Mettre à jour configurations** :
  - [ ] `env/.env.local.user`
  - [ ] `env/.env.dev.user`
  - [ ] `env/.env.playground.user`
  - [ ] Azure App Service (dev environment)
- [ ] **Tester tous les environnements** :
  - [ ] Local (Test Tool)
  - [ ] Playground
  - [ ] Dev (Azure)

### 🟡 Phase 3 : Mesures préventives (1-2 semaines)

- [ ] **Installer git-secrets** :
  - [ ] Documenter dans README.md
  - [ ] Ajouter à checklist onboarding
- [ ] **Créer pre-commit hooks** :
  - [ ] `.git-secrets` patterns
  - [ ] Script de validation templates
- [ ] **Setup CI/CD security** :
  - [ ] GitHub Actions (TruffleHog)
  - [ ] GitLeaks scan
- [ ] **Renforcer .gitignore** :
  - [ ] Ajouter patterns secrets
  - [ ] Tester avec `git check-ignore`

### 🟢 Phase 4 : Optimisations long-terme (1-3 mois)

- [ ] **Migrer vers Azure Key Vault** (DEV/PROD) :
  - [ ] Provisionner Key Vault
  - [ ] Migrer secrets
  - [ ] Mettre à jour code (`src/config.js`)
- [ ] **Activer Managed Identity** (PROD) :
  - [ ] App Service
  - [ ] Azure Search
  - [ ] Azure OpenAI
- [ ] **Rotation automatique** :
  - [ ] Politique Key Vault (90 jours)
  - [ ] Alertes expiration
- [ ] **Formation équipe** :
  - [ ] Workshop sécurité
  - [ ] Documentation best practices
  - [ ] Quiz conformité

---

## 📝 Notes additionnelles

### Commits affectés détaillés

```bash
# Commit avec clé 9XLQVHdI...bjZ
df8f9b7 - docs: add ADR-006 for AZURE_SEARCH_INDEX_NAME configuration management
3ea3262 - Import complet de uqam-gpt-postdoc-teams-data (dev-data)
46cec31 - Dernière tentative de connexion à azureSearch sourceURL (dev)
c4844b9 - Ajustement de outline.png (main)

# Commit de remédiation
9d11892 - security: mask Azure Search API key in documentation ✅
```

### Leçons apprées

1. **Ne jamais utiliser de vraies valeurs dans les exemples** de documentation
2. **Créer les templates `.example` AVANT les fichiers réels** pour éviter copy-paste
3. **Automatiser la validation** car la vigilance humaine est faillible
4. **Rotation préventive** même si pas de compromission avérée
5. **Documentation** est critique pour éviter la répétition

### Contact sécurité

En cas de **découverte de secrets** ou **incident de sécurité** :

1. **NE PAS créer de ticket public** GitHub
2. **Contacter immédiatement** : security@uqam.ca
3. **Révoquer/Régénérer** les clés compromises
4. **Documenter** l'incident dans un ADR privé

---

**Dernière mise à jour** : 2025-11-18  
**Version** : 1.0  
**Révision prochaine** : 2025-12-18 (après implémentation Phase 3)
