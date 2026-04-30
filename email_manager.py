import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from config import Settings


class EmailManager:
    def __init__(self, subject, settings: Settings):
        self.subject = subject
        self.settings = settings

    def send_email(self, message):

        recipients = [self.settings.EMAIL_HR, self.settings.EMAIL_FROM]

        msg = MIMEMultipart("alternative")
        msg["Subject"] = self.subject
        msg["From"] = self.settings.EMAIL_FROM
        msg["To"] = ", ".join(recipients)

        # plain text body with the word "test"
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP_SSL(
            self.settings.SMTP_HOST, self.settings.SMTP_PORT
        ) as server:
            server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
            server.sendmail(self.settings.EMAIL_FROM, recipients, msg.as_string())
        print("\n📧 Email")

    def send_sync_report(
        self, hires_data, dont_check_hires_data, terms_data, send=True
    ):

        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("sync_report.html")
        html_content = template.render(
            hires=hires_data,
            dont_check_hires=dont_check_hires_data,
            terms=terms_data,
        )

        msg = MIMEMultipart("alternative")
        msg["Subject"] = self.subject
        msg["From"] = self.settings.EMAIL_FROM
        msg["To"] = self.settings.REPORT_RECIPIENT

        # plain text body with the word "test"
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP_SSL(
            self.settings.SMTP_HOST, self.settings.SMTP_PORT
        ) as server:
            server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
            server.sendmail(
                self.settings.EMAIL_FROM,
                self.settings.REPORT_RECIPIENT,
                msg.as_string(),
            )
        print("\n📧 Email sent for report")
