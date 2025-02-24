import requests
import time

class RecaptchaSolver:
    def __init__(self, api_key, sitekey, page_url):
        self.api_key = api_key
        self.sitekey = sitekey
        self.page_url = page_url
        self.solve_url = "http://2captcha.com/in.php"
        self.result_url = "http://2captcha.com/res.php"

    def request_captcha_solution(self):
        """Submits the sitekey to 2Captcha and gets a request ID."""
        payload = {
            "key": self.api_key,
            "method": "userrecaptcha",
            "googlekey": self.sitekey,
            "pageurl": self.page_url,
            "json": 1
        }
        response = requests.post(self.solve_url, data=payload)
        result = response.json()

        if result["status"] == 1:
            return result["request"]
        else:
            raise Exception(f"Failed to request captcha solving: {result}")

    def get_solved_captcha(self, request_id):
        """Retrieves the solved captcha token from 2Captcha."""
        for _ in range(30):  # Check every 5 seconds for up to 150 seconds
            time.sleep(5)
            payload = {"key": self.api_key, "action": "get", "id": request_id, "json": 1}
            response = requests.get(self.result_url, params=payload)
            result = response.json()

            if result["status"] == 1:
                return result["request"]
            elif result["request"] == "CAPCHA_NOT_READY":
                continue
            else:
                raise Exception(f"Failed to retrieve captcha solution: {result}")

        raise Exception("Captcha solving timeout exceeded.")

    def solve_recaptcha(self):
        """Main function to solve reCAPTCHA and return the solution."""
        request_id = self.request_captcha_solution()
        print(f"Captcha request sent. Request ID: {request_id}")

        solution = self.get_solved_captcha(request_id)
        print(f"Captcha solved successfully: {solution}")

        return solution

# Set your API Key and target details
API_KEY = "4ed6fc69aea6bac555b4a2bb6301c2bc"  # Replace with your 2Captcha API key
SITEKEY = "6LcmkRIpAAAAAC5CvZ4DogDYSUX8Az0FYG4Xjya9"  # Found in request
PAGE_URL = "https://playboard.co/en/account/signup"  # The page where captcha is located

solver = RecaptchaSolver(API_KEY, SITEKEY, PAGE_URL)
captcha_solution = solver.solve_recaptcha()

# Now, you need to send this solution to the target website
print(f"Solved reCAPTCHA Token: {captcha_solution}")
