# Demo Project

Automation framework using:

- Playwright
- Pytest
- Python

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
Run UI Tests
pytest tests/ui
Run API Tests
pytest tests/api

