# ADR 011: Gestion du Wiki Multi-Projets et Déploiement Automatisé

## Statut

⚪ Supersédé par [ADR 004 - Migration Confluence Makefile](./004-migration-confluence-makefile.md)

**Note** : Cet ADR décrivait une approche GitHub Wiki. Le projet a migré vers Confluence Server. Conservé comme référence historique.

## Date

2025-11-21 (Création)  
2025-11-25 (Supersédé - Migration Confluence)

## Contexte

**Projet d'origine** : UQAM-GPT Documentation (GitHub Wiki)  
**Statut actuel** : Remplacé par approche Confluence Server (voir ADR 012)

Le projet UQAM-GPT nécessitait une documentation complète et centralisée pour plusieurs sous-projets (Postdoc, SeUQAM, Laboratoire, Approvisionnement). Cette documentation devait être :

1. **Versionnée** : Suivre l'évolution de chaque projet
2. **Centralisée** : Un seul point d'entrée pour toute la documentation
3. **Multi-projets** : Supporter plusieurs projets partageant la même infrastructure
4. **Accessible** : Via GitHub Wiki et dépôt principal GitHub
5. **Automatisée** : Déploiement simple via Makefile

### Architecture actuelle

- **Source de vérité** : `appPackage/wiki/` dans chaque projet (ex: uqam-gpt-postdoc-teams)
- **Dépôt de documentation** : `git@github.com:michel-heon/uqam-gpt-docs.git`
  - Branche `main` : Dépôt principal GitHub (landing page)
  - Wiki GitHub : `git@github.com:michel-heon/uqam-gpt-docs.wiki.git` (branche `master`)
- **Projets contributeurs** :
  - `uqam-gpt-postdoc-teams` (production)
  - `uqam-gpt-seuqam` (à venir)
  - `uqam-gpt-laboratoire` (à venir)
  - `uqam-gpt-approvisionnement` (à venir)

### Problème

Sans système de déploiement automatisé, la maintenance de la documentation devient complexe :

- Déploiement manuel vers deux destinations (wiki + repo principal)
- Risque d'incohérence entre source et destinations
- Difficulté de contribution pour plusieurs projets
- Pas de traçabilité des modifications

## Décision

Nous adoptons un **système de déploiement automatisé via Makefile** avec les principes suivants :

### 1. Structure du Dépôt de Documentation

#### Structure Source (appPackage/wiki/)

```
appPackage/wiki/
├── Home-Root.md           # Vue d'ensemble multi-projets (→ Home.md racine)
├── README.md              # Documentation contributeurs
└── postdoc/               # Fichiers sources organisés par projet
    ├── Home.md
    ├── Guide-Demarrage-Rapide.md
    ├── FAQ.md
    ├── Configuration-URLs-Manifest.md
    ├── Politique-de-Confidentialite.md
    ├── Conditions-Utilisation.md
    ├── Support.md
    └── Signalement-Problemes.md
```

#### Structure Déployée

**Important** : GitHub Wiki ne supporte pas les URLs avec sous-répertoires (ex: `wiki/postdoc/Home` ne fonctionne pas). Le système utilise donc un **préfixe de fichier** au lieu de sous-répertoires.

```
uqam-gpt-docs/
├── README.md              # Page d'accueil GitHub (généré depuis source)
└── (aucun autre fichier)  # Dépôt minimal

uqam-gpt-docs.wiki/
├── Home.md                        # Page d'accueil wiki (← Home-Root.md)
├── README.md                      # Documentation contributeurs
├── postdoc-Home.md                # ← postdoc/Home.md
├── postdoc-Guide-Demarrage-Rapide.md
├── postdoc-FAQ.md
├── postdoc-Configuration-URLs-Manifest.md
├── postdoc-Politique-de-Confidentialite.md
├── postdoc-Conditions-Utilisation.md
├── postdoc-Support.md
├── postdoc-Signalement-Problemes.md
├── seuqam-*.md            # Documentation UQAM-GPT SeUQAM (à venir)
├── laboratoire-*.md       # Documentation UQAM-GPT Laboratoire (à venir)
└── approvisionnement-*.md # Documentation UQAM-GPT Approvisionnement (à venir)
```

**Transformation lors du déploiement** :

- Source : `wiki/postdoc/Home.md` → Déployé : `postdoc-Home.md`
- Liens internes : Doivent utiliser le préfixe `postdoc-` (ex: `[Guide](postdoc-Guide-Demarrage-Rapide)`)


