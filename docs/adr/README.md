# Architecture Decision Records (ADR)

Ce répertoire contient les Architecture Decision Records (ADR) pour le projet **UQAM-GPT Wiki Automation**. Les ADR documentent les décisions architecturales importantes prises au cours du développement du système d'automatisation de migration et maintenance du wiki Confluence.

## Qu'est-ce qu'un ADR ?

Un **Architecture Decision Record (ADR)** est un document qui capture une décision architecturale importante, son contexte, les alternatives considérées, et les conséquences de la décision. Les ADR aident à :

- 📚 **Préserver le contexte** : Comprendre pourquoi certaines décisions ont été prises
- 🔍 **Faciliter l'onboarding** : Nouveaux contributeurs comprennent rapidement les choix techniques
- ✅ **Justifier les choix** : Expliquer les trade-offs et alternatives considérées
- 🔄 **Réévaluer** : Revisiter les décisions quand le contexte change

## Format ADR

Chaque ADR suit ce format standardisé :

```markdown
# ADR XXX: Titre de la décision

## Statut
Accepté | Rejeté | Déprécié | Superseded

## Contexte
Quel est le problème ou la situation qui nécessite une décision?

## Décision
Quelle solution avons-nous choisie?

## Conséquences
Quels sont les impacts (positifs et négatifs) de cette décision?

## Alternatives considérées
Quelles autres options avons-nous évaluées et pourquoi les avons-nous rejetées?
```

## Index des ADR

| # | Titre | Statut | Date |
|---|-------|--------|------|
| [000](./000-processus-creation-adr.md) | Processus de Création et Gestion des ADR | ✅ Accepté | 2025-11-25 |
| [001](./001-git-workflow-et-strategie-de-versioning.md) | Git Workflow et Stratégie de Versioning | ✅ Accepté | 2025-11-26 |
| [002](./002-securite-secrets-git.md) | Sécurité des Secrets dans l'Historique Git | ⚪ Supersédé | 2025-11-25 |
| [003](./003-gestion-wiki-multi-projets.md) | Gestion du Wiki Multi-Projets | ⚪ Supersédé | 2025-11-25 |
| [004](./004-migration-confluence-makefile.md) | Migration Confluence avec Makefile Automatisé | ✅ Accepté | 2025-11-25 |
| [005](./005-verification-first-approach.md) | Approche "Vérification d'abord" pour les opérations wiki | ✅ Accepté | 2025-11-25 |
| [006](./006-gestion-securisee-secrets.md) | Gestion Sécurisée des Secrets Confluence | ✅ Accepté | 2025-11-25 |

### Notes sur les ADR

- **ADR 000-001** : Processus et workflow fondamentaux adaptés au projet wiki
- **ADR 002-003** : Supersédés par des décisions plus récentes (voir ADR 004 et 006)
- **ADR 004-006** : Décisions architecturales principales du système d'automatisation wiki

## Résumé des décisions clés du projet Wiki

### ADR-004 : Migration Confluence avec Makefile Automatisé

**Problème** : Migration manuelle du wiki vers Confluence Server (wiki.uqam.ca) avec contraintes de francisation (Loi 101), format Confluence Storage XML, liens internes fonctionnels, et maintenance continue.

**Décision** : Adoption d'un **Makefile complet** avec 20+ commandes orchestrant des scripts Python modulaires pour automatiser tout le cycle de vie (migration, francisation, vérification, mise à jour).

**Impact** : Automatisation complète (`make update`), reproductibilité (setup en 5 minutes), 100% francisation, 8 pages migrées avec succès. Mais certains liens HTML persist (non critique) et dépendance au Personal Access Token.

**Fichiers clés** : `Makefile`, `MAKEFILE-GUIDE.md`, `scripts/quick-check.py`, `scripts/franciser-texte.py`

### ADR-005 : Approche "Vérification d'abord" pour opérations wiki

**Problème** : Scripts de modification automatique causaient des boucles infinies (`fix-links-v2.py`) et faux positifs (19 liens GitHub signalés dans exemples de configuration).

**Décision** : Pattern **check-before-fix** avec séparation stricte entre commandes de vérification (`check-*` : lecture seule, rapide, sans confirmation) et commandes de modification (`fix-*`/`update-*` : avec confirmations, logs détaillés, marquées EXPÉRIMENTAL si risquées).

**Impact** : 0 boucle infinie, 0 faux positif (logique intelligente ignore pages de config), workflow en 4 étapes (diagnostic → analyse → correction → vérification), confiance restaurée dans les outils automatiques.

**Scripts créés** : `quick-check.py`, `check-links-only.py`, `test-confluence-connection.py`

### ADR-006 : Gestion Sécurisée des Secrets Confluence

