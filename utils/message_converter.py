from aiogram.types import Message, CallbackQuery, InputFile
from aiogram import Router
from models.methods import add_homework_to_database
from models.functions import get_homework_for_date_and_subject
from models.functions import *


#-------------------- добавление разных типов сообщений в бд -----------------------------------------------------


# Добавление текстового сообщения в домашние задания
async def _save_text(date, message: Message, subject_id):
    await add_homework_to_database(date=date, text=message.text, type_messege="text", subject_id=subject_id)


# Добавление фото сообщения в домашние задания
async def _save_photo(date, message: Message, subject_id):
    photo = message.photo[-1]
    await add_homework_to_database(date=date, file_id=photo.file_id, text=message.caption, type_messege="photo", subject_id=subject_id)


# Добавление аудио сообщения в домашние задания
async def _save_audio(date, message: Message, subject_id):
    audio = message.audio
    await add_homework_to_database(date=date, file_id=audio.file_id, name=audio.duration, type_messege="audio", subject_id=subject_id)


# Добавление видео сообщения в домашние задания
async def _save_video(date, message: Message, subject_id):
    video = message.video
    await add_homework_to_database(date=date, file_id=video.file_id, name=video.duration, type_messege="video", subject_id=subject_id)


# Добавление документа сообщения в домашние задания
async def _save_document(date, message: Message, subject_id):
    document = message.document
    await add_homework_to_database(date=date, file_id=document.file_id, name=document.file_name, text=message.caption, type_messege="document", subject_id=subject_id)


# Добавление голосового сообщения в домашние задания
async def _save_voice(date, message: Message, subject_id):
    voice = message.voice
    await add_homework_to_database(date=date, file_id=voice.file_id, name=voice.duration, text=message.caption, type_messege="voice", subject_id=subject_id)


# Обработка сообщения и разделение функционала добавления дз в бд в зависимости от типа сообщения
async def save_message_to_database(date, subject_id, message: Message):
    if message.text:
        await _save_text(date, message, subject_id)
    elif message.photo:
        await _save_photo(date, message, subject_id)
    elif message.audio:
        await _save_audio(date, message, subject_id)
    elif message.video:
        await _save_video(date, message, subject_id)
    elif message.document:
        await _save_document(date, message, subject_id)
    elif message.voice:
        await _save_voice(date, message, subject_id)


#--------------- получение домашней работы из бд и конвертирование в сообщение ----------------------------------

# Конвертация полученных данных в текстовое сообщение
async def _create_message_text(homework, callback: CallbackQuery):
    await callback.message.answer(text=homework[4])


# Конвертация полученных данных в фото сообщение
async def _create_message_photo(homework, callback: CallbackQuery):
    await callback.message.answer_photo(photo=homework[2], caption=homework[4])


# Конвертация полученных данных в аудио сообщение
async def _create_message_audio(homework, callback: CallbackQuery):
    await callback.message.answer_audio(audio=homework[2], duration=homework[4])


# Конвертация полученных данных в видео сообщение
async def _create_message_video(homework, callback: CallbackQuery):
    await callback.message.answer_video(video=homework[2], duration=homework[4])


# Конвертация полученных данных в документ сообщение
async def _create_message_document(homework, callback: CallbackQuery):
    await callback.message.answer_document(document=homework[2], caption=homework[4])


# Конвертация полученных данных в голосовое сообщение
async def _create_message_voice(homework, callback: CallbackQuery):
    await callback.message.answer_voice(voice=homework[2], duration=homework[4])

# Выгрузка сообщения из бд
async def get_homeworks_from_database(date, subject_id, callback: CallbackQuery):
    data = get_homework_for_date_and_subject(date, subject_id)
    for homework in data:
        if homework[-2] == 'text':
            await _create_message_text(homework, callback)
        elif homework[-2] == 'photo':
            await _create_message_photo(homework, callback)
        elif homework[-2] == 'audio':
            await _create_message_audio(homework, callback)
        elif homework[-2] == 'video':
            await _create_message_video(homework, callback)
        elif homework[-2] == 'document':
            await _create_message_document(homework, callback)
        elif homework[-2] == 'voice':
            await _create_message_voice(homework, callback)


