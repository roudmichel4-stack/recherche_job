from dataclasses import dataclass


@dataclass
class JobOffer:
    id: str
    title: str
    company: str
    region: str
    description: str
    url: str


MOCK_OFFERS = [
    JobOffer(
        id="job-001",
        title="Data Scientist",
        company="Nova Analytics",
        region="Ile-de-France",
        description=(
            "Nous cherchons un Data Scientist Python/SQL avec experience en NLP, "
            "modelisation et deploiement cloud AWS."
        ),
        url="https://example.com/jobs/001",
    ),
    JobOffer(
        id="job-002",
        title="Machine Learning Engineer",
        company="Vision AI",
        region="Ile-de-France",
        description=(
            "Role MLOps: Docker, Kubernetes, PyTorch, APIs et optimisation de pipelines."
        ),
        url="https://example.com/jobs/002",
    ),
    JobOffer(
        id="job-003",
        title="Data Analyst",
        company="Insight Retail",
        region="Lyon",
        description=(
            "Analyse business SQL/Tableau, dashboarding et communication avec equipes metier."
        ),
        url="https://example.com/jobs/003",
    ),
    JobOffer(
        id="job-004",
        title="Backend Developer",
        company="StackFlow",
        region="Ile-de-France",
        description="Python APIs, microservices et architecture event-driven.",
        url="https://example.com/jobs/004",
    ),
]


def collect_jobs(target_titles: list[str], region: str, limit: int = 20) -> list[JobOffer]:
    target_titles_lower = [t.lower().strip() for t in target_titles if t.strip()]
    region_lower = region.lower().strip()

    filtered = []
    for offer in MOCK_OFFERS:
        title_match = (
            True if not target_titles_lower else any(t in offer.title.lower() for t in target_titles_lower)
        )
        region_match = not region_lower or region_lower in offer.region.lower()
        if title_match and region_match:
            filtered.append(offer)

    return filtered[:limit]
