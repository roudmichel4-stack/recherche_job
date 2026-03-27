from src.job_collector import JobOffer
from src.profile_analyzer import analyze_cv
from src.scoring_engine import rank_offers


def test_scoring_ranks_relevant_offer_first() -> None:
    cv_text = "Data Scientist avec 4 ans d'experience. Python SQL NLP AWS."
    profile = analyze_cv(cv_text, desired_titles=["Data Scientist", "Machine Learning Engineer"])

    offers = [
        JobOffer(
            id="a",
            title="Data Scientist",
            company="A",
            region="Ile-de-France",
            description="Python SQL NLP machine learning AWS",
            url="https://example.com/a",
        ),
        JobOffer(
            id="b",
            title="Backend Developer",
            company="B",
            region="Ile-de-France",
            description="Java Spring microservices",
            url="https://example.com/b",
        ),
    ]

    ranked = rank_offers(profile, offers, target_region="Ile-de-France")
    assert ranked[0].offer.id == "a"
    assert ranked[0].score > ranked[1].score
