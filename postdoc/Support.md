# Support - UQAM-GPT Postdoc

Centre d'assistance technique pour UQAM-GPT Postdoc

## Contact Support

### Équipe de Support

**Responsable Technique** : Michel Héon, Ph.D.  
**Organisation** : Vice-rectorat à la recherche, à la création et à la diffusion (VRRCD)  
**Université** : UQAM (Université du Québec à Montréal)

### Coordonnées

**Contact Principal** : Michel Héon

**Adresse Postale** :  
Université du Québec à Montréal  
Vice-rectorat à la recherche  
405, rue Sainte-Catherine Est  
Montréal (Québec) H2L 2C4  
Canada

### Heures de Disponibilité

**Service Bot** : 24/7 (automatisé)  
**Support Technique** : Lundi au vendredi, 9h-17h (HNE/HAE)  
**Réponse Email** : Sous 5 jours ouvrables (demandes générales)

### Délais de Réponse (SLA)

| Type de Demande | Temps de Réponse | Temps de Résolution |
|-----------------|------------------|---------------------|
| Critique (service down) | 4 heures | 24 heures |
| Important (bug majeur) | 1 jour ouvrable | 3 jours ouvrables |
| Mineur (amélioration) | 5 jours ouvrables | 2 semaines |
| Question générale | 5 jours ouvrables | - |

## Signaler un Problème

### Méthode 1 : Bouton In-App (Recommandé)

Après chaque réponse du bot, cliquez sur :

```
[Signaler un problème]
```

Un email pré-rempli s'ouvre avec :

- Votre question originale
- Extrait de la réponse problématique
- Template de description

**Avantages** :

- Contexte automatique
- Traçabilité complète
- Traitement prioritaire

### Méthode 2 : Email Direct

Envoyez un email à **Michel Héon** avec :

**Objet** : `[UQAM-GPT] Type de problème`

**Corps** :

```
Bonjour,

Type de problème : [Bug / Contenu inapproprié / Performance / Autre]

Description :
[Décrivez le problème en détail]

Question posée :
[Copiez la question que vous avez posée]

Réponse reçue :
[Copiez la réponse du bot ou faites une capture d'écran]

Comportement attendu :
[Ce que vous attendiez]

Environnement :
- Plateforme : [Teams Desktop / Web / Mobile iOS / Mobile Android]
- Date et heure : [Quand le problème s'est produit]
- Channel ou Chat : [Personnel / Groupe / Channel Teams]

Cordialement,
[Votre nom]
```

## Troubleshooting

### Problème : Le bot ne répond pas

#### Symptôme
Vous envoyez un message mais aucune réponse n'arrive.

#### Causes Possibles

**1. Dans un chat de groupe/équipe → Oubli de @mention**

**Incorrect** :
```
Quelles sont les conditions postdoc ?
```

**Correct** :
```
@UQAM-GPT Postdoc Quelles sont les conditions postdoc ?
```

**2. Service temporairement indisponible**
- Azure peut avoir des interruptions ponctuelles (< 0.1% du temps)
- **Solution** : Attendez 2-3 minutes et réessayez

**3. Rate limiting (limite de requêtes)**
- Maximum 10 requêtes par minute par utilisateur
- **Solution** : Patientez 1 minute entre les requêtes

#### Actions Correctives

1. Vérifiez que vous avez bien mentionné le bot avec `@UQAM-GPT Postdoc` dans les groupes
2. Attendez 2 minutes et réessayez
3. Vérifiez votre connexion internet
4. Redémarrez Teams (Desktop) ou rafraîchissez la page (Web)
5. Si le problème persiste > 10 minutes → Contactez le support

---

### Problème : Réponse incomplète ou coupée

#### Symptôme
La réponse s'arrête brutalement au milieu d'une phrase.

#### Causes Possibles

**1. Limite de tokens atteinte**
- Le modèle GPT a une limite de tokens (~4000 mots)
- Les réponses très longues peuvent être tronquées

**2. Timeout réseau**
- Connexion interrompue pendant le streaming

#### Solutions

**Posez une question de suivi** :
```
Peux-tu continuer ta réponse ?
```

**Divisez en sous-questions** :
```
Au lieu de : "Explique tout sur le financement postdoc"
Utilisez : "Quel est le montant du financement postdoc ?"
Puis : "Quelles sont les sources de financement disponibles ?"
```

