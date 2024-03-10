import dotenv
import os

dotenv.load_dotenv("/BOTS/MINI_BOT/settings/.env")
API_KEY_TG = os.environ["API_KEY_TG"]

data_items_path = "/BOTS/MINI_BOT/settings/data_items.json"
now_file_name_path = "/BOTS/MINI_BOT/settings/now_file_name.txt"
excel_files_path = "/BOTS/MINI_BOT/xmls_files/"
excel_files="/BOTS/MINI_BOT/xmls_files"