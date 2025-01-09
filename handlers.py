from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from config import TOKEN, ID
import keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from classes import Main
from db import Database

bot = Bot(token=TOKEN)

router = Router()

db = Database('db.db')

@router.message(CommandStart())
async def cmd_start(message: Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, f'id: {message.from_user.id}')

@router.message(Command('newsletter'))
async def newsletter(message: Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Вы точно хотите начать?',
                            reply_markup=kb.main)
    else:
        await bot.send_message(message.from_user.id, 'Вы не можете этого сделать!')

@router.callback_query(F.data == 'start')
async def startnewsletter(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Пришлите пожалуйста ваш текст!',
                           reply_markup=kb.cancelnewsletter)
    await state.set_state(Main.mainstate)

@router.message(Main.mainstate)
async def mainstate(message: Message, state: FSMContext):
    await state.update_data(mainstate=message.text)
    await bot.send_message(message.from_user.id, 'Вы хотите подтвердить?',
                           reply_markup=kb.confirmnewsletter)

@router.callback_query(F.data == 'confirm')
async def confirmnewsletter(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data["mainstate"]
    users = db.get_user()
    for row in users:
        try:
            await bot.send_message(chat_id=row[0], text=text)
            if int(row[1]) != 1:
                db.set_active(row[0], 1)
        except:
            db.set_active(row[0], 0)
    await state.clear()

@router.callback_query(F.data == 'notconfirm')
async def notconfirm(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Отмена')

@router.callback_query(F.data == 'cancel')
async def cancelnewsletter(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Отмена')

@router.callback_query(F.data == 'cancelnewsletter')
async def cancelnewsletteron(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Отмена')