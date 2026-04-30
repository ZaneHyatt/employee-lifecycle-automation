# Automated Onboarding & Offboarding Engine (Airtable → ECRS → Google Workspace)

Automates key steps of Erewhon’s employee onboarding and offboarding workflows using Airtable as the source-of-truth.  
Processes new hires and terminations, applies/removes employee discounts in ECRS/Catapult, manages Google Workspace accounts, updates Airtable status fields, and sends a recap email at the end of each run.

## What it does

### Onboarding (New Hires)

- Reads new-hire rows from Airtable
- Creates/updates employee discount in ECRS/Catapult
- Checks if the employee is a previous employee and handles accordingly
- Marks the Airtable record complete for non-cashier roles (cashiers can require additional steps)

### Offboarding (Terminations)

- Reads termination rows from Airtable
- Removes/ends employee discount in ECRS/Catapult
- Suspends/disables the employee’s Google Workspace account
- Sends a recap email summarizing actions taken and any exceptions

## Tech Stack

- Python
- Airtable API (source of truth + workflow state)
- ECRS/Catapult API (customer store coupons / employee discount)
- Google Admin SDK (account disable/suspend)
- SMTP email notifications
- Jinja2 templates for email/report formatting

## Project Structure (high level)

- `cli.py` — entry point (run manually or scheduled)
- `config.py` — environment-based configuration
- `clients/` — Airtable, ECRS, Google, email clients
- `services/` — orchestration logic for onboarding/offboarding
- `templates/` — email templates (Jinja2)

## Quickstart

```bash
./run.sh
```

## Setup

### 1) Create a virtualenv and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment variables

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

**Never commit `.env` or your service account JSON.**

### 3) Run

```bash
python cli.py
```

## Notes on credentials

- **Airtable**: use a Personal Access Token (PAT) with least-privilege scopes.
- **Google Workspace**: use a service account JSON + domain-wide delegation; set `GOOGLE_SERVICE_ACCOUNT_FILE` to the local file path.
- **SMTP**: for Gmail, use an app password (not your normal password).

## Example output

- Console logs show each record processed and what actions were taken.
- A summary HTML report is emailed to `REPORT_RECIPIENT`.

## Security

If you ever committed secrets to Git, rotate them immediately:

- Airtable PAT
- ECRS API key
- SMTP password/app password
- Google service account key

## License

MIT (recommended for a public portfolio repo).

## Disclaimer

This repository is a portfolio version of an internal automation tool. Organization-specific identifiers and credentials are not included.
