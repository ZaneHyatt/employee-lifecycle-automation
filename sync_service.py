import airtable_client
import email_manager


from config import (
    EMAIL_SUBJECT_CONFLICT,
    EMAIL_BODY_CONFLICT,
)


def new_hires(e_client, settings):

    ## pulls from airtable

    at_client = airtable_client.AirtableClient(
        token=settings.AIRTABLE_TOKEN,
        base_id=settings.AIRTABLE_BASE_ID,
        table_name=settings.HIRES_TABLE_ID,
        requests_per_second=settings.REQUESTS_PER_SECOND,
    )
    airtable_report = at_client.get_pending_records(settings.HIRES_PENDING_VIEW_ID)

    if airtable_report:
        print(airtable_report)
    else:
        print("No pending new hires")

    check = []
    dont_check = []

    ## loops through each report
    for report in airtable_report:

        print(report)

        print(f"\n{report['First Name']} {report['Last Name']}: ")

        required_fields = [
            "Employee ID",
            "First Name",
            "Last Name",
            "Phone Number",
        ]

        if any(not report.get(field, "").strip() for field in required_fields):
            print("Skippped: missing required field(s)")
        else:

            ## makes new customer
            new_customer = {
                "customerId": report["Phone Number"],
                "firstName": report["First Name"],
                "lastName": report["Last Name"],
                "company": report["Employee ID"],
            }

            if report["Job Title"] == "Cashier":
                new_customer["automaticDiscount"] = "Employee Cashiers"
            else:
                new_customer["automaticDiscount"] = "Employee Discount"

            e_client.edit_customer(new_customer)
            print("Added customer")

            ## adds the 50% discount
            e_client.add_customer_store_coupon(
                customer_id=report["Phone Number"],
                coupon_code=settings.EMPLOYEE_COUPON_CODE,  # or your real Employee 50% Discount code
                coupon_expires=settings.EMPLOYEE_COUPON_EXPIRES,
            )
            print("Added 50% discount")

            ## checks for loyalty conflict
            customer_info = e_client.get_customer_info(report["Phone Number"])

            if customer_info["Loyalty"] == "true":

                subject = EMAIL_SUBJECT_CONFLICT

                message = EMAIL_BODY_CONFLICT.format(
                    first_name=customer_info["First Name"],
                    last_name=customer_info["Last Name"],
                    customer_id=new_customer["customerId"],
                )

                email_mng = email_manager.EmailManager(subject, settings)
                email_mng.send_email(message)

        if (
            (report["Job Title"] != "Cashier")
            and (report["Job Title"] != "Nutrition")
            and (report["Job Title"] != "HABA")
        ):
            at_client.complete_record(report["Record ID"])
            dont_check.append(report)
        else:
            check.append(report)

    print("\nDone adding emp discount\n\n---------------------------\n")

    return check, dont_check


def terms(e_client, settings):

    ## pulls from airtable

    at_client = airtable_client.AirtableClient(
        token=settings.AIRTABLE_TOKEN,
        base_id=settings.AIRTABLE_BASE_ID,
        table_name=settings.TERMS_TABLE_ID,
        requests_per_second=settings.REQUESTS_PER_SECOND,
    )
    airtable_report = at_client.get_pending_records(settings.TERMS_PENDING_VIEW_ID)

    if airtable_report:
        print(airtable_report)
    else:
        print("No pending terms")

    ## loops through each report
    for report in airtable_report:

        print(f"\n{report['First Name']} {report['Last Name']}: ")

        try:

            ## terms customer
            term_customer = {
                "customerId": report["Phone Number"],
                "automaticDiscount": "",
            }

            e_client.edit_customer(term_customer)
            print("Removed customer")

            ## removes the 50% discount
            e_client.remove_customer_store_coupon(
                customer_id=report["Phone Number"],
                coupon_code=settings.EMPLOYEE_COUPON_CODE,  # or your real Employee 50% Discount code
            )
            print("Removed 50% discount")

        except Exception as e:
            print(f"Customer acount does not exist: {e}")

        at_client.complete_record(report["Record ID"])

    print("\nDone removing emp discount\n\n---------------------------\n")

    return airtable_report
