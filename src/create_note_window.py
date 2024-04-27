"""Модуль вікна створення нонатки"""


from PyQt6.QtWidgets import QMainWindow
from loguru import logger
from design import CreateNoteWindowDesign
from show_message import show_message
import note_edit_window
import notes


class CreateNoteWindow(QMainWindow):
    """Вікно створення нонатки"""
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        # Завантаження дизайну
        self.design = CreateNoteWindowDesign()
        self.design.setupUi(self)

        self.user_notes = notes.UserNotes()
        self.main_window = parent

        # Обробка натисканнь на кнопки
        self.design.close.clicked.connect(self.close)
        self.design.create_note.clicked.connect(self.create_note)

    def create_note(self) -> None:
        """Створити нонатку"""
        note_title = self.design.note_title.text()
        user_notes = self.user_notes.get_notes_as_json()

        if note_title in user_notes.keys():
            show_message('Нонатка існує', 'Нонатка з таким заголовком вже існує')

        if not note_title:
            show_message('Пусте ім\'я', 'Нонатка не може мати повністью пусте ім\'я')

        else:
            self.user_notes.add_note(note_title, '')
            self.main_window.load_user_notes()
            self.note_edit_window = note_edit_window.NoteEditWindow(self.main_window, note_title)
            self.note_edit_window.show()
            self.close()
