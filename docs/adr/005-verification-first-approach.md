# ADR 013: Approche "Vérification d'abord" pour les opérations wiki

## Statut

✅ Accepté

## Date

2025-11-25

## Contexte

Lors du développement du système d'automatisation wiki, plusieurs incidents ont révélé les risques des modifications automatiques :

### Incident 1 : Boucle infinie fix-links

**Symptôme** : Script `fix-links-v2.py` exécuté en boucle infinie
**Impact** : Processus consommant CPU, nécessitant `pkill -9 python3`
**Cause racine** :
- Itération sur 8 pages avec regex complexes
- Pas de limite de temps
- Pas de vérification préalable
- Modification sans confirmation

### Incident 2 : Modification des exemples de configuration

**Symptôme** : Script tentait de modifier les URLs GitHub dans les exemples JSON
**Impact** : Risque de casser la documentation de configuration
**Cause racine** :
- Pas de distinction entre liens réels et exemples de code
- Remplacement global sans contexte
- Pas de liste d'exclusion pour pages spéciales

### Incident 3 : Faux positifs dans la vérification

**Symptôme** : 19 liens GitHub signalés comme problèmes
**Impact** : Perte de confiance dans les rapports automatiques
**Cause racine** :
- Script ne distinguait pas pages de configuration
- Liens GitHub dans JSON considérés comme erreurs
- Pas de contexte métier dans la logique

## Décision

### Principe fondamental : Vérifier avant de modifier

Adoption du pattern **check-before-fix** avec séparation stricte :

```
COMMANDES DE VÉRIFICATION (check-*)
├── Lecture seule
├── Pas de modifications
├── Pas de confirmations requises
├── Exécution rapide et sûre
└── Génèrent des rapports

COMMANDES DE MODIFICATION (fix-*, update-*)
├── Modifications de données
├── Confirmations requises
├── Logs détaillés
├── Messages d'avertissement
└── Marquées "expérimental" si risquées
```

### 1. Scripts de vérification

#### quick-check.py (vérification rapide)

**Caractéristiques** :
- ✅ Lecture seule des 8 pages
- ✅ Ignore les pages de configuration pour liens GitHub
- ✅ Compte les anglicismes sans modifier
- ✅ Affiche versions actuelles
- ✅ Génère un rapport résumé avec recommandations

**Code clé** :

```python
# Pages où les liens GitHub sont normaux (documentation de configuration)
config_pages = ['Configuration URLs et Manifest', 'Politique de confidentialité']

# Ignorer les liens GitHub dans les pages de configuration
is_config_page = any(config_page in title for config_page in config_pages)
if not is_config_page:
    total_github_links += github_links
```

**Sortie** :

```
========================================
Résumé
========================================
Pages avec GitHub links: 0/8
Pages avec anglicismes: 0/8

État: ✅ Excellent - Pas de problèmes détectés
```

#### check-links-only.py (vérification des liens)

**Caractéristiques** :
- ✅ Identifie liens HTML vs liens Confluence natifs
- ✅ Ne modifie AUCUNE page
- ✅ Rapporte pages affectées et nombre de liens
- ✅ Statistiques détaillées

**Sortie** :

```
✅ 5 pages avec des liens HTML à réviser:
  - Documentation: 8 liens
  - Guide: 4 liens
  - FAQ: 9 liens
  - Support: 6 liens
  - Conditions: 1 lien

Total: 28 liens HTML détectés
```

### 2. Scripts de modification avec confirmations

#### fix-links (EXPÉRIMENTAL)

**Caractéristiques** :
- ⚠️ Marqué "EXPÉRIMENTAL" dans Makefile
- ⚠️ Confirmation manuelle requise
- ⚠️ Message d'avertissement avant exécution
- ⚠️ Recommandation de faire check-links d'abord

**Makefile** :

```makefile
fix-links: ## ⚠️ [EXPÉRIMENTAL] Corriger les liens (risque de boucle)
	@echo "$(YELLOW)⚠️ ATTENTION: Cette commande est EXPÉRIMENTALE$(NC)"
	@echo "$(YELLOW)Elle peut prendre beaucoup de temps ou causer des boucles.$(NC)"
	@echo "$(YELLOW)Recommandation: utilisez 'make check-links' pour diagnostic d'abord.$(NC)"
	@read -p "Voulez-vous vraiment continuer? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(PYTHON) $(SCRIPTS_DIR)/fix-links-v2.py; \
	else \
		echo "$(BLUE)Opération annulée.$(NC)"; \
	fi
```

#### update (mise à jour rapide)

**Caractéristiques** :
- ✅ Mise à jour du contenu uniquement
- ✅ NE PAS inclure fix-links
- ✅ Rapide et sûr (< 1 minute)
- ✅ Peut être exécuté fréquemment

**Workflow** :

```bash
# Modification locale
vim postdoc/Support.md

# Mise à jour rapide
make update

# Vérification post-update
make quick-check
```

### 3. Workflow recommandé