---

### Problème : Citations manquantes

#### Symptôme
La réponse n'inclut pas de citations [1], [2], [3].

#### Causes Possibles

**1. Chat personnel 1:1**
- Les citations arrivent **après** le streaming de la réponse (délai de 1-2 secondes)
- **Solution** : Patientez quelques secondes

**2. Aucune source trouvée**
- Si la question est hors périmètre UQAM, aucune citation disponible
- Le bot vous informe : "Aucune source UQAM trouvée"

#### Actions Correctives

1. Attendez 5 secondes après la fin du streaming
2. Vérifiez que votre question concerne bien les programmes postdoctoraux UQAM
3. Si toujours manquant → Signalez le bug

---

### Problème : Réponse incorrecte ou hallucination

#### Symptôme
Le bot donne une information fausse ou invente des faits.

#### Important
**L'IA peut commettre des erreurs** malgré les sources UQAM.

#### Actions Immédiates

1. **Vérifiez les sources citées** : Cliquez sur [1], [2], [3] pour lire les documents originaux
2. **Signalez le problème** : Cliquez sur **Signaler un problème**
3. **Consultez sources officielles** : Site UQAM, service postdoctoral

#### Prévention

- Ne faites jamais confiance aveuglément aux réponses IA
- Vérifiez toujours pour décisions importantes (candidature, financement)
- Contactez le service postdoctoral UQAM pour validation officielle

---

### Problème : Bot répond hors-sujet

#### Symptôme
La réponse ne correspond pas à votre question.

#### Causes Possibles

**1. Contexte conversationnel mal interprété**
- Le bot se souvient des messages précédents
- Il peut mal interpréter votre question de suivi

**2. Question ambiguë**
- Formulation trop vague ou multiple interprétations possibles

#### Solutions

**Reformulez avec plus de contexte** :
```
Au lieu de : "Et pour les étrangers ?"
Utilisez : "Quelles sont les conditions d'admissibilité pour les chercheurs internationaux au postdoctorat UQAM ?"
```

**Commencez une nouvelle conversation** :
- Chat personnel : Nouveau sujet = contexte reset
- Nouveau channel Teams pour un contexte dédié

---

### Problème : Performance lente (réponse tarde)

#### Symptôme
Le bot met > 10 secondes avant de commencer à répondre.

#### Causes Possibles

**1. Charge élevée du service Azure**
- Pic d'utilisation simultanée
- **Normal** : Réponse en 2-5 secondes

**2. Recherche vectorielle complexe**
- Si la question nécessite une recherche approfondie

#### Seuils Normaux

| Étape | Délai Normal | Délai Inquiétant |
|-------|--------------|------------------|
| Typing indicator | < 1 seconde | > 3 secondes |
| Premier mot | 2-5 secondes | > 10 secondes |
| Streaming complet | 5-15 secondes | > 30 secondes |
| Citations (1:1) | 1-2 secondes après | > 5 secondes |

#### Actions Correctives

1. Si < 15 secondes → Patientez (normal)
2. Si 15-30 secondes → Charge élevée, réessayez dans 2 minutes
3. Si > 30 secondes → Contactez le support (incident possible)

---

### Problème : Adaptive Card de feedback ne s'affiche pas

#### Symptôme
Pas de boutons **Signaler un problème** après la réponse.

#### Causes Possibles

**1. Version Teams obsolète**
- Adaptive Cards v1.5 requiert Teams version récente

**2. Bug temporaire**

#### Solutions

1. **Mettez à jour Teams** : Version Desktop → Aide → Vérifier les mises à jour
2. **Utilisez Teams Web** : <https://teams.microsoft.com> (navigateur récent)
3. **Signalez directement** : Contactez Michel Héon

---

### Problème : Erreur "Rate Limit Exceeded"

#### Symptôme
Message : "Trop de requêtes, veuillez patienter."

#### Cause
Vous avez dépassé la limite de **10 requêtes par minute**.

#### Solution

**Attendez 60 secondes** avant de poser une nouvelle question.

**Pourquoi cette limite ?**
- Protection contre abus
- Équité d'accès pour tous les utilisateurs
- Limitation coûts Azure

---

## Support Mobile (iOS / Android)

