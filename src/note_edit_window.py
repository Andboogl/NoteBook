"""Модуль вікна редагування нонатки"""


from PyQt6.QtWidgets import QMainWindow
from loguru import logger
from design import NoteEditWindowDesign
import notes

class NoteEditWindow(QMainWindow):
    """Вікно редагування нонатки"""
    def __init__(self, parent: QMainWindow, note_title: str) -> None:
        super().__init__(parent)

        # Завантаження дизайну
        self.design = NoteEditWindowDesign()
        self.design.setupUi(self)

        # Завантаження нонатки
        self.user_notes = notes.UserNotes()
        self.load_note(note_title)

        # Автозбереження та обробка кнопки закрити
        self.design.close.clicked.connect(self.close)
        self.design.note_title.editingFinished.connect(self.save)
        self.design.note_content.textChanged.connect(self.save)

        logger.info('Нонатка відкрита')

    def load_note(self, note_title: str) -> None:
        """Завантажити нонатку з нонаток користувача"""
        all_user_notes = self.user_notes.get_notes_as_json()
        note_content = all_user_notes[note_title]
        self.design.note_title.setText(note_title)
        self.design.note_content.setText(note_content)
        logger.info('Нонатка успішно завантаженна')

    def save(self) -> None:
        """Зберегти нонатку у файл нонаток"""
        note_title = self.design.note_title.text()
        note_content = self.design.note_content.toPlainText()

        if not note_title:
            note_title += ''
            self.design.note_title.setText(note_title + '')

        self.user_notes.add_note(note_title, note_content)
        logger.info('Зміни збережено')
