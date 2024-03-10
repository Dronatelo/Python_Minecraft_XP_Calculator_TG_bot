from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

calculate_bt = KeyboardButton("🧮")
#make_excel_bt = KeyboardButton("📗") временно функционал отключён
bot_settings_bt = KeyboardButton("⚙️")

menu_bt = KeyboardButton("↩MENU")
start_bt = KeyboardButton("/start")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu = ReplyKeyboardMarkup(resize_keyboard=True)
start_button = ReplyKeyboardMarkup(resize_keyboard=True)

main_menu.add(calculate_bt,bot_settings_bt)
menu.add(menu_bt)
start_button.add(start_bt)