### 2. Flux de Déploiement

```
┌─────────────────────────────────────────────────────────────┐
│ Projet Source (ex: uqam-gpt-postdoc-teams)                  │
│                                                              │
│  appPackage/wiki/                                           │
│  ├── Home.md              ← Source de vérité               │
│  ├── README.md            ← Source de vérité               │
│  ├── Home-Root.md         ← Vue d'ensemble multi-projets   │
│  ├── *.md                 ← Autres pages documentation     │
│  └── Makefile             ← Automatisation déploiement     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ make wiki-deploy MSG="..."
                              │ make docs-deploy-readme MSG="..."
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Dépôts de Destination                                        │
│                                                              │
│  uqam-gpt-docs.wiki/ (branche master)                       │
│  ├── Home.md              ← Copie de Home-Root.md          │
│  ├── README.md            ← Copie de README.md             │
│  └── postdoc/             ← Copie de tous les *.md         │
│                                                              │
│  uqam-gpt-docs/ (branche main)                              │
│  └── README.md            ← Copie de README.md             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │ GitHub.com           │
                    │ - Wiki navigable     │
                    │ - Landing page       │
                    └──────────────────────┘
```

### 3. Commandes Makefile

#### Déploiement Wiki (Multi-fichiers)

```makefile
# Configuration
WIKI_REPO := git@github.com:michel-heon/uqam-gpt-docs.wiki.git
WIKI_DIR := uqam-gpt-docs.wiki
WIKI_SOURCE := wiki
WIKI_BRANCH := master
WIKI_PROJECT := postdoc  # Nom du projet (postdoc, seuqam, etc.)

# Commandes disponibles
make wiki-init          # Clone le wiki
make wiki-pull          # Met à jour le clone local
make wiki-sync          # Synchronise fichiers source → wiki/projet/
make wiki-status        # Affiche le statut git
make wiki-diff          # Affiche les changements
make wiki-commit        # Commit avec message préfixé "projet:"
make wiki-push          # Push vers origin/master
make wiki-deploy        # Déploiement complet (pull + sync + commit + push)
make wiki-clean         # Supprime le clone local
make wiki-help          # Affiche l'aide
```

#### Déploiement Dépôt Principal (README uniquement)

```makefile
# Configuration
DOCS_REPO := git@github.com:michel-heon/uqam-gpt-docs.git
DOCS_DIR := ../../../uqam-gpt-docs
DOCS_BRANCH := main

# Commandes disponibles
make docs-sync-readme   # Synchronise README.md source → docs/
make docs-deploy-readme # Déploiement complet (sync + commit + push)
```

### 4. Règles de Gestion

