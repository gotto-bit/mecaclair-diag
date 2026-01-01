# 🚗 MecaClair Diag - Workflow Marketing Digital

Application complète de diagnostic automobile avec workflow marketing digital automatisé.

## 🎯 Vue d'ensemble

**MecaClair Diag** est un système complet qui combine:
- 📄 **Génération automatique de PDF de formation** avec templates marketing agressifs
- 💳 **Système de paiement et gestion des ventes**
- 📧 **Automatisation email marketing** (confirmation, upsell, nurturing)
- 🤖 **Agent IA de mise à jour** des symptômes/pannes avec probabilités
- 🔧 **API de diagnostic à distance** pour les clients
- 📊 **Dashboard analytics complet**

## ✨ Fonctionnalités Principales

### 1. Générateur de PDF Marketing
- Templates avec **leviers psychologiques** (urgence, rareté, preuve sociale)
- Personnalisation complète pour chaque client
- Intégration de la base de données de 5000+ pannes
- Copy marketing **agressif mais légal et éthique**

### 2. Système de Paiement
- Gestion complète des produits et prix
- Tracking des clients (basic vs premium)
- Statistiques de vente en temps réel
- Support multi-produits

### 3. Automatisation Email
- ✅ Email de confirmation avec PDF en pièce jointe
- 📈 Séquence d'upsell automatique (J+1, J+3)
- 🛒 Récupération de panier abandonné
- ⭐ Demande de témoignages

### 4. Agent IA Symptômes
- Base de données de 5000+ pannes référencées
- Calcul automatique des probabilités
- Recherche vectorielle (RAG) via ChromaDB
- Mises à jour automatiques depuis sources

### 5. API Diagnostic à Distance
- Endpoint de diagnostic intelligent
- Retour avec causes probables + probabilités
- Estimation des coûts de réparation
- Niveau d'urgence calculé

## 🚀 Installation

### Prérequis
- Python 3.9+
- pip

### Installation rapide

```bash
# Cloner le repo
git clone <repo-url>
cd mecaclair-diag

# Installer les dépendances
pip install -r requirements.txt

# Créer les dossiers de données
mkdir -p data/{pdfs,customers,symptoms,reports}
```

## 📖 Utilisation

### 1. Interface Streamlit (Dashboard complet)

```bash
streamlit run app.py
```

Accéder à: `http://localhost:8501`

**Sections disponibles:**
- 🏠 Dashboard (statistiques globales)
- 📄 Générateur de PDF
- 💳 Gestion des ventes
- 📧 Emails marketing
- 🤖 Agent symptômes
- 📊 Analytics
- 💡 Prompts marketing

### 2. API FastAPI (Diagnostic à distance)

```bash
python src/api/diagnostic_api.py
```

Accéder à: `http://localhost:8000/docs`

**Endpoints principaux:**
- `POST /api/diagnostic` - Obtenir un diagnostic
- `GET /api/products` - Liste des produits
- `POST /api/purchase` - Créer une vente
- `GET /api/stats` - Statistiques

### 3. Workflow Orchestrateur (Automatisation)

```bash
# Exécution unique
python workflow_orchestrator.py once

# Mode daemon (continu)
python workflow_orchestrator.py daemon

# Tâches spécifiques
python workflow_orchestrator.py orders   # Traiter commandes
python workflow_orchestrator.py upsell   # Envoyer upsells
python workflow_orchestrator.py symptoms # Mettre à jour symptômes
python workflow_orchestrator.py report   # Générer rapport
```

**Tâches automatiques (mode daemon):**
- ⏱️ Traitement commandes: toutes les 15 min
- 📧 Campagnes upsell: toutes les heures
- 🤖 Mise à jour symptômes: 3h00 quotidien
- 📊 Rapport quotidien: 23h00

## 📁 Structure du Projet

```
mecaclair-diag/
├── app.py                          # Interface Streamlit principale
├── workflow_orchestrator.py        # Orchestrateur automatisation
├── requirements.txt                # Dépendances Python
│
├── src/
│   ├── pdf_generator/
│   │   └── generator.py           # Génération PDF marketing
│   │
│   ├── payment/
│   │   └── payment_system.py      # Gestion ventes & clients
│   │
│   ├── marketing/
│   │   ├── email_automation.py    # Automatisation emails
│   │   └── prompts.py             # Prompts marketing
│   │
│   ├── agent/
│   │   └── symptom_updater.py     # Agent IA symptômes
│   │
│   └── api/
│       └── diagnostic_api.py       # API FastAPI
│
├── data/
│   ├── pdfs/                      # PDF générés
│   ├── customers/                 # Base clients & commandes
│   ├── symptoms/                  # Base de données symptômes
│   ├── chroma_db/                 # ChromaDB (RAG)
│   └── reports/                   # Rapports quotidiens
│
└── templates/                     # Templates (futurs)
```

