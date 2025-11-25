# Politique de Confidentialité - UQAM-GPT Postdoc

**Date de dernière mise à jour** : 2025-11-21

**Application concernée** : UQAM-GPT Postdoc (Microsoft Teams Agent)

**Éditeur** : Université du Québec à Montréal (UQAM)  
Vice-rectorat à la recherche, à la création et à la diffusion (VRRCD)

**Contact** : Michel Héon

## 1. Données Collectées

### Données Utilisateur

- **Identité Microsoft Teams** : ID utilisateur, nom d'affichage, adresse email (AAD)
- **Conversations** : Questions posées au bot, historique conversationnel
- **Métadonnées** : Horodatage, canal/groupe Teams, langue préférée

### Données Techniques

- **Logs d'utilisation** : Requêtes API, temps de réponse, erreurs
- **Diagnostics** : Traces d'exécution Azure AI Search, Application Insights
- **Performance** : Métriques d'utilisation du modèle GPT-4.1

### Données NON Collectées

- Localisation géographique précise
- Numéro de téléphone
- Informations de paiement (app gratuite)
- Données de santé ou biométriques

## 2. Stockage des Données

### Localisation Géographique

- **Région Azure** : Canada Centre (Toronto) et Canada Est (Québec)
- **Conformité** : PIPEDA (Canada) et Loi 25 (Québec)
- **Résidence des données** : 100% des données au Canada

### Infrastructure

- **Conversations** : Azure Cosmos DB (chiffrement at-rest AES-256)
- **Recherche vectorielle** : Azure AI Search (index sécurisé)
- **Logs/Diagnostics** : Azure Application Insights (logs anonymisés)
- **Secrets** : Azure Key Vault (HSM-backed)

### Durée de Rétention

| Type de Données | Durée | Justification |
|-----------------|-------|---------------|
| Historique conversations | 90 jours | Support utilisateur, amélioration continue |
| Logs diagnostics | 30 jours | Débogage, performance monitoring |
| Métriques anonymisées | 1 an | Statistiques d'usage, rapports |
| Signalements problèmes | 2 ans | Conformité légale, audit |

### Suppression Automatique

- Conversations > 90 jours : **Purge automatique** via Azure Cosmos DB TTL
- Utilisateur quitte l'organisation : **Suppression immédiate** (webhook AAD)

## 3. Utilisation des Données

### Finalités Principales

1. **Assistance conversationnelle** : Répondre aux questions sur programmes postdoctoraux
2. **Récupération contextuelle (RAG)** : Recherche dans documentation UQAM
3. **Historique conversationnel** : Maintenir le contexte des échanges

### Finalités Secondaires

1. **Amélioration du service** : Analyser questions fréquentes, identifier lacunes documentaires
2. **Support technique** : Diagnostiquer erreurs, optimiser performances
3. **Conformité légale** : Répondre à signalements, audits sécurité

### Utilisations INTERDITES

- Vente ou partage à des tiers commerciaux
- Publicité ciblée ou profilage marketing
- Entraînement de modèles IA tiers (hors Azure OpenAI)
- Surveillance des employés ou évaluation de performance

## 4. Partage des Données

### Partage Technique (Sous-traitants)

- **Microsoft Azure** : Hébergement infrastructure (Canada)
- **Azure OpenAI Service** : Traitement des requêtes IA (sans entraînement modèle)
- **Application Insights** : Monitoring (Microsoft, données anonymisées)

**Contrats de protection** : Tous les sous-traitants sont liés par :

- Data Processing Agreements (DPA) Microsoft
- Clauses RGPD standard européennes
- Conformité Loi 25 (Québec)

### Partage Organisationnel

- **Administrateurs UQAM** : Accès restreint pour support technique
- **Équipe VRRCD** : Accès lecture seule pour statistiques agrégées

### Divulgation Légale

L'UQAM peut divulguer des données si **requis par la loi** :

- Ordonnance judiciaire canadienne
- Demande gouvernementale légitime
- Protection des droits de l'UQAM ou sécurité publique

**Notification** : L'utilisateur sera informé sauf si interdit légalement.

## 5. Mesures de Sécurité

### Protection Technique

- **Chiffrement en transit** : TLS 1.3 pour toutes les communications
- **Chiffrement au repos** : AES-256 dans Cosmos DB et Azure Storage
- **Authentification** : Microsoft Entra ID (AAD) avec SSO
- **Autorisation** : RBAC (Role-Based Access Control) Azure
- **Gestion secrets** : Azure Key Vault (rotation automatique)
- **Monitoring** : Détection d'intrusions, alertes sécurité 24/7

### Protection Organisationnelle

- **Accès minimal** : Principe du moindre privilège
- **Logs d'audit** : Traçabilité complète des accès administrateurs
- **Formation** : Personnel sensibilisé à la protection des données
- **Révision régulière** : Audits trimestriels des accès

