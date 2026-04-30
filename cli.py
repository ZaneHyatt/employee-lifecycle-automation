import ecrs_client
import email_manager
import sync_service


from config import Settings


def main() -> None:

    settings = Settings()

    e_client = ecrs_client.ECRSClient(settings.ECRS_BASE_URL, settings.ECRS_API_KEY)

    check_hires, dont_check_hires = sync_service.new_hires(e_client, settings)

    check_terms = sync_service.terms(e_client, settings)

    print(f"Not complete for new hires: {check_hires}\n")
    print(f"Not complete for terms: {check_terms}")

    email_mng = email_manager.EmailManager("Daily Hire/Term Sync Report", settings)
    email_mng.send_sync_report(check_hires, dont_check_hires, check_terms)


if __name__ == "__main__":
    main()
