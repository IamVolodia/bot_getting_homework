import sqlite3
import asyncio


async def create_database():
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys=on")

    # Создание таблицы
    create_table_groups_query = '''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            password VARCHAR(10)
        )
    '''
    # Создание таблицы юзеров
    create_table_users_query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            username VARCHAR(100),
            status_admin INTEGER CHECK (status_admin IN (0, 1)),
            group_id INTEGER NULL,
            FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE SET NULL
        )
    '''
    create_table_subjects_query = '''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            group_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE CASCADE
        )
    '''
    create_table_homeworks_query = '''
        CREATE TABLE IF NOT EXISTS homeworks (
            homework_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            work_date DATE,
            file_id TEXT NULL,
            name TEXT NULL,
            text TEXT NULL,
            type_message VARCHAR(100) NOT NULL,
            subject_id INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
        )
    '''

    cursor.execute(create_table_groups_query)
    cursor.execute(create_table_users_query)
    cursor.execute(create_table_subjects_query)
    cursor.execute(create_table_homeworks_query)
    conn.commit()
    conn.close()



# Добавляем группу в базу данных
async def add_group_to_database(name, password):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()


    try:
        # Проверяем наличие группы в базе данных
        cursor.execute("SELECT COUNT(*) FROM groups WHERE name = ?", (name,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Если группы нет в базе данных, добавляем ее
            cursor.execute("INSERT INTO groups (name, password) VALUES (?, ?)", (name, password))
            conn.commit()

    finally:
        # Закрываем подключение к базе данных
        conn.close()



# Добавляем домашнее задание в базу данных
async def add_homework_to_database(date, type_messege, subject_id, name=None, text=None, file_id=None):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Добавляем дз
    cursor.execute("INSERT INTO homeworks (work_date, file_id, name, text, type_message, subject_id) VALUES (?, ?, ?, ?, ?, ?)", (date, file_id, name, text, type_messege, subject_id))
    conn.commit()

    # Закрываем подключение к базе данных
    conn.close()

# Добавляем пользователя в базу данных
async def add_user_to_database(user_id, username, status_admin=False, group_id=None):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()


    try:
        # Проверяем наличие пользователя в базе данных
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Если пользователя нет в базе данных, добавляем его
            cursor.execute("INSERT INTO users (user_id, username, status_admin, group_id) VALUES (?, ?, ?, ?)", (user_id, username, status_admin, group_id))
            conn.commit()
        else:
            # Изменяем имя в базе данных, т.к. пользователь мог его изменить в телеграмм
            cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            conn.commit()

    finally:
        # Закрываем подключение к базе данных
        conn.close()


# Добавляем предмет в базу данных
async def add_subject_to_database(name, group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    try:
        # Проверяем наличие предмета в базе данных
        cursor.execute("SELECT COUNT(*) FROM subjects WHERE name = ?", (name,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Если предмета нет в базе данных, добавляем его
            cursor.execute("INSERT INTO subjects (name, group_id) VALUES (?, ?)", (name, group_id))
            conn.commit()

    finally:
        # Закрываем подключение к базе данных
        conn.close()