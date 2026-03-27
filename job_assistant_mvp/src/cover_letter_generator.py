from typing import Protocol

from src.job_collector import JobOffer
from src.profile_analyzer import CandidateProfile


class LLMClientProtocol(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.4,
        )
        return response.output_text


def build_prompt(profile: CandidateProfile, offer: JobOffer) -> str:
    return f"""
Tu es un assistant de candidature.
Redige une lettre de motivation professionnelle en francais (150-220 mots), ton engage et concret.

Profil candidat:
- Competences: {", ".join(profile.skills) if profile.skills else "non precisees"}
- Experience: {profile.years_experience} ans

Offre:
- Poste: {offer.title}
- Entreprise: {offer.company}
- Region: {offer.region}
- Description: {offer.description}

Contraintes:
- Mettre en avant l'adaptation du profil au poste.
- Rester factuel, sans inventer d'experience.
- Terminer par une formule de disponibilite pour entretien.
""".strip()


def _fallback_letter(profile: CandidateProfile, offer: JobOffer) -> str:
    skills = ", ".join(profile.skills[:4]) if profile.skills else "mes competences techniques"
    return (
        f"Madame, Monsieur,\n\n"
        f"Je vous propose ma candidature au poste de {offer.title} chez {offer.company}. "
        f"Mon parcours me permet de mobiliser rapidement {skills}, en lien direct avec les besoins du poste. "
        f"Je suis motive a contribuer a vos projets et a produire des resultats concrets dans votre environnement.\n\n"
        f"Votre offre insiste sur {offer.description[:120]}... Cet axe correspond a ma demarche: "
        f"analyser les besoins, implementer des solutions robustes et collaborer efficacement avec les equipes.\n\n"
        f"Je reste disponible pour un entretien afin d'evoquer ma contribution possible.\n\n"
        f"Cordialement,"
    )


def generate_cover_letter(
    profile: CandidateProfile,
    offer: JobOffer,
    llm_api_key: str = "",
    llm_provider: str = "openai",
    llm_client: LLMClientProtocol | None = None,
) -> str:
    if llm_client is not None:
        return llm_client.generate(build_prompt(profile, offer))

    if llm_provider.lower() == "openai" and llm_api_key:
        try:
            client = OpenAIClient(api_key=llm_api_key)
            return client.generate(build_prompt(profile, offer))
        except Exception:
            # MVP fallback to keep the app usable without API or if provider fails.
            return _fallback_letter(profile, offer)

    return _fallback_letter(profile, offer)
