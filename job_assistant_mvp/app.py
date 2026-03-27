import streamlit as st
import tempfile
import os
from PyPDF2 import PdfReader

from src.config import load_config
from src.cover_letter_generator import generate_cover_letter
from src.job_collector import collect_jobs
from src.profile_analyzer import analyze_cv
from src.scoring_engine import rank_offers


def main() -> None:
    config = load_config()
    st.set_page_config(page_title="Assistant Recherche d'Emploi IA", layout="wide")
    st.title("Assistant Recherche d'Emploi IA (MVP)")

    st.sidebar.header("Parametres")
    target_jobs_raw = st.sidebar.text_input(
        "Metiers cibles (separes par virgule)", value=", ".join(config.targets)
    )
    target_region = st.sidebar.text_input("Region/Ville cible", value=config.region)
    llm_enabled = st.sidebar.checkbox("Activer generation via API LLM", value=False)
    llm_api_key = (
        st.sidebar.text_input("Cle API LLM", value=config.llm_api_key, type="password")
        if llm_enabled
        else ""
    )

    st.subheader("1) Import CV")
    uploaded_cv = st.file_uploader("Chargez votre CV (.txt ou .pdf)", type=["txt", "pdf"])
    cv_text = st.text_area(
        "Ou collez le contenu du CV ici",
        height=180,
        placeholder="Ex: Data Scientist, 4 ans d'experience, Python, SQL, NLP...",
    )

    if uploaded_cv and not cv_text:
        if uploaded_cv.type == "text/plain":
            cv_text = uploaded_cv.read().decode("utf-8", errors="ignore")
        elif uploaded_cv.type == "application/pdf":
            # Extraire le texte du PDF
            try:
                pdf_reader = PdfReader(uploaded_cv)
                cv_text = ""
                for page in pdf_reader.pages:
                    cv_text += page.extract_text() + "\n"
            except Exception as e:
                st.error(f"Erreur lors de l'extraction du texte du PDF : {e}")
                cv_text = ""

    if not cv_text.strip():
        st.info("Ajoutez un CV pour lancer le matching.")
        return

    target_jobs = [item.strip() for item in target_jobs_raw.split(",") if item.strip()]
    profile = analyze_cv(cv_text=cv_text, desired_titles=target_jobs)

    st.subheader("2) Offres collecte + scoring")
    offers = collect_jobs(target_titles=target_jobs, region=target_region, limit=30)
    ranked = rank_offers(profile=profile, offers=offers, target_region=target_region)

    if not ranked:
        st.warning("Aucune offre trouvee pour ce filtre. Essayez d'elargir la region/metiers.")
        return

    for idx, item in enumerate(ranked, start=1):
        with st.expander(f"#{idx} - {item.offer.title} | {item.offer.company} | Score {item.score}/100"):
            st.write(f"**Region:** {item.offer.region}")
            st.write(f"**Description:** {item.offer.description}")
            st.write(f"**Lien:** {item.offer.url}")
            if item.reasons:
                st.write("**Pourquoi ce score ?**")
                for reason in item.reasons:
                    st.write(f"- {reason}")

            if st.button(f"Generer lettre pour {item.offer.id}", key=f"letter-{item.offer.id}"):
                letter = generate_cover_letter(
                    profile=profile,
                    offer=item.offer,
                    llm_api_key=llm_api_key,
                    llm_provider=config.llm_provider,
                )
                st.text_area(
                    f"Lettre de motivation - {item.offer.title}",
                    value=letter,
                    height=280,
                    key=f"output-{item.offer.id}",
                )


if __name__ == "__main__":
    main()
