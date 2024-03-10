from aiogram import executor
from create_bot import dp
from handlers import start_connect, main_calculate, bot_settings

async def on_startup(_):
    print("Bot Online!")
    
start_connect.register_handlers_start_connect(dp)
main_calculate.register_handlers_main_items_calculate(dp)
bot_settings.register_handlers_bot_settings(dp)

def main():
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)

if __name__ == '__main__':
    main()
      