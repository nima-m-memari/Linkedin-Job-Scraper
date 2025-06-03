import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Data_Mining():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def password(self, path):
        with open(path, "r") as file:
            lines = file.readlines()
            USERNAME = (lines[0].split(":", 1))[1].strip()
            PASSWORD = (lines[1].split(":", 1))[1].strip()
        return USERNAME, PASSWORD

    def login(self):
        Username, Password = Data_Mining.password(self, f"Linkedin-Job-Scraper/app/password.txt")
        #opening site
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

data = Data_Mining()
data.login()
