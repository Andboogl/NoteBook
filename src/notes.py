"""
Модуль для роботи з нонатками користувача
"""


from json import load, dump
from os.path import expanduser, join, exists
from os import mkdir
from loguru import logger


class UserNotes:
    """
    Класс для роботи з нонатками користувача
    TODO: Шифрування за ключем
    TODO: Можливість змінювати шлях файла нонаток
    """
    def __init__(self) -> None:
        self.notes_folder = join(expanduser('~'), '.NoteBook')
        self.notes_file = join(self.notes_folder, 'notes.json')
        logger.info('Ініціалізовано класс UserNotes')

    def create_notes_folder(self) -> None:
        """Створити папку для нонаток, якщо її не існує"""
        if not exists(self.notes_folder):
            mkdir(self.notes_folder)
            logger.info('Створенна папка нонаток')

    def create_notes_file(self) -> None:
        """Створити файл нонаток, якщо його не існує"""
        if not exists(self.notes_file):
            self.create_notes_folder()
            open(self.notes_file, 'w', encoding='utf-8').close()
            logger.info('Створенно файл нонаток')

    def get_notes_as_json(self) -> dict:
        """Отримати всі нонатки з файлу у JSON форматі"""
        if exists(self.notes_file):
            with open(self.notes_file, 'r', encoding='utf-8') as notes_file:
                result = load(notes_file)

        else:
            result = {}

        logger.debug(f'Нонатки користувача отримані: {result}')
        return result

    def write_json_to_note_file(self, data: dict) -> None:
        """Записати JSON данні до файлу нонаток"""
        self.create_notes_file()

        with open(self.notes_file, 'w', encoding='utf-8') as notes_file:
            dump(data, notes_file, indent=4)
            logger.info('JSON данні записані у файл нонаток')

    def delete_note(self, title: str) -> None:
        """Видалити нонатку"""
        current_notes = self.get_notes_as_json()

        if current_notes.get(title, None):
            raise ValueError('Нонатки з таким імʼям не існує')

        current_notes.pop(title)
        self.write_json_to_note_file(current_notes)
        logger.warning(f'Видалена нонатка з імʼям {title}')

    def clear_all_notes(self) -> None:
        """Видалити всі нонатки"""
        self.write_json_to_note_file({})
        logger.warning('Видалені всі нонатки користувача')

    def add_note(self, title: str, text: str) -> None:
        """
        Додати нонатку. Метод також може використовуватися
        щоб змінити текст вже існуючої нонатки
        """
        if not title:
            raise ValueError('Заголовок нонатки не може бути повністью пустим')

        current_notes = self.get_notes_as_json()
        new_note = True if not current_notes.get(title, None) else False  # Чи є нонатка новою чи вже існує

        current_notes[title] = text

        self.write_json_to_note_file(current_notes)
        logger.info('Створенна нова нонатка' if new_note else 'Нонатку змінено')
