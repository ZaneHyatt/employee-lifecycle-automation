from __future__ import annotations

import requests
from typing import Any, Optional


class ECRSClient:
    def __init__(self, base_url, api_key, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "X-ECRS-APIKEY": self.api_key,
            "Accept": "application/json",
        }

    def _request(
        self, method: str, path: str, *, params: Optional[dict[str, Any]] = None
    ) -> Any:
        url = f"{self.base_url}{path}"
        response = requests.request(
            method,
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            print("Request failed:")
            print(f"  URL: {response.url}")
            print(f"  Status: {response.status_code}")
            print(f"  Body: {response.text}")
            raise exc

        return response.json()

    ## API methods

    def get_customer(
        self, customer_id: str, modified_since: Optional[str] = None
    ) -> Any:
        params: dict[str, Any] = {"customerId": customer_id}
        if modified_since:
            params["modifiedSince"] = modified_since
        return self._request("GET", "/api/Customer", params=params)

    def get_customer_store_coupons(self, customer_id: str) -> Any:
        return self._request(
            "GET", "/api/CustomerStoreCoupon", params={"customerId": customer_id}
        )

    def edit_customer(self, customer_data: dict[str, Any]) -> Any:

        return self._request("PUT", "/api/Customer", params=customer_data)

    def add_customer_store_coupon(
        self, customer_id: str, coupon_code: str, coupon_expires: str
    ) -> Any:
        params = {
            "customerId": customer_id,
            "couponCode": coupon_code,
            "couponExpires": coupon_expires,
        }

        return self._request("PUT", "/api/CustomerStoreCoupon", params=params)

    def remove_customer_store_coupon(self, customer_id: str, coupon_code: str) -> Any:
        params = {
            "customerId": customer_id,
            "couponCode": coupon_code,
        }

        return self._request("DELETE", "/api/CustomerStoreCoupon", params=params)

    def get_customer_info(self, customer_id: str) -> dict[str, Any]:
        customer_data = self.get_customer(customer_id)[0]
        coupon_data = self.get_customer_store_coupons(customer_id)

        needed_info: list[str] = []

        if customer_data.get("firstName", "") == "":
            needed_info.append("First Name")
        if customer_data.get("lastName", "") == "":
            needed_info.append("Last Name")
        if customer_data.get("company", "") == "":
            needed_info.append("Employee ID")
        if customer_data.get("automaticDiscount") != "Employee Discount":
            needed_info.append("Employee Discount")

        record: dict[str, Any] = {
            "First Name": customer_data.get("firstName"),
            "Last Name": customer_data.get("lastName"),
            "Employee ID": customer_data.get("company"),
            "Employee Discount": customer_data.get("automaticDiscount"),
            "Loyalty": customer_data.get("loyaltyEnabled"),
        }

        has_emp_coupon = any(
            item.get("couponName") == "Employee 50% Discount" for item in coupon_data
        )
        record["Employee 50% Discount"] = has_emp_coupon

        if not has_emp_coupon:
            needed_info.append("Employee 50% Discount")

        return record
