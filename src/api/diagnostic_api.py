"""
API FastAPI pour le diagnostic à distance
Permet aux clients de soumettre des symptômes et recevoir un diagnostic
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.symptom_updater import SymptomUpdateAgent
from payment.payment_system import PaymentSystem
from pdf_generator.generator import PDFFormationGenerator


app = FastAPI(
    title="MecaClair Diagnostic API",
    description="API de diagnostic automobile à distance",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des systèmes
symptom_agent = SymptomUpdateAgent()
payment_system = PaymentSystem()
pdf_generator = PDFFormationGenerator()


# --- MODÈLES PYDANTIC ---

class DiagnosticRequest(BaseModel):
    """Requête de diagnostic"""
    symptom_description: str
    vehicle_type: Optional[str] = "essence"
    vehicle_brand: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    customer_email: Optional[EmailStr] = None
    customer_name: Optional[str] = None


class DiagnosticResponse(BaseModel):
    """Réponse de diagnostic"""
    suggestions: List[dict]
    confidence_score: float
    recommended_actions: List[str]
    estimated_cost_range: str
    urgency_level: str


class PurchaseRequest(BaseModel):
    """Requête d'achat"""
    customer_email: EmailStr
    customer_name: str
    customer_phone: Optional[str] = None
    product_id: str
    payment_method: str = "stripe"


class PurchaseResponse(BaseModel):
    """Réponse d'achat"""
    order_id: str
    amount: float
    status: str
    pdf_download_url: Optional[str] = None


# --- ENDPOINTS ---

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🚗 MecaClair Diagnostic API",
        "version": "1.0.0",
        "endpoints": {
            "diagnostic": "/api/diagnostic",
            "products": "/api/products",
            "purchase": "/api/purchase",
            "stats": "/api/stats"
        }
    }


@app.post("/api/diagnostic", response_model=DiagnosticResponse)
async def get_diagnostic(request: DiagnosticRequest):
    """
    Endpoint principal de diagnostic à distance

    Retourne des suggestions de causes et solutions basées sur le symptôme décrit
    """
    try:
        # Obtenir suggestions de l'agent IA
        suggestions = symptom_agent.get_diagnostic_suggestions(
            symptom_description=request.symptom_description,
            vehicle_type=request.vehicle_type
        )

        if not suggestions:
            raise HTTPException(
                status_code=404,
                detail="Aucun diagnostic trouvé pour ce symptôme"
            )

        # Calculer le score de confiance global
        confidence_score = sum(s['confidence'] for s in suggestions) / len(suggestions)

        # Extraire les actions recommandées
        recommended_actions = []
        total_min_cost = 0
        total_max_cost = 0

        for suggestion in suggestions:
            for cause in suggestion['causes'][:2]:  # Top 2 causes
                action = f"{cause['cause']}: {cause['solution']}"
                if action not in recommended_actions:
                    recommended_actions.append(action)

                # Estimer les coûts
                if 'cost_estimate' in cause and cause['cost_estimate'] != "Variable":
                    try:
                        costs = cause['cost_estimate'].replace('€', '').split('-')
                        if len(costs) == 2:
                            total_min_cost += int(costs[0])
                            total_max_cost += int(costs[1])
                    except:
                        pass

        # Déterminer l'urgence
        severities = [s['severity'] for s in suggestions]
        if 'critical' in severities:
            urgency_level = "CRITIQUE - Intervention immédiate requise"
        elif 'high' in severities:
            urgency_level = "ÉLEVÉE - Intervention rapide recommandée"
        elif 'medium' in severities:
            urgency_level = "MOYENNE - Planifier intervention"
        else:
            urgency_level = "FAIBLE - Surveillance"

        # Estimation des coûts
        if total_min_cost > 0 and total_max_cost > 0:
            cost_range = f"{total_min_cost}-{total_max_cost}€"
        else:
            cost_range = "À évaluer en atelier"

        return DiagnosticResponse(
            suggestions=suggestions,
            confidence_score=confidence_score,
            recommended_actions=recommended_actions,
            estimated_cost_range=cost_range,
            urgency_level=urgency_level
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products")
async def get_products():
    """Liste tous les produits disponibles"""
    products = []
    for product_id, product in payment_system.products.items():
        products.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "features": product.features,
            "marketing_copy": product.marketing_copy
        })

    return {"products": products}


