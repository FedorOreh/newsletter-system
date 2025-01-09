from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать', callback_data='start'), InlineKeyboardButton(text='Отменить', callback_data='cancel')]
])

cancelnewsletter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancelnewsletter')]
])

confirmnewsletter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='confirm'), InlineKeyboardButton(text='Отменить', callback_data='notconfirm')]
])