import re
import os
import csv

class CSV_Editor():
    def __init__(self):
        #main path (Linkedin-Job-Scraper)
        self.path = os.path.dirname(os.path.dirname(__file__))

    def clean_salary(self, text:str):
        match = re.search(r"\$[\d.,K]+/?[a-z]+(?:\s*-\s*\$[\d.,K]+/?[a-z]+)?", text)
        if match:
            return match.group()
        else:
            return "None"
    
    def edited_csv(self):
        fieldnames=["ID", "Link", "Title", "Company", "Location", "Salary", "Work Arrangement"]
        
        job_data_path = os.path.join(self.path, "app", "preq", "job_data.csv")
        temp_path = os.path.join(self.path, "app", "preq", "temp.csv")
        with open(job_data_path, 'r') as old:
            with open(temp_path, 'w', newline='') as new:
                csv_reader = csv.DictReader(old)
                csv_writer = csv.DictWriter(new, fieldnames=fieldnames)
                csv_writer.writeheader()

                for line in csv_reader:
                    line["Salary"] = self.clean_salary(line["Salary"].strip())
                    
                    try:
                        line["Title"] = (line["Title"].strip().split("\n"))[0]
                    except:
                        pass
                    
                    try:
                        line["Work Arrangement"] = (line["Location"].strip().strip(')').split('('))[1]
                    except:
                        pass

                    try:
                        line["Location"] = (line["Location"].strip().strip(')').split('('))[0]
                    except:
                        pass
                    
                    csv_writer.writerow(line)
                
        self.replace(job_data_path, temp_path)
    
    def replace(self, old_file_path, new_file_path):
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
        if os.path.exists(new_file_path):
            os.rename(new_file_path, old_file_path)

x=CSV_Editor()
x.edited_csv()