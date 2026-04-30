import time
import csv
import requests
from typing import Any


class AirtableClient:
    def __init__(
        self,
        token: str,
        base_id: str,
        table_name: str,
        requests_per_second: float = 4,
    ) -> None:
        if not token:
            raise RuntimeError("AIRTABLE_TOKEN not set in environment or .env file")

        self.token = token
        self.base_id = base_id
        self.table_name = table_name
        self.requests_per_second = requests_per_second
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    ## fetches the records from any given view
    def fetch_view_records(self, view_name: str) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"view": view_name}
        all_records: list[dict[str, Any]] = []

        while True:
            resp = requests.get(self.base_url, headers=self.headers, params=params)
            resp.raise_for_status()
            data = resp.json()

            all_records.extend(data.get("records", []))

            offset = data.get("offset")
            if not offset:
                break

            params["offset"] = offset
            time.sleep(1 / self.requests_per_second)

        return all_records

    ## exports any records to a csv
    def export_fields_to_csv(
        self, records: list[dict[str, Any]], filename: str = "airtable_view_export.csv"
    ) -> None:
        if not records:
            return

        fieldnames: set[str] = set()
        for r in records:
            fieldnames.update(r.get("fields", {}).keys())

        ordered = sorted(fieldnames)

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ordered)
            writer.writeheader()
            for r in records:
                writer.writerow(r.get("fields", {}))

        print(f"Saved to {filename}")

    ## fetches the records just for the pending view and returns a clean output
    def get_pending_records(self, view_name: str) -> list[dict[str, str]]:
        print(f"Pulling records from view: {view_name}")
        raw_records = self.fetch_view_records(view_name)
        print(f"Total records pulled: {len(raw_records)}\n")

        records: list[dict[str, str]] = []
        for rec in raw_records:
            fields = rec.get("fields", {})
            records.append(
                {
                    "Record ID": rec.get("id", ""),
                    "Employee ID": str(fields.get("Employee ID", "")),
                    "First Name": str(fields.get("Employee First Name", "")),
                    "Last Name": str(fields.get("Employee Last Name", "")),
                    "Phone Number": str(fields.get("Phone Number", "")),
                    "Job Title": str(fields.get("Department", "")),
                    "Location": str(fields.get("Location", "")),
                }
            )

        return records

    ## marks a record as complete
    def complete_record(self, record_id: str) -> None:
        url = f"{self.base_url}/{record_id}"
        payload = {"fields": {"Status": "Complete"}}

        resp = requests.patch(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        print("Updated:", resp.json())
