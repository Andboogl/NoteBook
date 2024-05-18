"""Шляхи до місць де программа зберігає свої данні"""


from os import mkdir
from os.path import join, expanduser, exists
from datetime import datetime


NOTEBOOK_FOLDER_PATH = join(expanduser("~"), ".NoteBook")
LOG_FILE_PATH = join(NOTEBOOK_FOLDER_PATH, "logs", f'{datetime.now().strftime("%d.%m.%Y")}.log')
DATABASE_FILE_PATH = join(NOTEBOOK_FOLDER_PATH, "notes.db")


def create_notebook_folder():
    """Створити папку NoteBook якщо її ще не існує"""
    if not exists(NOTEBOOK_FOLDER_PATH):
        mkdir(NOTEBOOK_FOLDER_PATH)
