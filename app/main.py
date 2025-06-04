from preq.preq import *
from Data_Mining import *
from CSV_Editor import *

x=Data_Mining()
x.login()
x.jobs("python", "united state")
x.job_scraper(60)

y=CSV_Editor()
y.edited_csv()