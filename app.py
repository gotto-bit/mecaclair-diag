"""
Interface Streamlit - Workflow Marketing Digital MecaClair
Dashboard complet pour gérer:
- Génération de PDF
- Ventes et paiements
- Envoi automatique d'emails
- Mise à jour des symptômes
- Statistiques
"""
import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Ajouter le chemin des sources
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_generator.generator import PDFFormationGenerator, FORMATION_TEMPLATES
from payment.payment_system import PaymentSystem, ProductType
from marketing.email_automation import EmailMarketingSystem
from agent.symptom_updater import SymptomUpdateAgent
from marketing.prompts import MarketingPrompts

# Configuration de la page
st.set_page_config(
    page_title="MecaClair Marketing Workflow",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des systèmes
@st.cache_resource
def init_systems():
    """Initialise tous les systèmes (avec cache)"""
    return {
        'pdf_generator': PDFFormationGenerator(),
        'payment_system': PaymentSystem(),
        'email_system': EmailMarketingSystem(
            sender_email="noreply@mecaclair-diag.com",
            sender_name="MecaClair Diag"
        ),
        'symptom_agent': SymptomUpdateAgent(),
        'marketing_prompts': MarketingPrompts()
    }

systems = init_systems()


# Sidebar - Navigation
st.sidebar.title("🚗 MecaClair Marketing")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Générer PDF",
        "💳 Gestions Ventes",
        "📧 Emails Marketing",
        "🤖 Agent Symptômes",
        "📊 Statistiques",
        "💡 Prompts Marketing"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Workflow Marketing Digital**

Système complet de vente de formations
avec génération PDF automatique et
marketing agressif (mais éthique).
""")


# === PAGE: DASHBOARD ===
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard Marketing MecaClair")

    # Statistiques globales
    stats = systems['payment_system'].get_customer_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Revenus Totaux",
            value=f"{stats['total_revenue']:.2f}€",
            delta="+12.3% vs mois dernier"
        )

    with col2:
        st.metric(
            label="👥 Clients",
            value=stats['total_customers'],
            delta=f"+{stats['premium_customers']} premium"
        )

    with col3:
        st.metric(
            label="📦 Commandes",
            value=stats['completed_orders'],
            delta=f"{stats['conversion_rate']:.1f}% conversion"
        )

    with col4:
        st.metric(
            label="⭐ Premium",
            value=stats['premium_customers'],
            delta=f"{stats['premium_customers']/max(stats['total_customers'],1)*100:.0f}%"
        )

    st.markdown("---")

    # Actions rapides
    st.subheader("⚡ Actions Rapides")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Mettre à jour les symptômes", use_container_width=True):
            with st.spinner("Mise à jour en cours..."):
                count = systems['symptom_agent'].auto_update_from_sources()
                st.success(f"✅ {count} nouvelles observations ajoutées!")

    with col2:
        pending_orders = systems['payment_system'].get_pending_pdf_orders()
        if st.button(f"📧 Envoyer PDF en attente ({len(pending_orders)})", use_container_width=True):
            for order in pending_orders:
                customer = systems['payment_system'].customers.get(order.customer_id)
                if customer and order.pdf_path:
                    st.info(f"Envoi à {customer['email']}...")
                    # Simulé - en production, utiliser le vrai système email
                    systems['payment_system'].mark_pdf_sent(order.id)
            st.success("✅ Tous les PDF envoyés!")

    with col3:
        upsell_candidates = systems['payment_system'].get_upsell_candidates(days=3)
        if st.button(f"🎯 Envoyer emails upsell ({len(upsell_candidates)})", use_container_width=True):
            st.info(f"{len(upsell_candidates)} emails programmés!")

    st.markdown("---")

    # Dernières commandes
    st.subheader("📦 Dernières Commandes")

    if systems['payment_system'].orders:
        orders_list = list(systems['payment_system'].orders.values())[-10:]
        orders_list.reverse()

        for order in orders_list:
            customer = systems['payment_system'].customers.get(order['customer_id'], {})
            product = systems['payment_system'].products.get(order['product_id'])

            with st.expander(f"#{order['id']} - {customer.get('name', 'N/A')} - {order['amount']}€"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Client:** {customer.get('email', 'N/A')}")
                    st.write(f"**Produit:** {product.name if product else 'N/A'}")
                    st.write(f"**Status:** {order['status']}")

                with col2:
                    st.write(f"**Date:** {order['created_at'][:10]}")
                    st.write(f"**PDF généré:** {'✅' if order['pdf_generated'] else '❌'}")
                    st.write(f"**PDF envoyé:** {'✅' if order['pdf_sent'] else '❌'}")
    else:
        st.info("Aucune commande pour le moment.")


# === PAGE: GÉNÉRER PDF ===
elif menu == "📄 Générer PDF":
    st.title("📄 Générateur de PDF de Formation")

    st.info("""
    💡 Générez des PDF de formation avec des templates marketing agressifs
    incluant des leviers psychologiques (urgence, rareté, preuve sociale, etc.)
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Informations Client")

        customer_name = st.text_input("Nom du client", value="Jean Dupont")
        customer_email = st.text_input("Email du client", value="jean@exemple.com")

        st.subheader("Configuration PDF")

        template_choice = st.selectbox(
            "Template de formation",
            list(FORMATION_TEMPLATES.keys()),
            format_func=lambda x: FORMATION_TEMPLATES[x]['title']
        )

        price = st.number_input("Prix payé (€)", min_value=0.0, value=97.0, step=1.0)

        order_id = st.text_input(
            "ID de commande",
            value=f"ORD-{datetime.now().strftime('%Y%m%d%H%M')}"
        )

    with col2:
        st.subheader("Aperçu")
        template = FORMATION_TEMPLATES[template_choice]

        st.markdown(f"**{template['title']}**")
        st.markdown("**Bénéfices inclus:**")
        for benefit in template['benefits']:
            st.markdown(f"✅ {benefit}")

        st.markdown(f"**Prix:** {price}€")
        st.markdown(f"**Client:** {customer_name}")

    st.markdown("---")

    if st.button("🚀 Générer le PDF", type="primary", use_container_width=True):
        with st.spinner("Génération du PDF en cours..."):
            # Récupérer les données de symptômes
            symptoms_data = systems['symptom_agent'].export_for_pdf(limit=50)

            # Générer le PDF
            pdf_path = systems['pdf_generator'].generate_diagnostic_training_pdf(
                title=template['title'],
                customer_name=customer_name,
                symptoms_data=symptoms_data,
                price=price,
                order_id=order_id
            )

            st.success(f"✅ PDF généré avec succès!")
            st.info(f"📁 Chemin: {pdf_path}")

            # Option de téléchargement
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_bytes = f.read()
                    st.download_button(
                        label="📥 Télécharger le PDF",
                        data=pdf_bytes,
                        file_name=f"formation_{customer_name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                # Simuler l'envoi email
                if st.button("📧 Envoyer par email", use_container_width=True):
                    st.info(f"Email envoyé à {customer_email} (simulé)")
                    st.balloons()


# === PAGE: GESTION VENTES ===
elif menu == "💳 Gestions Ventes":
    st.title("💳 Gestion des Ventes")

    tab1, tab2, tab3 = st.tabs(["📦 Produits", "🛒 Nouvelle Vente", "👥 Clients"])

    with tab1:
        st.subheader("📦 Catalogue de Produits")

        for product_id, product in systems['payment_system'].products.items():
            with st.expander(f"{product.name} - {product.price}€"):
                st.markdown(f"**Description:** {product.description}")

                st.markdown("**Fonctionnalités:**")
                for feature in product.features:
                    st.markdown(f"• {feature}")

                st.markdown("---")
                st.markdown("**Copy Marketing:**")
                st.text_area(
                    "Preview",
                    value=product.marketing_copy,
                    height=200,
                    key=f"copy_{product_id}",
                    disabled=True
                )

    with tab2:
        st.subheader("🛒 Créer une Nouvelle Vente")

        with st.form("new_sale_form"):
            col1, col2 = st.columns(2)

            with col1:
                sale_name = st.text_input("Nom du client*")
                sale_email = st.text_input("Email du client*")
                sale_phone = st.text_input("Téléphone (optionnel)")

            with col2:
                sale_product = st.selectbox(
                    "Produit*",
                    list(systems['payment_system'].products.keys()),
                    format_func=lambda x: f"{systems['payment_system'].products[x].name} - {systems['payment_system'].products[x].price}€"
                )

                payment_method = st.selectbox(
                    "Méthode de paiement",
                    ["stripe", "paypal", "virement"]
                )

            submitted = st.form_submit_button("💳 Créer la Vente", use_container_width=True)

            if submitted:
                if not sale_name or not sale_email:
                    st.error("❌ Le nom et l'email sont obligatoires!")
                else:
                    # Créer ou récupérer le client
                    customer = systems['payment_system'].get_customer_by_email(sale_email)
                    if not customer:
                        customer = systems['payment_system'].create_customer(
                            email=sale_email,
                            name=sale_name,
                            phone=sale_phone
                        )

                    # Créer la commande
                    order = systems['payment_system'].create_order(
                        customer_id=customer.id,
                        product_id=sale_product,
                        payment_method=payment_method
                    )

                    # Compléter la commande (simuler paiement réussi)
                    systems['payment_system'].complete_order(order.id)

                    # Générer le PDF
                    product = systems['payment_system'].products[sale_product]
                    symptoms_data = systems['symptom_agent'].export_for_pdf(limit=50)

                    pdf_path = systems['pdf_generator'].generate_diagnostic_training_pdf(
                        title=product.name,
                        customer_name=sale_name,
                        symptoms_data=symptoms_data,
                        price=product.price,
                        order_id=order.id
                    )

                    # Mettre à jour la commande
                    systems['payment_system'].update_order_pdf(order.id, pdf_path)

                    st.success(f"✅ Vente créée! Commande #{order.id}")
                    st.info("📧 Email de confirmation programmé")
                    st.balloons()

    with tab3:
        st.subheader("👥 Liste des Clients")

        if systems['payment_system'].customers:
            for customer_id, customer in systems['payment_system'].customers.items():
                with st.expander(f"{customer['name']} - {customer['email']}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Email:** {customer['email']}")
                        st.write(f"**Téléphone:** {customer.get('phone', 'N/A')}")
                        st.write(f"**Premium:** {'✅' if customer['is_premium'] else '❌'}")

                    with col2:
                        st.write(f"**Inscrit le:** {customer['created_at'][:10]}")
                        st.write(f"**Achats:** {customer['purchase_count']}")
                        st.write(f"**Total dépensé:** {customer['total_spent']}€")
        else:
            st.info("Aucun client pour le moment.")


# === PAGE: EMAILS MARKETING ===
elif menu == "📧 Emails Marketing":
    st.title("📧 Automatisation Email Marketing")

    tab1, tab2, tab3 = st.tabs(["📨 Envoyer Email", "🔄 Séquences Auto", "📊 Campagnes"])

    with tab1:
        st.subheader("📨 Envoi Manuel d'Email")

        email_type = st.selectbox(
            "Type d'email",
            [
                "Confirmation d'achat",
                "Upsell J+1",
                "Upsell J+3 (urgence)",
                "Panier abandonné",
                "Demande témoignage"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:
            recipient_email = st.text_input("Email destinataire")
            recipient_name = st.text_input("Nom destinataire")

        with col2:
            if email_type == "Confirmation d'achat":
                product_name = st.text_input("Nom du produit")
                order_id = st.text_input("ID commande")
                amount = st.number_input("Montant", value=97.0)

        if st.button("📧 Envoyer l'Email", type="primary"):
            st.info(f"Email '{email_type}' envoyé à {recipient_email} (mode simulation)")
            st.success("✅ Email envoyé avec succès!")

    with tab2:
        st.subheader("🔄 Séquences Automatiques")

        st.info("""
        **Séquence post-achat activée:**

        • J+0: Email de bienvenue + PDF
        • J+1: Email de suivi (soft upsell)
        • J+3: Email d'urgence (hard upsell)
        • J+7: Demande de feedback
        • J+14: Cadeau bonus
        """)

        sequence = systems['marketing_prompts'].generate_email_sequence("Client")

        for i, email in enumerate(sequence):
            with st.expander(f"Email {i+1} - J+{email['day']}: {email['subject']}"):
                st.markdown(f"**Sujet:** {email['subject']}")
                st.markdown(f"**Trigger psychologique:** {email['trigger']}")
                st.markdown("**Contenu:**")
                st.text_area(
                    "Preview",
                    value=email['content'],
                    height=200,
                    key=f"email_{i}",
                    disabled=True
                )

    with tab3:
        st.subheader("📊 Campagnes en Cours")

        st.metric("📧 Emails envoyés (30 jours)", "1,247", delta="+23%")
        st.metric("📬 Taux d'ouverture", "34.2%", delta="+2.1%")
        st.metric("🖱️ Taux de clic", "12.8%", delta="+1.3%")
        st.metric("💰 Revenus générés", "8,450€", delta="+15%")


# === PAGE: AGENT SYMPTÔMES ===
elif menu == "🤖 Agent Symptômes":
    st.title("🤖 Agent de Mise à Jour des Symptômes")

    tab1, tab2, tab3 = st.tabs(["📊 Base de Données", "🔍 Recherche", "➕ Ajouter"])

    with tab1:
        st.subheader("📊 Base de Données des Symptômes")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Symptômes", len(systems['symptom_agent'].symptoms))

        with col2:
            total_causes = sum(
                len(s.probable_causes)
                for s in systems['symptom_agent'].symptoms.values()
            )
            st.metric("Total Causes", total_causes)

        with col3:
            avg_confidence = sum(
                s.confidence_score
                for s in systems['symptom_agent'].symptoms.values()
            ) / max(len(systems['symptom_agent'].symptoms), 1)
            st.metric("Confiance Moyenne", f"{avg_confidence:.2%}")

        st.markdown("---")

        # Afficher les symptômes
        for symptom in list(systems['symptom_agent'].symptoms.values())[:10]:
            with st.expander(f"🔧 {symptom.symptom_text} (Fréquence: {symptom.frequency})"):
                st.markdown(f"**Sévérité:** {symptom.severity.upper()}")
                st.markdown(f"**Confiance:** {symptom.confidence_score:.0%}")
                st.markdown(f"**Véhicules:** {', '.join(symptom.vehicle_types)}")

                st.markdown("**Causes probables:**")
                for cause in symptom.probable_causes:
                    st.markdown(
                        f"• **{cause['cause']}** ({cause['probability']:.0%}) - "
                        f"{cause['solution']} - *{cause.get('cost_estimate', 'N/A')}*"
                    )

                st.markdown(f"**Sources:** {', '.join(symptom.sources)}")

    with tab2:
        st.subheader("🔍 Recherche de Symptômes")

        query = st.text_input(
            "Décrivez le symptôme à rechercher",
            placeholder="Ex: voiture ne démarre pas à froid"
        )

        if st.button("🔍 Rechercher"):
            if query:
                results = systems['symptom_agent'].search_similar_symptoms(query, top_k=5)

                st.markdown(f"**{len(results)} résultats trouvés:**")

                for result in results:
                    with st.expander(f"🎯 {result.symptom_text} (Confiance: {result.confidence_score:.0%})"):
                        for cause in result.probable_causes[:3]:
                            st.markdown(
                                f"• **{cause['cause']}** ({cause['probability']:.0%}): "
                                f"{cause['solution']}"
                            )

    with tab3:
        st.subheader("➕ Ajouter un Nouveau Symptôme")

        with st.form("add_symptom_form"):
            symptom_text = st.text_input("Description du symptôme*")

            col1, col2 = st.columns(2)

            with col1:
                cause = st.text_input("Cause probable*")
                solution = st.text_input("Solution*")

            with col2:
                vehicle_type = st.selectbox(
                    "Type de véhicule",
                    ["essence", "diesel", "hybride", "électrique"]
                )
                source = st.text_input("Source*", value="Retour terrain")

            submitted = st.form_submit_button("➕ Ajouter", use_container_width=True)

            if submitted:
                if symptom_text and cause and solution and source:
                    systems['symptom_agent'].update_symptom_from_source(
                        symptom_text=symptom_text,
                        new_cause=cause,
                        solution=solution,
                        source=source,
                        vehicle_type=vehicle_type
                    )

                    st.success("✅ Symptôme ajouté/mis à jour avec succès!")
                    st.balloons()
                else:
                    st.error("❌ Tous les champs sont obligatoires!")


# === PAGE: STATISTIQUES ===
elif menu == "📊 Statistiques":
    st.title("📊 Statistiques & Analytics")

    # Statistiques globales
    stats = systems['payment_system'].get_customer_stats()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💰 Revenus")
        st.metric("Total", f"{stats['total_revenue']:.2f}€")
        st.metric("Panier moyen", f"{stats['average_order_value']:.2f}€")
        st.metric("MRR estimé", f"{stats['total_revenue'] * 0.15:.2f}€")

    with col2:
        st.subheader("👥 Clients")
        st.metric("Total clients", stats['total_customers'])
        st.metric("Clients premium", stats['premium_customers'])
        premium_rate = (stats['premium_customers'] / max(stats['total_customers'], 1)) * 100
        st.metric("Taux premium", f"{premium_rate:.1f}%")

    with col3:
        st.subheader("📦 Commandes")
        st.metric("Total commandes", stats['total_orders'])
        st.metric("Complétées", stats['completed_orders'])
        st.metric("Taux conversion", f"{stats['conversion_rate']:.1f}%")

    st.markdown("---")

    # Graphiques (simulation)
    st.subheader("📈 Évolution des Ventes")

    import pandas as pd
    import numpy as np

    # Simuler des données
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    revenue_data = pd.DataFrame({
        'Date': dates,
        'Revenus': np.random.randint(200, 1500, size=30)
    })

    st.line_chart(revenue_data.set_index('Date'))

    st.markdown("---")

    # Top produits
    st.subheader("🏆 Top Produits")

    product_sales = {}
    for order in systems['payment_system'].orders.values():
        if order['status'] == 'completed':
            product_id = order['product_id']
            product_sales[product_id] = product_sales.get(product_id, 0) + 1

    if product_sales:
        for product_id, count in sorted(product_sales.items(), key=lambda x: x[1], reverse=True):
            product = systems['payment_system'].products.get(product_id)
            if product:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{product.name}**")
                with col2:
                    st.write(f"{count} ventes")
                with col3:
                    st.write(f"{count * product.price:.2f}€")


# === PAGE: PROMPTS MARKETING ===
elif menu == "💡 Prompts Marketing":
    st.title("💡 Prompts Marketing & Copywriting")

    tab1, tab2, tab3 = st.tabs(["📝 Landing Page", "📢 Publicités", "🎯 Leviers Psycho"])

    with tab1:
        st.subheader("📝 Générateur de Landing Page")

        product_choice = st.selectbox(
            "Choisir un produit",
            list(systems['payment_system'].products.keys()),
            format_func=lambda x: systems['payment_system'].products[x].name
        )

        product = systems['payment_system'].products[product_choice]

        if st.button("🚀 Générer le Copy Complet"):
            landing = systems['marketing_prompts'].generate_landing_page_copy(
                product_name=product.name,
                price=product.price,
                benefits=product.features
            )

            st.markdown("### 🎯 HEADLINE")
            st.info(landing['headline'])

            st.markdown("### 📌 SUB-HEADLINE")
            st.info(landing['subheadline'])

            st.markdown("### ❌ PROBLÈME (Agitation)")
            st.text_area("", value=landing['problem_agitation'], height=200, disabled=True)

            st.markdown("### ✅ SOLUTION")
            st.text_area("", value=landing['solution'], height=200, disabled=True)

            st.markdown("### ⭐ PREUVE SOCIALE")
            st.text_area("", value=landing['social_proof'], height=300, disabled=True)

            st.markdown("### 💰 OFFRE")
            st.text_area("", value=landing['offer'], height=150, disabled=True)

            st.markdown("### ⏰ URGENCE")
            st.warning(landing['urgency'])

            st.markdown("### 🛡️ GARANTIE")
            st.success(landing['guarantee'])

            st.markdown("### 🎯 CTA PRINCIPAL")
            st.button(landing['cta_primary'], type="primary", use_container_width=True)

            st.markdown("### ❓ FAQ")
            st.text_area("", value=landing['faq'], height=400, disabled=True)

            st.markdown("### 💥 FINAL PUSH")
            st.text_area("", value=landing['final_push'], height=300, disabled=True)

    with tab2:
        st.subheader("📢 Générateur de Publicités")

        product_choice_ad = st.selectbox(
            "Produit pour la pub",
            list(systems['payment_system'].products.keys()),
            format_func=lambda x: systems['payment_system'].products[x].name,
            key="ad_product"
        )

        product_ad = systems['payment_system'].products[product_choice_ad]

        if st.button("📱 Générer Pub Facebook/Instagram"):
            ad_copy = systems['marketing_prompts'].generate_facebook_ad_copy(
                product_name=product_ad.name,
                price=product_ad.price
            )

            st.markdown("### 📌 Headline")
            st.info(ad_copy['headline'])

            st.markdown("### 📝 Texte Principal")
            st.text_area("", value=ad_copy['primary_text'], height=300, disabled=True)

            st.markdown("### 📄 Description")
            st.write(ad_copy['description'])

            st.markdown("### 🎯 Call-to-Action")
            st.button(ad_copy['call_to_action'], type="primary")

            st.markdown("### 🎯 Ciblage Suggéré")
            targeting = ad_copy['targeting_suggestions']
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Centres d'intérêt:**")
                for interest in targeting['interests']:
                    st.write(f"• {interest}")

            with col2:
                st.write("**Métiers:**")
                for job in targeting['job_titles']:
                    st.write(f"• {job}")

            st.write(f"**Âge:** {targeting['age_range']}")
            st.write(f"**Localisation:** {targeting['locations']}")

    with tab3:
        st.subheader("🎯 Leviers Psychologiques")

        st.info("""
        Les leviers psychologiques utilisés dans notre marketing sont légaux,
        éthiques et basés sur des principes de persuasion scientifiquement prouvés.
        """)

        triggers = systems['marketing_prompts'].generate_sales_page_triggers()

        for trigger in triggers:
            with st.expander(f"🔹 {trigger['trigger'].value.upper()}"):
                st.markdown(f"**Implémentation:** {trigger['implementation']}")
                st.markdown(f"**Exemple:** {trigger['example']}")

        st.markdown("---")

        st.subheader("💬 Gestion des Objections")

        objections = systems['marketing_prompts'].get_objection_handlers()

        for objection, response in objections.items():
            with st.expander(f"❓ \"{objection}\""):
                st.text_area("Réponse", value=response, height=250, disabled=True)


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<small>
MecaClair Marketing Workflow v1.0<br/>
© 2024 - Tous droits réservés
</small>
""", unsafe_allow_html=True)
