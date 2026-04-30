# Employee Lifecycle Automation

This project automates part of the employee onboarding and offboarding process for employee discounts.

It reads pending new hires and terminations from Airtable, updates the employee discount information in ECRS/Catapult, marks records complete in Airtable when appropriate, and sends a daily summary report by email.

> Important: This automation only handles adding and removing employee discounts. It does not create ECRS buyer/cashier accounts, remove Google Workspace users, or revoke Armatura access.

---

## What This Automation Does

### New Hires

For each pending new-hire record in Airtable, the script:

1. Reads employee details from the Airtable new-hire pending view.
2. Creates or updates the employee customer record in ECRS/Catapult.
3. Applies the employee discount coupon.
4. Checks for a possible loyalty/customer membership conflict.
5. Sends a conflict email if the employee already appears to have customer loyalty enabled.
6. Marks the Airtable record complete for employees that do not require manual follow-up.
7. Leaves Cashier, Nutrition, and HABA records pending for manual review.

Manual follow-up still required:

- HABA employees still need ECRS buyer accounts created.
- Cashier employees still need ECRS cashier accounts created.

### Terminations

For each pending termination record in Airtable, the script:

1. Reads employee details from the Airtable termination pending view.
2. Removes the employee automatic discount from ECRS/Catapult.
3. Removes the employee discount coupon.
4. Marks the Airtable termination record complete.
5. Includes the termination in the daily report.

Manual follow-up still required:

- Google Workspace users still need to be removed.
- MLK employees still need Armatura access revoked.

---

## Project Files

```text
employee-lifecycle-automation/
├── airtable_client.py        # Reads and updates Airtable records
├── cli.py                    # Main entry point for the script
├── config.py                 # Loads environment variables from .env
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image build instructions
├── ecrs_client.py            # ECRS/Catapult API client
├── email_manager.py          # Sends emails and daily HTML reports
├── requirements.txt          # Python dependencies
├── run.sh                    # Local setup/run helper
├── sync_service.py           # Main hire/term workflow logic
└── templates/
    └── sync_report.html      # HTML email report template
```

---

## Requirements

You need one of the following setup options:

### Option 1: Docker Recommended

- Docker
- Docker Compose
- A completed `.env` file

### Option 2: Local Python

- Python 3.12+
- `pip`
- A completed `.env` file

---

## Environment Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` and fill in the real values.

Required variables:

```env
# Airtable
AIRTABLE_TOKEN=your_airtable_pat_here
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
HIRES_TABLE_ID=tblXXXXXXXXXXXXX
HIRES_PENDING_VIEW_ID=viwXXXXXXXXXXX
HIRES_COMPLETE_VIEW_ID=viwXXXXXXXXXXX
TERMS_TABLE_ID=tblXXXXXXXXXXXX
TERMS_PENDING_VIEW_ID=viwXXXXXXXXXXX

# ECRS / Catapult
ECRS_API_KEY=your_ecrs_api_key
ECRS_BASE_URL=https://accountid.catapultweboffice.com

# Email / SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=alerts@company.com
SMTP_PASSWORD=app_password_here
EMAIL_FROM=alerts@company.com
REPORT_RECIPIENT=recipient@company.com
EMAIL_HR=hr@company.com

# Rate limiting
REQUESTS_PER_SECOND=4

# Employee discount coupon
EMPLOYEE_COUPON_CODE=your_coupon_code_here
EMPLOYEE_COUPON_EXPIRES=3000-1-1
EMPLOYEE_COUPON_NAME=Employee 50% Discount
```

Do not commit `.env` to GitHub.

---

## Running With Docker

From the project root, build the container:

```bash
docker compose build
```

Run the automation:

```bash
docker compose run --rm employee-lifecycle-automation
```

If successful, the script will:

1. Pull pending new hires from Airtable.
2. Pull pending terminations from Airtable.
3. Update ECRS/Catapult employee discounts.
4. Update Airtable records where applicable.
5. Send the daily email report.

---

## Running Locally Without Docker

From the project root:

```bash
./run.sh
```

The script will:

1. Create a virtual environment if one does not exist.
2. Install Python dependencies.
3. Check for a `.env` file.
4. Run `python cli.py`.

