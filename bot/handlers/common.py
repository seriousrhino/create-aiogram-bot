from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand, BotCommandScopeAllPrivateChats
from keyboards.menu import generate_menu, generate_new_user_menu
from utils.config import BOT_TOKEN, BOT_NAME

router = Router()
router.message.filter(F.chat.type == "private")

async def set_bot_commands(bot: Bot):
    
    # commands = [
    #         BotCommand(command="help", description="All available commands"),
    #         BotCommand(command="wallet", description="Set your wallet"),
    #         BotCommand(command="buy", description="Buy tokens"),
    #         BotCommand(command="sell", description="Sell tokens"),
    #         BotCommand(command="top", description="See trending tokens"),
    # ]
    # await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    
    return True
    

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    
    preload_message = await message.answer("Loading bot...")
    
    await state.clear()

    # chat_id = message.chat.id
    chat_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # user_data = {
    #     'chat_id': chat_id,
    #     'username': username,
    #     'first_name': first_name,
    #     'last_name': last_name,
    # }

    # Calling create_if_not_exists function
    # user_record = await user_manager.create_if_not_exists(user_data)

    # Saving user info to FSM under "info"
    # await state.set_data({'info': user_record})

    # Checking if the user has wallets
    # if user_record['inventory'] == 0:
    #     greeting_message += "Looks like you don't have any wallets added yet, let's change that!\n\n"
    #     keyboard = generate_new_user_menu() 
        
    greeting_message = "Let's get started! 💼\n\n"
    keyboard = generate_menu() 
    
    await preload_message.edit_text(
        text=greeting_message,
        parse_mode='Markdown',
        reply_markup=keyboard
    )
    
@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(
        text = "🚀 *Welcome to {BOT_NAME} on Telegram!* 🚀\n\n",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )
    
# @router.message(Command("wallet"))
@router.callback_query(F.data == "main_menu")
async def handle_menu(callback: CallbackQuery, state: FSMContext):
    print('Menu button pressed')
    
    message_id = callback.message.message_id
    
    try:
        callback.message.edit_text(text="👋 Hello and welcome to *{BOT_NAME} Bot*! 🤖\n")
        callback.message.edit_reply_markup(reply_markup=None)
        callback.message.delete()
    except:
        pass
    
    await trigger_menu(callback.message)
    

async def trigger_menu(message):
    menu_text = ("{BOT_NAME} Bot! 🤖\n\n"
                "What this bot does.\n\n"
                "Good luck! 💼")
    
    await message.answer(menu_text, reply_markup=generate_menu(),  show_alert=True)
