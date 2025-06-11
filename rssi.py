import streamlit as st
from sentence_transformers import SentenceTransformer
import fitz
import os
import json

from backend.pdf_utils import lire_et_chunker_pdfs
from backend.faiss_utils import construire_index, rechercher_passages
from backend.llm_utils import generer_reponse_llm
from backend.rss_utils import get_alertes_certfr
from backend.history_utils import sauvegarder_echange, charger_historique_persistant

# === Configuration de la page Streamlit ===
st.set_page_config(
    page_title="Assistant RSSI",
    page_icon="🛡️"
)

st.title("🛡️ Assistant RSSI Virtuel")
st.write("Pose une question liée à la cybersécurité, aux normes, ou aux incidents...")

@st.cache_resource
def load_embedding_model():
    """
    Charge le modèle d'embedding SentenceTransformer (mise en cache pour rapidité).
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_embedding_model()

# Création des onglets principaux de l'application
onglets = st.tabs([
    "🧠 Assistant RSSI",
    "📝 Synthèse de document",
    "📡 Veille cybersécurité",
    "❓ FAQ cybersécurité",
    "📁 Ajouter un document",
    "📜 Historique"
])

# Chargement de l'historique en début de session
if "historique" not in st.session_state:
    st.session_state["historique"] = charger_historique_persistant()

# === Onglet 1 – Assistant RSSI (RAG sur PDF) ===
with onglets[0]:
    st.subheader("💬 Pose ta question")
    if "question_input" not in st.session_state:
        st.session_state["question_input"] = ""
    with st.form("form_question", clear_on_submit=True):
        question = st.text_area("Ta question ❓", height=120, key="question_input")
        send = st.form_submit_button("Envoyer")
        if send:
            question_value = question
            if not question_value.strip():
                st.warning("Merci d'écrire une question.")
            else:
                with st.spinner("📚 Génération de la réponse..."):
                    try:
                        dossier_existe = os.path.exists("docs")
                        pdfs = []
                        if dossier_existe:
                            pdfs = [f for f in os.listdir("docs") if f.lower().endswith(".pdf")]
                        if not dossier_existe or not pdfs:
        
                            prompt = (
                                "Tu es un assistant RSSI spécialisé en cybersécurité.\n"
                                "Réponds à la question suivante en t'appuyant sur tes connaissances générales.\n"
                                f"Question : {question_value}\n"
                                "Réponds de manière claire, précise et complète, sans mentionner l'absence de documents."
                            )
                            answer = generer_reponse_llm(prompt)
                        else:
                            chunks, metadatas = lire_et_chunker_pdfs()
                            index, _ = construire_index(model, chunks)
                            passages_pertinents = rechercher_passages(model, question_value, chunks, index)
                            prompt = (
                                "Tu es un assistant RSSI spécialisé en cybersécurité.\n"
                                "Voici des extraits de documents de référence fournis par l'utilisateur. Utilise-les pour répondre si pertinent, sinon complète avec tes connaissances générales.\n"
                            )
                            for i, passage in enumerate(passages_pertinents, 1):
                                prompt += f"Passage {i} :\n{passage}\n\n"
                            prompt += f"Question : {question_value}\n"
                            prompt += "Réponds de manière claire, précise et complète, sans mentionner l'absence d'information dans les documents."
                            answer = generer_reponse_llm(prompt)
                        st.success("🧠 Réponse de l'assistant :")
                        st.markdown(answer)
                        st.session_state["historique"].append({
                            "question": question_value,
                            "reponse": answer
                        })
                        sauvegarder_echange(question_value, answer)
                    except Exception as e:
                        st.error(f"❌ Erreur : {e}")

# === Onglet 2 – Synthèse de documents PDF ===
with onglets[1]:
    st.subheader("📝 Synthétiseur de documents cybersécurité")
    st.write("Téléverse un document PDF (rapport, guide, bulletin...) pour en obtenir une synthèse claire.")
    fichier_pdf = st.file_uploader("📄 Choisis un fichier PDF", type=["pdf"])
    if fichier_pdf is not None:
        try:
            # Lecture du PDF uploadé
            with fitz.open(stream=fichier_pdf.read(), filetype="pdf") as doc:
                contenu = ""
                for page in doc:
                    contenu += page.get_text()
            if len(contenu.strip()) < 100:
                st.warning("⚠️ Le document semble vide ou non lisible.")
            else:
                if st.button("🧠 Générer une synthèse"):
                    with st.spinner("🤖 L'assistant lit le document et résume..."):
                        try:
                            prompt_synthese = (
                                "Tu es un expert cybersécurité.\n"
                                "Voici le contenu d'un document technique ou réglementaire :\n\n"
                                f"{contenu[:10000]}\n\n"
                                "Fais un résumé clair, structuré et synthétique de ce document.\n"
                                "Mets en évidence les points clés, les menaces évoquées et les recommandations s'il y en a."
                            )
                            reponse_synthese = generer_reponse_llm(prompt_synthese)
                            st.success("✅ Synthèse générée :")
                            st.markdown(reponse_synthese)
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la génération : {e}")
        except Exception as e:
            st.error(f"❌ Impossible de lire le PDF : {e}")

# === Onglet 3 – Veille cybersécurité (CERT-FR) ===
with onglets[2]:
    st.subheader("📡 Veille technologique sur la cybersécurité")
    st.info("Dernières alertes récupérées automatiquement depuis le CERT-FR :")
    alertes = get_alertes_certfr()
    for idx, alerte in enumerate(alertes):
        st.markdown(f"### 🛡️ {alerte['titre']}")
        st.markdown(f"🗓️ *Date : {alerte['date']}*")
        st.write(alerte["description"])
        st.markdown(f"[🔗 Lire l'alerte complète]({alerte['lien']})")
        # Bouton pour résumer l'alerte via LLM
        if st.button("🔄 Résumer cette alerte", key=f"resume_{idx}"):
            with st.spinner("🤖 Résumé en cours..."):
                try:
                    prompt_resume = (
                        "Fais un résumé clair et concis de cette alerte de cybersécurité.\n"
                        "Garde les points critiques et indique si c'est critique, modéré ou faible.\n\n"
                        f"Alerte : {alerte['description']}"
                    )
                    resume = generer_reponse_llm(prompt_resume)
                    st.success("Résumé de l'alerte :")
                    st.markdown(resume)
                except Exception as e:
                    st.error(f"❌ Erreur lors du résumé : {e}")
        st.markdown("---")

# === Onglet 4 – FAQ Cybersécurité ===
with onglets[3]:
    st.subheader("❓ Foire Aux Questions (FAQ) Cybersécurité")
    # Liste de questions fréquentes
    questions_faq = [
        "Pourquoi est-il important d'utiliser des mots de passe différents pour chaque compte ?",
        "Qu'est-ce qu'une authentification à deux facteurs (2FA) et pourquoi l'activer ?",
        "Pourquoi faut-il éviter de cliquer sur des liens suspects dans les emails ?",
        "Comment peut-on reconnaître un site sécurisé ?",
        "Pourquoi est-il essentiel de mettre à jour régulièrement ses logiciels et applications ?",
        "Qu'est-ce qu'un gestionnaire de mots de passe et pourquoi l'utiliser ?",
        "Pourquoi ne faut-il pas partager son mot de passe avec d'autres personnes ?",
        "Que faire si on reçoit un email étrange ou suspect ?",
        "Pourquoi faut-il faire attention aux informations partagées sur les réseaux sociaux ?",
        "Comment protéger son appareil avec un mot de passe ou une empreinte digitale ?",
        "Pourquoi faut-il éviter de se connecter à des réseaux Wi-Fi publics pour des transactions sensibles ?",
        "Comment vérifier si une application est sécurisée avant de la télécharger ?",
        "Pourquoi faut-il régulièrement sauvegarder ses données ?",
        "Qu'est-ce que le chiffrement et pourquoi est-il important ?",
        "Pourquoi est-il essentiel de se déconnecter de ses comptes après une session sur un ordinateur public ?"
    ]
    # Affichage des questions et génération de réponse à la demande
    for idx, question_faq in enumerate(questions_faq):
        if st.button(f"❓ {question_faq}", key=f"faq_{idx}"):
            with st.spinner("🤖 L'assistant réfléchit..."):
                try:
                    prompt_faq = (
                        "Tu es un expert en cybersécurité.\n"
                        "Réponds de façon claire, simple et concise à la question suivante :\n\n"
                        f"Question : {question_faq}"
                    )
                    reponse_faq = generer_reponse_llm(prompt_faq)
                    st.success("✅ Réponse de l'assistant :")
                    st.markdown(reponse_faq)
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération de réponse : {e}")

# === Onglet 5 – Ajouter un document PDF interne ===
with onglets[4]:
    st.subheader("📁 Ajouter un document interne au corpus")
    st.write("Tu peux ajouter un document PDF (ex : politique interne, rapport d'audit...).")
    fichier_ajout = st.file_uploader("📄 Sélectionne un fichier PDF à ajouter", type=["pdf"])
    if fichier_ajout is not None:
        if st.button("➕ Ajouter au corpus"):
            try:
                # Création du dossier docs si besoin et ajout du fichier
                os.makedirs("docs", exist_ok=True)
                chemin_fichier = os.path.join("docs", fichier_ajout.name)
                with open(chemin_fichier, "wb") as f:
                    f.write(fichier_ajout.read())
                st.success(f"✅ Document '{fichier_ajout.name}' ajouté dans le dossier /docs avec succès !")
                st.info("Il sera utilisé automatiquement lors de la prochaine question posée à l'assistant.")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'ajout du fichier : {e}")

# === Onglet 6 – Historique des échanges avec l'assistant ===
with onglets[5]:
    st.subheader("📜 Historique des échanges avec l'assistant")
    # Affichage de l'historique et export JSON
    if st.session_state["historique"]:
        for idx, echange in enumerate(reversed(st.session_state["historique"])):
            st.markdown(f"### ❓ Question {len(st.session_state['historique']) - idx}")
            st.markdown(f"**Question :** {echange['question']}")
            st.markdown(f"**Réponse :** {echange['reponse']}")
            st.markdown("---")
        historique_json = json.dumps(st.session_state["historique"], indent=4, ensure_ascii=False)
        st.download_button(
            label="📥 Télécharger l'historique en JSON",
            data=historique_json,
            file_name="historique_questions.json",
            mime="application/json"
        )
    else:
        st.info("🕵️ Aucun échange enregistré pour l'instant. Pose une question pour démarrer !") 