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
    # Разрешаем внешние ключи
    cursor.execute("PRAGMA foreign_keys=on")
    # Удаляем права админа у пользователей группы
    cursor.execute(f"UPDATE users SET status_admin == 0 WHERE group_id == ?", (group_id,))
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


# Получение предмета по имени и group_id
def get_subject_by_name(name, group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM subjects WHERE name == ? AND group_id == ?", (name, group_id))
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
    cursor.execute(f"UPDATE users SET group_id == NULL AND status_admin == 0 WHERE user_id == ?", (user_id,))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()


# Добавление пользователя в группу
def add_user_to_group(user_id, group_id = None, group_name = None):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    if group_name != None:
        cursor.execute(f"SELECT * FROM groups WHERE name == ?", (group_name,))
        group_id = cursor.fetchall()[-1][0]
    # Привязываем пользователя к группе
    cursor.execute(f"UPDATE users SET group_id == ? WHERE user_id == ?", (group_id, user_id))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()


# Получение всех предметов конкретной группы
def get_all_subjects_by_group(group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM subjects WHERE group_id == ?", (group_id,))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Удаление предмета
def del_subject(subject_id):
   # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    # Разрешаем внешние ключи
    cursor.execute("PRAGMA foreign_keys=on")
    # Удаляем предмет
    cursor.execute(f"DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
    conn.commit()
    # Закрываем подключение к базе данных
    conn.close()


# Получаем все предметы группы, где есть домашние задание на конкретную дату
def get_subject_with_homework_for_date(group_id, date):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    query = '''
        SELECT DISTINCT subjects.name, subjects.subject_id
        FROM homeworks
        INNER JOIN subjects ON homeworks.subject_id = subjects.subject_id
        WHERE homeworks.work_date = ? AND subjects.group_id = ?
    '''
    cursor.execute(query, (date, group_id))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()
    
    return data


# Получение предмета по id и group_id
def get_subject_by_id_and_group_id(subject_id, group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM subjects WHERE subject_id == ? AND group_id == ?", (subject_id, group_id))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Получаем все домашние задания за конкртную дату и предмет
def get_homework_for_date_and_subject(date, group_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    query = '''
        SELECT *
        FROM homeworks
        WHERE work_date = ? AND subject_id = ?
    '''
    cursor.execute(query, (date, group_id))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()
    
    return data


# Получение предмета по id и group_id
def get_subject_by_id(subject_id):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM subjects WHERE subject_id == ?", (subject_id,))
    data = cursor.fetchall()
    # Закрываем подключение к базе данных
    conn.close()

    return data


# Удаление домашнего задания у группы за конкретную дату
def del_homework_from_sebject_for_date(subject_id, date):
    # Создание подключения к базе данных
    conn = sqlite3.connect('models//database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    # Разрешаем внешние ключи
    cursor.execute("PRAGMA foreign_keys=on")

    # Удаляем группу
    cursor.execute(f"DELETE FROM homeworks WHERE work_date = ? and subject_id = ?", (date, subject_id))
    conn.commit()

    # Закрываем подключение к базе данных
    conn.close()