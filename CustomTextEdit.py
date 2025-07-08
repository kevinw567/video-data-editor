from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QMimeData

class CustomTextEdit(QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        if source.hasText():
            self.insertPlainText(source.text())
            
