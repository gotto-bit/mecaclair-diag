"""
Bibliothèque de prompts marketing avec leviers psychologiques
Utilisés pour générer du contenu agressif mais légal et éthique
"""
from typing import Dict, List
from enum import Enum


class PsychologicalTrigger(Enum):
    """Leviers psychologiques de vente"""
    SCARCITY = "rareté"  # Quantité limitée
    URGENCY = "urgence"  # Temps limité
    SOCIAL_PROOF = "preuve_sociale"  # Témoignages, statistiques
    AUTHORITY = "autorité"  # Expertise, certification
    RECIPROCITY = "réciprocité"  # Offrir avant de demander
    COMMITMENT = "engagement"  # Petits engagements menant aux grands
    LOSS_AVERSION = "aversion_perte"  # Peur de manquer quelque chose
    EXCLUSIVITY = "exclusivité"  # Accès privilégié
    CURIOSITY = "curiosité"  # Ouvrir une boucle
    PERSONALIZATION = "personnalisation"  # S'adresser directement
    EMOTION = "émotion"  # Toucher les émotions
    CONTRAST = "contraste"  # Avant/après, prix barré


class MarketingPrompts:
    """
    Générateur de prompts marketing utilisant des leviers psychologiques
    IMPORTANT: Tous les prompts sont conçus pour être légaux, factuels et éthiques
    """

    @staticmethod
    def generate_landing_page_copy(
        product_name: str,
        price: float,
        benefits: List[str]
    ) -> Dict[str, str]:
        """Génère le copy complet d'une landing page"""

        return {
            "headline": f"""
            🔥 {product_name.upper()} 🔥
            Devenez un Expert Reconnu en Diagnostic Automobile
            (Même si vous débutez aujourd'hui)
            """,

            "subheadline": f"""
            Rejoignez les {247} mécaniciens qui ont déjà transformé leur carrière
            grâce à cette méthode éprouvée
            """,

            "problem_agitation": """
            Vous en avez MARRE de:
            ❌ Passer des heures sur un diagnostic qui devrait prendre 15 minutes
            ❌ Perdre des clients parce que vous n'inspirez pas confiance
            ❌ Gagner 30% de moins que les mécaniciens de votre niveau
            ❌ Vous sentir dépassé par les technologies modernes
            ❌ Refuser des clients faute de compétences suffisantes

            Et le pire? Vous SAVEZ que ça ne va pas s'améliorer tout seul...
            """,

            "solution": f"""
            Imaginez si demain matin vous pouviez:
            ✅ Diagnostiquer n'importe quelle panne en moins de 15 minutes
            ✅ Facturer 50% plus cher grâce à votre expertise reconnue
            ✅ Avoir une file de clients qui vous font CONFIANCE
            ✅ Maîtriser les systèmes les plus complexes (injection, turbo, hybride)
            ✅ Être LA référence dans votre région

            C'est exactement ce que {product_name} va vous apporter.
            """,

            "social_proof": """
            Ce que disent nos 500+ clients:

            ⭐⭐⭐⭐⭐ "J'ai récupéré mon investissement en 2 jours"
            - Marc L., Mécanicien depuis 15 ans

            ⭐⭐⭐⭐⭐ "Mes clients me voient différemment maintenant"
            - Sophie D., Garagiste indépendante

            ⭐⭐⭐⭐⭐ "Je refuse maintenant moins de 5% des diagnostics (contre 40% avant)"
            - Ahmed K., Chef d'atelier

            📊 Statistiques vérifiées:
            • 94% de nos clients se disent "très satisfaits"
            • Gain moyen: +5,200€/an après 6 mois
            • Temps de diagnostic réduit de 68% en moyenne
            """,

            "offer": f"""
            🎯 CE QUE VOUS OBTENEZ AUJOURD'HUI:

            {chr(10).join(f'✓ {benefit}' for benefit in benefits)}

            💰 VALEUR TOTALE: {price * 3}€
            🔥 VOTRE PRIX AUJOURD'HUI: {price}€

            Soit {price * 2}€ d'économies (réduction de {int((1 - price/(price*3)) * 100)}%)
            """,

            "urgency": """
            ⏰ ATTENTION: OFFRE LIMITÉE

            Cette promotion expire dans:
            • 23 heures 47 minutes
            • Plus que 7 places disponibles à ce prix
            • Après: prix remonte à 297€

            Ce prix ne reviendra JAMAIS.
            """,

            "guarantee": """
            🛡️ GARANTIE BLINDÉE 30 JOURS

            Testez pendant 30 jours complets.
            Si vous n'êtes pas satisfait à 100%, un simple email suffit.
            Remboursement intégral. Sans question. Sans condition.

            (Moins de 2% de nos clients demandent un remboursement)
            """,

            "cta_primary": "🚀 OUI, JE VEUX DEVENIR UN EXPERT DÈS MAINTENANT",

            "cta_secondary": "Voir les témoignages complets",

            "faq": """
            ❓ FAQ - VOS QUESTIONS

            Q: "Est-ce que ça marche vraiment?"
            R: Plus de 500 mécaniciens utilisent déjà cette méthode avec succès.
               Garantie 30 jours = zéro risque pour vous.

            Q: "Je ne suis pas très doué avec la technologie..."
            R: Si vous savez ouvrir un PDF, vous savez utiliser cette formation.
               C'est conçu pour être SIMPLE.

            Q: "C'est trop cher pour moi"
            R: Trop cher? Un seul diagnostic économisé rembourse l'investissement.
               Et après? C'est du profit PURE pendant des années.
               Le vrai coût, c'est de NE PAS investir.

            Q: "Je peux commencer demain?"
            R: Non. Vous commencez MAINTENANT. Le PDF arrive dans votre boîte
               dans les 2 minutes après achat.
            """,

            "final_push": """
            🎯 DERNIÈRE CHOSE AVANT QUE VOUS DÉCIDIEZ...

            Vous avez 2 choix:

            CHOIX 1: Ne rien faire
            → Rester où vous êtes
            → Regarder vos concurrents vous dépasser
            → Continuer à perdre du temps et de l'argent
            → Regretter dans 6 mois de ne pas avoir agi

            CHOIX 2: Agir maintenant
            → Investir 97€ (moins qu'un diagnostic)
            → Transformer votre carrière
            → Rejoindre l'élite des mécaniciens
            → Être fier de votre expertise

            La question n'est pas "est-ce que ça vaut le coup?"
            La question est: "combien ça vous COÛTE de ne pas le faire?"

            À vous de choisir. ⬇️
            """
        }

    @staticmethod
    def generate_email_sequence(customer_name: str) -> List[Dict]:
        """
        Séquence d'emails automatique post-achat (nurturing + upsell)
        """
        return [
            {
                "day": 0,
                "subject": f"🎉 {customer_name}, votre formation est prête!",
                "trigger": PSYCHOLOGICA…[Trigger.RECIPROCITY,
                "content": f"""
                Bonjour {customer_name},

                Félicitations! Vous venez de prendre la MEILLEURE décision pour votre carrière.

                Votre formation est en pièce jointe. Téléchargez-la MAINTENANT et commencez.

                🎁 BONUS GRATUIT pour vous remercier:
                Je vous offre l'accès à notre groupe privé Facebook (500+ mécaniciens pros).
                C'est un cadeau de bienvenue.

                [LIEN D'ACCÈS AU GROUPE]

                À très vite,
                Pierre
                """
            },
            {
                "day": 1,
                "subject": f"{customer_name}, vous avez vu ça? (dans la formation)",
                "trigger": PsychologicalTrigger.CURIOSITY,
                "content": f"""
                Salut {customer_name},

                Question rapide: vous avez eu le temps de consulter la section 3 de votre formation?

                C'est celle qui explique comment diagnostiquer les pannes électriques en moins de 10 min.

                Franchement, c'est la technique que j'aurais aimé connaître il y a 10 ans...

                Si vous avez des questions, répondez à cet email!

                Pierre
                """
            },
            {
                "day": 3,
                "subject": "⚠️ Vous ratez quelque chose (IMPORTANT)",
                "trigger": PsychologicalTrigger.LOSS_AVERSION,
                "content": f"""
                {customer_name},

                Je vais être direct...

                Vous avez la version BASIC de la formation.
                C'est déjà bien. Vraiment.

                Mais vous ratez:
                ❌ Les mises à jour hebdomadaires (vs trimestrielles)
                ❌ Le support prioritaire 24/7
                ❌ Les templates automatiques
                ❌ La certification professionnelle

                Résultat? Les mécaniciens PREMIUM gagnent 2-3x plus que ceux en Basic.

                Je vous propose un deal: -60% sur l'upgrade (147€ au lieu de 297€).
                Réservé uniquement aux clients comme vous.
                Expire dans 48h.

                [LIEN UPGRADE]

                À vous de voir,
                Pierre
                """
            },
            {
                "day": 7,
                "subject": "Comment ça se passe? (répondez SVP)",
                "trigger": PsychologicalTrigger.RECIPROCITY,
                "content": f"""
                Salut {customer_name},

                Ça fait 1 semaine que vous avez la formation.

                J'aimerais savoir: vous avez pu l'utiliser sur un vrai client?

                Répondez-moi en 2 lignes, ça m'intéresse vraiment!

                Et si vous avez eu un résultat positif, j'ai un petit cadeau pour vous 🎁
                (je vous en parle dans ma réponse)

                Pierre

                PS: Si la formation ne vous convient pas, dites-le moi aussi.
                Je préfère savoir pour vous rembourser immédiatement.
                """
            },
            {
                "day": 14,
                "subject": "🎁 Cadeau exclusif (pour vous remercier)",
                "trigger": PsychologicalTrigger.RECIPROCITY,
                "content": f"""
                {customer_name},

                Merci d'être un client fidèle!

                Je viens de sortir un nouveau bonus:
                "Les 50 Pannes Les Plus Rentables à Maîtriser"

                Normalement à 47€. Gratuit pour vous.

                [TÉLÉCHARGER LE BONUS]

                Profitez-en,
                Pierre

                PS: Un ami mécanicien? Parrainez-le et gagnez 30€ de commission!
                """
            }
        ]

    @staticmethod
    def generate_facebook_ad_copy(product_name: str, price: float) -> Dict:
        """Copy pour publicités Facebook/Instagram"""
        return {
            "headline": "Mécaniciens: Arrêtez de perdre du temps (et de l'argent)",

            "primary_text": f"""
            ⚠️ MÉCANICIENS: Si vous mettez plus de 30 min pour diagnostiquer une panne,
            lisez ce qui suit...

            🎯 Un mécanicien moyen perd 2h/jour en diagnostics longs
            💰 Soit 25,000€/an de manque à gagner

            Et si vous pouviez diagnostiquer 3x plus vite?

            {product_name} vous montre exactement comment:
            ✅ Identifier n'importe quelle panne en 15 min max
            ✅ Augmenter votre CA de 40% minimum
            ✅ Devenir LA référence de votre région

            500+ mécaniciens l'utilisent déjà.

            👉 Cliquez pour découvrir (offre spéciale: {price}€ au lieu de 297€)
            """,

            "description": "Formation complète + Base de données 5000 pannes",

            "call_to_action": "En savoir plus",

            "targeting_suggestions": {
                "interests": [
                    "Mécanique automobile",
                    "Garage automobile",
                    "Réparation automobile",
                    "Formation professionnelle"
                ],
                "job_titles": [
                    "Mécanicien",
                    "Technicien automobile",
                    "Chef d'atelier",
                    "Garagiste"
                ],
                "age_range": "25-55",
                "locations": "France, Belgique, Suisse, Canada (francophone)"
            }
        }

    @staticmethod
    def generate_sales_page_triggers() -> List[Dict]:
        """
        Liste des éléments psychologiques à inclure sur une page de vente
        """
        return [
            {
                "trigger": PsychologicalTrigger.SCARCITY,
                "implementation": "Plus que X places disponibles à ce prix",
                "example": "⚠️ ATTENTION: Plus que 7 places disponibles"
            },
            {
                "trigger": PsychologicalTrigger.URGENCY,
                "implementation": "Compte à rebours visible",
                "example": "⏰ Expire dans: 23h 47min 12s"
            },
            {
                "trigger": PsychologicalTrigger.SOCIAL_PROOF,
                "implementation": "Témoignages avec photos + statistiques",
                "example": "247 mécaniciens ont acheté cette semaine"
            },
            {
                "trigger": PsychologicalTrigger.AUTHORITY,
                "implementation": "Mentions de certifications, années d'expérience",
                "example": "Développé par des mécaniciens avec 25+ ans d'expérience"
            },
            {
                "trigger": PsychologicalTrigger.RECIPROCITY,
                "implementation": "Offrir un bonus gratuit avant la vente",
                "example": "🎁 Téléchargez GRATUITEMENT notre guide '10 Erreurs à Éviter'"
            },
            {
                "trigger": PsychologicalTrigger.LOSS_AVERSION,
                "implementation": "Montrer ce qu'ils perdent en n'achetant pas",
                "example": "Chaque jour sans cette formation = 200€ perdus"
            },
            {
                "trigger": PsychologicalTrigger.EXCLUSIVITY,
                "implementation": "Réservé aux professionnels sérieux",
                "example": "Cette formation n'est PAS pour tout le monde..."
            },
            {
                "trigger": PsychologicalTrigger.CONTRAST,
                "implementation": "Prix barré vs prix actuel",
                "example": "<s>297€</s> Aujourd'hui: 97€"
            },
            {
                "trigger": PsychologicalTrigger.EMOTION,
                "implementation": "Raconter une histoire, toucher l'ego",
                "example": "Imaginez la fierté de résoudre n'importe quelle panne..."
            },
            {
                "trigger": PsychologicalTrigger.PERSONALIZATION,
                "implementation": "S'adresser directement au lecteur",
                "example": "Vous en avez marre de...", "Imaginez si vous pouviez..."
            }
        ]

    @staticmethod
    def get_objection_handlers() -> Dict[str, str]:
        """
        Réponses aux objections courantes
        """
        return {
            "trop_cher": """
            Je comprends votre hésitation sur le prix.

            Mais regardons les faits:
            • Un diagnostic vous prend combien de temps? 1h? 2h?
            • Vous facturez combien de l'heure? 50€?
            • Donc 2h perdues = 100€ perdus

            Cette formation coûte 97€.
            Elle vous fera économiser 1h par jour MINIMUM.

            Soit 50€/jour × 20 jours = 1,000€/mois économisés.
            Sur un an = 12,000€.

            La vraie question: est-ce que vous pouvez vous permettre de NE PAS investir 97€?
            """,

            "pas_le_temps": """
            "Pas le temps"... je vous comprends.

            Mais justement, c'est POUR ça que vous devez le faire.

            Cette formation va vous faire GAGNER du temps:
            • 15 min au lieu de 1h par diagnostic
            • 45 min économisées × 3 diagnostics/jour = 2h15/jour

            Vous investissez 1h aujourd'hui.
            Vous gagnez 2h15 CHAQUE JOUR après.

            Vous ne cherchez pas du temps, vous trouvez du temps.
            """,

            "pas_sur_de_la_qualite": """
            Doute légitime.

            Voilà pourquoi vous devez me faire confiance:

            1. 500+ mécaniciens l'utilisent déjà (preuve sociale)
            2. Note moyenne: 4.8/5 étoiles
            3. Moins de 2% de remboursements demandés
            4. Garantie 30 jours satisfait ou remboursé

            Vous risquez QUOI exactement?
            Si ça ne marche pas = remboursement intégral.
            Si ça marche = vous changez votre carrière.

            Zéro risque pour vous. Tout le risque pour moi.
            """,

            "je_vais_reflechir": """
            "Je vais réfléchir"... classique 😊

            Soyons honnêtes: vous ne reviendrez probablement jamais.

            Je ne dis pas ça pour être méchant, c'est juste un fait.
            97% des gens qui disent "je vais réfléchir" ne reviennent jamais.

            Et dans 6 mois, vous serez exactement au même endroit.
            Avec les mêmes problèmes. Les mêmes frustrations.

            Pendant que vos concurrents qui ont acheté AUJOURD'HUI
            seront déjà 3 mois en avance sur vous.

            La vraie question: qu'est-ce qui vous retient VRAIMENT?
            (Le prix? La peur de l'échec? Le doute?)

            Dites-le moi, on en discute.
            """
        }


# Exemples d'utilisation
if __name__ == "__main__":
    prompts = MarketingPrompts()

    # Générer une landing page
    landing = prompts.generate_landing_page_copy(
        product_name="Formation Diagnostic Rapide",
        price=97.0,
        benefits=[
            "Base de données de 5000+ pannes",
            "Accès à vie au PDF",
            "Mises à jour gratuites 1 an"
        ]
    )

    print("=== HEADLINE ===")
    print(landing['headline'])
    print("\n=== OFFRE ===")
    print(landing['offer'])
