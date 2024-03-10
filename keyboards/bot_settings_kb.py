from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#send_table_mail = KeyboardButton("📧📗")
replace_table= KeyboardButton("🔄📗")
set_excel_file = KeyboardButton("📚")
del_excel_file = KeyboardButton("❌")

menu_bt = KeyboardButton("↩MENU")

settings_menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu = ReplyKeyboardMarkup(resize_keyboard=True)

settings_menu.add(replace_table,set_excel_file,del_excel_file,menu_bt)

menu.add(menu_bt)

