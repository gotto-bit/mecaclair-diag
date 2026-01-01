"""
Générateur de PDF de formation avec templates marketing agressifs
Utilise des leviers psychologiques tout en restant éthique et légal
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime
import os
from typing import Dict, List


class PDFFormationGenerator:
    """Générateur de PDF de formation sur le diagnostic automobile"""

    def __init__(self, output_dir: str = "data/pdfs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configure les styles personnalisés pour le marketing"""
        # Style titre principal (impact psychologique fort)
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FF0000'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Style pour les call-to-action
        self.styles.add(ParagraphStyle(
            name='CTA',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#FF6600'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#FFFF99')
        ))

        # Style pour les bénéfices (liste à puces marketing)
        self.styles.add(ParagraphStyle(
            name='Benefit',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#006600'),
            spaceAfter=10,
            leftIndent=20,
            fontName='Helvetica-Bold'
        ))

        # Style pour l'urgence
        self.styles.add(ParagraphStyle(
            name='Urgency',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#CC0000'),
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

    def generate_diagnostic_training_pdf(
        self,
        title: str,
        customer_name: str,
        symptoms_data: List[Dict],
        price: float,
        order_id: str
    ) -> str:
        """
        Génère un PDF de formation personnalisé

        Args:
            title: Titre de la formation
            customer_name: Nom du client (personnalisation)
            symptoms_data: Données des symptômes et diagnostics
            price: Prix payé (preuve de valeur)
            order_id: ID de commande

        Returns:
            Chemin du PDF généré
        """
        filename = f"{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []

        # PAGE DE GARDE - IMPACT PSYCHOLOGIQUE MAXIMUM
        story.append(Spacer(1, 1*inch))

        # Titre accrocheur avec urgence
        title_text = f"🔥 {title.upper()} 🔥"
        story.append(Paragraph(title_text, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Personnalisation (levier: reconnaissance)
        personalization = f"<b>Formation exclusive pour : {customer_name}</b>"
        story.append(Paragraph(personalization, self.styles['CTA']))
        story.append(Spacer(1, 0.5*inch))

        # Preuve de valeur (levier: justification d'achat)
        value_proof = f"""
        <b>Investissement réalisé: {price}€</b><br/>
        Valeur réelle de cette formation: {price * 3}€<br/>
        <i>Vous économisez {price * 2}€ grâce à cette offre exclusive!</i>
        """
        story.append(Paragraph(value_proof, self.styles['Urgency']))
        story.append(Spacer(1, 0.3*inch))

        # Exclusivité et rareté (levier psychologique fort)
        exclusivity = """
        ⚠️ <b>ATTENTION: Document confidentiel</b> ⚠️<br/>
        Cette formation est réservée aux professionnels qui ont pris
        la décision d'investir dans leur avenir.<br/>
        Seulement 3% des mécaniciens possèdent ces informations.
        """
        story.append(Paragraph(exclusivity, self.styles['Urgency']))

        story.append(PageBreak())

        # PAGE 2 - BÉNÉFICES CONCRETS
        benefits_title = "<b>CE QUE VOUS ALLEZ MAÎTRISER DÈS AUJOURD'HUI:</b>"
        story.append(Paragraph(benefits_title, self.styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))

        benefits = [
            "✅ Diagnostiquer 10x plus rapidement n'importe quelle panne",
            "✅ Augmenter vos revenus de 40% en réduisant le temps de diagnostic",
            "✅ Devenir LA référence locale en diagnostic automobile",
            "✅ Fidéliser vos clients grâce à votre expertise reconnue",
            "✅ Économiser des milliers d'euros en évitant les erreurs de diagnostic",
            "✅ Accéder à une base de données de +5000 pannes référencées"
        ]

        for benefit in benefits:
            story.append(Paragraph(benefit, self.styles['Benefit']))
            story.append(Spacer(1, 0.1*inch))

        story.append(Spacer(1, 0.3*inch))

        # Urgence d'action (levier: FOMO)
        action_urgency = """
        <b>🚀 COMMENCEZ IMMÉDIATEMENT!</b><br/>
        Chaque minute passée sans ces connaissances vous coûte de l'argent.
        Vos concurrents qui ont cette formation diagnostiquent déjà plus vite que vous.
        """
        story.append(Paragraph(action_urgency, self.styles['CTA']))

        story.append(PageBreak())

        # CONTENU TECHNIQUE - DONNÉES DE SYMPTÔMES
        content_title = "<b>MODULE 1: BASE DE DONNÉES DIAGNOSTIQUE PROFESSIONNELLE</b>"
        story.append(Paragraph(content_title, self.styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))

        intro_text = """
        Cette section contient les données de diagnostic les plus recherchées
        par les professionnels. Ces informations valent leur pesant d'or et sont
        mises à jour régulièrement par notre système d'intelligence artificielle.
        """
        story.append(Paragraph(intro_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # Tableau des symptômes avec probabilités
        if symptoms_data:
            table_data = [['Symptôme', 'Cause Probable', 'Probabilité', 'Solution Rapide']]

            for symptom in symptoms_data[:20]:  # Top 20 symptômes
                table_data.append([
                    symptom.get('symptom', 'N/A'),
                    symptom.get('cause', 'N/A'),
                    f"{symptom.get('probability', 0):.0%}",
                    symptom.get('solution', 'N/A')
                ])

            table = Table(table_data, colWidths=[2*inch, 2*inch, 1*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))

            story.append(table)

        story.append(PageBreak())

        # PAGE FINALE - APPEL À L'ACTION ET UPSELL
        final_title = "<b>FÉLICITATIONS! VOUS ÊTES MAINTENANT UN EXPERT</b>"
        story.append(Paragraph(final_title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        congratulations = """
        Vous avez pris la meilleure décision pour votre carrière de mécanicien.
        <b>Mais ce n'est que le début...</b>
        """
        story.append(Paragraph(congratulations, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        # Upsell agressif mais légal
        upsell = """
        <b>🎁 OFFRE SPÉCIALE RÉSERVÉE AUX ACHETEURS:</b><br/><br/>

        Vous voulez aller encore plus loin?<br/><br/>

        <b>Formation PREMIUM disponible avec:</b><br/>
        ➤ Accès illimité à la base de données en temps réel<br/>
        ➤ Mises à jour automatiques chaque semaine<br/>
        ➤ Support prioritaire 24/7<br/>
        ➤ Certification professionnelle reconnue<br/>
        ➤ Communauté privée de 500+ experts<br/><br/>

        <b>Prix normal: 497€</b><br/>
        <b>Prix pour vous AUJOURD'HUI SEULEMENT: 197€</b><br/>
        <i>(60% de réduction - Offre expire dans 48h)</i><br/><br/>

        ⏰ <b>Cette offre ne reviendra jamais à ce prix!</b>
        """
        story.append(Paragraph(upsell, self.styles['CTA']))
        story.append(Spacer(1, 0.3*inch))

        # Garantie (levier: réduction du risque)
        guarantee = """
        <b>GARANTIE SATISFAIT OU REMBOURSÉ 30 JOURS</b><br/>
        Si vous n'êtes pas 100% satisfait, nous vous remboursons intégralement.
        Sans question. Sans condition. C'est notre engagement.
        """
        story.append(Paragraph(guarantee, self.styles['Benefit']))
        story.append(Spacer(1, 0.3*inch))

        # Contact et suivi
        footer = f"""
        <b>Informations de commande:</b><br/>
        Numéro: {order_id}<br/>
        Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>
        Client: {customer_name}<br/><br/>

        <i>Pour toute question: support@mecaclair-diag.com</i>
        """
        story.append(Paragraph(footer, self.styles['Normal']))

        # Génération du PDF
        doc.build(story)

        return filepath

    def generate_upsell_reminder_pdf(self, customer_name: str, original_purchase: str) -> str:
        """Génère un PDF de relance pour l'upsell (follow-up marketing)"""
        filename = f"upsell_{customer_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []

        story.append(Spacer(1, 1*inch))

        # Titre personnalisé
        title = f"🎯 {customer_name}, NE MANQUEZ PAS CETTE OPPORTUNITÉ!"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))

        # Rappel de l'achat initial (preuve sociale interne)
        reminder = f"""
        Vous avez déjà fait confiance à MecaClair Diag en achetant:<br/>
        <b>"{original_purchase}"</b><br/><br/>

        Vous faites partie des <b>3% de mécaniciens</b> qui investissent
        dans leur formation continue. Bravo!<br/><br/>

        Mais voici ce que vous ratez encore...
        """
        story.append(Paragraph(reminder, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # FOMO intensif
        fomo = """
        ⚠️ <b>VOS CONCURRENTS SONT EN TRAIN DE VOUS DÉPASSER</b> ⚠️<br/><br/>

        Pendant que vous hésitez:<br/>
        ❌ 127 mécaniciens ont upgradé vers la version PREMIUM ce mois<br/>
        ❌ Ils diagnostiquent maintenant 3x plus vite que vous<br/>
        ❌ Ils facturent plus cher grâce à leur expertise<br/>
        ❌ Leurs clients sont plus satisfaits et reviennent<br/><br/>

        <b>Combien de temps allez-vous attendre avant d'agir?</b>
        """
        story.append(Paragraph(fomo, self.styles['Urgency']))
        story.append(Spacer(1, 0.3*inch))

        # Offre dernière chance
        last_chance = """
        <b>🔥 DERNIÈRE CHANCE - OFFRE EXPIRE DANS 24H 🔥</b><br/><br/>

        Formation PREMIUM + Accès à vie: <s>497€</s> <b>147€</b><br/>
        <i>(70% de réduction exceptionnelle)</i><br/><br/>

        + BONUS GRATUITS si vous agissez maintenant:<br/>
        🎁 Ebook "Les 50 Pannes Les Plus Rentables" (valeur: 47€)<br/>
        🎁 Templates de devis automatiques (valeur: 97€)<br/>
        🎁 Accès VIP à la communauté privée (valeur: inestimable)<br/><br/>

        <b>Valeur totale: 641€</b><br/>
        <b>Votre prix aujourd'hui: 147€</b><br/><br/>

        ⏰ Cette page s'auto-détruira dans 24h!
        """
        story.append(Paragraph(last_chance, self.styles['CTA']))

        doc.build(story)

        return filepath


# Templates de contenu pour différents types de formations
FORMATION_TEMPLATES = {
    "diagnostic_rapide": {
        "title": "FORMATION DIAGNOSTIC RAPIDE - Devenez 10x Plus Efficace",
        "benefits": [
            "Réduire de 80% le temps de diagnostic",
            "Identifier instantanément les pannes critiques",
            "Augmenter votre CA de 5000€/mois minimum"
        ]
    },
    "systeme_electrique": {
        "title": "MAÎTRISE COMPLÈTE DU SYSTÈME ÉLECTRIQUE AUTOMOBILE",
        "benefits": [
            "Ne plus jamais sécher sur un problème électrique",
            "Devenir LE spécialiste électrique de votre région",
            "Facturer 150€/h pour votre expertise unique"
        ]
    },
    "moteur_moderne": {
        "title": "EXPERT MOTEUR - Injection, Turbo, Hybride",
        "benefits": [
            "Comprendre tous les moteurs modernes",
            "Diagnostiquer les pannes complexes en 15min",
            "Attirer les clients premium qui paient bien"
        ]
    }
}