You can also run it manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python cli.py
```

---

## Scheduling With Cron

To run this every day at 6:00 AM using Docker, edit cron:

```bash
crontab -e
```

Add this line:

```bash
0 6 * * * cd /path/to/employee-lifecycle-automation && docker compose run --rm employee-lifecycle-automation >> cron.log 2>&1
```

Replace `/path/to/employee-lifecycle-automation` with the actual repo path on the server.

Example:

```bash
0 6 * * * cd /home/zane/scripts/employee-lifecycle-automation && docker compose run --rm employee-lifecycle-automation >> cron.log 2>&1
```

To check the latest cron output:

```bash
tail -n 100 cron.log
```

---

## How the Workflow Works

### Main entry point

The script starts in:

```bash
cli.py
```

`cli.py` loads settings, creates the ECRS client, runs the new-hire workflow, runs the termination workflow, and sends the final report.

### New-hire logic

The new-hire workflow is in:

```bash
sync_service.py
```

Function:

```python
new_hires(e_client, settings)
```

This function processes pending hire records from Airtable and applies employee discount settings in ECRS.

### Termination logic

Also in:

```bash
sync_service.py
```

Function:

```python
terms(e_client, settings)
```

This function processes pending termination records from Airtable and removes employee discounts from ECRS.

### Email report

The report is sent from:

```bash
email_manager.py
```

The HTML template is:

```bash
templates/sync_report.html
```

Edit the template if you need to change the wording or layout of the report email.

---

## Important Manual Steps Not Covered

This automation does not fully complete onboarding or offboarding.

### New hires still need manual review when applicable

- HABA employees need ECRS buyer accounts created.
- Cashier employees need ECRS cashier accounts created.

### Terminations still need manual review when applicable

- Google Workspace users need to be removed manually.
- MLK employees need Armatura access revoked manually.

These reminders are included in the daily email report.

---

## Common Maintenance Tasks

### Change the employee discount coupon

Update this value in `.env`:

```env
EMPLOYEE_COUPON_CODE=your_new_coupon_code
```

If the expiration date changes, update:

```env
EMPLOYEE_COUPON_EXPIRES=3000-1-1
```

Then rerun the container:

```bash
docker compose run --rm employee-lifecycle-automation
```

### Change who receives the daily report

Update this value in `.env`:

```env
REPORT_RECIPIENT=recipient@company.com
```

### Change who receives membership conflict alerts

Update this value in `.env`:

```env
EMAIL_HR=hr@company.com
```

### Change report wording

Edit:

```bash
templates/sync_report.html
```

Then rebuild and run:

```bash
docker compose build
docker compose run --rm employee-lifecycle-automation
```

---

## Troubleshooting

### Missing required environment variable

Error example:

```text
RuntimeError: Missing required environment variable: AIRTABLE_TOKEN
```

Fix:

1. Open `.env`.
2. Confirm the missing variable exists.
3. Confirm there are no extra spaces around the value.
4. Rerun the script.

### Airtable records are not being pulled

Check:

- `AIRTABLE_TOKEN`
- `AIRTABLE_BASE_ID`
- `HIRES_TABLE_ID`
- `HIRES_PENDING_VIEW_ID`
- `TERMS_TABLE_ID`
- `TERMS_PENDING_VIEW_ID`

Also confirm the Airtable pending views actually contain records.

### ECRS request failed

The script prints the failed URL, status code, and response body.

Check:

- `ECRS_API_KEY`
- `ECRS_BASE_URL`
- Employee phone number/customer ID formatting
- Whether the customer exists in ECRS
- Whether the coupon code is valid

### Email did not send

Check:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `REPORT_RECIPIENT`

For Gmail SMTP, use an app password, not the normal account password.

### Docker changes are not showing up

Rebuild the image:

```bash
docker compose build --no-cache
```

Then rerun:

```bash
docker compose run --rm employee-lifecycle-automation
```

### Cron is not running

Check cron logs:

```bash
tail -n 100 cron.log
```

Make sure the cron command uses the full correct repo path.

Also verify Docker works manually before relying on cron:

```bash
cd /path/to/employee-lifecycle-automation
docker compose run --rm employee-lifecycle-automation
```

---

## Security Notes

Never commit these files or values:

- `.env`
- API keys
- SMTP passwords
- Airtable tokens
- ECRS API keys

The repo already ignores `.env`, but always check before pushing:

```bash
git status
```

If a secret is accidentally committed, remove it from the repo and rotate the secret immediately.

---

## Before Handing This Off

Before giving this repo to another teammate, confirm:

- Docker build works.
- Docker run works.
- `.env.example` is up to date.
- `.env` is not committed.
- The daily report sends successfully.
- The cron path is correct for the server.
- The README matches the current behavior.

Recommended final test:

```bash
docker compose build --no-cache
docker compose run --rm employee-lifecycle-automation
```