### Fonctionnalités Supportées

Conversation personnelle (1:1)  
@mention dans groupes/équipes  
Citations cliquables  
Adaptive Cards feedback  
Signalement de problèmes  

### Problèmes Connus

**Réponses longues** : Plus difficiles à lire sur petit écran  
→ **Solution** : Utilisez mode portrait, scroll vertical

**Markdown complexe** : Peut s'afficher différemment  
→ **Solution** : Acceptable, le contenu reste lisible

### Signaler un Bug Mobile

Lors du signalement, précisez :
- Modèle appareil (ex: iPhone 14, Samsung Galaxy S23)
- Version OS (iOS 17.2, Android 14)
- Version Teams app

---

## Confidentialité et Sécurité

### Données Collectées

Le support peut accéder à :
- Votre question et la réponse du bot (pour diagnostic)
- Logs techniques (timestamp, erreurs, performance)
- Votre ID Teams et nom d'affichage

Le support N'A PAS accès à :
- Vos autres conversations Teams
- Vos emails Outlook
- Vos fichiers SharePoint

[Politique de Confidentialité complète](Politique-de-Confidentialite)

### Signalement de Contenu Inapproprié

Si le bot génère un contenu :
- Offensant, discriminatoire
- Biaisé ou trompeur
- Exposant des informations sensibles

**Action immédiate** : Cliquez **Signaler un problème**

**Engagement** :
- Analyse sous 24 heures
- Correction instructions système si nécessaire
- Notification de suivi sous 48 heures

---

## Ressources Additionnelles

### Documentation

- [Guide de Démarrage Rapide](Guide-Demarrage-Rapide) - Installation et premiers pas
- [FAQ - Questions Fréquentes](FAQ) - Réponses rapides
- [Politique de Confidentialité](Politique-de-Confidentialite) - Protection données

### Liens Externes

- [Microsoft Teams Support](https://support.microsoft.com/teams) - Support général Teams
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service) - Technologie sous-jacente
- [UQAM Recherche](https://recherche.uqam.ca/) - Site officiel VRRCD

---

## Feedback et Suggestions

Vos retours nous aident à améliorer UQAM-GPT Postdoc !

### Types de Feedback Souhaités

- 💡 Suggestions de fonctionnalités
- Idées d'amélioration UX
- Documentation manquante ou peu claire
- Nouveaux cas d'usage
- 🐛 Bugs non critiques

### Envoyer un Feedback

**Contact** : Michel Héon  
**Objet** : `[UQAM-GPT] Feedback - [Sujet]`

**Template** :
```
Type : [Suggestion / Bug / Documentation / Autre]

Description :
[Décrivez votre feedback en détail]

Impact souhaité :
[Comment cela améliorerait votre expérience]

Priorité pour vous : [Basse / Moyenne / Élevée]
```

---

## Mises à Jour et Maintenance

### Maintenance Planifiée

**Fréquence** : Mensuelle  
**Jour** : Premier dimanche du mois, 2h-6h HAE  
**Impact** : Service interrompu pendant 15-30 minutes

**Notification** : Email 48h à l'avance aux utilisateurs actifs

### Mises à Jour de Fonctionnalités

**Déploiement** : Progressif (rollout graduel)  
**Tests** : Environnement sandbox avant production  
**Documentation** : Mise à jour simultanée du wiki

### Historique des Incidents

[À venir : Page dédiée avec historique incidents et résolutions]

---

## Statistiques de Service

### Disponibilité (SLA)

**Objectif** : 99.5% uptime (43 minutes downtime/mois maximum)  
**Actuel** : [Données à venir]

### Temps de Réponse Moyen

**Bot first response** : 2.5 secondes (médiane)  
**Support email** : 3.2 jours ouvrables (médiane)  
**Résolution bugs critiques** : 18 heures (médiane)

---

## Questions Sans Réponse ?

Si votre problème n'est pas couvert dans cette page :

1. Consultez la [FAQ](FAQ) - Questions fréquentes
2. Vérifiez la [documentation complète](Home)
3. Contactez-nous : **Michel Héon**

**Nous nous engageons à répondre à toutes les demandes sous 5 jours ouvrables.**

---

**Dernière mise à jour** : 2025-11-20  
**Version** : 1.0.0
