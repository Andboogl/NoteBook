"""Модуль для обробки натискань у головному вікні программи"""


from loguru import logger
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox
from PyQt6.QtGui import QFont
from design import MainWindowDesign
import create_note_window
import note_edit_window
import show_message
import notes


class MainWindow(QMainWindow):
    """Головне вікно программи"""
    def __init__(self) -> None:
        super().__init__(None)

        # Завантаження дизайну
        self.design = MainWindowDesign()
        self.design.setupUi(self)

        # Завантаження нонаток користувача
        self.user_notes = notes.UserNotes()
        self.load_user_notes()

        # Обробка натискань на кнопки та комбінації клавіш
        self.design.open_note.clicked.connect(self.open_note)
        self.design.create_note.clicked.connect(self.create_note)
        self.design.delete_note.clicked.connect(self.delete_note)
        self.design.delete_all_notes.clicked.connect(self.delete_all_notes)

        self.design.delete_note.setShortcut('Delete')  # Устанавливаем клавишу Delete как сочетание
        self.design.open_note.setShortcut('Return')

    def load_user_notes(self) -> None:
        """Завантажити нонатки користувача"""
        try:
            self.design.notes.clear()
            notes = self.user_notes.get_notes_as_json()

            # Шрифт елементів QListWidget
            note_font = QFont()
            note_font.setBold(True)
            note_font.setPointSize(15)

            for note in notes.keys():
                note_item = QListWidgetItem(self.design.notes)
                note_item.setText(note)
                note_item.setFont(note_font)
                self.design.notes.addItem(note_item)

            logger.info('Успішно завантаженні нонатки користувача')

        except Exception as error:
            message = 'Виникла помилка під час завантаження нонаток'
            logger.error(f'{message}. Помилка {error}')
            show_message.show_error_message(message, error)

    def get_selected_note(self) -> None:
        """Отримати вибрану нонатку"""
        selected_note = self.design.notes.currentItem()

        if selected_note:
            selected_note = selected_note.text()
            logger.debug(f'Вибрана нонатка: {selected_note}')
            return selected_note

        else:
            show_message.show_message('Виберіть нонатку', 'Ви не вибрали нонатку')

    def open_note(self) -> None:
        """Відкрити вибрану нонатку"""
        selected_note = self.get_selected_note()

        if selected_note:
            self.note_edit_window = note_edit_window.NoteEditWindow(self, selected_note)
            self.note_edit_window.show()

    def create_note(self) -> None:
        """Створити нонатку"""
        self.create_note_window = create_note_window.CreateNoteWindow(self)
        self.create_note_window.show()

    def delete_note(self) -> None:
        """Видалити вибрану нонатку"""
        selected_note = self.get_selected_note()

        if selected_note:
            self.user_notes.delete_note(selected_note)
            self.load_user_notes()

    def delete_all_notes(self) -> None:
        """Видалити всі нонатки"""
        selected_button = QMessageBox.question(self,
                             'Видалити всі нонатки?',
                             'Ви дійсно хочете видалити всі нонатки? Цю дію не можна відмінити',
                             QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Ok)
        logger.debug(f'Вибрана кнопка: {selected_button}')

        if selected_button == 1024:
            self.user_notes.clear_all_notes()
            self.load_user_notes()
