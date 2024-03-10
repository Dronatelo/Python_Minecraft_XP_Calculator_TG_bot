from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.main_kb import main_menu,start_button
from settings.mail_sender import send_mail_password

class connect_to_bot(StatesGroup):
    get_mail=State()
    logging=State()
#@dp.message_handler(commands='start',state=None)
async def start(message: types.Message, state=None):
    await message.answer("Ввведите Вашу почту",reply_markup=start_button)
    await connect_to_bot.get_mail.set()
     
#@dp.message_handler(state="*",commands = "cancel")

#@dp.message_handler(state=connect_to_bot.get_mail)
async def get_password_check_mail(message: types.Message, state: FSMContext):
    global check_password
    check_mail = message.text
    
    check_password = send_mail_password(check_mail)
    print(check_password)
    async with state.proxy() as data:
        data['password'] = check_password
    async with state.proxy() as data:
        data['mail'] = check_mail
        password = data['password'] 
        
    if type(password) != int:
        await message.answer("Проверьте правильность написания адреса эл.почты!")
        await state.finish()
        await start(message)
    else:
        await message.answer("Введите пароль",reply_markup=start_button)
        await connect_to_bot.logging.set()

#@dp.message_handler(state=connect_to_bot.logging)
async def try_loggining(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        password = data['password'] 
    input_password = message.text
    
    if str(input_password) == str(password):
        await message.answer('Вы успешно авторизовались✅', reply_markup=main_menu)
        await state.finish()  
    else:
        await message.answer('🚫Неверный пароль!🚫', reply_markup=start_button)
        await state.finish()

def register_handlers_start_connect(dp: Dispatcher):
    dp.register_message_handler(start,commands="start",state=None)
    dp.register_message_handler(get_password_check_mail,state=connect_to_bot.get_mail)
    dp.register_message_handler(try_loggining,state=connect_to_bot.logging)
