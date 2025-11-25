# Signalement et amélioration

## Vue d'ensemble

Le système de signalement permet aux utilisateurs de signaler du contenu inapproprié ou problématique généré par l'IA. Ce mécanisme est conforme aux exigences du Microsoft Teams Store pour les applications utilisant l'IA générative.

### Exigences Teams Store

**Reporting Mechanism** : Système visible pour signaler du contenu problématique  
**Reference to Content** : Contexte de la question et réponse inclus dans le signalement  
**Accessibility** : Accessible depuis chaque réponse du bot  
**Response Process** : Email direct vers l'équipe de support

## Implémentation Technique

### Adaptive Card après chaque réponse

Après chaque réponse générée par l'IA, une **Adaptive Card** est automatiquement envoyée avec deux actions :

1. **Signaler un problème** : Ouvre un email pré-rempli avec contexte
2. **📧 Contacter le support** : Ouvre un email pour assistance générale

### Code Implémenté

```javascript
// Mécanisme de signalement après chaque réponse
const feedbackCard = {
  type: "AdaptiveCard",
  $schema: "http://adaptivecards.io/schemas/adaptive-card.json",
  version: "1.5",
  body: [
    {
      type: "TextBlock",
      text: "Cette réponse vous a-t-elle été utile ?",
      size: "Small",
      weight: "Lighter",
      wrap: true
    }
  ],
  actions: [
    {
      type: "Action.OpenUrl",
      title: "Signaler un problème",
      url: "mailto:heon@cotechnoe.com?subject=Signalement..."
    },
    {
      type: "Action.OpenUrl",
      title: "📧 Contacter le support",
      url: "mailto:heon@cotechnoe.com?subject=Support..."
    }
  ]
};
```

### Contenu de l'Email de Signalement

L'email pré-rempli contient :

```
Sujet: Signalement UQAM-GPT Postdoc

Bonjour,

Je souhaite signaler un problème avec la réponse suivante :

Question : [Question de l'utilisateur]

Réponse : [Extrait de la réponse générée - 500 premiers caractères]

Problème identifié :
[L'utilisateur décrit le problème ici]

Cordialement
```

## Flux Utilisateur

### Scénario 1 : Signalement d'un problème

```
1. L'utilisateur pose une question
2. Le bot génère une réponse avec citations
3. Une Adaptive Card apparaît : "Cette réponse vous a-t-elle été utile ?"
4. L'utilisateur clique sur "Signaler un problème"
5. Son client email s'ouvre avec un message pré-rempli
6. L'utilisateur complète la section "Problème identifié"
6. L'utilisateur envoie l'email
7. L'équipe de support (Michel Héon) reçoit le signalement
```

### Scénario 2 : Assistance générale

```
1. L'utilisateur a besoin d'aide
2. L'utilisateur clique sur "📧 Contacter le support"
3. Son client email s'ouvre avec l'adresse pré-remplie
4. L'utilisateur rédige sa demande d'assistance
5. L'utilisateur envoie l'email
6. L'équipe de support répond dans un délai raisonnable
```

## Types de Problèmes Signalables

### Contenu Inapproprié
- Réponses offensantes ou discriminatoires
- Contenu biaisé ou trompeur
- Informations sensibles exposées

### Problèmes Techniques
- Citations incorrectes ou manquantes
- Réponses hors périmètre (non-UQAM)
- Hallucinations factuelles
- Erreurs de formatage

### Qualité de la Réponse
- Informations inexactes malgré les sources
- Réponse non pertinente à la question
- Mauvaise interprétation du contexte

## Configuration

### Email de Support

Le contact actuellement configuré est : **Michel Héon**

Pour modifier cette adresse :

```javascript
// Dans src/app/app.js, ligne ~192
url: `mailto:NOUVELLE_ADRESSE@uqam.ca?subject=Signalement...`
```

### Email UQAM Recommandé

Pour production, il est recommandé d'utiliser une adresse institutionnelle UQAM, par exemple :
- `recherche-postdoc@uqam.ca`
- `soutien-gpt-postdoc@uqam.ca`
- `aide-recherche@uqam.ca`

## Tests

### Test 1 : Affichage de la Card

