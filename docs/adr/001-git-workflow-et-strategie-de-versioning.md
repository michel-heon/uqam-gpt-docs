# ADR 001: Git Workflow et Stratégie de Versioning

## Statut

✅ Accepté

## Date

2025-11-17

## Contexte

Le projet **UQAM-GPT Wiki** nécessite une stratégie de gestion de code source qui permette de :
- Maintenir la synchronisation entre fichiers markdown sources et pages Confluence
- Faciliter les contributions et révisions de documentation
- Maintenir un historique clair des modifications du contenu wiki
- Permettre des rollbacks rapides en cas d'erreur de contenu
- Gérer plusieurs contributeurs travaillant sur différentes pages en parallèle

Le repository `michel-heon/uqam-gpt-docs.wiki` existe déjà sur la branche `master` avec des scripts d'automatisation (Makefile), mais sans convention formelle de workflow pour les contributions de contenu.

## Décision

### 1. Structure des branches (Workflow simplifié pour wiki)

Nous adoptons une structure simplifiée adaptée à un projet de documentation/wiki :

```
master (Confluence production)
  ↑
utilisateur/page-ou-feature (modifications)
```

#### **Branche `master`**
- **Rôle** : Source de vérité pour contenu markdown publié sur Confluence
- **Protection** : Protégée, merges via pull requests
- **Synchronisation** : `make update` déploie vers wiki.uqam.ca
- **Contenu** : Fichiers markdown (`postdoc/*.md`), scripts, Makefile

#### **Branches personnelles `utilisateur/page-ou-feature`**

**⭐ DÉCISION CLÉ : Préfixe utilisateur pour contributions wiki**

Pattern : `utilisateur/description-page` pour modifications de contenu

