"""Головне вікно программи"""


from typing import Union
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox
from loguru import logger
from design.main_window_design import MainWindowDesign
from database import Database
import messages
from paths import DATABASE_FILE_PATH
from .create_note_window import CreateNoteWindow
from .note_edit_window import NoteEditWindow


class MainWindow(QMainWindow):
    """Головне вікно программи"""
    def __init__(self):
        super().__init__(None)

        # Завантаження дизайну
        self.design = MainWindowDesign()
        self.design.setupUi(self)
        self.database = Database()  # Завантаження бази данних
        self.load_notes()  # Завантаження нонаток
        self.create_note_window = CreateNoteWindow(self)  # Вікно створення нонатки

        # Обробка натискань на кнопки
        self.design.create_note.clicked.connect(self.create_note_window.show)
        self.design.delete_note.clicked.connect(self.delete_note)
        self.design.open_note.clicked.connect(self.open_note)
        self.design.delete_all_notes.clicked.connect(self.delete_all_notes)

        logger.success("Успішно завантажено нонатки користувача, "
                       "базу данних та головне вікно программи")

    def get_selected_note(self) -> Union[str, None]:
        """Метод повертає заголовок вибраної користувачем нонатки"""
        selected_items = self.design.notes.selectedItems()

        if selected_items:
            selected_item_title = selected_items[0].text()
            logger.debug(selected_item_title)
            return selected_item_title

        else:
            logger.debug("Користувач не вибрав нонатку")
            messages.standart("Виберіть нонатку")

    def open_note(self) -> None:
        """Відкрити вікно редагування вибраної нонатки"""
        note_title = self.get_selected_note()

        if note_title:
            self.note_edit_window = NoteEditWindow(note_title, self)
            self.note_edit_window.show()

    def delete_note(self) -> None:
        """Видалити вибрану користувачем нонатку"""
        note_title = self.get_selected_note()

        if note_title:
            try:
                self.database.delete_note(note_title)

            except Exception as error:
                logger.error(error)
                messages.error("Не вдалося видалити нонатку. Схоже, інша "
                               "программа вже видалила її", error)
            
            self.load_notes()

    def delete_all_notes(self) -> None:
        """Видалити всі нонатки"""
        are_you_sure = QMessageBox.question(self, "Виконати операцію?", "Чи дійсно ви хочете видалити всі нонатки? Цю дію не можна відмінити")
        logger.debug(are_you_sure)

        if are_you_sure == QMessageBox.StandardButton.Yes:
            self.database.delete_all_notes()
            self.load_notes()
        
    def load_notes(self) -> None:
        """Завантажити нонатки користувача в QListWidget"""
        try:
            self.design.notes.clear()
            notes = self.database.get_notes()

            for note in notes:
                item = QListWidgetItem(self.design.notes)
                item.setText(note[0])
                self.design.notes.addItem(item)

            logger.success("Успішно завантажені нонатки користувача")

        except Exception as error:
            logger.error(error)
            messages.error("Помилка при завантажені нонаток користувача. "
                           f"Спробуйте видалити базу данних за шляхом {DATABASE_FILE_PATH}", error)

    def closeEvent(self, a0) -> None:
        """Ця функція запускається при закриті программи. Вона закриває зʼєднаня з базою данних"""
        self.database.close()
        a0.accept()
