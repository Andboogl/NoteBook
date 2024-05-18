"""Показ повідомленнь на єкран"""


from typing import Union
from PyQt6.QtWidgets import QMessageBox


def standart(text: str) -> None:
    """Показати звичайне повідомлення"""
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.exec()


def error(text: str, err: Union[str, Exception]) -> None:
    """Показати повідомлення про помилку"""
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.setDetailedText(str(err))
    message_box.exec()