## 🎯 Workflow Marketing Complet

### Parcours Client Automatisé

```
1. CLIENT ACHÈTE
   ↓
2. COMMANDE CRÉÉE
   ↓
3. PDF GÉNÉRÉ AUTOMATIQUEMENT
   ↓
4. EMAIL DE CONFIRMATION (+ PDF)
   ↓
5. J+1: EMAIL SOFT UPSELL
   ↓
6. J+3: EMAIL HARD UPSELL (urgence)
   ↓
7. J+7: DEMANDE FEEDBACK
   ↓
8. J+14: BONUS GRATUIT
```

### Leviers Psychologiques Utilisés

✅ **Rareté** - "Plus que 7 places disponibles"
✅ **Urgence** - "Expire dans 23h47min"
✅ **Preuve sociale** - "247 mécaniciens ont déjà acheté"
✅ **Autorité** - "25+ ans d'expérience"
✅ **Réciprocité** - Bonus gratuits avant vente
✅ **Aversion à la perte** - "Chaque jour sans = 200€ perdus"
✅ **Exclusivité** - "Réservé aux professionnels sérieux"
✅ **Contraste** - Prix barré vs prix actuel
✅ **Émotion** - Histoires et transformation
✅ **Personnalisation** - "Vous", "Votre"

**IMPORTANT:** Tous les leviers sont utilisés de manière **éthique et légale**, basés sur des principes de persuasion scientifiquement prouvés.

## 💡 Produits Disponibles

### 1. Formation BASIC (97€)
- Base de données 5000+ pannes
- PDF téléchargeable à vie
- Mises à jour trimestrielles

### 2. Formation PREMIUM (297€)
- Tout de la BASIC +
- Accès plateforme en ligne à vie
- Mises à jour hebdomadaires
- Support 24/7
- Communauté VIP
- Certificat professionnel

### 3. Diagnostic à Distance (47€/mois)
- Accès plateforme diagnostic
- Rapports PDF automatiques
- Interface client branded

### 4. Pack COMPLET (397€)
- Premium + Diagnostic 1 an
- Coaching 1h privé
- Tous les bonus
- Garantie résultats 90j

## 📊 Statistiques & Analytics

Le système track automatiquement:
- 💰 Revenus totaux & panier moyen
- 👥 Nombre de clients (basic vs premium)
- 📦 Taux de conversion
- 📧 Performance emails (à venir)
- 🤖 Croissance base de symptômes

## 🔒 Configuration Email

Pour activer l'envoi d'emails automatiques, configurez les variables d'environnement:

```bash
# Créer un fichier .env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=votre@email.com
SMTP_PASSWORD=votre_mot_de_passe
```

**Note:** Pour Gmail, utilisez un "App Password" au lieu de votre mot de passe principal.

## 🤖 Base de Données Symptômes

L'agent IA maintient automatiquement une base de:
- **Symptômes** (ex: "Voyant moteur allumé")
- **Causes probables** avec probabilités (ex: "Sonde lambda 35%")
- **Solutions** (ex: "Remplacer sonde lambda")
- **Coûts estimés** (ex: "120-250€")
- **Sources** (forums, docs techniques, retours terrain)

## 📈 Roadmap

- [ ] Intégration Stripe pour paiements réels
- [ ] Tracking avancé des emails (ouvertures, clics)
- [ ] A/B Testing des copies marketing
- [ ] Webhooks pour intégrations tierces
- [ ] App mobile client (diagnostic)
- [ ] Certification professionnelle automatisée
- [ ] Marketplace de formations

## 🤝 Support

Pour toute question ou problème:
- 📧 Email: support@mecaclair-diag.com
- 📚 Documentation complète dans `/docs` (à venir)

## 📄 Licence

Propriétaire - Tous droits réservés © 2024

## ⚠️ Disclaimer Marketing

Tous les templates marketing et prompts fournis sont conçus pour être:
- ✅ **Légaux** - Conformes aux lois sur la publicité
- ✅ **Éthiques** - Pas de manipulation malhonnête
- ✅ **Factuels** - Basés sur des données réelles ou raisonnables
- ✅ **Transparents** - Garanties clairement énoncées

**Responsabilité:** L'utilisateur est responsable de l'utilisation des outils marketing et doit s'assurer de respecter les lois locales sur la publicité et la protection des consommateurs.

---

**Développé avec ❤️ pour révolutionner la formation en diagnostic automobile**
