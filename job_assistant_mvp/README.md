# Assistant Recherche d'Emploi IA (MVP)

MVP Python + Streamlit pour:
- importer un CV,
- collecter des offres ciblees (mock),
- scorer les offres selon le profil,
- generer une lettre de motivation (LLM si cle API, sinon fallback local).

## Installation

```bash
cd /home/michel/code_python/fromt/projeia/job_assistant_mvp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variables d'environnement (optionnel)

```bash
export TARGET_JOBS="Data Scientist,Machine Learning Engineer,Data Analyst"
export TARGET_REGION="Ile-de-France"
export LLM_PROVIDER="openai"
export LLM_API_KEY="sk-..."
```

## Lancer l'application

```bash
streamlit run app.py
```

## Tests

```bash
pytest -q
```
