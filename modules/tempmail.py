import requests
import urllib.parse
import random

class TempMail:
    def __init__(self):
        """Initialize TempMail object with a random email."""
        self.BASE_URL = "https://privatix-temp-mail-v1.p.rapidapi.com/request"
        self.HEADERS = {
            "x-rapidapi-host": "privatix-temp-mail-v1.p.rapidapi.com",
            "x-rapidapi-key": "cc49edd246msh7f5b0cc796687d4p19f428jsnf2b9ce580e27"
        }
        self.email = self.generate_email()

    def get_domains(self):
        """Fetch available domains for temp email."""
        url = f"{self.BASE_URL}/domains/"
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code == 200:
            return response.json()
        return []

    def generate_email(self):
        """Create a random temp email using available domains."""
        domains = self.get_domains()
        if not domains:
            raise Exception("Failed to fetch available domains.")
        
        email = f"user{random.randint(1000, 9999)}@{random.choice(domains)}"
        print(f"Generated Temp Email: {email}")
        return email

    def get_email_list(self):
        """Fetch list of received emails and return message IDs."""
        # Extract only the local part of the email before '@'
        local_part = self.email.split('@')[0]
        encoded_email = urllib.parse.quote(local_part)
        
        url = f"{self.BASE_URL}/mail/id/{encoded_email}/"
        response = requests.get(url, headers=self.HEADERS)

        if response.status_code == 200:
            emails = response.json()
            if isinstance(emails, dict) and "error" in emails:
                return []
            return emails  # List of emails with their IDs
        
        return []

    def get_email_content(self):
        """Fetch the content of the latest received email."""
        emails = self.get_email_list()
        if not emails:
            return "No emails received yet."

        latest_email_id = emails[0]["mail_id"]  # Extract first email ID
        url = f"{self.BASE_URL}/mail/id/{latest_email_id}/"
        response = requests.get(url, headers=self.HEADERS)

        if response.status_code == 200:
            return response.json()
        return "Failed to fetch email content."

# Usage
temp_mail = TempMail()
print(f"Your Temp Email: {temp_mail.email}")

# Get emails
emails = temp_mail.get_email_list()
if emails:
    print("Email IDs:", [email["mail_id"] for email in emails])
    latest_email = temp_mail.get_email_content()
    print("Latest Email Content:", latest_email)
else:
    print("No emails received yet.")
