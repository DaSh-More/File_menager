from funcs import clear, error


def sign_up(users):
    while True:
        clear()
        print("Регистрация\n")
        login = input("Логин: ")
        if login == "":
            break
        password = input("Пароль: ")
        if login in users:
            error("Такой пользователь уже существует")
        else:
            users[login] = password
            error("Регистрация прошла успешно")
            break
    clear()
    return users


def sign_in(users):
    home = ""
    while True:
        clear()
        print("Авторизация\n")
        login = input("Логин: ")
        if login == "":
            break
        if login not in users:
            error("Такого пользователя не существует")
            continue
        password = input("Пароль: ")
        if users[login] != password:
            error("Неверный логин или пароль")
        else:
            home = login
            break
    clear()
    return home


def auth(users):
    res = "-"
    home = ""
    while True:
        print("Авторизация [0]\nРегистрация [1]")
        res = input(": ")
        if res in ("", "0"):
            home = sign_in(users)
            if home != "":
                break
        elif res == "1":
            users = sign_up(users)
    return home, users
