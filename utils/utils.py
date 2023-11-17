# Добавляем нолик к дню даты, инче бд просто не видит дату, мда
def change_date(date):
    if int(date.split("-")[-1]) < 10 and len(date.split("-")[-1]) == 1:
        date = date.split("-")
        date[-1] = "0" + date[-1]
        date = "-".join(date)
    return date