- **Rôle** : Modification de pages wiki ou amélioration des scripts
- **Nomenclature** : `utilisateur/description-courte`
  - ✅ `michel-heon/update-faq-page`
  - ✅ `jane-doe/add-troubleshooting`
  - ✅ `michel-heon/improve-makefile`
  - ❌ `feature/update-faq` (moins clair sur l'auteur)

**Avantages du préfixe utilisateur :**

1. **Isolation complète** : Chaque contributeur travaille dans son espace
2. **Zéro conflit de noms** : Impossible que 2 personnes créent la même branche
3. **Traçabilité instantanée** : `git branch -r` montre qui travaille sur quoi
4. **Collaboration flexible** : Facile de créer une branche partagée si besoin (`equipe/feature`)
5. **Permissions granulaires** : Possible de configurer protections par utilisateur

**Exemple concret pour wiki :**

```bash
# Michel met à jour la FAQ
git checkout -b michel-heon/update-faq-page

# Jane ajoute du troubleshooting (en parallèle)
git checkout -b jane-doe/add-troubleshooting

# Aucun conflit, aucune confusion! ✅
```

- **Cycle de vie** : Créées depuis `master`, mergées dans `master`, supprimées après merge
- **Synchronisation** : Après merge, `make update` déploie vers Confluence

### 2. Convention de versioning (Simplifié pour wiki)

Pour un projet wiki/documentation, nous adoptons une **approche de versioning simplifiée** basée sur les dates et fonctionnalités :

```
wiki-{YYYY-MM-DD}[-{description}]
```

#### **Pattern de tags**

| Type | Format | Exemple | Usage |
|------|--------|---------|-------|
| Release majeure | `wiki-{YYYY-MM-DD}` | `wiki-2025-11-25` | Déploiement Confluence stable |
| Feature specifique | `wiki-{YYYY-MM-DD}-{feature}` | `wiki-2025-11-25-makefile-automation` | Ajout fonctionnalité majeure |
| Hotfix | `wiki-{YYYY-MM-DD}-hotfix-{n}` | `wiki-2025-11-26-hotfix-1` | Correction urgente |

**Optionnel** : Pour releases majeures d'infrastructure, utiliser SemVer :

```
v{MAJOR}.{MINOR}.{PATCH}
```

#### **Exemples concrets**

- **MAJOR (v1.0.0)** : Migration initiale vers Confluence + Makefile complet
- **MINOR (v1.1.0)** : Ajout scripts de francisation automatique  
- **PATCH (v1.1.1)** : Correction boucle infinie fix-links

**⭐ RÈGLE : Tags descriptifs pour wiki**

Pour les mises à jour wiki, utiliser des **descriptions claires** :

✅ **RECOMMANDÉ** :

- `wiki-2025-11-25-makefile-automation` (feature: description explicite)
- `wiki-2025-11-26-security-updates` (feature: traçable)
- `wiki-2025-12-01-faq-restructure` (feature: clair)

❌ **ÉVITER** (peu informatif) :

- `wiki-2025-11-25` (trop générique pour feature)
- `update-1`, `update-2` (non daté, peu informatif)
- `v1.0.0-alpha.1` (SemVer inutile pour docs)

**Avantages** :

- � Date claire pour historique chronologique
- 🔍 Identification rapide du contenu
- 📋 Traçabilité dans les déploiements Confluence
- 🤝 Communication facilitée entre contributeurs
- 🏷️ Tags auto-documentés

### 3. Workflow de développement wiki

#### **Cycle de vie d'une mise à jour wiki**

```bash
# 1. Créer une branche personnelle depuis master
git checkout master
git pull origin master
git checkout -b user/update-faq-page

# 2. Édition des fichiers markdown localement
# Exemple: modifier postdoc/FAQ.md
vim postdoc/FAQ.md

# 3. Vérification avant commit (make check)
make check-links          # Vérifier liens internes
make check-formatting     # Vérifier formatage markdown
make check-structure      # Vérifier structure Confluence

# 4. Commit des modifications
git add postdoc/FAQ.md
git commit -m "docs: mise à jour section troubleshooting FAQ"

# 5. Push et création PR vers master
git push origin user/update-faq-page

# 6. Après validation, merge vers master
git checkout master
git merge user/update-faq-page

# 7. Déploiement vers Confluence
make update               # Déploie vers wiki.uqam.ca
git tag -a wiki-2025-11-26-faq-update -m "Wiki: mise à jour FAQ troubleshooting"
git push origin master --tags

# 8. Nettoyage
git branch -d user/update-faq-page
git push origin --delete user/update-faq-page
```

**Note** : Utilisez votre nom d'utilisateur (ou `user/`) pour les branches personnelles.

#### **Hotfix urgent wiki**

```bash
# Créer depuis master
git checkout master
git checkout -b hotfix/fix-broken-links

# Correction et vérification
vim postdoc/Home.md
make check-links          # Vérifier correction

# Commit et tag hotfix
git add postdoc/Home.md
git commit -m "fix: correction liens cassés page accueil"
git tag -a wiki-2025-11-26-hotfix-1 -m "Hotfix: liens cassés accueil"

# Merge vers master et déploiement immédiat
git checkout master
git merge hotfix/fix-broken-links
make update               # Déploiement urgent Confluence
git push origin master --tags

# Nettoyage
git branch -d hotfix/fix-broken-links
```

### 4. Protection de la branche master

**Règles de protection recommandées pour `master`** :

- ✅ Require pull request reviews (minimum 1 reviewer)
- ✅ Require status checks to pass (make check-*)
- ✅ Require branches to be up to date before merge
- ⚠️ Direct pushes autorisés pour administrateurs (déploiements urgents)
- ✅ Delete branch on merge (nettoyage automatique)

**Vérifications automatiques (CI/CD)** :

- `make check-links` - Validation liens internes
- `make check-formatting` - Validation markdown
- `make check-structure` - Validation structure Confluence

### 5. Messages de commit (Conventional Commits simplifié)

Format standardisé pour wiki et documentation :

```
<type>(<scope>): <description>

[corps optionnel]
```

**Types pour wiki** :

- `docs`: Modification contenu wiki (principal)
- `fix`: Correction erreur/lien cassé
- `feat`: Ajout nouvelle page/section
- `refactor`: Restructuration sans changement contenu
- `chore`: Maintenance infrastructure (Makefile, scripts)

**Exemples wiki** :

```
docs(faq): ajout section troubleshooting connexion

- Ajout Q&A pour erreurs SSL
- Ajout Q&A pour timeout API
- Mise à jour liens vers documentation
```

```
fix(home): correction liens cassés navigation

Liens relatifs vers postdoc/* corrigés pour Confluence
```

## Conséquences

### Positives ✅

- **Simplicité** : Workflow direct master + branches utilisateur
- **Sécurité** : Branche master protégée évite erreurs
- **Traçabilité** : Tags datés pour historique déploiements
- **Rollback** : Retour facile via tags et Makefile
- **Collaboration** : Chaque contributeur sa branche, pas de conflits
- **Automatisation** : Intégration avec `make check-*` et `make update`

### Négatives ⚠️

- **Discipline tags** : Nécessite respect convention `wiki-YYYY-MM-DD`
- **PRs obligatoires** : Overhead pour petites corrections (mais sécurité++)
- **Make dépendance** : Workflow dépend infrastructure Makefile

### Risques 🔴

- **Tags oubliés** : Risque de déploiement sans tag → Mitigé par documentation
- **Conflits merge** : Si modifications simultanées même page → Mitigé par communication
- **Branches longues** : Branches user/* non mergées → Mitigé par nettoyage régulier

## Alternatives considérées

### 1. **Branches `feature/*` sans préfixe utilisateur**

```bash
feature/update-faq
feature/add-troubleshooting
```

**Avantages :**

- Nomenclature standard Git Flow
- Simplicité apparente

**Inconvénients :**

- ❌ **Conflits de noms** : Si 2 contributeurs modifient FAQ
- ❌ **Manque de traçabilité** : Qui travaille sur quelle branche?
- ❌ **Collaboration difficile** : Partage entre contributeurs = conflits

**Verdict :** Rejeté en faveur de branches personnelles `user/`

### 2. **Workflow trunk-based (master direct)**

```bash
# Commits directs vers master sans branches
```

**Avantages :**

- ✅ **Simplicité maximale** : Pas de branches ni PRs
- ✅ **Vélocité** : Déploiement immédiat
- ✅ **Pas de merges** : Pas de conflits de merge

**Inconvénients :**

- ❌ **Risque élevé** : Erreurs directement en production Confluence
- ❌ **Pas de review** : Modifications non validées
- ❌ **Pas de rollback** : Difficile de revenir en arrière
- ❌ **Conflits directs** : Plusieurs contributeurs simultanés = chaos

**Verdict :** Rejeté - Trop risqué pour wiki collaboratif public

### 3. **Git Flow complet (avec dev, release, hotfix)**

```bash
master → release/* → dev → feature/*
```

**Avantages :**

- ✅ Process structuré pour releases complexes

**Inconvénients :**

- ❌ Trop complexe pour projet documentation
- ❌ Overhead inutile (pas de releases planifiées)
- ❌ Branches multiples difficiles à maintenir

**Verdict :** Rejeté - Overkill pour wiki

## Implémentation

### Phase 1 : Configuration (Complété)

- [x] Créer ADR
- [x] Configurer protection branche master GitHub
- [x] Documenter workflow dans ADR
- [x] Créer Makefile avec commandes check/update

### Phase 2 : Pratiques courantes

- [x] Utiliser branches `user/*` pour modifications
- [x] Toujours exécuter `make check-*` avant commit
- [x] Créer PR vers master pour validation
- [x] Taguer déploiements avec `wiki-YYYY-MM-DD`
- [x] Déployer via `make update` depuis master

### Phase 3 : Améliorations futures (Optionnel)

- [ ] Configurer GitHub Actions pour CI automatique
- [ ] Automatiser déploiement Confluence sur merge
- [ ] Générer changelog depuis tags et commits

## Références

- [Conventional Commits](https://www.conventionalcommits.org/) - Format commits standardisé
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow) - Workflow branches simple
- [ADR 004 Migration Confluence](./004-migration-confluence-makefile.md) - Makefile wiki automation
- [ADR 005 Verification First](./005-verification-first-approach.md) - Pattern check-before-fix

## Historique des révisions

| Date | Version | Changements | Auteur |
|------|---------|-------------|--------|
| 2025-11-17 | 1.0 | Création initiale (Teams app) | GitHub Copilot |
| 2025-11-26 | 2.0 | Adaptation complète pour projet wiki | GitHub Copilot |
