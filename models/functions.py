import sqlite3


# Получаем группу пользователя из базы данных
def get_user_group(user_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT group_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close() # Закрытие соединения с базой данных

    if result:
        return result[0] # Возвращаем идентификатор группы пользователя


# Получаем данные группы из базы данных
def get_date_group(group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
    result = cursor.fetchone()

    conn.close() # Закрытие соединения с базой данных

    if result:
        return result # Возвращаем данные группы


# Получаем список всех групп из базы данных
def get_all_groups():
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute("SELECT group_id, name, password FROM groups")
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Получаем список всех админов из базы данных
def get_all_admins():
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute("SELECT user_id, username FROM users WHERE status_admin == 1")
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Удаление прав админа пользователя
def del_admin(user_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Изменяем в статусе админ права на false
    cursor.execute(f"UPDATE users SET status_admin == 0 WHERE user_id == ?", (user_id,))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()


# Добавление прав админа пользователю
def add_admin(user_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Изменяем в статусе админ права на true
    cursor.execute(f"UPDATE users SET status_admin == 1 WHERE user_id == ?", (user_id,))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()


# Получение данных пользователя
def get_user(user_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM users WHERE user_id == ?", (user_id,))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Удаление группы
def del_group(group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Удаляем группу
    cursor.execute(f"DELETE FROM groups WHERE group_id = ?", (group_id,))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()


# Получение группы по имени
def get_group_by_name(name):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM groups WHERE name == ?", (name,))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Дбавление группы
def add_group(name, password):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM groups WHERE name == ?", (name,))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Получение всех пользователей конкретной группы
def get_all_users_by_group(group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM users WHERE group_id == ?", (group_id,))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Удаление пользователя из группы
def del_user_from_group(user_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"UPDATE users SET group_id == NULL WHERE user_id == ?", (user_id,))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()