**Problème** : Nécessité d'authentification API REST Confluence avec Personal Access Token sensible, risques d'exposition dans Git, logs, ou partage accidentel.

**Décision** : Fichier `.env` pour configuration (dans `.gitignore`), template `.env.example` avec documentation, masquage token dans logs, cycle de vie défini (création → utilisation → révocation post-migration), commande `make security-check` pour validation.

**Impact** : 0 token dans Git (confirmé par audit), 100% masquage logs, onboarding simplifié avec template, mais setup manuel requis pour chaque développeur et pas de rotation automatique.

**Sécurité** : Token révocable après migration, principe du moindre privilège appliqué.

## Processus de création d'un ADR

### Quand créer un ADR ?

Créez un ADR pour toute décision qui :

- ✅ Impacte l'architecture système de manière significative
- ✅ Nécessite de justifier des trade-offs entre plusieurs options
- ✅ Peut être remise en question plus tard ("Pourquoi avons-nous fait ça ?")
- ✅ Implique des conséquences importantes (positives ou négatives)

### Comment créer un ADR ?

1. **Numéroter** : Utiliser le prochain numéro séquentiel (ex: `006-titre-decision.md`)
2. **Structurer** : Suivre le format standard (Statut, Contexte, Décision, Conséquences, Alternatives)
3. **Justifier** : Expliquer le raisonnement, pas juste la conclusion
4. **Documenter alternatives** : Montrer que d'autres options ont été considérées
5. **Références** : Citer documentation, recherche, standards
6. **Réviser** : Faire relire par l'équipe avant acceptation
7. **Mettre à jour index** : Ajouter l'ADR à ce README

### Template ADR

Voir [adr-template.md](./adr-template.md) pour le template complet à copier lors de la création d'un nouvel ADR.

## Maintenance des ADR

### Statuts possibles

| Statut | Description |
|--------|-------------|
| **Proposé** | ADR en cours de discussion, pas encore accepté |
| **Accepté** | Décision validée et en application |
| **Déprécié** | Décision toujours en place mais à remplacer |
| **Superseded** | Remplacé par un nouvel ADR (indiquer lequel) |
| **Rejeté** | Décision proposée mais finalement rejetée |

### Révision des ADR

Les ADR sont **immutables** une fois acceptés. Si une décision doit être modifiée :

1. ❌ **Ne pas** modifier l'ADR original
2. ✅ Créer un **nouvel ADR** expliquant la nouvelle décision
3. ✅ Marquer l'ancien ADR comme **"Superseded by ADR-XXX"**
4. ✅ Mettre à jour l'index

### Historique des révisions

Chaque ADR maintient un tableau d'historique en bas du document :

```markdown
## Historique des révisions

| Date | Version | Changements | Auteur |
|------|---------|-------------|--------|
| 2025-11-17 | 1.0 | Création initiale | GitHub Copilot |
| 2025-12-01 | 1.1 | Clarification section X | Équipe |
```

## Références

### Ressources ADR

- [Michael Nygard - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)
- [Architecture Decision Records (Book)](https://www.oreilly.com/library/view/architecture-decision-records/9781492090038/)

### Outils ADR

- [adr-tools](https://github.com/npryce/adr-tools) - CLI pour gérer ADR
- [log4brains](https://github.com/thomvaill/log4brains) - ADR avec UI web
- [ADR Manager](https://marketplace.visualstudio.com/items?itemName=ks89.vscode-adr-manager) - Extension VS Code

## Démarrage rapide

### Consulter les ADR du projet Wiki

Pour comprendre les décisions prises pour ce projet :

1. **Commencer par** : [ADR-004 Migration Confluence](./004-migration-confluence-makefile.md) - Architecture complète
2. **Puis lire** : [ADR-005 Vérification d'abord](./005-verification-first-approach.md) - Leçons apprises
3. **Compléter avec** : [ADR-006 Sécurité secrets](./006-gestion-securisee-secrets.md) - Bonnes pratiques sécurité

## Utilisation des commandes wiki

```bash
# Diagnostic rapide (1 minute)
make quick-check

# Mise à jour contenu
vim postdoc/Support.md
make update

# Vérification post-update
make verify

# Sécurité
make security-check
```

Voir [MAKEFILE-GUIDE.md](../../MAKEFILE-GUIDE.md) pour documentation complète.

## Contact

Pour questions sur les ADR ou propositions de nouvelles décisions architecturales :

- **Projet** : UQAM-GPT Wiki Automation
- **Repository** : [michel-heon/uqam-gpt-docs.wiki](https://github.com/michel-heon/uqam-gpt-docs.wiki)
- **Documentation** : Voir `MAKEFILE-GUIDE.md` et `MAKEFILE-STATUS.md`

*Dernière mise à jour : 2025-11-25*
