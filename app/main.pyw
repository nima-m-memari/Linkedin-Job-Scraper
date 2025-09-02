import os

main_path = os.path.dirname(os.path.dirname(__file__))
command = f"streamlit run \"{os.path.join(main_path, "app", "GUI.py")}\" --server.port 2404"
os.system(command)