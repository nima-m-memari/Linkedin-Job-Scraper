import os

main_path = os.path.dirname(os.path.dirname(__file__))
# cache_path = os.path.join(main_path, "app", "cache", "cache.json")
# if os.path.exists(cache_path):
#     os.remove(cache_path)
command = f"streamlit run \"{os.path.join(main_path, "app", "GUI.py")}\""
os.system(command)