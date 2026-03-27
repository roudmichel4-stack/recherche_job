from src.cover_letter_generator import generate_cover_letter
from src.job_collector import JobOffer
from src.profile_analyzer import analyze_cv


class DummyLLMClient:
    def generate(self, prompt: str) -> str:
        assert "Data Scientist" in prompt
        return "Lettre test generee"


def test_cover_letter_uses_injected_llm_client() -> None:
    profile = analyze_cv("Data Scientist 3 ans Python SQL", desired_titles=["Data Scientist"])
    offer = JobOffer(
        id="job-1",
        title="Data Scientist",
        company="Nova",
        region="Ile-de-France",
        description="Python SQL NLP",
        url="https://example.com/1",
    )
    content = generate_cover_letter(profile=profile, offer=offer, llm_client=DummyLLMClient())
    assert content == "Lettre test generee"


def test_cover_letter_fallback_without_api_key() -> None:
    profile = analyze_cv("Data Analyst 2 ans SQL Tableau", desired_titles=["Data Analyst"])
    offer = JobOffer(
        id="job-2",
        title="Data Analyst",
        company="Insight",
        region="Lyon",
        description="SQL Tableau dashboarding",
        url="https://example.com/2",
    )
    content = generate_cover_letter(profile=profile, offer=offer, llm_api_key="")
    assert "Madame, Monsieur" in content
