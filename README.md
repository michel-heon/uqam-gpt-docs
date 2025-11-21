# UQAM-GPT Documentation

Documentation officielle de l'écosystème **UQAM-GPT**, une suite d'agents conversationnels intelligents développés par l'Université du Québec à Montréal (UQAM).

## 📚 Wiki Documentation

La documentation complète est disponible dans le **[Wiki GitHub](https://github.com/michel-heon/uqam-gpt-docs/wiki)**.

## 🎯 Projets UQAM-GPT

### 🎓 [UQAM-GPT Postdoc](https://github.com/michel-heon/uqam-gpt-docs/wiki/postdoc/Home)

Agent conversationnel dédié aux **programmes postdoctoraux** de l'UQAM.

- **Statut** : ✅ En production
- **Plateforme** : Microsoft Teams
- **Repository** : [uqam-gpt-postdoc-teams](https://github.com/UQAM-RECHERCHE/uqam-gpt-postdoc-teams)

**Documentation** :
- [Guide de démarrage rapide](https://github.com/michel-heon/uqam-gpt-docs/wiki/postdoc/Guide-Demarrage-Rapide)
- [FAQ](https://github.com/michel-heon/uqam-gpt-docs/wiki/postdoc/FAQ)
- [Support](https://github.com/michel-heon/uqam-gpt-docs/wiki/postdoc/Support)
- [Politique de confidentialité](https://github.com/michel-heon/uqam-gpt-docs/wiki/postdoc/Politique-de-Confidentialite)

### 🔐 UQAM-GPT SeUQAM *(à venir)*

Agent conversationnel pour le **Service des équipements** de l'UQAM.

- **Statut** : 🚧 En planification
- **Public cible** : Personnel UQAM, chercheurs, étudiants
- **Fonctionnalités** : Gestion équipements, réservations, support technique

### 🔬 UQAM-GPT Laboratoire *(à venir)*

Agent conversationnel pour la **gestion des laboratoires de recherche**.

- **Statut** : 📋 En planification
- **Public cible** : Chercheurs, techniciens, gestionnaires de laboratoires
- **Fonctionnalités** : Gestion espaces, équipements, sécurité, réservations

### 🛒 UQAM-GPT Approvisionnement *(à venir)*

Agent conversationnel pour le **Service des approvisionnements** de l'UQAM.

- **Statut** : 📋 En planification
- **Public cible** : Personnel administratif, chercheurs, services UQAM
- **Fonctionnalités** : Procédures d'achat, fournisseurs, appels d'offres

## 🏗️ Architecture Commune

Tous les projets UQAM-GPT partagent une architecture technique commune :

- **LLM** : GPT-4.1 (Azure OpenAI Service)
- **Base de données** : Azure Cosmos DB (historique conversations)
- **Recherche** : Azure AI Search (indexation documentation, RAG)
- **Secrets** : Azure Key Vault
- **Hébergement** : 100% Canada (Toronto + Québec)
- **Framework** : Teams AI Library + Bot Framework SDK
- **Runtime** : Node.js 20 LTS

## 🔒 Conformité et Sécurité

Tous les projets respectent :

- **Loi 25** (Québec) - Protection des renseignements personnels
- **PIPEDA** (Canada) - Protection des données personnelles  
- **ISO 27001** - Gestion de la sécurité de l'information
- **Résidence des données** : 100% Canada
- **Chiffrement** : TLS 1.3 (transit), AES-256 (repos)
- **Rétention** : 90 jours maximum, suppression automatique

## 👥 Équipe

**Développement et Maintenance**  
Michel Héon, Ph.D.  
Vice-rectorat à la recherche, à la création et à la diffusion (VRRCD)  
Université du Québec à Montréal (UQAM)

## 📄 Licence

La documentation est fournie sous licence **Creative Commons BY-NC-ND 4.0** :

- **BY** : Attribution requise
- **NC** : Pas d'utilisation commerciale  
- **ND** : Pas de modifications

Le code source des projets peut avoir des licences différentes (voir chaque repository).

## 🔗 Liens Utiles

- **[Wiki Documentation](https://github.com/michel-heon/uqam-gpt-docs/wiki)** - Documentation complète
- **[UQAM Recherche](https://recherche.uqam.ca/)** - Vice-rectorat à la recherche
- **[Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service)** - Technologie sous-jacente

## 📞 Contact

Pour toute question sur la documentation ou l'écosystème UQAM-GPT :

- **Documentation technique** : Consultez le [Wiki](https://github.com/michel-heon/uqam-gpt-docs/wiki)
- **Support projet** : Voir la page Support de chaque projet
- **Issues** : Ouvrez un ticket dans le repository du projet concerné

---

**Dernière mise à jour** : 2025-11-21  
**Projets actifs** : 1/4 (Postdoc)
