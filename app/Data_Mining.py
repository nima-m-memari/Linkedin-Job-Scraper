import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Data_Mining():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def password(self, path:str):
        with open(path, "r") as file:
            lines = file.readlines()
            USERNAME = (lines[0].split(":", 1))[1].strip()
            PASSWORD = (lines[1].split(":", 1))[1].strip()
        return USERNAME, PASSWORD

    def login(self):
        Username, Password = self.password(f"Linkedin-Job-Scraper/app/password.txt")
        #opening login url
        self.driver.get("https://www.linkedin.com/login/")
        self.driver.maximize_window()
        time.sleep(5)
        #typing username
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys(Username)
        time.sleep(1)
        #typing password
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(Password)
        time.sleep(1)
        #entering "Enter" key on keyboard
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

    def jobs(self, job_name:str, location:str):
        #opening jobs url
        self.driver.get("https://www.linkedin.com/jobs/")
        time.sleep(5)
        #typing job name
        job_name_input = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]')
        job_name_input.clear()
        job_name_input.send_keys(job_name)
        time.sleep(1)
        #typing location
        location_input = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="City, state, or zip code"]')
        location_input.clear()
        location_input.send_keys(location)
        time.sleep(1)
        #entering "Enter" key on keyboard
        location_input.send_keys(Keys.RETURN)
        time.sleep(5)

data = Data_Mining()
data.login()
data.jobs('python', 'united states')

