
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from database import add_event, save_vote, get_votes
import re

router = Router()
pending = {}

@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer("Привет! Я помогу организовать мероприятие. Напиши /newevent, чтобы начать.")

@router.message(Command("newevent"))
async def new_event(msg: Message):
    await msg.answer("Введите название мероприятия:")
    pending[msg.from_user.id] = {"step": "title"}

@router.message(lambda msg: msg.from_user.id in pending and pending[msg.from_user.id]["step"] == "title")
async def get_title(msg: Message):
    pending[msg.from_user.id]["title"] = msg.text
    pending[msg.from_user.id]["step"] = "options"
    await msg.answer("Введите варианты времени (по одному в строке):")

@router.message(lambda msg: msg.from_user.id in pending and pending[msg.from_user.id]["step"] == "options")
async def get_options(msg: Message):
    options = msg.text.strip().split("\n")
    title = pending[msg.from_user.id]["title"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"vote|{opt}")] for opt in options]
    )
    sent = await msg.answer(f"📅 <b>{title}</b>
Голосуйте за удобное время:", reply_markup=markup, parse_mode="HTML")
    event_id = add_event(title, options, sent.message_id, sent.chat.id)
    pending.pop(msg.from_user.id)

@router.callback_query(F.data.startswith("vote|"))
async def vote_callback(call: CallbackQuery):
    choice = call.data.split("|")[1]
    msg = call.message
    # Имитация event_id — в реальной логике нужно подтянуть из БД по message_id
    event_id = 1
    save_vote(event_id, call.from_user.id, choice)
    votes = get_votes(event_id)
    result = "\n".join([f"{opt}: {count} голос(ов)" for opt, count in votes])
    await msg.edit_text(msg.text.split("\n")[0] + "\n\n" + result, reply_markup=msg.reply_markup)
    await call.answer("Голос засчитан!")
