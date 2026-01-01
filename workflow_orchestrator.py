"""
Orchestrateur du Workflow Marketing Digital
Automatise l'ensemble du processus de vente et marketing
"""
import os
import sys
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List

# Ajouter le chemin des sources
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_generator.generator import PDFFormationGenerator
from payment.payment_system import PaymentSystem
from marketing.email_automation import EmailMarketingSystem
from agent.symptom_updater import SymptomUpdateAgent


class MarketingWorkflowOrchestrator:
    """
    Orchestrateur principal du workflow marketing digital

    Automatise:
    1. Génération de PDF après achat
    2. Envoi automatique des PDF
    3. Séquences d'emails marketing (upsell, nurturing)
    4. Mise à jour de la base de symptômes
    5. Relances panier abandonné
    """

    def __init__(
        self,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 587,
        smtp_email: str = "",
        smtp_password: str = ""
    ):
        print("🚀 Initialisation du Workflow Orchestrateur...")

        # Initialiser tous les systèmes
        self.pdf_generator = PDFFormationGenerator()
        self.payment_system = PaymentSystem()
        self.email_system = EmailMarketingSystem(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            sender_email=smtp_email,
            sender_password=smtp_password
        )
        self.symptom_agent = SymptomUpdateAgent()

        print("✅ Tous les systèmes initialisés")

    def process_pending_orders(self):
        """
        Traite les commandes en attente:
        1. Génère les PDF manquants
        2. Envoie les PDF non envoyés
        """
        print("\n🔄 Traitement des commandes en attente...")

        pending_orders = self.payment_system.get_pending_pdf_orders()

        if not pending_orders:
            print("✅ Aucune commande en attente")
            return

        print(f"📦 {len(pending_orders)} commande(s) à traiter")

        for order in pending_orders:
            try:
                # Récupérer les infos client et produit
                customer_data = self.payment_system.customers.get(order.customer_id)
                if not customer_data:
                    print(f"⚠️ Client introuvable pour commande {order.id}")
                    continue

                product = self.payment_system.products.get(order.product_id)
                if not product:
                    print(f"⚠️ Produit introuvable pour commande {order.id}")
                    continue

                # Générer le PDF si nécessaire
                if not order.pdf_generated or not order.pdf_path:
                    print(f"📄 Génération PDF pour commande {order.id}...")

                    symptoms_data = self.symptom_agent.export_for_pdf(limit=50)

                    pdf_path = self.pdf_generator.generate_diagnostic_training_pdf(
                        title=product.name,
                        customer_name=customer_data['name'],
                        symptoms_data=symptoms_data,
                        price=product.price,
                        order_id=order.id
                    )

                    self.payment_system.update_order_pdf(order.id, pdf_path)
                    print(f"✅ PDF généré: {pdf_path}")

                    # Recharger l'ordre
                    order_data = self.payment_system.orders[order.id]
                    order.pdf_path = order_data['pdf_path']

                # Envoyer l'email avec le PDF
                if not order.pdf_sent and order.pdf_path:
                    print(f"📧 Envoi email à {customer_data['email']}...")

                    success = self.email_system.send_purchase_confirmation(
                        customer_email=customer_data['email'],
                        customer_name=customer_data['name'],
                        product_name=product.name,
                        order_id=order.id,
                        pdf_path=order.pdf_path,
                        amount=product.price
                    )

                    if success:
                        self.payment_system.mark_pdf_sent(order.id)
                        print(f"✅ Email envoyé à {customer_data['email']}")
                    else:
                        print(f"❌ Échec envoi email à {customer_data['email']}")

            except Exception as e:
                print(f"❌ Erreur traitement commande {order.id}: {e}")

        print("✅ Traitement des commandes terminé\n")

    def send_upsell_campaigns(self):
        """
        Envoie les campagnes d'upsell automatiques
        J+1 et J+3 après achat pour clients non-premium
        """
        print("\n🎯 Envoi des campagnes upsell...")

        # Candidats J+1 (soft upsell)
        candidates_day1 = self.payment_system.get_upsell_candidates(days=1)

        for customer, order in candidates_day1:
            try:
                # Vérifier si déjà envoyé (à implémenter: tracking des emails)
                product = self.payment_system.products.get(order.product_id)

                print(f"📧 Upsell J+1 pour {customer.email}...")

                success = self.email_system.send_upsell_email_day1(
                    customer_email=customer.email,
                    customer_name=customer.name,
                    original_product=product.name if product else "Formation"
                )

                if success:
                    print(f"✅ Email J+1 envoyé à {customer.email}")

            except Exception as e:
                print(f"❌ Erreur upsell J+1 pour {customer.email}: {e}")

        # Candidats J+3 (hard upsell avec urgence)
        candidates_day3 = self.payment_system.get_upsell_candidates(days=3)

        for customer, order in candidates_day3:
            try:
                print(f"📧 Upsell J+3 (urgence) pour {customer.email}...")

                success = self.email_system.send_upsell_email_day3(
                    customer_email=customer.email,
                    customer_name=customer.name
                )

                if success:
                    print(f"✅ Email J+3 envoyé à {customer.email}")

            except Exception as e:
                print(f"❌ Erreur upsell J+3 pour {customer.email}: {e}")

        print("✅ Campagnes upsell terminées\n")

    def update_symptoms_database(self):
        """
        Met à jour la base de données des symptômes
        Via l'agent autonome
        """
        print("\n🤖 Mise à jour de la base de symptômes...")

        try:
            updates_count = self.symptom_agent.auto_update_from_sources()
            print(f"✅ {updates_count} nouvelles observations ajoutées")
            print(f"📊 Total symptômes: {len(self.symptom_agent.symptoms)}")

        except Exception as e:
            print(f"❌ Erreur mise à jour symptômes: {e}")

        print("✅ Mise à jour terminée\n")

    def generate_daily_report(self):
        """Génère un rapport quotidien des performances"""
        print("\n📊 Génération du rapport quotidien...")

        stats = self.payment_system.get_customer_stats()

        report = f"""
        ═══════════════════════════════════════
        📊 RAPPORT QUOTIDIEN - {datetime.now().strftime('%d/%m/%Y')}
        ═══════════════════════════════════════

        💰 REVENUS
        • Total: {stats['total_revenue']:.2f}€
        • Panier moyen: {stats['average_order_value']:.2f}€

        👥 CLIENTS
        • Total: {stats['total_customers']}
        • Premium: {stats['premium_customers']}
        • Taux premium: {(stats['premium_customers']/max(stats['total_customers'],1)*100):.1f}%

        📦 COMMANDES
        • Total: {stats['total_orders']}
        • Complétées: {stats['completed_orders']}
        • Taux conversion: {stats['conversion_rate']:.1f}%

        🤖 BASE DE DONNÉES
        • Symptômes: {len(self.symptom_agent.symptoms)}
        • Dernière mise à jour: {datetime.now().strftime('%H:%M')}

        ═══════════════════════════════════════
        """

        print(report)

        # Sauvegarder le rapport
        reports_dir = "data/reports"
        os.makedirs(reports_dir, exist_ok=True)

        report_path = os.path.join(
            reports_dir,
            f"report_{datetime.now().strftime('%Y%m%d')}.txt"
        )

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Rapport sauvegardé: {report_path}\n")

    def run_full_workflow(self):
        """Exécute le workflow complet"""
        print("\n" + "="*50)
        print(f"🚀 WORKFLOW COMPLET - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*50 + "\n")

        # 1. Traiter les commandes
        self.process_pending_orders()

        # 2. Envoyer les campagnes upsell
        self.send_upsell_campaigns()

        # 3. Mettre à jour les symptômes (1x par jour)
        if datetime.now().hour == 3:  # 3h du matin
            self.update_symptoms_database()

        # 4. Générer le rapport (1x par jour)
        if datetime.now().hour == 23:  # 23h
            self.generate_daily_report()

        print("="*50)
        print("✅ WORKFLOW TERMINÉ")
        print("="*50 + "\n")

    def schedule_workflows(self):
        """Configure les tâches planifiées"""
        print("📅 Configuration des tâches planifiées...\n")

        # Traiter les commandes toutes les 15 minutes
        schedule.every(15).minutes.do(self.process_pending_orders)
        print("✅ Commandes: toutes les 15 minutes")

        # Campagnes upsell toutes les heures
        schedule.every(1).hours.do(self.send_upsell_campaigns)
        print("✅ Upsell: toutes les heures")

        # Mise à jour symptômes 1x par jour à 3h
        schedule.every().day.at("03:00").do(self.update_symptoms_database)
        print("✅ Mise à jour symptômes: 3h00")

        # Rapport quotidien à 23h
        schedule.every().day.at("23:00").do(self.generate_daily_report)
        print("✅ Rapport quotidien: 23h00")

        print("\n🔄 Démarrage de l'orchestrateur...\n")

    def run_daemon(self):
        """Exécute l'orchestrateur en mode daemon"""
        self.schedule_workflows()

        # Exécuter une première fois immédiatement
        self.run_full_workflow()

        # Boucle infinie
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérifier chaque minute


def main():
    """Point d'entrée principal"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🚗 MECACLAIR DIAG - WORKFLOW MARKETING ORCHESTRATEUR   ║
    ║                                                           ║
    ║   Automatisation complète du workflow de vente           ║
    ║   et marketing digital                                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Initialiser l'orchestrateur
    orchestrator = MarketingWorkflowOrchestrator(
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_email=os.getenv("SMTP_EMAIL", ""),
        smtp_password=os.getenv("SMTP_PASSWORD", "")
    )

    # Mode de fonctionnement
    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "once":
            # Exécution unique
            orchestrator.run_full_workflow()

        elif mode == "daemon":
            # Mode daemon (continu)
            orchestrator.run_daemon()

        elif mode == "orders":
            # Traiter seulement les commandes
            orchestrator.process_pending_orders()

        elif mode == "upsell":
            # Envoyer seulement les upsells
            orchestrator.send_upsell_campaigns()

        elif mode == "symptoms":
            # Mettre à jour seulement les symptômes
            orchestrator.update_symptoms_database()

        elif mode == "report":
            # Générer seulement le rapport
            orchestrator.generate_daily_report()

        else:
            print(f"❌ Mode inconnu: {mode}")
            print_usage()

    else:
        print_usage()


def print_usage():
    """Affiche l'aide d'utilisation"""
    print("""
    UTILISATION:

    python workflow_orchestrator.py [MODE]

    MODES DISPONIBLES:

    once        Exécute le workflow complet une fois
    daemon      Démarre en mode continu (tâches planifiées)
    orders      Traite uniquement les commandes en attente
    upsell      Envoie uniquement les emails upsell
    symptoms    Met à jour uniquement la base de symptômes
    report      Génère uniquement le rapport quotidien

    EXEMPLES:

    # Exécuter une fois
    python workflow_orchestrator.py once

    # Démarrer en mode daemon
    python workflow_orchestrator.py daemon

    # Traiter les commandes
    python workflow_orchestrator.py orders
    """)


if __name__ == "__main__":
    main()
