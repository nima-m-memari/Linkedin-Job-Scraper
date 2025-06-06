from preq.preq import *
from Data_Mining import *
from CSV_Editor import *

class Pages:
    def home_page(self):
        st.set_page_config("Home")
        st.title("Linkedin Job Scraper")

        if "name" not in st.session_state:
            with st.form("name_form"):
                name = st.text_input("Enter your name").strip()
                submitted = st.form_submit_button("Enter")

            if submitted:
                if not name.strip():
                    st.warning("Your name can't be blank")
                else:
                    st.session_state["name"] = name
                    st.success(f"Hello {name}")
                    self.loading("Loading...")
                    st.session_state["current_page"] = "login_page"
                    st.rerun()
        else:
            st.session_state["current_page"] = "login_page"
            st.rerun()

    def login_page(self):
        st.set_page_config("Account")
        st.title("Linkedin Job Scraper")
        cookies_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "cache", "cookies.pkl")
        
        if os.path.exists(cookies_path):
            st.write(f"Welcome Back {st.session_state["name"]}")
            continue_button = st.button("Continue")
            sign_out_button = st.button("Sign Out")
            back_button = st.button("Back")
            if continue_button:
                st.session_state["current_page"] = "job_page"
                self.loading("Loading...")
                st.rerun()
            elif sign_out_button:
                Data_Mining().log_out()
                self.loading("Signing Out...")
                st.rerun()
            elif back_button:
                del st.session_state["name"]
                st.session_state["current_page"] = "home_page"
                self.loading("Loading...")
                st.rerun()
        else:
            st.write(f"Welcome Back {st.session_state["name"]}")
            st.write(f"Please Consider Logining To Your Linkedin Account To Continue")
            if not st.session_state.get("login_progress", False):
                sign_in_button = st.button("Sign In")
                back_button = st.button("Back")
                if sign_in_button:
                    st.session_state["login_progress"] = True
                    st.rerun()

                elif back_button:
                    del st.session_state["name"]
                    st.session_state["current_page"] = "home_page"
                    self.loading("Loading...")
                    st.rerun()
            else:
                sign_in_button = st.button("Sign In", disabled=True)
                back_button = st.button("Back", disabled=True)
                with st.spinner("Please Wait For Login To Be Complete..."):
                    Data_Mining().login()
                del st.session_state["login_progress"]
                st.rerun()

    def job_page(self):
        st.set_page_config("Search")
        st.title("Job Search")

        with st.form("job_search_form"):
            job_counts = st.slider("How Many Jobs Do You Want Me To Search?", min_value=1, max_value=100, value=10, step=1)
            job_title = st.text_input("Job Title").strip()
            job_location = st.text_input("Job Location").strip()
            submitted = st.form_submit_button("Search")

            if submitted:
                self.loading("Loading...")
                if (not job_title) or (not job_location):
                    st.warning("Please fill in both the Job Title and Job Location.")
                else:
                    st.success("Inputs Received Successfully.")
                    st.session_state["job_counts"] = job_counts
                    st.session_state["job_title"] = job_title
                    st.session_state["job_location"] = job_location
                    st.session_state["current_page"] = "job_scraper"
                    st.rerun()

        back_button = st.button("Back")
        if back_button:
            st.session_state["current_page"] = "login_page"
            self.loading("Loading...")
            st.rerun()
    
    def job_scraper(self):
        st.set_page_config("Searching...")
        st.title("Searching...")
        with st.spinner("Please Wait..."):
            time.sleep(2)
            temp = Data_Mining()
            temp.login()
            temp.jobs(st.session_state["job_title"], st.session_state["job_location"])
            temp.job_scraper(st.session_state["job_counts"])
            CSV_Editor().edited_csv()
        st.session_state["current_page"] = "show_jobs"
        st.rerun()

    def show_jobs(self):
        #This Function Is Made By ChatGPT
        st.set_page_config("Results", layout="wide")
        st.title("Job Results")

        # بارگیری داده
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "cache", "job_data.csv")
        df = pd.read_csv(csv_path)

        # حذف ستون ID در صورت وجود
        if "ID" in df.columns:
            df = df.drop(columns=["ID"])

        # محدود کردن تعداد ردیف‌ها بر اساس مقدار ذخیره‌شده
        df = df.head(st.session_state.get("job_counts", len(df)))

        # شماره‌گذاری از 1 و ساخت لینک کلیک‌پذیر
        df.insert(0, "No", range(1, len(df) + 1))
        df["Link"] = df["Link"].apply(lambda url: f"https://www.linkedin.com/jobs/view/{url.strip().split('/')[-2]}/")

        # وسط‌چین کردن ستون‌های No و Link
        df["No"] = df["No"].apply(lambda x: f"<div style='text-align:center'>{x}</div>")
        df["Link"] = df["Link"].apply(lambda url: f"<div style='text-align:center'><a href='{url}' target='_blank'>View</a></div>")

        # بزرگ کردن ستون Salary و جایگزینی — به جای مقادیر خالی
        if "Salary" in df.columns:
            df["Salary"] = df["Salary"].apply(
                lambda val: f"<div style='min-width:150px'>{val}</div>" if pd.notna(val) else "<div style='min-width:150px; text-align:center'>—</div>"
            )

        # تولید HTML و وسط‌چین کردن عنوان ستون‌ها
        html_table = df.to_html(escape=False, index=False)
        html_table = html_table.replace('<th>', "<th style='text-align:center'>")

        # نمایش جدول
        st.markdown(html_table, unsafe_allow_html=True)
        
        if st.button("Quit"):
            self.loading("Quiting...")
            os.kill(os.getpid(), signal.SIGTERM)
        # دکمه برگشت
        if st.button("Back"):
            st.session_state["current_page"] = "job_page"
            self.loading("Loading...")
            st.rerun()

    def loading(self, text:str):
        with st.spinner(text):
            time.sleep(2)

if "pages_class" not in st.session_state:
    st.session_state["pages_class"] = Pages()

current_page = st.session_state.get("current_page", "home_page")

if current_page == "home_page":
    st.session_state["pages_class"].home_page()
elif current_page == "login_page":
    st.session_state["pages_class"].login_page()
elif current_page == "job_page":
    st.session_state["pages_class"].job_page()
elif current_page == "job_scraper":
    st.session_state["pages_class"].job_scraper()
elif current_page == "show_jobs":
    st.session_state["pages_class"].show_jobs()