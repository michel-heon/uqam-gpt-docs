# UQAM-GPT Documentation

Documentation officielle de l'écosystème **UQAM-GPT**, une suite d'agents conversationnels intelligents développés par l'Université du Québec à Montréal (UQAM).

## Wiki Documentation

La documentation complète est disponible dans le **[Wiki GitHub](https://github.com/michel-heon/uqam-gpt-docs/wiki)**.

## Projets UQAM-GPT

### UQAM-GPT Postdoc

Agent conversationnel dédié aux programmes postdoctoraux de l'UQAM.

- **Statut** : En production
- **Plateforme** : Microsoft Teams
- **Repository** : [uqam-gpt-postdoc-teams](https://github.com/UQAM-RECHERCHE/uqam-gpt-postdoc-teams)
- **Documentation** : [Wiki Postdoc](https://github.com/michel-heon/uqam-gpt-docs/wiki/postdoc/Home)

### UQAM-GPT SeUQAM (à venir)

Agent conversationnel pour le Service des équipements de l'UQAM.

- **Statut** : En planification
- **Public cible** : Personnel UQAM, chercheurs, étudiants

### UQAM-GPT Laboratoire (à venir)

Agent conversationnel pour la gestion des laboratoires de recherche.

- **Statut** : En planification
- **Public cible** : Chercheurs, techniciens, gestionnaires

### UQAM-GPT Approvisionnement (à venir)

Agent conversationnel pour le Service des approvisionnements de l'UQAM.

- **Statut** : En planification
- **Public cible** : Personnel administratif, chercheurs

## Architecture Technique

Tous les projets UQAM-GPT partagent une architecture commune :

- **LLM** : GPT-4.1 (Azure OpenAI Service)
- **Base de données** : Azure Cosmos DB
- **Recherche** : Azure AI Search (RAG)
- **Secrets** : Azure Key Vault
- **Hébergement** : Canada (Toronto + Québec)
- **Framework** : Teams AI Library + Bot Framework SDK
- **Runtime** : Node.js 20 LTS

## Conformité et Sécurité

- **Loi 25** (Québec) - Protection des renseignements personnels
- **PIPEDA** (Canada) - Protection des données personnelles  
- **ISO 27001** - Gestion de la sécurité de l'information
- **Résidence des données** : 100% Canada
- **Chiffrement** : TLS 1.3 (transit), AES-256 (repos)
- **Rétention** : 90 jours maximum

## Équipe

Michel Héon, Ph.D.  
Vice-rectorat à la recherche, à la création et à la diffusion (VRRCD)  
Université du Québec à Montréal (UQAM)

## Licence

Documentation sous licence **Creative Commons BY-NC-ND 4.0** (Attribution, Non-Commercial, No-Derivatives).

Le code source des projets peut avoir des licences différentes (voir chaque repository).

## Liens

- [Wiki Documentation](https://github.com/michel-heon/uqam-gpt-docs/wiki)
- [UQAM Recherche](https://recherche.uqam.ca/)
- [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service)

## Contact

- **Documentation** : [Wiki](https://github.com/michel-heon/uqam-gpt-docs/wiki)
- **Support** : Voir la page Support de chaque projet dans le wiki
- **Issues** : Ouvrez un ticket dans le repository du projet concerné

**Dernière mise à jour** : 2025-11-21 | **Projets actifs** : 1/4 (Postdoc)
