# FAQ - Questions Fréquentes

Réponses aux questions les plus courantes sur UQAM-GPT Postdoc

## Questions Générales

### Qu'est-ce que UQAM-GPT Postdoc ?

**UQAM-GPT Postdoc** est un agent conversationnel intelligent basé sur GPT-4.1 (Azure OpenAI) intégré à Microsoft Teams. Il aide le personnel de l'UQAM à obtenir des informations sur les programmes postdoctoraux en interrogeant la documentation officielle de l'université.

**Technologie** : RAG (Retrieval-Augmented Generation) - Le bot recherche d'abord dans la documentation UQAM avant de générer sa réponse.

---

### À qui s'adresse UQAM-GPT Postdoc ?

**Public cible** :

- Personnel administratif gérant les programmes postdoctoraux
- Coordonnateurs de recherche
- Gestionnaires UQAM impliqués dans l'accueil des chercheurs postdoctoraux
- Chercheurs principaux encadrant des postdocs

**Note** : Ce n'est PAS un outil pour les candidats externes (pas d'accès public).

---

### Est-ce gratuit ?

**Oui**, UQAM-GPT Postdoc est **100% gratuit** pour le personnel UQAM.

- Aucun coût pour l'utilisateur
- Aucun abonnement requis
- Aucune limite de questions (sauf rate limiting raisonnable: 10/minute)

---

### Quelle est la différence avec ChatGPT ?

| Critère | UQAM-GPT Postdoc | ChatGPT |
|---------|------------------|---------|
| **Sources** | Documentation UQAM uniquement | Internet général |
| **Citations** | Oui, liens vérifiables | Non (sauf ChatGPT Plus avec browsing) |
| **Périmètre** | Programmes postdoctoraux UQAM | Connaissances générales |
| **Hébergement** | Canada (Azure) | USA (OpenAI) |
| **Confidentialité** | Loi 25 + PIPEDA | Politique OpenAI |
| **Intégration** | Microsoft Teams natif | Site web externe |
| **Historique** | Conversations organisées | Conversations linéaires |

**En résumé** : UQAM-GPT est spécialisé, vérifié et conforme aux exigences UQAM.

---

## Confidentialité et Sécurité

### Mes conversations sont-elles privées ?

**Oui et non** :

**Privées de :**

- Autres utilisateurs UQAM
- Microsoft (hors sous-traitance technique)
- Internet public

**Accessibles par :**

- Vous-même (votre historique)
- Administrateurs système UQAM (support technique uniquement)
- Azure OpenAI (traitement IA, **sans entraînement de modèle**)

**Durée de conservation** : 90 jours, puis suppression automatique.

[En savoir plus](Politique-de-Confidentialite)

---

### Le bot a-t-il accès à mes emails Teams/Outlook ?

**Non, absolument pas**.

Le bot n'a accès qu'à :

- Les messages que vous lui envoyez directement
- Les messages dans les channels où il est ajouté (uniquement quand @mentionné)
- Votre nom et ID Teams (authentification)

Le bot N'A PAS accès à :

- Vos emails Outlook
- Vos messages Teams privés avec d'autres personnes
- Vos fichiers SharePoint
- Votre calendrier

---

### Où sont stockées mes données ?

**Localisation** : 100% Canada

- **Région Azure primaire** : Canada Centre (Toronto)
- **Région secondaire** : Canada Est (Québec)

**Conformité** :

- Loi 25 (Québec)
- PIPEDA (Canada)
- ISO 27001 (Azure)

**Chiffrement** :

- TLS 1.3 en transit
- AES-256 au repos

---

### Puis-je supprimer mes données ?

**Oui**, vous avez un **droit de suppression** (Loi 25).

**Méthode** :

1. Envoyez un email à **Michel Héon**
2. Objet : `Demande de suppression - UQAM-GPT`
3. Indiquez votre ID Teams ou email UQAM

**Délai** : Suppression effective sous 7 jours ouvrables.

**Limitations** : Signalements de problèmes conservés 2 ans (obligation légale).

---

## Utilisation

### Comment poser une question ?

**Chat personnel (1:1)** :

- Tapez directement votre question
- Pas besoin de @mention

**Chat de groupe ou Teams** :

- Mentionnez le bot : `@UQAM-GPT Postdoc Votre question`
- Obligatoire pour que le bot réponde

[Guide complet](Guide-Demarrage-Rapide)

---

### Combien de questions puis-je poser ?

**Limite** : 10 questions par minute (rate limiting)

**Raisons** :

- Protection contre abus
- Équité d'accès pour tous
- Gestion coûts Azure

**En pratique** : Largement suffisant pour usage normal. Si dépassé, patientez 60 secondes.

---

### Le bot comprend-il l'anglais ?

**Oui**, UQAM-GPT comprend et répond en **français ET anglais**.

**Fonctionnement** :
- Question en français → Réponse en français
- Question en anglais → Réponse en anglais
- Mélange des deux → Le bot s'adapte

**Cependant** : Les sources UQAM sont principalement en français. Les réponses en anglais citent donc souvent des sources françaises.