1. **Source unique de vérité** : `appPackage/wiki/` dans chaque projet
2. **Fichier spécial** : `Home-Root.md` devient `Home.md` (vue d'ensemble wiki)
3. **Préfixe de commit** : `"projet: message"` (ex: `"postdoc: ajout FAQ"`)
4. **Branches** : 
   - Wiki utilise `master` (branche par défaut GitHub Wiki)
   - Wiki a aussi `main` (synchronisée avec `master` pour compatibilité)
   - Dépôt principal utilise `main`
5. **Isolation projet** : Chaque projet utilise un préfixe de fichier (ex: `postdoc-*.md`)
6. **Structure sources** : Fichiers organisés en sous-répertoires (`wiki/postdoc/`) mais déployés avec préfixe
7. **README.md partagé** : Même source déployée au wiki et au repo principal

### 5. Workflow Contributeur

```bash
# 1. Modifier la documentation source
cd appPackage/wiki
vim Guide-Demarrage-Rapide.md

# 2. Déployer vers le wiki
cd ..
make wiki-deploy MSG="mise à jour guide démarrage"

# 3. (Optionnel) Mettre à jour le README.md
vim wiki/README.md
make docs-deploy-readme MSG="mise à jour README"

# 4. Commit dans le projet source
git add wiki/
git commit -m "docs: mise à jour guide démarrage"
git push
```

## Conséquences

### Positives ✅

1. **Automatisation complète** : Plus de manipulation git manuelle
2. **Cohérence garantie** : Source unique déployée automatiquement
3. **Multi-projets scalable** : Ajout facile de nouveaux projets (seuqam, laboratoire, etc.)
4. **Traçabilité** : Commits préfixés par projet
5. **Simplicité** : Une commande `make wiki-deploy` pour tout déployer
6. **Isolation** : Chaque projet travaille indépendamment dans son sous-dossier
7. **Dual deployment** : Wiki + landing page GitHub synchronisés

### Négatives ⚠️

1. **Dépendance Makefile** : Contributeurs doivent comprendre le système
2. **Clones locaux** : Espace disque pour `uqam-gpt-docs.wiki/` et `uqam-gpt-docs/`
3. **Maintenance** : Ajout d'un nouveau projet nécessite mise à jour Makefile
4. **Limitation GitHub Wiki** : Pas de support des sous-répertoires dans les URLs, nécessite préfixes de fichiers
5. **Branche master** : Wiki GitHub utilise `master` par défaut (bien que `main` soit disponible)
6. **Conflit potentiel** : Si plusieurs contributeurs déploient simultanément
7. **Liens internes** : Doivent utiliser le préfixe projet (ex: `postdoc-Home` au lieu de `Home`)

### Mitigations

1. **Documentation claire** : Commandes `wiki-help` et `docs-help`
2. **Validation** : `wiki-check-sources` vérifie fichiers avant déploiement
3. **Status visible** : `wiki-status` et `wiki-diff` avant commit
4. **Pull automatique** : `wiki-deploy` fait `git pull` avant push
5. **Messages obligatoires** : Validation `MSG=""` requise

## Alternatives Considérées

### Alternative 1: Git Submodules

**Rejetée** : Trop complexe pour contributeurs non-experts Git

### Alternative 2: GitHub Actions CI/CD

**Rejetée** : Nécessite configuration complexe, latence déploiement

### Alternative 3: Wiki unique sans sous-dossiers

**Rejetée** : Collision noms fichiers entre projets, pas scalable

### Alternative 4: Dépôts séparés par projet

**Rejetée** : Fragmentation documentation, pas de vue d'ensemble

### Alternative 5: Déploiement manuel

**Rejetée** : Source d'erreurs, pas reproductible, fastidieux

## Implémentation

### Phase 1: Wiki Multi-Projets ✅ (Complété)

- [x] Configuration Makefile (WIKI_REPO, WIKI_DIR, WIKI_SOURCE, WIKI_BRANCH, WIKI_PROJECT)
- [x] Commandes wiki-* (init, pull, sync, status, diff, commit, push, deploy, clean, help)
- [x] Déploiement structure postdoc/
- [x] Home-Root.md comme page d'accueil wiki
- [x] Tests et validation

### Phase 2: Dépôt Principal ✅ (Complété)

- [x] Configuration Makefile (DOCS_REPO, DOCS_DIR, DOCS_BRANCH)
- [x] Commande docs-sync-readme
- [x] Commande docs-deploy-readme
- [x] Synchronisation README.md concis (sans icônes)

### Phase 3: Nouveaux Projets (À venir)

- [ ] Duplication système pour uqam-gpt-seuqam
- [ ] Duplication système pour uqam-gpt-laboratoire
- [ ] Duplication système pour uqam-gpt-approvisionnement
- [ ] Tests multi-projets simultanés

### Phase 4: Améliorations (Optionnel)

- [ ] `make deploy-all` : Déploie wiki + readme en une commande
- [ ] Validation markdown (linting)
- [ ] Détection conflits avant push
- [ ] GitHub Actions backup (déploiement automatique sur PR merge)

## Références

- [GitHub Wiki Documentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis)
- [Makefile Best Practices](https://makefiletutorial.com/)
- [ADR 001: Git Workflow et Stratégie de Versioning](./001-git-workflow-et-strategie-de-versioning.md)

## Notes

- **Home.md wiki** : Généré depuis `Home-Root.md` (vue d'ensemble multi-projets)
- **Home.md projet** : Spécifique à chaque projet (source: `postdoc/Home.md`, déployé: `postdoc-Home.md`)
- **README.md** : Documentation pour contributeurs (pas pour utilisateurs finaux)
- **Politique branches** : 
  - Wiki = `master` (branche par défaut) et `main` (synchronisée)
  - Repo principal = `main`
- **Organisation sources** : Sous-répertoires par projet (`wiki/postdoc/`) pour clarté
- **Déploiement** : Préfixes de fichiers (`postdoc-*.md`) car GitHub Wiki ne supporte pas les sous-répertoires dans les URLs
- **Liens internes** : Toujours utiliser le format avec préfixe (ex: `[Guide](postdoc-Guide-Demarrage-Rapide)` même dans les sources)
