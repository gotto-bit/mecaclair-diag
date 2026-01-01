"""
Système de gestion des paiements et commandes
Intégration Stripe + Base de données locale
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ProductType(Enum):
    """Types de produits disponibles"""
    FORMATION_BASIC = "formation_basic"
    FORMATION_PREMIUM = "formation_premium"
    DIAGNOSTIC_ACCESS = "diagnostic_access"
    FULL_BUNDLE = "full_bundle"


@dataclass
class Product:
    """Définition d'un produit"""
    id: str
    name: str
    description: str
    price: float
    product_type: ProductType
    features: List[str]
    marketing_copy: str  # Copy marketing agressif


@dataclass
class Customer:
    """Informations client"""
    id: str
    email: str
    name: str
    phone: Optional[str]
    created_at: str
    total_spent: float
    purchase_count: int
    is_premium: bool


@dataclass
class Order:
    """Commande client"""
    id: str
    customer_id: str
    product_id: str
    amount: float
    status: str  # pending, completed, failed, refunded
    payment_method: str
    created_at: str
    completed_at: Optional[str]
    pdf_generated: bool
    pdf_sent: bool
    pdf_path: Optional[str]


class PaymentSystem:
    """Gestion complète du système de paiement et commandes"""

    def __init__(self, data_dir: str = "data/customers"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.customers_file = os.path.join(data_dir, "customers.json")
        self.orders_file = os.path.join(data_dir, "orders.json")
        self.products = self._initialize_products()
        self._load_data()

    def _initialize_products(self) -> Dict[str, Product]:
        """Initialise le catalogue de produits avec marketing agressif"""
        products = {
            "formation_basic": Product(
                id="formation_basic",
                name="Formation Diagnostic Rapide",
                description="Devenez un expert du diagnostic automobile",
                price=97.0,
                product_type=ProductType.FORMATION_BASIC,
                features=[
                    "Base de données de 5000+ pannes",
                    "Probabilités de diagnostic IA",
                    "PDF téléchargeable à vie",
                    "Mises à jour trimestrielles"
                ],
                marketing_copy="""
                🔥 OFFRE LIMITÉE: 97€ au lieu de 297€ 🔥

                ⚠️ Cette offre expire dans 48h! ⚠️

                Ce que vous obtenez IMMÉDIATEMENT:
                ✅ Accès instantané à 5000+ pannes référencées
                ✅ Système d'IA qui calcule les probabilités
                ✅ Téléchargement PDF illimité
                ✅ Mises à jour gratuites pendant 1 an

                🎯 127 mécaniciens ont déjà acheté cette formation ce mois!

                💰 GARANTIE 30 JOURS - Satisfait ou remboursé!

                Chaque jour sans cette formation vous coûte 200€ en temps perdu...
                """
            ),
            "formation_premium": Product(
                id="formation_premium",
                name="Formation PREMIUM - Accès à vie",
                description="Devenez LA référence en diagnostic automobile",
                price=297.0,
                product_type=ProductType.FORMATION_PREMIUM,
                features=[
                    "TOUT de la formation Basic +",
                    "Accès à vie à la plateforme en ligne",
                    "Mises à jour automatiques hebdomadaires",
                    "Support prioritaire 24/7",
                    "Communauté privée VIP",
                    "Certificat professionnel",
                    "Templates de devis automatiques",
                    "Bonus: Ebook '50 Pannes Rentables'"
                ],
                marketing_copy="""
                🚀 FORMATION PREMIUM - INVESTISSEMENT QUI CHANGE TOUT 🚀

                Prix normal: 997€
                Prix aujourd'hui: 297€ (70% de réduction!)
                ⏰ Plus que 5 places à ce prix!

                POURQUOI LES MEILLEURS CHOISISSENT PREMIUM:

                ➤ Accès À VIE (pas de renouvellement)
                ➤ Mises à jour HEBDOMADAIRES (vs trimestrielles)
                ➤ Support 24/7 (réponse en moins de 2h)
                ➤ Communauté de 500+ experts
                ➤ Certificat reconnu (valorisez-vous auprès de vos clients)

                🎁 BONUS EXCLUSIFS (valeur: 394€):
                ✓ Ebook "Les 50 Pannes Les Plus Rentables" (97€)
                ✓ Templates de devis PRO (147€)
                ✓ Formation "Négociation Client" (150€)

                💡 Calcul simple:
                - Temps économisé par diagnostic: 30 min
                - Diagnostics par jour: 3
                - Gain de temps: 1h30/jour
                - Sur 1 an: 390 heures
                - À 50€/h = 19,500€ économisés!

                L'investissement se rembourse en 2 jours maximum.

                ⚠️ ATTENTION: Prix augmente de 100€ dans 6 heures!
                """
            ),
            "diagnostic_access": Product(
                id="diagnostic_access",
                name="Accès Plateforme Diagnostic (1 mois)",
                description="Diagnostic à distance pour vos clients",
                price=47.0,
                product_type=ProductType.DIAGNOSTIC_ACCESS,
                features=[
                    "Accès 1 mois à la plateforme",
                    "Diagnostic illimité",
                    "Rapports PDF automatiques",
                    "Interface client branded"
                ],
                marketing_copy="""
                💼 PROPOSEZ LE DIAGNOSTIC À DISTANCE À VOS CLIENTS 💼

                Seulement 47€/mois - Annulation quand vous voulez

                TRANSFORMEZ VOTRE BUSINESS:

                🎯 Attirez de nouveaux clients (diagnostic gratuit = porte d'entrée)
                🎯 Vendez plus de services (diagnostic = upsell automatique)
                🎯 Démarquez-vous de la concurrence (technologie moderne)
                🎯 Gagnez du temps (pré-diagnostic avant rendez-vous)

                💰 RENTABILITÉ IMMÉDIATE:
                - Coût: 47€/mois
                - Facturez le diagnostic: 30€
                - Il vous faut seulement 2 clients/mois pour être rentable!

                🔥 En moyenne, nos utilisateurs gagnent 850€/mois supplémentaires!

                ✨ Essai 14 jours offert - Testez sans risque!
                """
            ),
            "full_bundle": Product(
                id="full_bundle",
                name="PACK COMPLET - Tout Inclus",
                description="Formation Premium + Diagnostic + Bonus",
                price=397.0,
                product_type=ProductType.FULL_BUNDLE,
                features=[
                    "Formation PREMIUM complète",
                    "Accès plateforme diagnostic (1 an inclus)",
                    "Support VIP prioritaire",
                    "Tous les bonus",
                    "Coaching privé 1h",
                    "Garantie résultats 90 jours"
                ],
                marketing_copy="""
                🏆 PACK COMPLET - DEVENEZ UN EXPERT RECONNU 🏆

                Valeur totale: 1,544€
                Prix aujourd'hui: 397€ seulement!

                💥 ÉCONOMISEZ 1,147€ (74% de réduction) 💥

                VOUS OBTENEZ ABSOLUMENT TOUT:

                📚 Formation PREMIUM (valeur: 997€)
                🔧 Accès diagnostic 1 AN (valeur: 564€ = 47€×12)
                🎯 Coaching privé 1h avec expert (valeur: 197€)
                🎁 Tous les bonus (valeur: 394€)

                ⚡ EN PLUS: GARANTIE RÉSULTATS ⚡
                Si vous ne gagnez pas au moins 2,000€ supplémentaires
                dans les 90 jours, on vous rembourse ET vous gardez tout!

                C'est notre garantie béton. Zéro risque pour vous.

                🎖️ RÉSERVÉ AUX PROFESSIONNELS AMBITIEUX:
                Cette offre est pour les mécaniciens qui veulent:
                ✓ Dominer leur marché local
                ✓ Doubler leur CA dans l'année
                ✓ Être reconnus comme experts
                ✓ Travailler avec les clients premium

                👥 Seulement 50 packs disponibles à ce prix
                📊 Déjà 34 vendus cette semaine
                ⏰ Offre expire: 23h47min

                ⚠️ Ce prix ne reviendra JAMAIS!

                Cliquez maintenant avant que les 16 places restantes partent...
                """
            )
        }
        return products

    def _load_data(self):
        """Charge les données clients et commandes"""
        # Charger clients
        if os.path.exists(self.customers_file):
            with open(self.customers_file, 'r', encoding='utf-8') as f:
                self.customers = json.load(f)
        else:
            self.customers = {}

        # Charger commandes
        if os.path.exists(self.orders_file):
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                self.orders = json.load(f)
        else:
            self.orders = {}

    def _save_data(self):
        """Sauvegarde les données"""
        with open(self.customers_file, 'w', encoding='utf-8') as f:
            json.dump(self.customers, f, indent=2, ensure_ascii=False)

        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, indent=2, ensure_ascii=False)

    def create_customer(self, email: str, name: str, phone: Optional[str] = None) -> Customer:
        """Crée un nouveau client"""
        customer_id = str(uuid.uuid4())
        customer = Customer(
            id=customer_id,
            email=email,
            name=name,
            phone=phone,
            created_at=datetime.now().isoformat(),
            total_spent=0.0,
            purchase_count=0,
            is_premium=False
        )

        self.customers[customer_id] = asdict(customer)
        self._save_data()

        return customer

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Récupère un client par email"""
        for customer_data in self.customers.values():
            if customer_data['email'] == email:
                return Customer(**customer_data)
        return None

    def create_order(
        self,
        customer_id: str,
        product_id: str,
        payment_method: str = "stripe"
    ) -> Order:
        """Crée une nouvelle commande"""
        if product_id not in self.products:
            raise ValueError(f"Produit {product_id} inconnu")

        product = self.products[product_id]
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        order = Order(
            id=order_id,
            customer_id=customer_id,
            product_id=product_id,
            amount=product.price,
            status="pending",
            payment_method=payment_method,
            created_at=datetime.now().isoformat(),
            completed_at=None,
            pdf_generated=False,
            pdf_sent=False,
            pdf_path=None
        )

        self.orders[order_id] = asdict(order)
        self._save_data()

        return order

    def complete_order(self, order_id: str) -> Order:
        """Marque une commande comme complétée"""
        if order_id not in self.orders:
            raise ValueError(f"Commande {order_id} introuvable")

        order_data = self.orders[order_id]
        order_data['status'] = 'completed'
        order_data['completed_at'] = datetime.now().isoformat()

        # Mettre à jour le client
        customer_data = self.customers[order_data['customer_id']]
        customer_data['total_spent'] += order_data['amount']
        customer_data['purchase_count'] += 1

        # Vérifier si upgrade vers premium
        product_type = self.products[order_data['product_id']].product_type
        if product_type in [ProductType.FORMATION_PREMIUM, ProductType.FULL_BUNDLE]:
            customer_data['is_premium'] = True

        self._save_data()

        return Order(**order_data)

    def update_order_pdf(self, order_id: str, pdf_path: str):
        """Met à jour le chemin du PDF généré"""
        if order_id not in self.orders:
            raise ValueError(f"Commande {order_id} introuvable")

        self.orders[order_id]['pdf_generated'] = True
        self.orders[order_id]['pdf_path'] = pdf_path
        self._save_data()

    def mark_pdf_sent(self, order_id: str):
        """Marque le PDF comme envoyé"""
        if order_id not in self.orders:
            raise ValueError(f"Commande {order_id} introuvable")

        self.orders[order_id]['pdf_sent'] = True
        self._save_data()

    def get_pending_pdf_orders(self) -> List[Order]:
        """Récupère les commandes complétées sans PDF envoyé"""
        pending_orders = []
        for order_data in self.orders.values():
            if (order_data['status'] == 'completed' and
                not order_data['pdf_sent']):
                pending_orders.append(Order(**order_data))
        return pending_orders

    def get_upsell_candidates(self, days: int = 3) -> List[tuple[Customer, Order]]:
        """
        Identifie les clients pour upsell
        (achat basic récent mais pas premium)
        """
        candidates = []
        cutoff_date = datetime.now() - timedelta(days=days)

        for order_data in self.orders.values():
            if order_data['status'] != 'completed':
                continue

            # Vérifier si achat basic récent
            order_date = datetime.fromisoformat(order_data['created_at'])
            if order_date < cutoff_date:
                continue

            # Vérifier si pas déjà premium
            customer_data = self.customers[order_data['customer_id']]
            if customer_data['is_premium']:
                continue

            # Vérifier si produit basic
            product_type = self.products[order_data['product_id']].product_type
            if product_type == ProductType.FORMATION_BASIC:
                candidates.append((
                    Customer(**customer_data),
                    Order(**order_data)
                ))

        return candidates

    def get_customer_stats(self) -> Dict:
        """Statistiques globales"""
        total_revenue = sum(
            order['amount']
            for order in self.orders.values()
            if order['status'] == 'completed'
        )

        completed_orders = sum(
            1 for order in self.orders.values()
            if order['status'] == 'completed'
        )

        premium_customers = sum(
            1 for customer in self.customers.values()
            if customer['is_premium']
        )

        return {
            'total_customers': len(self.customers),
            'total_orders': len(self.orders),
            'completed_orders': completed_orders,
            'total_revenue': total_revenue,
            'premium_customers': premium_customers,
            'conversion_rate': (completed_orders / len(self.orders) * 100)
                if self.orders else 0,
            'average_order_value': (total_revenue / completed_orders)
                if completed_orders > 0 else 0
        }
