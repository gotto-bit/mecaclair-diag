# 🚀 Guide de Démarrage Rapide - MecaClair Diag

## Installation en 3 étapes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer l'interface Streamlit

```bash
streamlit run app.py
```

Ouvrir: http://localhost:8501

### 3. Tester le système

#### Option A: Via l'interface Streamlit

1. Allez dans **💳 Gestions Ventes** > **🛒 Nouvelle Vente**
2. Remplissez:
   - Nom: "Jean Dupont"
   - Email: "jean@test.com"
   - Produit: Formation BASIC
3. Cliquez sur **💳 Créer la Vente**
4. Le PDF sera généré automatiquement!

#### Option B: Via l'API

```bash
# Terminal 1: Lancer l'API
python src/api/diagnostic_api.py

# Terminal 2: Tester un diagnostic
curl -X POST "http://localhost:8000/api/diagnostic" \
  -H "Content-Type: application/json" \
  -d '{
    "symptom_description": "voyant moteur allumé",
    "vehicle_type": "diesel"
  }'
```

## 📋 Fonctionnalités à Tester

### ✅ Générateur de PDF
- Menu: **📄 Générer PDF**
- Personnalisez le client et générez un PDF de formation
- Téléchargez le résultat!

### ✅ Base de Symptômes
- Menu: **🤖 Agent Symptômes** > **🔍 Recherche**
- Recherchez: "démarrage difficile"
- Voyez les causes probables avec probabilités!

### ✅ Prompts Marketing
- Menu: **💡 Prompts Marketing** > **📝 Landing Page**
- Sélectionnez un produit
- Cliquez sur **🚀 Générer le Copy Complet**
- Admirez le copywriting agressif mais éthique!

### ✅ Analytics
- Menu: **📊 Statistiques**
- Consultez les revenus, conversions, etc.

## 🤖 Automatisation Complète

Pour lancer l'orchestrateur qui automatise tout:

```bash
# Exécution unique (test)
python workflow_orchestrator.py once

# Mode daemon (production)
python workflow_orchestrator.py daemon
```

**Tâches automatisées:**
- ⏱️ Génération + envoi de PDF toutes les 15 min
- 📧 Campagnes upsell toutes les heures
- 🤖 Mise à jour symptômes quotidienne (3h00)
- 📊 Rapport quotidien (23h00)

## 📧 Configuration Email (optionnel)

Pour activer l'envoi d'emails:

```bash
# Copier le template
cp .env.example .env

# Éditer .env avec vos identifiants
nano .env
```

**Pour Gmail:**
1. Activez la validation en 2 étapes
2. Générez un "App Password"
3. Utilisez ce password dans `.env`

## 🎯 Exemples d'Utilisation

### Créer une vente complète (script)

```python
from src.payment.payment_system import PaymentSystem
from src.pdf_generator.generator import PDFFormationGenerator
from src.agent.symptom_updater import SymptomUpdateAgent

# Initialiser
payment = PaymentSystem()
pdf_gen = PDFFormationGenerator()
agent = SymptomUpdateAgent()

# Créer client
customer = payment.create_customer(
    email="test@example.com",
    name="Test Client"
)

# Créer commande
order = payment.create_order(
    customer_id=customer.id,
    product_id="formation_basic"
)

# Compléter
payment.complete_order(order.id)

# Générer PDF
symptoms = agent.export_for_pdf(limit=50)
pdf_path = pdf_gen.generate_diagnostic_training_pdf(
    title="Formation Test",
    customer_name="Test Client",
    symptoms_data=symptoms,
    price=97.0,
    order_id=order.id
)

print(f"PDF généré: {pdf_path}")
```

### Diagnostic via API (Python)

```python
import requests

response = requests.post(
    "http://localhost:8000/api/diagnostic",
    json={
        "symptom_description": "fumée noire à l'échappement",
        "vehicle_type": "diesel"
    }
)

result = response.json()
print(f"Confiance: {result['confidence_score']:.0%}")
for suggestion in result['suggestions']:
    print(f"- {suggestion['symptom']}")
```

## 🐛 Dépannage

### Erreur: Module not found

```bash
# Assurez-vous d'être dans le bon répertoire
cd mecaclair-diag

# Réinstallez les dépendances
pip install -r requirements.txt
```

### Streamlit ne démarre pas

```bash
# Vérifier la version Python
python --version  # Doit être 3.9+

# Réinstaller Streamlit
pip install --upgrade streamlit
```

### ChromaDB erreur

```bash
# Supprimer la DB et relancer
rm -rf data/chroma_db
streamlit run app.py
```

## 📚 Documentation Complète

Consultez le [README.md](README.md) pour:
- Architecture détaillée
- Tous les endpoints API
- Leviers psychologiques utilisés
- Configuration avancée

## 💡 Premiers Pas Recommandés

1. ✅ **Jour 1**: Explorez l'interface Streamlit
2. ✅ **Jour 2**: Testez l'API de diagnostic
3. ✅ **Jour 3**: Générez votre premier PDF
4. ✅ **Jour 4**: Configurez les emails
5. ✅ **Jour 5**: Lancez l'orchestrateur en mode daemon

## 🤝 Besoin d'Aide?

- 📧 Email: support@mecaclair-diag.com
- 💬 Consultez les exemples dans chaque module
- 📖 Lisez le README complet

---

**Bon workflow marketing! 🚀**