```
┌─────────────────────────┐
│  1. DIAGNOSTIC          │
│  make quick-check       │
└───────────┬─────────────┘
            │
            ↓ Problèmes détectés?
            │
     ┌──────┴──────┐
     │             │
    Non           Oui
     │             │
     ↓             ↓
┌─────────┐  ┌──────────────────┐
│ OK      │  │ 2. ANALYSE       │
│ Terminé │  │ make check-links │
└─────────┘  └────────┬─────────┘
                      │
                      ↓ Action requise?
                      │
               ┌──────┴──────┐
               │             │
           Critique       Mineur
               │             │
               ↓             ↓
     ┌─────────────────┐  ┌──────────┐
     │ 3. CORRECTION   │  │ Ignorer  │
     │ (manuelle ou    │  │          │
     │  avec confirm)  │  └──────────┘
     └────────┬────────┘
              │
              ↓
     ┌─────────────────┐
     │ 4. VÉRIFICATION │
     │ make verify     │
     └─────────────────┘
```

### 4. Architecture des commandes

#### Catégorie: Tests et Diagnostic

```makefile
test-connection    # Vérifier connexion Confluence (30s)
quick-check       # Diagnostic rapide complet (1 min)
check-links       # Vérifier formats des liens (1 min)
```

**Garanties** :
- ✅ Aucune modification des données
- ✅ Exécution sans confirmation
- ✅ Temps d'exécution prévisible
- ✅ Rapports clairs et actionnables

#### Catégorie: Migration et Mises à jour

```makefile
migrate          # Migration initiale complète (avec confirm)
update           # Mise à jour contenu seulement (safe)
franciser        # Francisation (avec confirm)
fix-links        # Correction liens (EXPÉRIMENTAL, avec confirm)
```

**Garanties** :
- ⚠️ Modifications de données
- ⚠️ Confirmations requises (sauf update)
- ⚠️ Logs détaillés
- ⚠️ Messages d'avertissement pour commandes risquées

## Conséquences

### Positives

✅ **Confiance dans les outils** : Vérifications sans risque
✅ **Diagnostic rapide** : `make quick-check` donne l'état en 1 minute
✅ **Prévention d'erreurs** : Confirmations empêchent modifications accidentelles
✅ **Visibilité** : Scripts expérimentaux clairement identifiés
✅ **Efficacité** : Workflow en 4 étapes logique et reproductible

### Négatives

⚠️ **Étapes supplémentaires** : Diagnostic avant correction (bénéfice > coût)
⚠️ **Certaines corrections manuelles** : Fix-links trop risqué pour automatisation complète
⚠️ **Complexité du Makefile** : Plus de commandes à apprendre (compensé par `make help`)

### Métriques d'amélioration

**Avant "verification-first"** :
- ❌ Boucles infinies non détectées
- ❌ Faux positifs dans rapports (19 liens GitHub)
- ❌ Modifications sans preview
- ❌ Aucune commande de diagnostic

**Après "verification-first"** :
- ✅ 0 boucle infinie (fix-links isolé)
- ✅ 0 faux positif (pages config ignorées)
- ✅ 3 commandes de vérification stables
- ✅ 100% des modifications avec confirmation

## Alternatives considérées

### Alternative 1 : Mode "--dry-run" pour chaque script

**Avantage** : Une seule commande avec option
**Inconvénient** : Complexifie chaque script, risque d'oubli du flag

**Rejetée** : Préférence pour séparation explicite check-* vs fix-*

### Alternative 2 : Tout vérifier dans une seule commande

**Avantage** : Un seul rapport global
**Inconvénient** : Plus long, moins de contrôle granulaire

**Adoptée partiellement** : `quick-check` fait diagnostic global, mais `check-links` reste séparé pour analyse détaillée

### Alternative 3 : Pas de confirmations, rollback automatique

**Avantage** : Plus rapide, undo possible
**Inconvénient** : Complexité (versioning Confluence), faux sentiment de sécurité

**Rejetée** : Confluence ne supporte pas rollback facile, confirmations plus sûres

## Références

- [The Twelve-Factor App - Config](https://12factor.net/config) : Principe de séparation build/run/verify
- [Google SRE Book - Safe Rollouts](https://sre.google/sre-book/release-engineering/) : Validation avant déploiement
- [Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) : "Do one thing and do it well"

## Mise en œuvre

**Commandes de vérification créées** :
- `make test-connection` : Valider token et accès API
- `make quick-check` : Diagnostic complet intelligent
- `make check-links` : Analyse des formats de liens
- `make list-pages` : Lister pages et versions

**Modifications de comportement** :
- `make update` : Ne fait PLUS fix-links
- `make fix-links` : Ajout confirmation + message WARNING
- `make migrate` : Ajout confirmation

**Documentation** :
- MAKEFILE-GUIDE.md : Section "Workflows recommandés"
- MAKEFILE-STATUS.md : Section "Commandes recommandées vs éviter"

## Notes

Ce ADR documente une **leçon apprise** pendant le développement. L'incident de la boucle infinie a révélé l'importance de la séparation vérification/modification.

Le pattern **check-before-fix** est maintenant le standard pour tous les nouveaux scripts. Les scripts existants ont été classés "expérimental" s'ils ne respectent pas ce principe.

La règle d'or : **Si c'est risqué, ça doit demander confirmation. Si c'est safe, ça ne modifie rien.**
