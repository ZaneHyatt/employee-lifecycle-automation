from dataclasses import dataclass
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    # Airtable
    AIRTABLE_TOKEN: str = _require("AIRTABLE_TOKEN")
    AIRTABLE_BASE_ID: str = _require("AIRTABLE_BASE_ID")
    HIRES_TABLE_ID: str = _require("HIRES_TABLE_ID")
    HIRES_PENDING_VIEW_ID: str = _require("HIRES_PENDING_VIEW_ID")
    HIRES_COMPLETE_VIEW_ID: str = _require("HIRES_COMPLETE_VIEW_ID")
    TERMS_TABLE_ID: str = _require("TERMS_TABLE_ID")
    TERMS_PENDING_VIEW_ID: str = _require("TERMS_PENDING_VIEW_ID")

    # ECRS
    ECRS_API_KEY: str = _require("ECRS_API_KEY")
    ECRS_BASE_URL: str = _require("ECRS_BASE_URL")

    # Email
    SMTP_HOST: str = _require("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = _require("SMTP_USER")
    SMTP_PASSWORD: str = _require("SMTP_PASSWORD")
    EMAIL_FROM: str = _require("EMAIL_FROM")
    REPORT_RECIPIENT: str = _require("REPORT_RECIPIENT")
    EMAIL_HR: str = _require("EMAIL_HR")

    EMPLOYEE_COUPON_CODE: str = _require("EMPLOYEE_COUPON_CODE")
    EMPLOYEE_COUPON_EXPIRES: str = os.getenv("EMPLOYEE_COUPON_EXPIRES", "3000-1-1")
    EMPLOYEE_COUPON_NAME: str = os.getenv(
        "EMPLOYEE_COUPON_NAME", "Employee 50% Discount"
    )

    # Rate limiting
    REQUESTS_PER_SECOND: int = int(os.getenv("REQUESTS_PER_SECOND", "4"))


EMAIL_SUBJECT_CONFLICT = "ℹ️ Employee Discount Conflict – Customer Membership Detected"

EMAIL_BODY_CONFLICT = """
Hello Membership Team,

A new employee being onboarded for an employee discount currently has an active customer membership on file. Please review to prevent conflicts.

Employee Name: {first_name} {last_name}
Customer ID: {customer_id}

Thank you,
IT Department
"""
