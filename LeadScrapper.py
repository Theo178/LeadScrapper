from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from modules.tempmail import TempMail  # Your temp mail class
from modules.captcha import RecaptchaSolver  # Your captcha solving class

# Initialize browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Step 1: Generate a Temporary Email
temp_mail = TempMail()
email = temp_mail.email
print(f"Generated Email: {email}")

# Step 2: Open Signup Page
driver.get("https://playboard.co/en/account/signup")
time.sleep(3)  # Wait for page to load

# Step 3: Fill in Form
name = "TestUser"
password = "SecurePassword123!"

driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "name").send_keys(name)
driver.find_element(By.NAME, "password").send_keys(password)

# Step 4: Solve CAPTCHA
solver = RecaptchaSolver(api_key="4ed6fc69aea6bac555b4a2bb6301c2bc")
site_key = "6LcmkRIpAAAAAC5CvZ4DogDYSUX8Az0FYG4Xjya9"  # Extracted sitekey
captcha_token = solver.solve_recaptcha(site_key, driver.current_url)
captcha_input = driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{captcha_token}';")
time.sleep(2)  # Wait for token to be registered

# Step 5: Submit the Form
driver.find_element(By.XPATH, '//button[text()="Sign Up"]').click()
time.sleep(5)

# Step 6: Open Email and Click Verification Link
print("Checking for verification email...")
verification_link = temp_mail.get_verification_link()
if verification_link:
    driver.get(verification_link)
    print("Email verified successfully!")
else:
    print("No verification email received.")

# Close browser
driver.quit()
