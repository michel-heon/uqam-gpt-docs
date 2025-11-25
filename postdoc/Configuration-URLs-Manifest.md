# Documentation des URLs manifest.json pour publication wiki

## Vue d'ensemble

Ce document explique les trois URLs requises dans le `manifest.json` de l'application Teams et leur correspondance avec la documentation wiki.

## Structure actuelle du manifest.json

```json
"developer": {
    "name": "Michel Héon Ph.D.(UQAM/VRRCD)",
    "websiteUrl": "https://uqam.ca",
    "privacyUrl": "https://uqam.ca/siteweb/confidentialite",
    "termsOfUseUrl": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
}
```

## URLs recommandées pour le wiki GitHub

Une fois le wiki publié sur `git@github.com:michel-heon/uqam-gpt-docs.git`, les URLs devraient pointer vers les pages correspondantes.

### Format des URLs GitHub Wiki

Les wikis GitHub sont accessibles via :
```
https://github.com/<owner>/<repo>/wiki/<PageName>
```

Pour notre projet :
```
https://github.com/michel-heon/uqam-gpt-docs/wiki/<PageName>
```

## Mapping des URLs

### 1. websiteUrl - Site principal du projet

**Description** : Point d'entrée principal de la documentation

**Options** :

**Option A - Page d'accueil du wiki** (RECOMMANDÉ)
```json
"websiteUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki"
```
- ✅ Pointe directement vers la documentation
- ✅ Accessible publiquement
- ✅ Maintenu par l'équipe projet

**Option B - Page Home du wiki**
```json
"websiteUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki/Home"
```
- ✅ Identique à l'option A (redirection automatique)

**Option C - Site UQAM générique** (ACTUEL)
```json
"websiteUrl": "https://uqam.ca"
```
- ⚠️ Trop générique, ne pointe pas vers la documentation spécifique
- ❌ Ne respecte pas l'esprit de la validation Teams Store

### 2. privacyUrl - Politique de confidentialité

**Description** : Politique de confidentialité spécifique à l'application

**Options** :

**Option A - Page wiki dédiée** (RECOMMANDÉ)
```json
"privacyUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki/Politique-de-Confidentialite"
```
- ✅ Contenu complet et détaillé (463 lignes)
- ✅ Conforme Loi 25, PIPEDA, RGPD
- ✅ Spécifique à UQAM-GPT Postdoc
- ✅ Accessible sans authentification
- ✅ HTTPS obligatoire (✅ GitHub)

**Option B - Page UQAM générique** (ACTUEL)
```json
"privacyUrl": "https://uqam.ca/siteweb/confidentialite"
```
- ❌ Politique générale UQAM, pas spécifique à l'application
- ❌ Ne mentionne pas Azure OpenAI, RAG, traitement IA
- ❌ Peut échouer la validation Teams Store

**Option C - URL UQAM personnalisée** (SI DISPONIBLE)
```json
"privacyUrl": "https://recherche.uqam.ca/gpt-postdoc/confidentialite"
```
- ✅ Domaine institutionnel
- ⚠️ Nécessite hébergement sur serveur UQAM
- ⚠️ Maintenance et mise à jour par services UQAM

### 3. termsOfUseUrl - Conditions d'utilisation

**Description** : Conditions d'utilisation et licence de l'application

**Options** :

**Option A - Page wiki dédiée** (RECOMMANDÉ)
```json
"termsOfUseUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki/Conditions-Utilisation"
```
- ✅ Contenu complet et spécifique à l'application
- ✅ Explique la licence CC BY-NC-ND 4.0 dans le contexte de l'app
- ✅ Inclut garanties, responsabilités, usage commercial interdit
- ✅ Mentionnent UQAM comme titulaire des droits
- ✅ Contact et support spécifiques (Michel Héon)

**Option B - Licence Creative Commons directe** (ACTUEL)
```json
"termsOfUseUrl": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
```
- ⚠️ Licence générique CC, ne mentionne pas UQAM
- ❌ Ne contient pas les conditions spécifiques à l'application
- ❌ Pas de clause de non-garantie spécifique
- ❌ Pas d'informations sur l'usage institutionnel acceptable
- ⚠️ Peut être insuffisant pour validation Teams Store

**Option C - Combinaison** (COMPROMIS)
```json
"termsOfUseUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki/Conditions-Utilisation"
```
Puis dans Conditions-Utilisation.md, référence claire à CC BY-NC-ND 4.0
- ✅ Meilleur des deux mondes
- ✅ Contexte UQAM + licence standard

## Recommandations finales

### Configuration recommandée pour manifest.json

```json
"developer": {
    "name": "Michel Héon Ph.D.(UQAM/VRRCD)",
    "websiteUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki",
    "privacyUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki/Politique-de-Confidentialite",
    "termsOfUseUrl": "https://github.com/michel-heon/uqam-gpt-docs/wiki/Conditions-Utilisation"
}
```

