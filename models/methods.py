import sqlite3
import asyncio


async def create_database():
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

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
            group_id INT NULL,
            FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE SET NULL
        )
    '''
    create_table_subjects_query = '''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            group_id INT,
            FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE CASCADE
        )
    '''
    create_table_homeworks_query = '''
        CREATE TABLE IF NOT EXISTS homeworks (
            homework_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            work_date DATE,
            message TEXT,
            subject_id INT,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
        )
    '''

    cursor.execute(create_table_groups_query)
    cursor.execute(create_table_users_query)
    cursor.execute(create_table_subjects_query)
    cursor.execute(create_table_homeworks_query)
    conn.commit()



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
