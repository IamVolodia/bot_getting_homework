import sqlite3
import asyncio

# Создание подключения к базе данных
conn = sqlite3.connect('models//database.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

async def create_database():
    # Создание таблицы
    create_table_groups_query = '''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INT PRIMARY KEY,
            name VARCHAR(100),
            password VARCHAR(10)
        )
    '''
    create_table_users_query = '''
        CREATE TABLE IF NOT EXISTS users (
            users_id INT PRIMARY KEY,
            name VARCHAR(100),
            status_admin INTEGER CHECK (is_active IN (0, 1))
            group INT,
            FOREIGN KEY group REFERENCES groups(group_id)
        )
    '''
    await asyncio.sleep(0)  # Для асинхронности

    cursor.execute(create_table_groups_query)
    cursor.execute(create_table_users_query)
    conn.commit()


# Добавляем группу в базу данных
async def add_user_to_database(group_id, name, password):
    try:
        # Проверяем наличие группы в базе данных
        cursor.execute("SELECT COUNT(*) FROM groups WHERE group_id = ?", (group_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Если группы нет в базе данных, добавляем ее
            cursor.execute("INSERT INTO groups (group_id, name, password) VALUES (?, ?, ?)", (group_id, name, password))
            conn.commit()
        else:
            return f''

    finally:
        # Закрываем подключение к базе данных
        conn.close()


# Добавляем пользователя в базу данных
async def add_user_to_database(user_id, username, admin=False, group=None):
    try:
        # Проверяем наличие пользователя в базе данных
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Если пользователя нет в базе данных, добавляем его
            cursor.execute("INSERT INTO users (user_id, username, admin, group) VALUES (?, ?, ?, ?)", (user_id, username, admin, group))
            conn.commit()
        else:
            # Изменяем имя в базе данных, т.к. пользователь мог его изменить в телеграмм
            cursor.execute(f"UPDATE users SET username = '{username}' WHERE user_id = {user_id}")
            conn.commit()

    finally:
        # Закрываем подключение к базе данных
        conn.close()


# Получаем список всех групп из базы данных
async def get_all_groups():
    try:
        # Получаем все данные из таблицы
        cursor.execute("SELECT group_id, name, password FROM users")
        data = cursor.fetchall()
        await data

    finally:
        # Закрываем подключение к базе данных
        conn.close()


# Получаем группу пользователя из базы данных
async def get_user_group(user_id):
    # Выполнение запроса
    cursor.execute("SELECT group_id FROM users WHERE users_id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close() # Закрытие соединения с базой данных

    if result:
        return result[0] # Возвращаем идентификатор группы пользователя

# Получаем данные группы из базы данных
async def get_date_group(group_id):
    # Выполнение запроса
    cursor.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
    result = cursor.fetchone()

    conn.close() # Закрытие соединения с базой данных

    if result:
        return result # Возвращаем данные группы