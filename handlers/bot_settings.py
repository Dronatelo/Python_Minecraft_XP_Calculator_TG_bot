from aiogram import types,Dispatcher
from aiogram.types import ContentTypes
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.bot_settings_kb import settings_menu,menu
from keyboards.main_kb import main_menu

from settings.mail_sender import send_mail_file,mails
from settings.file_settings import excel_files,excel_files_path
from calculate_file import get_file_now_name,del_line,add_line

from datetime import date
date_today = date.today()
import os

def buty_print(mass):
        files_list =""
        for i in range(0,len(mass)):
            files_list += f'{i+1}. '+f'{mass[i]}'+"\n"
        return files_list

def this_file_name(n):
        files = os.listdir(excel_files)
        file_names = []
        for i in range(0,len(files)):
            file_names.append(f'{files[i]}')
            
        return file_names[n-1]

#@dp.message_handler(Text(equals='⚙️'), state=None)
async def menu_setting(message: types.Message):
    await message.answer(#"📧📗 - отправить текущую таблицу по почте;"+"\n"
                         '🔄📗 - Добавить таблицу'+'\n'+
                         '📚 - Выбрать excel файл'+'\n'+
                         '❌ - Удалить excel файл',
                         reply_markup=settings_menu)

#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True))
async def menu_def(message: types.Message):

    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

class send_excel_file(StatesGroup):
    get_mail_address = State()

#@dp.message_handler(Text(equals='📧📗'),state=None)
async def get_mail_for_send_table(message: types.Message, state: FSMContext):
    await message.answer("Введите адрес почты. ",reply_markup=menu)
    await send_excel_file.get_mail_address.set()

#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

#@dp.message_handler(state=send_excel_file.get_mail_address)
async def table_sender(message: types.Message, state: FSMContext):
    get_mail_user = message.text
    
    if get_mail_user in mails:
        
        send_mail_file("drediv88@gmail.com",get_mail_user,f"{get_file_now_name()}","File excel")

        await message.answer('Таблица отправлена на почту!', reply_markup=main_menu)
        await state.finish()
    else:
        await message.answer('Такой почты нет!', reply_markup=main_menu)
        await state.finish()

class replace_file_excel(StatesGroup):
    get_file = State()
    get_name_file = State()
        
#@dp.message_handler(Text(equals='🔄📗'),state=None)
async def replace_file(message: types.Message, state: FSMContext):
    await message.answer("Дайте название файлу",reply_markup=menu)
    await replace_file_excel.get_name_file.set()

#@dp.message_handler(state=replace_file_excel.get_name_file)
async def get_name_for_file_excel(message: types.Message, state: FSMContext):
    name_excel = message.text
    async with state.proxy() as data:
        data['name_excel'] = name_excel
    await message.answer("Отправьте новый файл для замены.",reply_markup=menu)
    await replace_file_excel.get_file.set()
     
#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

#@dp.message_handler(state=replace_file_excel.get_file,content_types=ContentTypes.DOCUMENT)
async def save_excel_file(message: types.Message, state: FSMContext):
    document = message.document

    derict = excel_files
    files = os.listdir(derict)
    document.file_name = "table_craft_"f'{date_today}.xlsx'
    print(document)
    
    async with state.proxy() as data:
        name_excel = data['name_excel']
    
    for i in range(0,len(files)):
        if document.file_name == files[i]:
            await document.download(destination_file=excel_files_path+f'{name_excel}_{date_today}_'f'{len(files)}.xlsx')
        else:
            await document.download(destination_file=excel_files_path+f'{name_excel}_{date_today}.xlsx')

    await message.answer('Файл 'f'{name_excel}_{date_today} cохранён!', reply_markup=main_menu)
    await state.finish()

class select_file(StatesGroup):
    sl_file = State()

#@dp.message_handler(Text(equals='📚'),state=None)
async def select_excel_file(message: types.Message, state: FSMContext):
    
    files = os.listdir(excel_files)
    
    await message.answer(buty_print(files))
    await message.answer("Сейчас выбран по умолчанию: "f'{get_file_now_name()}')
    await message.answer("Выберете файл для замены",reply_markup=menu)
    await select_file.sl_file.set()

#dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)

#@dp.message_handler(state=select_file.sl_file)
async def save_changes_save_excel_file_default(message: types.Message, state: FSMContext):
    name_file = message.text
        
    del_line()
    add_line(this_file_name(int(name_file)))

    await message.answer(f"Файл {this_file_name(int(name_file))} выбран!", reply_markup=main_menu)
    await state.finish()

class delete_file(StatesGroup):
    get_name_file_and_del = State()
#@dp.message_handler(Text(equals='❌'),state=None)
async def delete_excel_file(message: types.Message, state: FSMContext):
    files = os.listdir(excel_files)
    
    await message.answer(buty_print(files))
    await message.answer("Выберете файл для удаления",reply_markup=menu)
    await delete_file.get_name_file_and_del.set()

#@dp.message_handler(state=delete_file.get_name_file_and_del)
async def get_name_for_del(message: types.Message, state: FSMContext):
    name_file = message.text

    name = this_file_name(int(name_file))
    os.remove(excel_files_path+name)
    await message.answer(f"Удаление файла {name} произведено!",reply_markup=main_menu)
    await state.finish()
    
def register_handlers_bot_settings(dp: Dispatcher):
    dp.register_message_handler(menu_setting, Text(equals="⚙️"),state=None)
    dp.register_message_handler(menu_def,Text(equals='↩MENU',ignore_case=True))
    dp.register_message_handler(get_mail_for_send_table,Text(equals="📧📗"),state=None)
    dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
    dp.register_message_handler(table_sender,state=send_excel_file.get_mail_address)
    dp.register_message_handler(replace_file,Text(equals="🔄📗"),state=None)
    dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
    dp.register_message_handler(get_name_for_file_excel,state=replace_file_excel.get_name_file)
    dp.register_message_handler(save_excel_file,state=replace_file_excel.get_file,content_types=ContentTypes.DOCUMENT)
    dp.register_message_handler(select_excel_file,Text(equals="📚"),state=None)
    dp.register_message_handler(cancel_handler,Text(equals='↩MENU',ignore_case=True),state="*")
    dp.register_message_handler(save_changes_save_excel_file_default,state=select_file.sl_file)
    dp.register_message_handler(delete_excel_file,Text(equals='❌'),state=None)
    dp.register_message_handler(get_name_for_del,state=delete_file.get_name_file_and_del)
