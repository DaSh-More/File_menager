from pathlib import Path
from funcs import colorize
import shutil


def remove(path: Path):
    if path.is_dir():
        # Удаляем все внутри папки
        for file in path.iterdir():
            remove(file)
        path.rmdir()
    elif path.is_file():
        path.unlink()


def make_dir(path: Path):
    path.mkdir()


def ls(path: Path):
    """
    Возвращает содержимое папки
    """
    return "\n".join(
        map(
            lambda x: x.name if x.is_file() else colorize(x.name, "yellow"),
            path.iterdir(),
        )
    )


def rename(path_from: Path, name: str):
    """
    Переименование файла
    """
    path_from.rename(path_from.with_name(name))


def copy(path_from: Path, path_to: Path):
    shutil.copy(path_from, path_to)


def move(path_from: Path, path_to: Path):
    """
    Перемещение файла / папки
    """
    path_from.rename(path_to)


def read(path: Path):
    with open(path) as f:
        data = f.read()
    return data


def write(path: Path, text: str):
    with open(path, "w") as f:
        f.write(text)


def to_archive(path: Path):
    shutil.make_archive(path.name, "zip", path)


def from_arhive(path: Path):
    shutil.unpack_archive(path, path.parent)


def get_path(path: str, current_dir, maindir):
    maindir = Path(maindir)
    if path[0] == "/":
        return maindir / path.lstrip("./")
    else:
        new_path = (current_dir / path).resolve()
        if maindir in [*new_path.parents, new_path]:
            return new_path


def get_folder_size(path: Path):
    if not path.is_dir():
        return 0
    return sum(path.stat().st_size for path in path.rglob("*.*") if path.is_file())


def help_():
    print(f"""
- {colorize('помощь', color='yellow')} - Вывести эту справку
- {colorize('папка <папка>', color='yellow')} - Перейти в другую папку
- {colorize('файлы', color='yellow')} - Список файлов и папок в папке
- {colorize('создать_папку <папка>', color='yellow')} - Создание папки в текущей папке
- {colorize('создать_файл <файл>', color='yellow')} - Создание фала в текущей папке
- {colorize('прочитать <файл>', color='yellow')} - Прочитать текст из файла
- {colorize('записать <файл> <текст>', color='yellow')} - Записать текст в файл
- {colorize('удалить <папка/файл>', color='yellow')} - Удаление папки или файла в текущей директории
- {colorize('копировать <путь откуда> <путь куда>', color='yellow')} - Копирование файла или папки
- {colorize('архивировать <папка/файл>', color='yellow')} - Довавление папки или файла в архив
- {colorize('разархивировать <файл.zip> [путь куда]', color='yellow')} - Извлечение архива по указанному пути
- {colorize('переименовать <старое имя> <новое имя>', color='yellow')} - Перемименование папки или файла
- {colorize('переместить <путь откуда> <путь куда>', color='yellow')} - Перемещение папки или файла    
- {colorize('место', color='yellow')} - Вывести свободное место в папке
""")
