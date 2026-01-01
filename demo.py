#!/usr/bin/env python
"""
Script de démonstration - MecaClair Diag
Teste rapidement toutes les fonctionnalités
"""
import sys
import os

# Ajouter le chemin des sources
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_generator.generator import PDFFormationGenerator
from payment.payment_system import PaymentSystem
from agent.symptom_updater import SymptomUpdateAgent
from marketing.prompts import MarketingPrompts


def print_banner(text):
    """Affiche un banner"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def demo_symptom_agent():
    """Démo de l'agent symptômes"""
    print_banner("🤖 DÉMO: Agent Symptômes & Diagnostic")

    agent = SymptomUpdateAgent()

    print(f"📊 Base de données: {len(agent.symptoms)} symptômes chargés")
    print()

    # Recherche
    query = "voyant moteur allumé"
    print(f"🔍 Recherche: '{query}'")
    results = agent.search_similar_symptoms(query, top_k=3)

    for i, symptom in enumerate(results, 1):
        print(f"\n{i}. {symptom.symptom_text}")
        print(f"   Confiance: {symptom.confidence_score:.0%} | Fréquence: {symptom.frequency}")
        print(f"   Causes probables:")

        for cause in symptom.probable_causes[:2]:
            print(f"      • {cause['cause']} ({cause['probability']:.0%})")
            print(f"        → {cause['solution']}")

    # Ajouter un nouveau symptôme
    print("\n➕ Ajout d'une nouvelle observation...")
    agent.update_symptom_from_source(
        symptom_text="Bruit anormal au freinage",
        new_cause="Plaquettes usées",
        solution="Remplacer plaquettes de frein",
        source="Retour terrain - Demo",
        vehicle_type="essence"
    )
    print("✅ Observation ajoutée!")


def demo_payment_system():
    """Démo du système de paiement"""
    print_banner("💳 DÉMO: Système de Paiement")

    payment = PaymentSystem()

    print("📦 Produits disponibles:")
    for product_id, product in payment.products.items():
        print(f"\n• {product.name} - {product.price}€")
        print(f"  Type: {product.product_type.value}")

    # Créer un client de test
    print("\n👤 Création d'un client de test...")
    customer = payment.create_customer(
        email="demo@mecaclair.com",
        name="Client Demo"
    )
    print(f"✅ Client créé: {customer.name} ({customer.email})")

    # Créer une commande
    print("\n🛒 Création d'une commande...")
    order = payment.create_order(
        customer_id=customer.id,
        product_id="formation_basic"
    )
    print(f"✅ Commande créée: #{order.id} - {order.amount}€")

    # Compléter la commande
    print("\n💰 Finalisation de la commande...")
    payment.complete_order(order.id)
    print(f"✅ Commande complétée!")

    # Statistiques
    print("\n📊 Statistiques:")
    stats = payment.get_customer_stats()
    print(f"   Total clients: {stats['total_customers']}")
    print(f"   Total commandes: {stats['completed_orders']}")
    print(f"   Revenus: {stats['total_revenue']:.2f}€")
    print(f"   Panier moyen: {stats['average_order_value']:.2f}€")


def demo_pdf_generator():
    """Démo du générateur de PDF"""
    print_banner("📄 DÉMO: Générateur de PDF Marketing")

    pdf_gen = PDFFormationGenerator()
    agent = SymptomUpdateAgent()

    print("📝 Génération d'un PDF de formation...")

    # Récupérer les données
    symptoms_data = agent.export_for_pdf(limit=20)

    # Générer le PDF
    pdf_path = pdf_gen.generate_diagnostic_training_pdf(
        title="Formation Diagnostic Rapide - DEMO",
        customer_name="Client Demo",
        symptoms_data=symptoms_data,
        price=97.0,
        order_id="DEMO-001"
    )

    print(f"✅ PDF généré avec succès!")
    print(f"📁 Chemin: {pdf_path}")
    print(f"📊 Contenu: {len(symptoms_data)} symptômes inclus")


