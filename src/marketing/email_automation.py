"""
Système d'automatisation email marketing
Envoi automatique de PDF après achat + séquences de relance
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional
import os
from datetime import datetime


class EmailMarketingSystem:
    """Gestion des emails automatiques et séquences marketing"""

    def __init__(
        self,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 587,
        sender_email: str = "",
        sender_password: str = "",
        sender_name: str = "MecaClair Diag"
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name

    def send_email(
        self,
        recipient_email: str,
        recipient_name: str,
        subject: str,
        html_body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Envoie un email avec pièces jointes optionnelles"""
        try:
            # Créer le message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Corps HTML
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)

            # Ajouter les pièces jointes
            if attachments:
                for filepath in attachments:
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            attach = MIMEApplication(f.read(), _subtype="pdf")
                            attach.add_header(
                                'Content-Disposition',
                                'attachment',
                                filename=os.path.basename(filepath)
                            )
                            msg.attach(attach)

            # Envoyer l'email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.sender_email and self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False

    def send_purchase_confirmation(
        self,
        customer_email: str,
        customer_name: str,
        product_name: str,
        order_id: str,
        pdf_path: str,
        amount: float
    ) -> bool:
        """Email de confirmation d'achat avec PDF en pièce jointe"""

        subject = f"🎉 {customer_name}, votre formation est prête! [Commande #{order_id}]"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border: 1px solid #ddd;
                }}
                .cta-button {{
                    display: inline-block;
                    background: #FF6600;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .highlight {{
                    background: #FFF3CD;
                    border-left: 4px solid #FFC107;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    background: #333;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    border-radius: 0 0 10px 10px;
                }}
                ul {{
                    list-style: none;
                    padding: 0;
                }}
                ul li:before {{
                    content: "✅ ";
                    color: #28a745;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 FÉLICITATIONS {customer_name.upper()}!</h1>
                <p>Vous avez fait le meilleur investissement pour votre carrière</p>
            </div>

            <div class="content">
                <h2>Votre commande est confirmée ✅</h2>

                <p><strong>Numéro de commande:</strong> #{order_id}<br/>
                <strong>Date:</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}<br/>
                <strong>Formation:</strong> {product_name}<br/>
                <strong>Montant:</strong> {amount}€</p>

                <div class="highlight">
                    <h3>📎 VOTRE FORMATION EST EN PIÈCE JOINTE!</h3>
                    <p>Vous trouverez votre PDF de formation directement attaché à cet email.
                    <strong>Téléchargez-le maintenant</strong> et commencez immédiatement!</p>
                </div>

                <h3>🎯 Les prochaines étapes:</h3>
                <ul>
                    <li>Téléchargez le PDF (pièce jointe ci-dessus)</li>
                    <li>Imprimez-le ou consultez-le sur tablette</li>
                    <li>Commencez à diagnostiquer plus rapidement DÈS AUJOURD'HUI</li>
                    <li>Appliquez les méthodes sur votre prochain client</li>
                </ul>

                <h3>💎 Vous voulez aller encore PLUS LOIN?</h3>
                <p>Vous avez fait le premier pas, bravo! Mais saviez-vous que les mécaniciens
                qui passent à la version <strong>PREMIUM</strong> gagnent en moyenne
                <strong>5,200€ de plus par an?</strong></p>

                <a href="https://mecaclair-diag.com/upgrade?order={order_id}" class="cta-button">
                    🔥 UPGRADER VERS PREMIUM (-60% pour vous!)
                </a>

                <p style="font-size: 14px; color: #666;">
                    <em>Cette offre spéciale expire dans 48h. C'est maintenant ou jamais.</em>
                </p>

                <h3>❓ Questions?</h3>
                <p>Répondez simplement à cet email, notre équipe vous répondra en moins de 2h!</p>

                <p style="margin-top: 30px;">
                    <strong>Merci de votre confiance,</strong><br/>
                    L'équipe MecaClair Diag 🔧
                </p>
            </div>

            <div class="footer">
                <p>MecaClair Diag - Formation professionnelle en diagnostic automobile</p>
                <p>support@mecaclair-diag.com | Tel: +33 X XX XX XX XX</p>
                <p style="font-size: 10px; margin-top: 10px;">
                    Vous recevez cet email car vous avez acheté une formation sur notre site.<br/>
                    Garantie satisfait ou remboursé 30 jours.
                </p>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            recipient_email=customer_email,
            recipient_name=customer_name,
            subject=subject,
            html_body=html_body,
            attachments=[pdf_path] if pdf_path else None
        )

    def send_upsell_email_day1(
        self,
        customer_email: str,
        customer_name: str,
        original_product: str
    ) -> bool:
        """Email de relance J+1 - Soft upsell"""

        subject = f"{customer_name}, comment se passe votre formation?"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px;
                    background: #fff;
                }}
                .cta-button {{
                    display: inline-block;
                    background: #FF6600;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>👋 Bonjour {customer_name}!</h2>
            </div>

            <div class="content">
                <p>J'espère que vous avez pu consulter votre formation <strong>"{original_product}"</strong>!</p>

                <p>J'ai une question rapide: <strong>Avez-vous déjà pu l'utiliser sur un client?</strong></p>

                <p>Si oui, j'adorerais connaître vos résultats! Répondez simplement à cet email.</p>

                <p>Et si vous voulez aller <strong>encore plus vite</strong>, j'ai quelque chose pour vous...</p>

                <h3>🚀 Passez à la vitesse supérieure</h3>

                <p>La plupart de nos clients qui obtiennent les <strong>meilleurs résultats</strong>
                ont tous un point commun: ils sont passés à la version <strong>PREMIUM</strong>.</p>

                <p><strong>Pourquoi?</strong> Parce qu'ils ont accès:</p>
                <ul>
                    <li>✅ Aux mises à jour <strong>chaque semaine</strong> (vs tous les 3 mois)</li>
                    <li>✅ Au support prioritaire <strong>24/7</strong></li>
                    <li>✅ À la communauté privée de 500+ experts</li>
                    <li>✅ Aux templates qui automatisent leur travail</li>
                </ul>

                <p><strong>Résultat:</strong> Ils gagnent 2x à 3x plus que ceux qui restent en version basic.</p>

                <p>Comme vous êtes déjà client, je vous offre <strong>-60% sur l'upgrade</strong>
                (au lieu de -40% pour le grand public).</p>

                <a href="https://mecaclair-diag.com/upgrade-vip" class="cta-button">
                    Voir l'offre PREMIUM (-60%)
                </a>

                <p style="font-size: 14px; color: #666;">
                    <em>Cette réduction est valable uniquement pour vous, pendant 48h.</em>
                </p>

                <p>À très vite,<br/>
                <strong>Pierre</strong><br/>
                Fondateur, MecaClair Diag</p>

                <p style="font-size: 12px; color: #999; margin-top: 30px;">
                    PS: Si vous ne souhaitez plus recevoir ces offres spéciales,
                    <a href="#">cliquez ici</a>.
                </p>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            recipient_email=customer_email,
            recipient_name=customer_name,
            subject=subject,
            html_body=html_body
        )

    def send_upsell_email_day3(
        self,
        customer_email: str,
        customer_name: str
    ) -> bool:
        """Email de relance J+3 - Upsell agressif avec urgence"""

        subject = f"⚠️ {customer_name}, cette offre expire ce soir à minuit"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .urgent {{
                    background: #FF0000;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                }}
                .content {{
                    padding: 30px;
                    background: #fff;
                }}
                .countdown {{
                    background: #FFF3CD;
                    border: 3px solid #FFC107;
                    padding: 20px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    color: #CC0000;
                    margin: 20px 0;
                }}
                .cta-button {{
                    display: block;
                    background: #FF6600;
                    color: white;
                    padding: 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 18px;
                    text-align: center;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="urgent">
                ⏰ DERNIÈRES HEURES - OFFRE EXPIRE CE SOIR À MINUIT
            </div>

            <div class="content">
                <p>Bonjour {customer_name},</p>

                <p>Je vais être <strong>100% direct avec vous</strong>...</p>

                <p>Il vous reste <strong>moins de 12 heures</strong> pour profiter de la réduction
                de -60% sur l'upgrade PREMIUM.</p>

                <div class="countdown">
                    ⏰ EXPIRE DANS: 11h 47min
                </div>

                <p><strong>Pourquoi je vous envoie cet email?</strong></p>

                <p>Parce que je sais que vous avez du potentiel. Vous avez déjà investi dans votre
                formation, ce qui prouve que vous êtes <strong>différent</strong> des autres mécaniciens.</p>

                <p>Mais voilà la vérité que personne ne vous dira:</p>

                <blockquote style="border-left: 4px solid #CC0000; padding-left: 20px; font-style: italic;">
                    "Les mécaniciens qui restent en version basic gagnent en moyenne 28,000€/an.
                    Ceux qui passent PREMIUM gagnent 44,000€/an."
                </blockquote>

                <p><strong>C'est 16,000€ de différence par an.</strong></p>

                <p>Sur 5 ans, ça fait <strong>80,000€</strong> que vous laissez sur la table.</p>

                <p>Pour un simple upgrade à 147€ (au lieu de 297€).</p>

                <p><strong>Franchement, est-ce que ça vaut le coup d'hésiter?</strong></p>

                <a href="https://mecaclair-diag.com/upgrade-last-chance" class="cta-button">
                    🔥 OUI, JE VEUX GAGNER 16,000€ DE PLUS PAR AN
                </a>

                <p style="background: #E8F5E9; padding: 15px; border-radius: 5px;">
                    <strong>🎁 BONUS SPÉCIAL si vous cliquez maintenant:</strong><br/>
                    En plus de tout le reste, je vous offre gratuitement la formation
                    "Comment facturer 50% plus cher" (valeur: 97€).<br/>
                    <em>Mais seulement si vous passez commande dans les 12 prochaines heures.</em>
                </p>

                <p><strong>C'est votre choix:</strong></p>
                <ul>
                    <li>❌ Rester là où vous êtes et regarder vos concurrents vous dépasser</li>
                    <li>✅ Saisir cette opportunité et rejoindre l'élite des mécaniciens</li>
                </ul>

                <p>À vous de décider.</p>

                <p>Cordialement,<br/>
                <strong>Pierre</strong><br/>
                Fondateur, MecaClair Diag</p>

                <p style="font-size: 12px; color: #999; margin-top: 40px;">
                    PS: Cette offre ne reviendra PAS. Une fois expiré, le prix remontera à 297€.
                    Ne le regrettez pas dans 6 mois...
                </p>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            recipient_email=customer_email,
            recipient_name=customer_name,
            subject=subject,
            html_body=html_body
        )

    def send_abandonment_email(
        self,
        customer_email: str,
        customer_name: str,
        cart_product: str,
        cart_amount: float
    ) -> bool:
        """Email de panier abandonné (récupération de vente)"""

        subject = f"😢 {customer_name}, vous avez oublié quelque chose..."

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background: #2196F3;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px;
                    background: #fff;
                }}
                .product-box {{
                    background: #f9f9f9;
                    border: 2px solid #ddd;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .discount {{
                    background: #4CAF50;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .cta-button {{
                    display: block;
                    background: #FF6600;
                    color: white;
                    padding: 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 18px;
                    text-align: center;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Votre formation vous attend... 📚</h2>
            </div>

            <div class="content">
                <p>Bonjour {customer_name},</p>

                <p>J'ai remarqué que vous étiez sur le point de vous inscrire à notre formation,
                mais que vous n'avez pas finalisé votre commande.</p>

                <div class="product-box">
                    <h3>{cart_product}</h3>
                    <p style="font-size: 24px; color: #2196F3;">
                        <strong>{cart_amount}€</strong>
                    </p>
                </div>

                <p><strong>Qu'est-ce qui vous a arrêté?</strong></p>

                <ul>
                    <li>❓ Le prix vous semble élevé?</li>
                    <li>❓ Vous avez des doutes sur la qualité?</li>
                    <li>❓ Ce n'est pas le bon moment?</li>
                </ul>

                <p>Je comprends. C'est pour ça que je veux vous aider...</p>

                <div class="discount">
                    🎁 CODE PROMO SPÉCIAL: -15€ sur votre commande<br/>
                    Code: <strong>RETOUR15</strong>
                </div>

                <p><strong>Mais ce n'est pas tout!</strong></p>

                <p>Si vous finalisez votre commande dans les prochaines 24h, je vous offre
                <strong>gratuitement</strong> l'ebook "Les 10 Erreurs à Éviter en Diagnostic" (valeur: 27€).</p>

                <a href="https://mecaclair-diag.com/checkout?recover=true" class="cta-button">
                    Finaliser ma commande (avec -15€)
                </a>

                <p style="background: #E3F2FD; padding: 15px; border-radius: 5px;">
                    <strong>💬 Vous avez des questions?</strong><br/>
                    Répondez simplement à cet email, je vous répondrai personnellement
                    dans l'heure qui suit!
                </p>

                <p>À très bientôt j'espère,<br/>
                <strong>Pierre</strong><br/>
                Fondateur, MecaClair Diag</p>

                <p style="font-size: 11px; color: #999; margin-top: 30px;">
                    Le code promo RETOUR15 expire dans 24h et ne peut être utilisé qu'une seule fois.
                </p>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            recipient_email=customer_email,
            recipient_name=customer_name,
            subject=subject,
            html_body=html_body
        )

    def send_testimonial_request(
        self,
        customer_email: str,
        customer_name: str,
        days_since_purchase: int
    ) -> bool:
        """Demande de témoignage (preuve sociale + engagement)"""

        subject = f"{customer_name}, puis-je vous demander une faveur?"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .content {{
                    padding: 30px;
                    background: #fff;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <p>Bonjour {customer_name},</p>

                <p>Ça fait maintenant {days_since_purchase} jours que vous utilisez notre formation.</p>

                <p>J'ai une question simple: <strong>Est-ce que ça vous a aidé?</strong></p>

                <p>Si oui, j'aimerais vous demander un petit service...</p>

                <p><strong>Pourriez-vous partager votre expérience en 2-3 phrases?</strong></p>

                <p>Ça aiderait énormément d'autres mécaniciens qui hésitent encore à se former.</p>

                <p>Répondez simplement à cet email avec:</p>
                <ul>
                    <li>✅ Ce que vous avez le plus apprécié</li>
                    <li>✅ Les résultats que vous avez obtenus</li>
                    <li>✅ Votre recommandation (si vous en avez une!)</li>
                </ul>

                <p><strong>En échange</strong>, je vous offrirai accès gratuit à notre
                prochaine formation bonus (valeur: 47€) dès sa sortie!</p>

                <p>Merci d'avance,<br/>
                <strong>Pierre</strong></p>

                <p style="font-size: 12px; color: #999; margin-top: 30px;">
                    Votre témoignage pourrait changer la carrière d'un autre mécanicien.
                    Merci de prendre 2 minutes! 🙏
                </p>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            recipient_email=customer_email,
            recipient_name=customer_name,
            subject=subject,
            html_body=html_body
        )
