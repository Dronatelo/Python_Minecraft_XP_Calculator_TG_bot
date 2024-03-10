from aiogram import types
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import main_menu,menu
from create_bot import dp

#@dp.message_handler(Text(equals='📗'))
async def ip_message(message: types.Message, state: FSMContext):
    start_buttons = ["📝",'✏️','❌','↩MENU']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    prnt = out_data(data_items_path)
    await message.answer(prnt)
    await message.answer("📝 - добавить новый предмет;"+"\n"+'✏️ - редактировать предмет;'+"\n"+"❌ - удалить предмет;",reply_markup=keyboard)

class add_item(StatesGroup):
    id_item=State()
    name_item=State()
    craft_xp=State()
    smit_xp=State()      
#@dp.message_handler(Text(equals='📝'))
async def ip_message(message: types.Message, state: FSMContext):
    start_buttons = ['↩MENU']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer("Введите id ресурcа. ",reply_markup=keyboard)
    await add_item.id_item.set()

#@dp.message_handler(state=add_item.id_item)
async def ip_message(message: types.Message, state: FSMContext):
    id_items = message.text
    if id_items == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['id_items'] = id_items

        await message.answer("Введите название ресурcа")
        await add_item.name_item.set()

#@dp.message_handler(state=add_item.name_item)
async def ip_message(message: types.Message, state: FSMContext):
    name_items = message.text
    if name_items == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['name_items'] = name_items

        await message.answer("Введите данные craft ресурcа")
        await add_item.craft_xp.set()

#@dp.message_handler(state=add_item.craft_xp)
async def ip_message(message: types.Message, state: FSMContext):
    craft_xp = message.text
    if craft_xp == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['craft_xp'] = craft_xp

        await message.answer("Введите данные smit ресурcа")
        await add_item.smit_xp.set()

#@dp.message_handler(state=add_item.smit_xp)
async def ip_message(message: types.Message, state: FSMContext):
    smit_xp = message.text
    if smit_xp == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['smit_xp'] = smit_xp

        async with state.proxy() as data:
                sm = data['smit_xp']
                cr = data['craft_xp']
                nm = data['name_items']
                idi = data['id_items']
        
        add_data(idi,nm,cr,sm)

        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Предмет добавлен!', reply_markup=keyboard)
        await state.finish()

class edit_item(StatesGroup):
    check_id = State()
    e_id_item=State()
    e_name_item=State()
    e_craft_xp=State()
    e_smit_xp=State()
      
#@dp.message_handler(Text(equals='✏️'))
async def ip_message(message: types.Message, state: FSMContext):
    start_buttons = ['↩MENU']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer("Введите id ресурcа, который хотите заменить. ",reply_markup=keyboard)
    await edit_item.check_id.set()

#@dp.message_handler(state=edit_item.check_id)
async def ip_message(message: types.Message, state: FSMContext):
    che_id = message.text
    if che_id == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['che_id'] = che_id

        await message.answer("Введите новый id, на который хотите заменить")
        await edit_item.e_id_item.set() 

#@dp.message_handler(state=edit_item.e_id_item)
async def ip_message(message: types.Message, state: FSMContext):
    e_id_items = message.text
    if e_id_items == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['e_id_item'] = e_id_items

        await message.answer("Введите новое название предмета")
        await edit_item.e_name_item.set() 

#@dp.message_handler(state=edit_item.e_name_item)
async def ip_message(message: types.Message, state: FSMContext):
    e_name_items = message.text
    if e_name_items == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['e_name_item'] = e_name_items

        await message.answer("Введите новое значение craft xp")
        await edit_item.e_craft_xp.set()

#@dp.message_handler(state=edit_item.e_craft_xp)
async def ip_message(message: types.Message, state: FSMContext):
    e_craft_xps = message.text
    if e_craft_xps == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['e_craft_xp'] = e_craft_xps

        await message.answer("Введите новое значение smit xp")
        await edit_item.e_smit_xp.set()  

#@dp.message_handler(state=edit_item.e_smit_xp)
async def ip_message(message: types.Message, state: FSMContext):
    e_smit_xps = message.text
    if e_smit_xps == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:
        async with state.proxy() as data:
                data['e_smit_xp'] = e_smit_xps
        async with state.proxy() as data:
                che_id = data['che_id']
                smm = data['e_smit_xp']
                crf = data['e_craft_xp']
                nmr = data['e_name_item']
                idid = data['e_id_item']

        fdcid = find_data_id(che_id)
        edit_data(fdcid,idid,nmr,crf,smm)

        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Предмет изменён!', reply_markup=keyboard)
        await state.finish()

class del_item(StatesGroup):
    del_proc_id = State()
      
#@dp.message_handler(Text(equals='❌'))
async def ip_message(message: types.Message, state: FSMContext):
    start_buttons = ['↩MENU']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer("Введите id ресурcа, который хотите удалить. ",reply_markup=keyboard)
    await del_item.del_proc_id.set()

#s@dp.message_handler(state=del_item.del_proc_id)
async def ip_message(message: types.Message, state: FSMContext):
    del_id = message.text
    if del_id == "↩MENU":
        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Вы возвращены в меню❗', reply_markup=keyboard)
        await state.finish()
    else:

        num_del = find_data_id(del_id)
        
        delete_data(num_del) 

        start_buttons = ['🧮XP','📗','⚙️','↩MENU']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer('Предмет удалён!', reply_markup=keyboard)
        await state.finish()