@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """Détails d'un produit spécifique"""
    if product_id not in payment_system.products:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    product = payment_system.products[product_id]
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "features": product.features,
        "marketing_copy": product.marketing_copy
    }


@app.post("/api/purchase", response_model=PurchaseResponse)
async def create_purchase(request: PurchaseRequest):
    """
    Crée une commande et génère le PDF automatiquement

    Workflow complet:
    1. Créer ou récupérer le client
    2. Créer la commande
    3. Simuler le paiement (en prod: intégration Stripe)
    4. Générer le PDF
    5. Marquer la commande comme complétée
    """
    try:
        # 1. Créer ou récupérer le client
        customer = payment_system.get_customer_by_email(request.customer_email)
        if not customer:
            customer = payment_system.create_customer(
                email=request.customer_email,
                name=request.customer_name,
                phone=request.customer_phone
            )

        # 2. Créer la commande
        order = payment_system.create_order(
            customer_id=customer.id,
            product_id=request.product_id,
            payment_method=request.payment_method
        )

        # 3. Simuler le paiement (en production: intégration Stripe réelle)
        # Pour la démo, on marque directement comme payé
        payment_system.complete_order(order.id)

        # 4. Générer le PDF
        product = payment_system.products[request.product_id]
        symptoms_data = symptom_agent.export_for_pdf(limit=50)

        pdf_path = pdf_generator.generate_diagnostic_training_pdf(
            title=product.name,
            customer_name=request.customer_name,
            symptoms_data=symptoms_data,
            price=product.price,
            order_id=order.id
        )

        # 5. Mettre à jour la commande avec le PDF
        payment_system.update_order_pdf(order.id, pdf_path)

        return PurchaseResponse(
            order_id=order.id,
            amount=product.price,
            status="completed",
            pdf_download_url=f"/api/download/{order.id}"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Statistiques du système (admin)"""
    stats = payment_system.get_customer_stats()

    return {
        "customers": stats,
        "symptoms_database": {
            "total_symptoms": len(symptom_agent.symptoms),
            "last_update": datetime.now().isoformat()
        }
    }


@app.post("/api/admin/update-symptoms")
async def trigger_symptom_update():
    """
    Déclenche manuellement la mise à jour des symptômes
    (en production: sécurisé par authentification admin)
    """
    try:
        updates_count = symptom_agent.auto_update_from_sources()

        return {
            "status": "success",
            "updates_applied": updates_count,
            "total_symptoms": len(symptom_agent.symptoms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/symptoms/search")
async def search_symptoms(query: str, limit: int = 5):
    """Recherche de symptômes similaires"""
    try:
        results = symptom_agent.search_similar_symptoms(query, top_k=limit)

        return {
            "query": query,
            "results": [
                {
                    "symptom": s.symptom_text,
                    "causes": s.probable_causes,
                    "severity": s.severity,
                    "confidence": s.confidence_score
                }
                for s in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- WEBHOOKS ---

@app.post("/api/webhooks/stripe")
async def stripe_webhook(payload: dict):
    """
    Webhook Stripe pour les paiements réels
    À configurer dans le dashboard Stripe
    """
    # En production: vérifier la signature Stripe
    event_type = payload.get('type')

    if event_type == 'payment_intent.succeeded':
        # Traiter le paiement réussi
        order_id = payload.get('metadata', {}).get('order_id')
        if order_id:
            payment_system.complete_order(order_id)

    return {"status": "received"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
