from aiogram.types import Message
from models.methods import add_homework_to_database
from models.functions import *


# Добавление текстового сообщения в домашние задания
async def _save_text(date, message: Message, subject_id):
    await add_homework_to_database(date=date, text=text, type_messege="text", subject_id=subject_id)


# Добавление фото сообщения в домашние задания
async def _save_photo(date, message: Message, subject_id):
    photo = message.photo[-1]
    await add_homework_to_database(date=date, file_id=photo.file_id, text=message.caption, type_messege="photo", subject_id=subject_id)


# Добавление аудио сообщения в домашние задания
async def _save_audio(date, message: Message, subject_id):
    audio = message.audio
    await add_homework_to_database(date=date, file_id=audio.file_id, text=audio.duration, type_messege="audio", subject_id=subject_id)


# Обработка сообщения и разделение функционала добавления дз в бд в зависимости от типа сообщения
async def save_message_to_database(date, subject_id, message: Message):
    if message.text:
        await _save_text(date, message.text, subject_id)
    if message.photo:
        await _save_photo(date, message, subject_id)
    if message.audio:
        await _save_audio(date, message, subject_id)