### Conformité et Certifications

- **ISO 27001** : Certification Microsoft Azure
- **SOC 2 Type II** : Compliance Azure
- **PIPEDA** : Loi canadienne sur la protection des renseignements personnels
- **Loi 25** : Loi modernisant des dispositions législatives en matière de protection des renseignements personnels (Québec)

## 6. Vos Droits

En vertu de la **Loi 25 (Québec)** et du **PIPEDA (Canada)**, vous disposez des droits suivants :

### 1. Droit d'Accès

**Obtenir une copie** de vos données personnelles collectées.

**Comment** : Envoyer demande à Michel Héon avec objet "Demande d'accès - UQAM-GPT"

**Délai** : Réponse sous 30 jours

### 2. Droit de Rectification

**Corriger des données inexactes** ou incomplètes.

**Comment** : Email avec détails des corrections requises

**Délai** : Traitement sous 15 jours

### 3. Droit de Suppression

**Demander l'effacement** de vos données personnelles.

**Comment** : Email avec demande explicite de suppression

**Délai** : Suppression effective sous 7 jours (conversations + logs)

**Limitations** : Données requises pour conformité légale (signalements) conservées jusqu'à expiration légale.

### 4. Droit d'Opposition

**S'opposer au traitement** de vos données pour finalités secondaires (amélioration, statistiques).

**Comment** : Email avec indication des traitements refusés

**Impact** : Fonctionnalités principales maintenues, statistiques anonymisées uniquement

### 5. Droit de Portabilité

**Récupérer vos données** dans format structuré, couramment utilisé, lisible par machine.

**Format fourni** : JSON avec historique conversations, horodatages, métadonnées

**Comment** : Email avec demande d'export

**Délai** : Export fourni sous 15 jours

### 6. Droit de Plainte

**Déposer une plainte** auprès de l'autorité de protection des données.

**Québec** : Commission d'accès à l'information (CAI)  

- Site : [www.cai.gouv.qc.ca](https://www.cai.gouv.qc.ca/)
- Téléphone : 1-888-528-7741

**Canada** : Commissariat à la protection de la vie privée  

- Site : [www.priv.gc.ca](https://www.priv.gc.ca/)
- Téléphone : 1-800-282-1376

## 7. Contact et Questions

### Responsable de la Protection des Données

**Nom** : Michel Héon, Ph.D.  
**Fonction** : Coordonnateur technique UQAM-GPT  
**Organisation** : UQAM - Vice-rectorat à la recherche, à la création et à la diffusion (VRRCD)

**Contact** : Michel Héon  
**Adresse postale** :  
Université du Québec à Montréal  
405, rue Sainte-Catherine Est  
Montréal (Québec) H2L 2C4  
Canada

### Temps de Réponse

- **Demandes générales** : 5 jours ouvrables
- **Demandes d'accès/suppression** : 30 jours (maximum légal)
- **Incidents sécurité** : 72 heures (notification obligatoire)

### Support Technique

- **Contact** : Michel Héon
- **Signalement problème** : Via bouton "Signaler un problème" dans l'app
- **Documentation** : [https://github.com/michel-heon/uqam-gpt-docs/wiki](https://github.com/michel-heon/uqam-gpt-docs/wiki)

## 8. Modifications de cette Politique

### Notification des Changements

L'UQAM se réserve le droit de **modifier cette politique** à tout moment. En cas de changement :

1. **Notification in-app** : Message dans Teams au prochain usage
2. **Email** : Envoi à tous les utilisateurs actifs (si changement majeur)
3. **Historique** : Versions précédentes archivées sur wiki

### Version et Historique

| Version | Date | Changements Principaux |
|---------|------|------------------------|
| 1.0 | 2025-11-21 | Version initiale pour publication Teams Store |

### Acceptation Implicite

**Utilisation continue** = Acceptation des modifications.  
Si vous refusez les modifications, cessez d'utiliser l'application.

## 9. Cadre Légal et Juridiction

### Lois Applicables

Cette politique est régie par :

1. **Loi 25 (Québec)** : Loi modernisant des dispositions législatives en matière de protection des renseignements personnels
2. **PIPEDA (Canada)** : Loi sur la protection des renseignements personnels et les documents électroniques
3. **RGPD (Europe)** : Si utilisateurs européens (applicabilité extraterritoriale)
4. **Loi sur l'accès à l'information** : Transparence administrative UQAM

### Juridiction

**Tribunaux compétents** : Tribunaux du Québec (Montréal)

**Langue** : En cas de conflit entre versions linguistiques, la version **française** prévaut.

### Conformité Microsoft Teams

Cette application respecte les [Microsoft Teams Store policies](https://learn.microsoft.com/en-us/legal/marketplace/certification-policies#1140-teams) et les [Microsoft Privacy Standards](https://privacy.microsoft.com/).
