"""Вікно редагування нонатки"""


from loguru import logger
from PyQt6.QtWidgets import QMainWindow
from design.note_edit_window_design import NoteEditWindowDesign
from database import Database
import messages


class NoteEditWindow(QMainWindow):
    """Вікно редагування нонатки"""
    def __init__(self, note_title: str, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.note_title = note_title
        self.main_window = parent

        # Завантаження дизайну
        self.design = NoteEditWindowDesign()
        self.design.setupUi(self)
        self.database = Database()  # Завантаження бази данних
        self.load_note(note_title)  # Завантаження нонатки

        # Натискання на кнопки та автозбереження
        self.design.close.clicked.connect(self.close)
        self.design.note_title.textChanged.connect(self.save_changes)
        self.design.note_content.textChanged.connect(self.save_changes)

        logger.success("Успішно завантаженно нонатку, вікно редагування нонатки та базу данних")

    def load_note(self, note_title: str) -> None:
        """Завантажити нонатку з бази данних"""
        try:
            logger.debug("Here")
            note_info = self.database.get_note(note_title)
            self.design.note_title.setText(note_info[0])
            self.design.note_content.setText(note_info[1])

        except Exception as error:
            logger.error(error)
            messages.error("Не вдалося завантажити нонатку. Можливо, інша "
                           "программа видалила її", error)
            self.close()

    def save_changes(self) -> None:
        """Зберегти зміни нонатки"""
        new_title = self.design.note_title.text()
        new_content = self.design.note_content.toPlainText()
        db_note = self.database.get_note(self.note_title)

        if db_note[0] != new_title:
            if new_title.strip():
                self.database.change_note(self.note_title, new_title)
                self.note_title = new_title
                self.main_window.load_notes()

            else:
                messages.standart("Заголовок нонатки не може бути пустим")

        if db_note[1] != new_content:
            if new_content.strip():
                self.database.change_note(self.note_title, new_content=new_content)
