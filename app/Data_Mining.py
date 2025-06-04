from preq.preq import *

class Data_Mining():
    def __init__(self):
        #main path (Linkedin-Job-Scraper)
        self.path = os.path.dirname(os.path.dirname(__file__))
        driver_path = os.path.join(self.path, "app", "preq", "chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(driver_path))

    def password(self):
        password_path = os.path.join(self.path, "app", "preq", "password.txt")
        with open(password_path, "r") as file:
            lines = file.readlines()
            USERNAME = (lines[0].split(":", 1))[1].strip()
            PASSWORD = (lines[1].split(":", 1))[1].strip()
        return USERNAME, PASSWORD

    def login(self):
        Username, Password = self.password()
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

    def job_scraper(self, counts:int):
        def loop_count(counts:int):
            if counts:
                if counts % 25 == 0:
                    return counts//25
                else:
                    loop_counts = ((counts//25) + 1)
                    return loop_counts
            else:
                return 1
        
        job_data = list()

        for i in range(loop_count(counts)):
            time.sleep(2)
            jobs = self.driver.find_elements(By.XPATH, "//li[@data-occludable-job-id]")
            for job in jobs:
                self.driver.execute_script("arguments[0].scrollIntoView();", job)

                try:
                    job_id = job.get_attribute("data-occludable-job-id")

                    job_title_element = job.find_element(By.XPATH, ".//a[contains(@class, 'job-card-container__link')]")
                    job_title = job_title_element.text.strip()

                    company_element = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__subtitle')]")
                    company_name = company_element.text.strip()

                    location_element = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__caption')]//li")
                    location = location_element.text.strip()

                    try:
                        salary_element = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__metadata')]//li")
                        salary = salary_element.text.strip()
                    except:
                        salary = "None"

                    job_data.append({
                        'ID': job_id,
                        'Link': f"https://www.linkedin.com/jobs/view/{job_id}/",
                        'Title': job_title,
                        'Company': company_name,
                        'Location': location,
                        'Salary': salary
                    })

                except:
                    continue
            
            time.sleep(2)
            next_button_element = self.driver.find_element(By.XPATH, "//button[@aria-label='View next page']")
            next_button_element.click()
        
        job_data_path = os.path.join(self.path, "app", "preq", "job_data.csv")
        with open(job_data_path, "w", newline='') as jobs_data:
            writer = csv.DictWriter(jobs_data, fieldnames=["ID", "Link", "Title", "Company", "Location", "Salary"])
            writer.writeheader()
            writer.writerows(job_data)