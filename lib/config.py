import os

app_data_dir= os.path.join(os.environ.get("USERPROFILE"),"AppData","Roaming","codx")
os.makedirs(app_data_dir,exist_ok=True)