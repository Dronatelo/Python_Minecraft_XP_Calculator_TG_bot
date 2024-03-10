from datetime import date
from aiogram import types,Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.main_kb import main_menu,menu
from calculate_file import calculate_data, output_data,data_items_path,find_data_name,find_data_id_bot

date_today = date.today()

global calcul_data,calcul_account
calcul_data = [0,0,0,0]
calcul_account = []

def zeroing():
    calcul_account.clear()
    calcul_data[0]=0
    calcul_data[1]=0
    calcul_data[2]=0
    calcul_data[3]=0
     
class calculate(StatesGroup):
    get_id_items=State()
    get_amount=State()
    final_sum=State()

#@dp.message_handler(Text(equals='🧮'),state=None)
async def start_calculate_item(message: types.Message):
    get_data_list = output_data(data_items_path)
    await message.answer(get_data_list)
    await message.answer("Выберете id ресурса! ",reply_markup=menu)
    await calculate.get_id_items.set()

#@dp.message_handler(state="*",commands = "cancel")
#@dp.message_handler(Text(equals='cancel',ignore_case=True),state="*")
async def cancel_handler(message: types.Message,state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Вы возвращены в меню!",reply_markup=main_menu)
      
#@dp.message_handler(state=calculate.get_id_items)
async def get_id_item(message: types.Message, state: FSMContext):
    check_id_item = message.text
    if check_id_item == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
    else:
        if check_id_item == find_data_id_bot(check_id_item):
            async with state.proxy() as data:
                    data['id_item'] = check_id_item
            await message.answer("Введите количество ресурcа")
            await calculate.get_amount.set()
        else:
            await message.answer(f"Error id! That ID '{check_id_item}' doesn't exist!", reply_markup=main_menu)
            await state.finish()
        
#@dp.message_handler(state=calculate.get_amount)
async def main_calculate_def(message: types.Message, state: FSMContext):
    set_ammount = message.text
    
    if set_ammount == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
    else:
        try:
            async with state.proxy() as data:
                id_item = data['id_item']
            int_set_ammount = int(set_ammount)

            get_calcul_account = f"{find_data_name(id_item)} x "+f"{int_set_ammount}"
            calcul_account.append(get_calcul_account)
            
            print(calcul_account)


            x,y,j,k=calculate_data(data_items_path,id_item,int_set_ammount)
            async with state.proxy() as data:
                data['x'] = x
                data['y'] = y
                data['j'] = j
                data['k'] = k
                
            async with state.proxy() as data:
                x=data['x']
                y=data['y']
                j=data['j']
                k=data['k']

            calcul_data[0]+=x
            calcul_data[1]+=y
            calcul_data[2]+=j
            calcul_data[3]+=k

            choice = ['Да','Вывести','↩MENU']
            choice_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            choice_kb.add(*choice)
            await message.answer('Проделать ещё расчёт?', reply_markup=choice_kb)
            await calculate.final_sum.set()
        except:
            def debug():
                import sys
                frame = sys._getframe(1)

                name = frame.f_code.co_name
                line_number = frame.f_lineno
                filename = frame.f_code.co_filename

                # return 'File "%s", line %d, in %s: %s' % (filename, line_number, name)
                return line_number
            
            print("Error code! Line: ",debug())
            await message.answer("Error: Wrong type of second variable!", reply_markup=main_menu)
            await state.finish()
            zeroing()
     
#@dp.message_handler(state=calculate.final_sum)
async def end_calculate(message: types.Message, state: FSMContext):
    user_answer = message.text

    if user_answer == "↩MENU":
        await message.answer('Вы возвращены в меню❗', reply_markup=main_menu)
        await state.finish()
        
    elif(user_answer == "Да"):
        await message.answer("Выберете id ресурса!")
        await calculate.get_id_items.set()

    elif(user_answer=="Вывести"):
        def buty_print(massive):
            string_print =""
            for i in range(len(massive)):
                string_print+=f'{massive[i]}'+"\n"
            return string_print

        def answer():
            answ = ""
            answ +="Craft XP: "f'{round(calcul_data[0],2)}'+"\n"
            if calcul_data[1] == 0:
                pass
            else:
                answ +="Smit XP: "f'{round(calcul_data[1],2)}'+"\n"
            if calcul_data[2] == 0:
                pass
            else:
                answ +="Magic XP: "f'{round(calcul_data[2],2)}'+"\n"
            if calcul_data[3]==0:
                pass
            else:
                answ +="Create XP: "f'{round(calcul_data[3],2)}'
            return answ
            
        await message.answer(buty_print(calcul_account))
        #'Craft XP: 'f'{round(calcul_data[0],2)}'+'\n'+'Smit XP: 'f'{round(calcul_data[1],2)}'+"\n"+""
        await message.answer(answer(),reply_markup=main_menu)
        await state.finish()
        zeroing()

    else:
        await message.answer("Error command", reply_markup=main_menu)
        await state.finish()
        zeroing()
              
def register_handlers_main_items_calculate(dp: Dispatcher):
    dp.register_message_handler(start_calculate_item, Text(equals="🧮"),state=None)
    dp.register_message_handler(cancel_handler,state="*",commands="cancel")
    dp.register_message_handler(cancel_handler,Text(equals='cancel',ignore_case=True),state="*")
    dp.register_message_handler(get_id_item,state=calculate.get_id_items)
    dp.register_message_handler(main_calculate_def,state=calculate.get_amount)
    dp.register_message_handler(end_calculate,state=calculate.final_sum)