```
1. Démarrer une conversation avec le bot
2. Poser une question : "Quelles sont les conditions d'admissibilité?"
3. Vérifier qu'une Adaptive Card apparaît après la réponse
4. Vérifier le texte : "Cette réponse vous a-t-elle été utile ?"
5. Vérifier les 2 boutons présents
```

### Test 2 : Signalement Problème

```
1. Recevoir une réponse du bot
2. Cliquer sur "Signaler un problème"
3. Vérifier que le client email s'ouvre
4. Vérifier que l'objet est "Signalement UQAM-GPT Postdoc"
5. Vérifier que le corps contient :
   - Question posée
   - Extrait de la réponse
   - Section "Problème identifié" vide
```

### Test 3 : Contact Support

```
1. Recevoir une réponse du bot
2. Cliquer sur "📧 Contacter le support"
3. Vérifier que le client email s'ouvre
4. Vérifier que l'objet est "Support UQAM-GPT Postdoc"
5. Vérifier que le destinataire est correct
```

### Test 4 : Multi-plateforme

Tester sur :
- Teams Desktop (Windows/macOS)
- Teams Web
- Teams Mobile (iOS/Android)

## Améliorations Futures

### Phase 2 : Système de Ticketing

Remplacer l'email par une intégration avec un système de ticketing :

```javascript
{
  type: "Action.Submit",
  title: "Signaler un problème",
  data: {
    action: "report",
    question: userInput,
    response: content,
    conversationId: activity.conversation.id,
    userId: activity.from.id,
    timestamp: new Date().toISOString()
  }
}
```

Handler :

```javascript
app.on('adaptiveCard/action', async ({ send, activity }) => {
  if (activity.value?.action === 'report') {
    // Envoyer à Azure Service Bus / Logic App / Dataverse
    const ticketId = await createSupportTicket(activity.value);
    await send(` Signalement enregistré. Numéro de suivi : ${ticketId}`);
  }
});
```

### Phase 3 : Analytics

Suivre les métriques de signalement :
- Nombre de signalements par jour/semaine
- Types de problèmes les plus fréquents
- Temps de réponse moyen
- Taux de résolution

### Phase 4 : Feedback Loop

Utiliser les signalements pour :
- Améliorer les instructions système
- Ajuster les prompts RAG
- Enrichir la base documentaire
- Fine-tuner le modèle (si applicable)

## Conformité Légale

### RGPD / Loi 25 (Québec)

- Email contient uniquement les données nécessaires (question/réponse)
- Pas de données sensibles dans l'URL (encodage approprié)
- Utilisateur contrôle l'envoi de l'email
- Adresse email support visible et accessible

### Microsoft Teams Store Requirements

- Reporting mechanism clairement visible
- Accessible après chaque réponse IA
- Processus simple et non-intrusif
- Contact rapide avec l'équipe

## Processus de Gestion des Signalements

### Workflow Recommandé

1. **Réception** : Email arrive dans boîte support
2. **Triage** : Classification du problème (critique/important/mineur)
3. **Investigation** : Analyse de la question/réponse/contexte
4. **Action** :
   - Correction instructions système
   - Mise à jour documentation
   - Correction bug technique
5. **Réponse** : Retour à l'utilisateur sous 48h
6. **Suivi** : Vérification que le problème ne se reproduit pas

### SLA Suggéré

| Priorité | Temps de Réponse | Temps de Résolution |
|----------|------------------|---------------------|
| Critique | 4 heures | 24 heures |
| Important | 24 heures | 72 heures |
| Mineur | 48 heures | 1 semaine |

## Références

- [Microsoft AI Content Policy](https://learn.microsoft.com/en-us/legal/marketplace/certification-policies#1-apps-with-artificial-intelligenceai-generated-content-must-meet-below-requirements)
- [Adaptive Cards - Action.OpenUrl](https://adaptivecards.io/explorer/Action.OpenUrl.html)
- [Teams Store Guidelines - User Reporting](https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/deploy-and-publish/appsource/prepare/teams-store-validation-guidelines#apps-powered-by-ai)

---

**Implémentation** : `src/app/app.js` (lignes ~185-210)  
**Auteur** : Michel Héon Ph.D. (UQAM/VRRCD)  
**Date** : 2025-11-20  
**Status** : Implémenté et prêt pour tests