---

### Puis-je parler au bot comme à un humain ?

**Oui !** Le bot comprend le langage naturel conversationnel.

**Exemples acceptés** :
- "C'est quoi les conditions pour un postdoc ?"
- "Quelles sont les conditions d'admissibilité postdoctorale ?"
- "Je voudrais savoir si un étranger peut postuler"
- "Admissibilité ?" (trop vague, mais essaie de répondre)

**Conseil** : Plus vous êtes spécifique, meilleure est la réponse.

---

## Contenu et Périmètre

### Sur quoi le bot peut-il répondre ?

**Périmètre INCLUS** :
- Programmes postdoctoraux UQAM
- Conditions d'admissibilité
- Financement et bourses
- Procédures administratives
- Documents requis
- Délais et échéanciers
- Contacts administratifs

**Périmètre EXCLUS** :
- Programmes d'autres universités
- Conseils juridiques personnalisés
- Décisions officielles (ex: acceptation candidature)
- Informations confidentielles sur candidats
- Statistiques non publiques

---

### Le bot a-t-il accès aux dossiers de candidature ?

**Non**. Le bot n'a accès qu'à la **documentation publique UQAM**.

Il ne peut pas :
- Consulter un dossier individuel
- Connaître le statut d'une candidature
- Accéder aux bases de données internes

**Pour questions sur dossiers spécifiques** : Contactez directement le service postdoctoral UQAM.

---

### Les réponses sont-elles toujours exactes ?

**Non, l'IA peut faire des erreurs** ("hallucinations").

**Pourquoi ?**
- GPT-4.1 est un modèle probabiliste, pas une base de données
- Il génère du texte en se basant sur patterns
- Malgré RAG et sources, erreurs possibles

**Bonne pratique** :
1. Lisez la réponse du bot
2. Cliquez sur les citations [1], [2], [3]
3. Vérifiez dans le document source
4. Pour décisions importantes, validez avec service postdoctoral UQAM

**Signalez toute réponse incorrecte** avec le bouton de signalement.

---

### Pourquoi le bot cite-t-il ses sources ?

**Raisons** :
1. **Transparence** : Vous savez d'où vient l'information
2. **Vérification** : Vous pouvez consulter le document original
3. **Confiance** : Les sources sont officielles UQAM
4. **Conformité** : Exigence Teams Store pour apps IA

**Format** : `[1]`, `[2]`, `[3]` = liens cliquables vers documents UQAM

---

### Que faire si le bot ne trouve pas de réponse ?

**Le bot vous l'indique** :
> "Je n'ai pas trouvé d'information spécifique dans la documentation UQAM sur ce sujet."

**Actions possibles** :
1. Reformulez votre question avec d'autres mots
2. Divisez en sous-questions plus précises
3. Contactez directement le service postdoctoral UQAM
4. Consultez le site web UQAM Recherche

**Note** : Si le sujet est hors périmètre postdoctoral, c'est normal.

---

## Problèmes et Support

### Le bot ne répond pas, que faire ?

**Checklist rapide** :
1. Dans un groupe/team → Avez-vous utilisé `@UQAM-GPT Postdoc` ?
2. Attendez 2 minutes (peut être temporaire)
3. Vérifiez votre connexion internet
4. Redémarrez Teams
5. Si > 10 minutes → [Contactez le support](Support)

