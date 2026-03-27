import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    """Runtime configuration for the MVP."""

    llm_provider: str
    llm_api_key: str
    targets: list[str]
    region: str
    data_dir: Path


def _parse_targets(raw_targets: str) -> list[str]:
    return [item.strip() for item in raw_targets.split(",") if item.strip()]


def load_config() -> AppConfig:
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    targets = _parse_targets(
        os.getenv("TARGET_JOBS", "Data Scientist, Machine Learning Engineer, Data Analyst")
    )
    region = os.getenv("TARGET_REGION", "Ile-de-France")

    return AppConfig(
        llm_provider=os.getenv("LLM_PROVIDER", "openai"),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        targets=targets,
        region=region,
        data_dir=data_dir,
    )
