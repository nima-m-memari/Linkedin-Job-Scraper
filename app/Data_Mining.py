from preq.preq import *

class Data_Mining():
    def __init__(self):
        #main path (Linkedin-Job-Scraper)
        self.path = os.path.dirname(os.path.dirname(__file__))
        driver_path = os.path.join(self.path, "app", "preq", "chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(driver_path))

    def login(self):
        cookies_path = os.path.join(self.path, "app", "cache", "cookies.pkl")
        driver = self.driver
        
        def is_logged_in():
            try:
                driver.find_element(By.ID, "global-nav")
                return True
            except:
                return False            
            
        def save_cookies():
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie["name"] == "li_at":
                    pickle.dump(cookie, open(cookies_path, "wb"))
                    break
        
        def load_cookies():
            if not os.path.exists(cookies_path):
                return False
            
            cookies = pickle.load(open(cookies_path, "rb"))
            
            driver.get("https://www.linkedin.com/")
            time.sleep(2)
            try:
                if cookies["name"] == "li_at":
                    driver.add_cookie({
                        "name": "li_at",
                        "value": cookies["value"],
                        "domain": ".linkedin.com"
                    })
            except:
                pass
            time.sleep(2)
            
            return True
        
        def start():            
            #seeing if we can log in with cookies
            if load_cookies():
                driver.get("https://www.linkedin.com/")
                driver.minimize_window()
                time.sleep(2)
                if is_logged_in():
                    return
                
            #user must sign in
            driver.get("https://www.linkedin.com/login/")
            driver.maximize_window()
            #it will wait until user signed in
            while True:
                if "/feed" in driver.current_url:
                    break
                time.sleep(1)
            
            #saving cookies for next time login
            if is_logged_in():
                save_cookies()
        
        start()

    def log_out(self):
        cookies_path = os.path.join(self.path, "app", "cache", "cookies.pkl")
        if os.path.exists(cookies_path):
            os.remove(cookies_path)

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
        
        job_data_path = os.path.join(self.path, "app", "cache", "job_data.csv")
        with open(job_data_path, "w", newline='') as jobs_data:
            writer = csv.DictWriter(jobs_data, fieldnames=["ID", "Link", "Title", "Company", "Location", "Salary"])
            writer.writeheader()
            writer.writerows(job_data)