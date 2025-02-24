import requests
import time

class TempMail:
    BASE_URL = "https://www.1secmail.com/api/v1/"
    
    def __init__(self):
        self.email = self.generate_email()

    def generate_email(self):
        """Generates a new temporary email."""
        response = requests.get(f"{self.BASE_URL}?action=genRandomMailbox")
        if response.status_code == 200:
            email = response.json()[0]
            print(f"Generated Email: {email}")
            return email
        else:
            raise Exception("Failed to generate email")

    def get_messages(self):
        """Fetches the list of received messages."""
        username, domain = self.email.split("@")
        response = requests.get(f"{self.BASE_URL}?action=getMessages&login={username}&domain={domain}")
        if response.status_code == 200:
            messages = response.json()
            if messages:
                print(f"📩 {len(messages)} new email(s) received!")
                return messages
            else:
                print("📭 No new emails yet...")
                return []
        else:
            raise Exception("Failed to fetch messages")

    def read_email(self, email_id):
        """Fetches and prints details of a specific email."""
        username, domain = self.email.split("@")
        response = requests.get(f"{self.BASE_URL}?action=readMessage&login={username}&domain={domain}&id={email_id}")
        if response.status_code == 200:
            email_data = response.json()
            print(f"\n📧 Email from: {email_data['from']}")
            print(f"📌 Subject: {email_data['subject']}")
            print(f"📝 Body:\n{email_data['textBody']}")
        else:
            raise Exception("Failed to read email")


# Example Usage:
if __name__ == "__main__":
    temp_mail = TempMail()
    
    print("\n📬 Checking for new emails...")
    time.sleep(5)  # Wait a few seconds before checking

    messages = temp_mail.get_messages()
    
    if messages:
        for msg in messages:
            temp_mail.read_email(msg['id'])
