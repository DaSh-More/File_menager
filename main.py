import json
from pathlib import Path
from funcs import colorize, cprint

from auth import auth
from file_funcs import (
    ls,
    remove,
    read,
    write,
    move,
    copy,
    rename,
    to_archive,
    from_arhive,
    get_path,
    get_folder_size,
    help_,
)


def cwd(path):
    return path.relative_to(config["maindir"])


with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

maindir = Path(config["maindir"])
if not maindir.is_dir():
    raise ValueError("Главной директоирии не существует")

# Авторизуемся
home, users = auth(config["users"])
# home, users = "admin", config["users"]
config["users"] = users
maindir = maindir / home

current_dir = maindir

# Если надо, создаем директорию пользователюы
if not maindir.is_dir():
    maindir.mkdir()

# Сохраняем конфиг, возможно с новыми пользователями
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f)

# Основной цикл программы
while True:
    com, *args = input(colorize(f"{cwd(current_dir)}> ", "green")).strip().split()
    com = com.lower()

    # Проверка на наличее свобоного места
    if (
        com
        in (
            "создать_файл",
            "записать",
            "копировать",
            "переместить",
            "переименовать",
        )
        and (config["max_folder_size"] - get_folder_size(maindir) / 2**20) <= 0
    ):
        cprint("В папке закончилось место")
    # Выход
    if com == "выход":
        break
    # Вывод списка директорий
    elif com == "файлы":
        print("\n", ls(current_dir), "\n", sep="")

    # Переход в другую папку
    elif com == "папка":
        if len(args) < 1:
            cprint("Не указана папка назначения")
            continue
        new_path = get_path(args[0], current_dir, maindir)
        if new_path is None:
            cprint("Нельзя выйти из главной папки")
            continue
        if not new_path.is_dir():
            cprint(f'Папки "{cwd(new_path)}" не существует')
            continue
        current_dir = new_path
    # Удаление папки / файла
    elif com == "удалить":
        if len(args) < 1:
            cprint("Не указан путь для удаления")
            continue
        new_path = get_path(args[0], current_dir, maindir)
        if new_path is None:
            cprint("Нельзя выйти из главной папки")
            continue
        if not new_path.exists():
            cprint(f'"{cwd(new_path)}" не существует')
            continue
        remove(new_path)

    # Создание папки
    elif com == "создать_папку":
        if len(args) < 1:
            cprint("Не указано название папки")
            continue
        folder = current_dir / args[0]
        if folder.exists():
            cprint(f"Папка {cwd(folder)} уже существует")
            continue
        folder.mkdir()
        cprint(f"Создана папка {cwd(folder)}", color="yellow")

    # Создание файла
    elif com == "создать_файл":
        if len(args) < 1:
            cprint("Не указано название файла")
            continue
        file = current_dir / args[0]
        if file.exists():
            cprint(f"Файл {cwd(file)} уже существует")
            continue
        file.write_text("")
        cprint(f"Создан файл {cwd(file)}", color="yellow")

    # Чтение файла
    elif com == "прочитать":
        if len(args) < 1:
            cprint("Не указано название файла")
            continue
        path = get_path(args[0], current_dir, maindir)
        if path is None:
            cprint("Нельзя выйти из папки")
            continue
        data = read(path)
        print("\n", data, "\n", sep="")

    # Запись в файл
    elif com == "записать":
        if len(args) < 2:
            cprint("Не указано название файла или текст для записи")
            continue
        path = get_path(args[0], current_dir, maindir)
        if path is None:
            cprint("Нельзя выйти из папки")
            continue
        write(path, args[1])
        cprint("Текст записан", color="yellow")
    # Копирование файла / папку
    elif com == "копировать":
        if len(args) < 2:
            cprint("Не указан исходный путь или путь назначения")
            continue
        path_from = get_path(args[0], current_dir, maindir)
        path_to = get_path(args[1], current_dir, maindir)
        if path_from is None or path_to is None:
            cprint("Нельзя выйти из папки")
            continue
        copy(path_from, path_to)
    # Перемещение файла / папки
    elif com == "переместить":
        if len(args) < 2:
            cprint("Не указан исходный путь или путь назначения")
            continue
        path_from = get_path(args[0], current_dir, maindir)
        path_to = get_path(args[1], current_dir, maindir)
        if path_from is None or path_to is None:
            cprint("Нельзя выйти из папки")
            continue
        move(path_from, path_to)
    # Переименование файла
    elif com == "переименовать":
        if len(args) < 2:
            cprint("Не указан исходный путь или новое имя файла")
            continue
        path = get_path(args[0], current_dir, maindir)
        if path is None:
            cprint("Нельзя выйти из папки")
            continue
        rename(path, args[1])
    # Архивация папки / файла
    elif com == "архивировать":
        if len(args) < 1:
            cprint("Не указан путь к файлу")
            continue
        path = get_path(args[0], current_dir, maindir)
        if path is None:
            cprint("Нельзя выйти из папки")
            continue
        to_archive(path)
    # Разорхивация папки / файла
    elif com == "разархивировать":
        if len(args) < 1:
            cprint("Не указан путь к файлу")
            continue
        path = get_path(args[0], current_dir, maindir)
        if path is None:
            cprint("Нельзя выйти из папки")
            continue
        from_arhive(path)
    elif com == "место":
        empty = config["max_folder_size"] - get_folder_size(maindir) / 2**20
        print(
            f"Свободно {empty:.2f} мб из {config['max_folder_size']} мб ({empty / config['max_folder_size']:.1%})"
        )
    elif com == "помощь":
        help_()
    else:
        cprint(f'Файл "{cwd(current_dir / com)}" не найден')
