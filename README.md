# Keystroke Authentication
### Ore Benson

Full-stack keystroke authentication website.

This is a research website, designed to collect and analyse keystroke data using various machine learning algorithms.

Full research and report shown in Documentation.pdf.

## Technologies
* Python > 3.11.1
* Matplotlib > 3.7.1
* Skikit-learn > 1.2.2
* Scipy > 1.10.1

## Setup
```
> pip install -r requirements.txt
```
### Activate VE
```
> python -m venv .venv
> .\.venv\Scripts\activate
> pip install -r requirements.txt
> pip freeze > requirements.txt
> deactivate
> uvicorn app.main:app --reload
```
