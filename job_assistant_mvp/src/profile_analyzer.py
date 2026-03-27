import re
from dataclasses import dataclass


KNOWN_SKILLS = {
    "python",
    "sql",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "aws",
    "gcp",
    "docker",
    "kubernetes",
    "power bi",
    "tableau",
    "spark",
    "nlp",
}


@dataclass
class CandidateProfile:
    full_text: str
    skills: list[str]
    years_experience: int
    desired_titles: list[str]


def _extract_years_experience(cv_text: str) -> int:
    patterns = [
        r"(\d+)\s*\+?\s*ans",
        r"(\d+)\s*\+?\s*years",
    ]
    for pattern in patterns:
        match = re.search(pattern, cv_text.lower())
        if match:
            return int(match.group(1))
    return 0


def _extract_skills(cv_text: str) -> list[str]:
    text = cv_text.lower()
    found = sorted(skill for skill in KNOWN_SKILLS if skill in text)
    return found


def analyze_cv(cv_text: str, desired_titles: list[str] | None = None) -> CandidateProfile:
    titles = desired_titles or []
    return CandidateProfile(
        full_text=cv_text.strip(),
        skills=_extract_skills(cv_text),
        years_experience=_extract_years_experience(cv_text),
        desired_titles=titles,
    )