### Validation des URLs

Avant de soumettre au Teams Store, vérifier :

1. **Accessibilité publique** : Ouvrir chaque URL en navigation privée (sans authentification GitHub)
2. **HTTPS** : Toutes les URLs doivent utiliser HTTPS (✅ GitHub le fait automatiquement)
3. **Contenu approprié** : Pas de liens vers AppSource, marketplace, ou contenu commercial
4. **Langue** : Français (primaire) avec traductions anglaises si nécessaire
5. **Maintenance** : URLs stables, pas de redirections temporaires

### Domaines valides (validDomains)

Ajouter GitHub au tableau validDomains du manifest.json :

```json
"validDomains": [
    "github.com"
]
```

Cela permet aux liens wiki de fonctionner correctement dans l'application Teams.

## Étapes de mise à jour

### 1. Publier le wiki

```bash
# Clone le dépôt wiki
git clone git@github.com:michel-heon/uqam-gpt-docs.git

# Copier les fichiers wiki
cp appPackage/wiki/*.md uqam-gpt-docs/

# Commit et push
cd uqam-gpt-docs/
git add .
git commit -m "docs: publish UQAM-GPT Postdoc user documentation"
git push origin main
```

### 2. Vérifier les URLs publiques

Tester dans un navigateur (navigation privée) :
- <https://github.com/michel-heon/uqam-gpt-docs/wiki>
- <https://github.com/michel-heon/uqam-gpt-docs/wiki/Home>
- <https://github.com/michel-heon/uqam-gpt-docs/wiki/Politique-de-Confidentialite>
- <https://github.com/michel-heon/uqam-gpt-docs/wiki/Conditions-Utilisation>

### 3. Mettre à jour manifest.json

Modifier les trois URLs dans `appPackage/manifest.json` avec les URLs wiki vérifiées.

### 4. Ajouter GitHub aux domaines valides

```json
"validDomains": [
    "github.com"
]
```

### 5. Valider le manifest

```bash
# Validation syntaxique
npx teamsfx validate --env local

# Test d'empaquetage
npx teamsfx package --env local
```

### 6. Tester dans Teams

- Installer l'application mise à jour
- Cliquer sur "Privacy Policy" dans les informations de l'app
- Vérifier que la page wiki s'ouvre correctement
- Vérifier les liens internes du wiki

## Fichiers wiki créés

Les fichiers suivants sont prêts pour publication :

1. **Home.md** (126 lignes) - Page d'accueil avec navigation
2. **Guide-Demarrage-Rapide.md** (268 lignes) - Guide de démarrage
3. **Support.md** (464 lignes) - Support et dépannage
4. **FAQ.md** (539 lignes) - 30 questions fréquentes
5. **Politique-de-Confidentialite.md** (463 lignes) - Politique de confidentialité complète
6. **Signalement-Problemes.md** (285 lignes) - Processus de signalement
7. **Conditions-Utilisation.md** (183 lignes) - CONDITIONS NOUVELLEMENT CRÉÉES

Total : 7 fichiers, 2328 lignes, ~78K

## Conformité Teams Store

Cette configuration satisfait les exigences suivantes du Microsoft Teams Store :

- ✅ **Privacy Policy URL** - Pointe vers documentation complète et spécifique
- ✅ **Terms of Use URL** - Pointe vers conditions détaillées avec licence
- ✅ **Website URL** - Pointe vers documentation utilisateur complète
- ✅ **HTTPS obligatoire** - GitHub Wiki utilise HTTPS
- ✅ **Accessibilité publique** - Aucune authentification requise
- ✅ **Domaine approprié** - github.com acceptable pour documentation open-source
- ✅ **Contenu conforme** - Pas de liens commerciaux ou AppSource

## Alternatives futures

Si l'UQAM souhaite héberger la documentation sur ses propres serveurs :

### Option serveur UQAM

```json
"websiteUrl": "https://recherche.uqam.ca/gpt-postdoc",
"privacyUrl": "https://recherche.uqam.ca/gpt-postdoc/confidentialite",
"termsOfUseUrl": "https://recherche.uqam.ca/gpt-postdoc/conditions"
```

**Avantages** :
- Domaine institutionnel (uqam.ca)
- Contrôle total sur l'hébergement
- Peut inclure branding UQAM

**Inconvénients** :
- Nécessite configuration serveur web
- Maintenance par services informatiques UQAM
- Processus d'approbation potentiellement long
- Moins flexible pour mises à jour rapides

**Recommandation** : Commencer avec GitHub Wiki pour soumission Teams Store, migrer vers serveur UQAM si demandé par l'administration.

## Support et questions

Pour toute question sur cette configuration :

**Michel Héon, Ph.D.**  
Vice-rectorat à la recherche, à la création et à la diffusion  
Université du Québec à Montréal  
Contact : Michel Héon

---

**Dernière mise à jour** : 20 novembre 2025  
**Version manifest** : 1.1.1
