"""Вінко створення нонатки"""


from PyQt6.QtWidgets import QMainWindow
from loguru import logger
from design.create_note_window_design import CreateNoteWindowDesign
from database import Database
from paths import DATABASE_FILE_PATH
import messages


class CreateNoteWindow(QMainWindow):
    """Вінко створенння нонатки"""
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__(main_window)
        self.main_window = main_window

        # Завантаження дизайну
        self.design = CreateNoteWindowDesign()
        self.design.setupUi(self)
        self.database = Database()  # Завантаження бази данних

        # Обробка натискань на кнопки
        self.design.create_note.clicked.connect(self.create_note)
        self.design.close.clicked.connect(self.close)
        logger.success("Завантаженно вікно створення нонатки та базу данних")

    def create_note(self) -> None:
        """Створити нонатку"""
        title = self.design.note_title.text()

        if not title.strip():
            message = "Заголовок нонатки не може бути пустим"
            logger.warning(message)
            messages.standart(message)

        else:
            try:
                self.database.create_note(title, "")
                self.main_window.load_notes()
                self.close()

            except Exception as error:
                logger.error(str(error))
                messages.error("Нонатка з таким імʼям вже існує. Якщо це не так, видаліть "
                               f"базу данних за шляхом {DATABASE_FILE_PATH}", str(error))
