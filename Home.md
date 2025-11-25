# UQAM-GPT - Documentation Générale

Bienvenue dans la documentation de l'écosystème **UQAM-GPT**, une suite d'agents IA conversationnels développés par l'Université du Québec à Montréal (UQAM) pour répondre aux besoins spécifiques de la communauté universitaire.

## 📚 Projets Disponibles

### 🎓 [UQAM-GPT Postdoc](./postdoc/Home.md)

Agent conversationnel dédié aux **programmes postdoctoraux** de l'UQAM.

- **Public cible** : Chercheurs postdoctoraux, candidats, superviseurs
- **Fonctionnalités** : Questions/réponses sur programmes, bourses, procédures
- **Technologie** : Azure OpenAI (GPT-4.1), Azure AI Search (RAG)
- **Plateforme** : Microsoft Teams

**📖 Documentation** : [Guide de démarrage](./postdoc/Guide-Demarrage-Rapide.md) | [FAQ](./postdoc/FAQ.md) | [Support](./postdoc/Support.md)

---

### 🔐 UQAM-GPT SeUQAM *(à venir)*

Agent conversationnel pour le **Service des équipements** de l'UQAM.

- **Public cible** : Personnel UQAM, chercheurs, étudiants
- **Fonctionnalités** : Gestion équipements, réservations, support technique
- **Statut** : En planification

**📖 Documentation** : *(en cours de rédaction)*

---

### 🔬 UQAM-GPT Laboratoire *(à venir)*

Agent conversationnel pour la **gestion des laboratoires de recherche**.

- **Public cible** : Responsables de laboratoires, techniciens, chercheurs
- **Fonctionnalités** : Gestion ressources, sécurité, protocoles
- **Statut** : En planification

**📖 Documentation** : *(en cours de rédaction)*

---

### 🛒 UQAM-GPT Approvisionnement *(à venir)*

Agent conversationnel pour le **Service des approvisionnements**.

- **Public cible** : Personnel administratif, chercheurs, professeurs
- **Fonctionnalités** : Demandes d'achat, suivi commandes, politiques
- **Statut** : En planification

**📖 Documentation** : *(en cours de rédaction)*

---

## 🏗️ Architecture Commune

Tous les agents UQAM-GPT partagent une architecture technique similaire :

### Infrastructure Azure

- **Hébergement** : Azure Canada (Toronto & Québec)
- **IA** : Azure OpenAI Service (GPT-4.1)
- **Recherche** : Azure AI Search (RAG - Retrieval-Augmented Generation)
- **Stockage** : Azure Cosmos DB (conversations)
- **Sécurité** : Azure Key Vault, Microsoft Entra ID (AAD)
- **Monitoring** : Application Insights

### Conformité et Sécurité

- ✅ **Loi 25** (Québec) - Protection des renseignements personnels
- ✅ **PIPEDA** (Canada) - Protection vie privée
- ✅ **Microsoft Teams Store** - Politiques de certification
- ✅ **ISO 27001** - Certification Azure
- ✅ **Résidence des données** : 100% Canada

### Principes de Conception

1. **Privacy by Design** : Protection des données dès la conception
2. **Transparence IA** : Divulgation obligatoire de l'utilisation d'IA
3. **Périmètre UQAM** : Restriction aux membres de l'organisation
4. **Support bilingue** : Français (prioritaire) et anglais
5. **Accessibilité** : Conformité WCAG 2.1

## 🛠️ Technologies

| Composant | Technologie | Version |
|-----------|-------------|---------|
| LLM | Azure OpenAI | GPT-4.1 |
| Framework | Teams AI Library | 1.5.0 |
| Runtime | Node.js | 20.x LTS |
| Plateforme | Microsoft Teams | Latest |
| Recherche | Azure AI Search | Latest |
| Base de données | Azure Cosmos DB | Latest |

## 👥 Équipe

**Éditeur** : Université du Québec à Montréal (UQAM)  
**Vice-rectorat** : Recherche, Création et Diffusion (VRRCD)  
**Coordonnateur technique** : Michel Héon, Ph.D.  
**Contact** : Michel Héon

## 📞 Support

Pour toute question ou assistance :

1. **Consulter la documentation** du projet spécifique (voir liens ci-dessus)
2. **FAQ** : Questions fréquemment posées par projet
3. **Support technique** : Contacter l'équipe VRRCD via Michel Héon
4. **Signalement de problèmes** : Utiliser le bouton "Signaler un problème" dans l'application

## 🔗 Ressources Externes

- [Microsoft Teams Platform](https://learn.microsoft.com/en-us/microsoftteams/platform/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [Loi 25 (Québec)](https://www.cai.gouv.qc.ca/loi-25/)
- [PIPEDA (Canada)](https://www.priv.gc.ca/fr/sujets-lies-a-la-protection-de-la-vie-privee/lois-sur-la-protection-des-renseignements-personnels-au-canada/la-loi-sur-la-protection-des-renseignements-personnels-et-les-documents-electroniques-pipeda/)

## 📜 Licences et Conditions

Chaque projet possède ses propres :

- **Politique de confidentialité** : Traitement des données personnelles
- **Conditions d'utilisation** : Règles d'usage de l'application
- **Restrictions d'accès** : Périmètre organisationnel UQAM

Consultez la documentation spécifique de chaque projet pour plus de détails.

---

**Dernière mise à jour** : 2025-11-21  
**Version du wiki** : 1.0
