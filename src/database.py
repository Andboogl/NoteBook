"""База данних. Потрібна для зберігання нонаток користувача"""


from sqlite3 import connect
from loguru import logger
from paths import create_notebook_folder, DATABASE_FILE_PATH


class Database:
    """База данних. Потрібна для зберігання нонаток користувача"""
    @logger.catch
    def __init__(self) -> None:
        create_notebook_folder()
        self.db = connect(DATABASE_FILE_PATH)
        self.db.execute("CREATE TABLE IF NOT EXISTS notes(title PRIMARY KEY, content)")
        self.db.commit()
        logger.success("Успішно ініціалізовано базу данних")

    def create_note(self, title: str, content: str) -> None:
        """Метод створює нову нонатку та зберігає її у базу данних"""
        if not title.strip():
            logger.error("Неправильні параметри для database.Database.create_note")
            raise ValueError("Заголовок нонатки не може бути пустим")

        self.db.execute("INSERT INTO notes VALUES(?, ?)", (title, content))
        self.db.commit()
        logger.success("Створена нова нонатка")

    def change_note(self, old_title: str, new_title: str=None, new_content: str=None) -> None:
        """Змінити нонатку"""
        if not self.__is_note_exists(old_title):
            logger.error("Неправильні параметри database.Database.change_note")
            raise ValueError("Такої нонатки не існує")

        if new_title:
            if not new_title.strip():
                logger.error("Неправильні параметри database.Database.change_note")
                raise ValueError("Заголовок нонатки не може бути пустим")

            if old_title != new_title and self.__is_note_exists(new_title):
                logger.error("Неправильні параметри database.Database.change_note")
                raise ValueError("Нонатка з таким імʼям вже існує")

            self.db.execute("UPDATE notes SET title == ? WHERE title == ?", (new_title, old_title))
            old_title = new_title
            self.db.commit()
            logger.success("Успішно змінено заголовок нонатки")

        if new_content:
            self.db.execute("UPDATE notes SET content == ? WHERE title == ?",
                            (new_content, old_title))
            self.db.commit()
            logger.success("Успішно змінено текст нонатки")

    def delete_note(self, title: str) -> None:
        """Метод видаляє нонатку"""
        if not self.__is_note_exists(title):
            logger.error(f"Нонатки с заголовком {title} не існує")
            raise ValueError("Такої нонатки не існує")

        self.db.execute("DELETE FROM notes WHERE title == ?", (title,))
        self.db.commit()
        logger.success(f"Успішно видалена нонатка з заголовком {title}")

    def delete_all_notes(self) -> None:
        """Метод видаляє всі нонатки користувача"""
        self.db.execute("DELETE FROM notes")
        self.db.commit()
        logger.success("Успішно видалені всі нонатки користувача")

    def get_notes(self) -> list:
        """Метод повертає всі нонатки користувача"""
        result =  self.db.execute("SELECT * FROM notes").fetchall()
        logger.success("Успішно отримані всі нонатки користувача")
        return result

    def get_note(self, title: str) -> list:
        """Отримати інформацію про нонатку"""
        if not self.__is_note_exists(title):
            raise ValueError("Такої нонатки не існує")

        info = self.db.execute("SELECT content FROM notes WHERE title == ?", (title,)).fetchone()
        logger.debug(f"Отримана інформація про нонатку: {info}")
        return [title, info[0]]

    def __is_note_exists(self, title: str) -> bool:
        """Перевіряє, чи існує нонатка с заголовком title"""
        all_notes = self.get_notes()

        for note in all_notes:
            if note[0] == title:
                logger.debug(f"Нонатка з заголовком {title} існує")
                return True

        logger.debug(f"Нонатки з заголовком {title} не існує")
        return False

    def close(self) -> None:
        """Закрити зʼєднаня з базою данних"""
        self.db.close()
        logger.success("Успішно закрито зʼєднаня з базою данних")
