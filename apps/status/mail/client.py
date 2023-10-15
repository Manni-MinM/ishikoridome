import requests

from config import Config

from requests.packages.urllib3.util.retry import Retry


class MailgunClient:
    def __init__(self):
        domain_name = Config.MAILGUN_DOMAIN_NAME
        self.base_url = f"https://api.mailgun.net/v3/{domain_name}/messages"
        self.base_email = f"mailgun@{domain_name}"
        self.timeout = Config.MAILGUN_TIMEOUT_SECONDS
        self.retry_strategy = Retry(
            backoff_factor=0.5,
            total=Config.MAILGUN_RETRIES,
        )
        self.session = requests.Session()
        self.session.auth = ("api", Config.MAILGUN_API_KEY)

    def send_mail(self, target_email, subject, text):
        resp = self.session.post(
            self.base_url,
            timeout=self.timeout,
            data={
                "from": self.base_email,
                "to": [{target_email}],
                "subject": subject,
                "text": text,
            },
        )

        resp.raise_for_status()

        data = resp.json()
        return data
