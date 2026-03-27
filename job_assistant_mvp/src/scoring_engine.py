from dataclasses import dataclass

from src.job_collector import JobOffer
from src.profile_analyzer import CandidateProfile


@dataclass
class ScoredJob:
    offer: JobOffer
    score: int
    reasons: list[str]


def _normalize_score(raw: float) -> int:
    return max(0, min(100, int(round(raw))))


def score_offer(profile: CandidateProfile, offer: JobOffer, target_region: str) -> ScoredJob:
    score = 0.0
    reasons: list[str] = []
    text_blob = f"{offer.title} {offer.description}".lower()

    skill_hits = [skill for skill in profile.skills if skill in text_blob]
    if skill_hits:
        skill_score = min(50, len(skill_hits) * 10)
        score += skill_score
        reasons.append(f"Competences alignees: {', '.join(skill_hits)}")

    if profile.desired_titles and any(
        wanted.lower() in offer.title.lower() for wanted in profile.desired_titles
    ):
        score += 25
        reasons.append("Titre du poste proche de l'objectif")

    if target_region and target_region.lower() in offer.region.lower():
        score += 15
        reasons.append("Region cible respectee")

    if profile.years_experience >= 2:
        score += 10
        reasons.append("Niveau d'experience exploitable")

    return ScoredJob(offer=offer, score=_normalize_score(score), reasons=reasons)


def rank_offers(
    profile: CandidateProfile, offers: list[JobOffer], target_region: str
) -> list[ScoredJob]:
    scored = [score_offer(profile, offer, target_region) for offer in offers]
    return sorted(scored, key=lambda item: item.score, reverse=True)