[Guide Troubleshooting complet](Support.md#troubleshooting)

---

### Comment signaler une réponse inappropriée ?

**Méthode 1 (Recommandée)** : Bouton in-app

Après chaque réponse du bot, cliquez sur :
```
[Signaler un problème]
```

**Méthode 2** : Email direct

Envoyez à **Michel Héon** avec :
- Votre question
- Réponse du bot (copie ou screenshot)
- Description du problème

**Délai de traitement** : Analyse sous 24 heures, correction sous 48 heures.

---

### Qui contacter pour support technique ?

**Responsable** : Michel Héon, Ph.D. (VRRCD)  
**Délai réponse** : 5 jours ouvrables (demandes générales)

[Page Support complète](Support)

---

### Le service est-il disponible 24/7 ?

**Bot** : Oui, 24/7/365  
**Support humain** : ⏰ Lun-Ven 9h-17h (HNE/HAE)

**Maintenance** : Premier dimanche du mois, 2h-6h (15-30 min downtime)

---

## Technique

### Quelle technologie utilise le bot ?

**Architecture** :
- **Modèle IA** : GPT-4.1 (Azure OpenAI Service)
- **Recherche** : Azure AI Search (vector search + keyword)
- **Plateforme** : Microsoft Teams AI Library v2.0
- **Hébergement** : Azure Canada (Toronto + Québec)
- **Base de données** : Azure Cosmos DB (conversations)
- **Monitoring** : Application Insights

**Approche** : RAG (Retrieval-Augmented Generation)
1. Recherche dans index UQAM
2. Extraction passages pertinents
3. Génération réponse avec contexte
4. Citation des sources

---

### Comment fonctionne le RAG ?

**RAG = Retrieval-Augmented Generation**

**Étapes** :
1. **Recherche** : Votre question → Azure AI Search vectorielle
2. 📄 **Extraction** : Top 5 passages les plus pertinents
3. **Génération** : GPT-4.1 rédige réponse basée sur passages
4. 📑 **Citations** : Sources ajoutées avec liens

**Avantage** : Réponses basées sur faits UQAM, pas sur "mémoire" GPT générale.

---

### Le modèle GPT est-il entraîné sur nos données ?

**Non, jamais.**

**Azure OpenAI Entreprise** :
- Vos données ne sont PAS utilisées pour entraîner les modèles OpenAI
- Isolation complète entre clients Azure
- Pas de partage avec ChatGPT public

**Contrat Microsoft** : Data Processing Agreement (DPA) conforme RGPD + Loi 25.

---

### Puis-je intégrer le bot dans mon propre outil ?

**Non**, UQAM-GPT Postdoc est exclusivement disponible via **Microsoft Teams**.

**Raisons** :
- Authentification via Microsoft Entra ID (SSO)
- Sécurité et contrôle d'accès
- Conformité UQAM

**Alternative** : Si vous avez un besoin spécifique, contactez Michel Héon pour discuter.

---

## Mobile

### Le bot fonctionne-t-il sur mobile ?

**Oui**, 100% fonctionnel sur **iOS et Android**.

**Fonctionnalités supportées** :
- Conversation 1:1
- @mention dans groupes/teams
- GPT-Channels
- Citations cliquables
- Adaptive Cards feedback
- Signalement de problèmes

**Astuce** : Pour réponses longues, mode portrait recommandé.

---

### Les citations fonctionnent-elles sur mobile ?

**Oui**, les liens sont cliquables.

Selon votre configuration :
- Ouverture dans navigateur mobile (Safari, Chrome)
- Ou dans app Teams intégrée (si document SharePoint)

---

## Cas d'Usage

### Exemples de questions efficaces ?

**Admissibilité** :
```
Quelles sont les conditions d'admissibilité pour un chercheur international au postdoctorat UQAM ?
```

**Financement** :
```
Quel est le montant du financement postdoctoral offert par l'UQAM et peut-on le cumuler avec d'autres bourses ?
```

**Candidature** :
```
Quels documents sont requis pour soumettre une candidature postdoctorale et où trouver les formulaires ?
```

**Procédures** :
```
Quel est le processus d'évaluation des candidatures postdoctorales et quels sont les délais ?
```

---

### Puis-je utiliser le bot pour comparer plusieurs candidatures ?

**Oui**, c'est un excellent cas d'usage !

**Méthode recommandée** : Utilisez des conversations Teams séparées

Créez une conversation ou un channel dédié par candidat pour garder l'historique organisé.

**Avantage** : Contexte isolé, pas de confusion entre candidats.

---

### Comment former mon équipe à utiliser le bot ?

**Ressources disponibles** :
1. [Guide de Démarrage Rapide](Guide-Demarrage-Rapide) - À partager
2. Cette FAQ - Questions courantes
3. [Page Support](Support) - Assistance technique

**Suggestion** : Session de 30 minutes
- 10 min : Présentation et démo
- 10 min : Installation et premier usage
- 10 min : Questions/réponses

**Contact pour formation** : Michel Héon

---

## Mises à Jour

### Le bot est-il régulièrement amélioré ?

**Oui**, développement continu.

**Fréquence** :
- Mises à jour mineures : Mensuelles
- Nouvelles fonctionnalités : Trimestrielles
- Corrections bugs critiques : Sous 24h

**Notification** : Email 48h avant maintenance planifiée.

---

### Comment suggérer une amélioration ?

**Contact** : Michel Héon  
**Objet** : `[UQAM-GPT] Suggestion - [Résumé]`

**Template** :
```
Type : Suggestion de fonctionnalité

Description :
[Décrivez votre idée en détail]

Cas d'usage :
[Comment vous utiliseriez cette fonctionnalité]

Impact attendu :
[En quoi cela améliorerait votre travail]

Priorité pour vous : [Basse / Moyenne / Élevée]
```

Toutes les suggestions sont examinées ! 🙏

---

### Puis-je voir le code source ?

**Oui**, le projet est open source (pour le personnel UQAM).

**Repository GitHub** : [UQAM-RECHERCHE/uqam-gpt-postdoc-teams](https://github.com/UQAM-RECHERCHE/uqam-gpt-postdoc-teams)

**Contenu** :
- Code source complet (Node.js)
- Documentation technique
- Décisions d'architecture
- Instructions de déploiement

**Licence** : Creative Commons BY-NC-ND 4.0

---

## Question Non Listée ?

Si votre question n'apparaît pas dans cette FAQ :

1. Consultez la [documentation complète](Home)
2. Vérifiez la [page Support](Support)
3. Contactez-nous : **Michel Héon**

**Nous mettons à jour cette FAQ régulièrement** en fonction de vos questions !

---

**Dernière mise à jour** : 2025-11-20  
**Version** : 1.0.0  
**Contributions** : Vos questions aident à améliorer cette FAQ !