def demo_marketing_prompts():
    """Démo des prompts marketing"""
    print_banner("💡 DÉMO: Prompts Marketing")

    prompts = MarketingPrompts()

    print("🎯 Génération de copy pour landing page...")

    landing = prompts.generate_landing_page_copy(
        product_name="Formation Diagnostic Rapide",
        price=97.0,
        benefits=[
            "Base de données 5000+ pannes",
            "Diagnostic en 15 min",
            "Support 24/7"
        ]
    )

    print("\n📌 HEADLINE:")
    print(landing['headline'])

    print("\n📌 URGENCE:")
    print(landing['urgency'])

    print("\n📌 GARANTIE:")
    print(landing['guarantee'])

    print("\n📢 Génération de publicité Facebook...")
    ad = prompts.generate_facebook_ad_copy(
        product_name="Formation Premium",
        price=297.0
    )

    print(f"\n📝 Headline: {ad['headline']}")
    print(f"🎯 CTA: {ad['call_to_action']}")

    print("\n🧠 Leviers psychologiques disponibles:")
    triggers = prompts.generate_sales_page_triggers()
    for trigger in triggers[:5]:
        print(f"   • {trigger['trigger'].value.upper()}")


def demo_complete_workflow():
    """Démo du workflow complet"""
    print_banner("🚀 DÉMO: Workflow Complet")

    print("Ce workflow simule l'ensemble du processus:")
    print("\n1. Client achète une formation")
    print("2. Commande créée automatiquement")
    print("3. PDF généré avec données actualisées")
    print("4. Email envoyé (simulé)")
    print("5. Séquence upsell programmée")

    payment = PaymentSystem()
    pdf_gen = PDFFormationGenerator()
    agent = SymptomUpdateAgent()

    # 1. Créer client
    print("\n👤 Création du client...")
    customer = payment.create_customer(
        email="workflow@demo.com",
        name="Workflow Demo"
    )

    # 2. Créer commande
    print("🛒 Création de la commande...")
    order = payment.create_order(
        customer_id=customer.id,
        product_id="formation_premium"
    )

    # 3. Compléter commande
    print("💰 Finalisation du paiement...")
    payment.complete_order(order.id)

    # 4. Générer PDF
    print("📄 Génération du PDF personnalisé...")
    product = payment.products["formation_premium"]
    symptoms = agent.export_for_pdf(limit=30)

    pdf_path = pdf_gen.generate_diagnostic_training_pdf(
        title=product.name,
        customer_name=customer.name,
        symptoms_data=symptoms,
        price=product.price,
        order_id=order.id
    )

    payment.update_order_pdf(order.id, pdf_path)

    # 5. Simuler envoi email
    print("📧 Envoi de l'email de confirmation (simulé)...")
    payment.mark_pdf_sent(order.id)

    print("\n✅ WORKFLOW TERMINÉ!")
    print(f"\n📊 Résumé:")
    print(f"   Client: {customer.name} ({customer.email})")
    print(f"   Commande: #{order.id}")
    print(f"   Produit: {product.name}")
    print(f"   Montant: {product.price}€")
    print(f"   PDF: {pdf_path}")
    print(f"   Status: Complet ✅")


def main():
    """Point d'entrée principal"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      🚗 MECACLAIR DIAG - DÉMONSTRATION COMPLÈTE         ║
    ║                                                          ║
    ║         Workflow Marketing Digital Automatisé           ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    demos = {
        "1": ("Agent Symptômes", demo_symptom_agent),
        "2": ("Système Paiement", demo_payment_system),
        "3": ("Générateur PDF", demo_pdf_generator),
        "4": ("Prompts Marketing", demo_marketing_prompts),
        "5": ("Workflow Complet", demo_complete_workflow),
        "all": ("Tout Exécuter", None)
    }

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("\nChoisissez une démo:")
        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")

        print("\nUsage: python demo.py [numéro]")
        print("Example: python demo.py 1")
        print("         python demo.py all\n")
        return

    if choice == "all":
        # Exécuter toutes les démos
        for key, (name, func) in demos.items():
            if key != "all" and func:
                try:
                    func()
                    input("\nAppuyez sur Entrée pour continuer...")
                except Exception as e:
                    print(f"\n❌ Erreur: {e}")

    elif choice in demos and demos[choice][1]:
        # Exécuter une démo spécifique
        try:
            demos[choice][1]()
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

    else:
        print(f"\n❌ Choix invalide: {choice}")
        print("Utilisez: 1, 2, 3, 4, 5, ou all\n")

    print("\n" + "="*60)
    print("  ✅ Démonstration terminée!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
