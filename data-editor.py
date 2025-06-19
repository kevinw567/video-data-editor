import sys

from datetime import datetime
from mutagen.mp4 import MP4

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QDateEdit, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QCheckBox, QTabWidget


class DragDropLabel(QLabel):
    fileDropped = pyqtSignal(dict) # signal to emit metadata
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.filepath = ""
        self.metadata = {}
        
        self.setAcceptDrops(True)
        self.setText("Drag and drop afile here or click to open a file")
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        self.setFixedHeight(300)
        
    
    # accept event when a file is dragged over the widget
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    
    # accept file when dropped
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            filepath = event.mimeData().urls()[0].toLocalFile()
            self.filepath = filepath
            self.setText(f"File dropped: {filepath}")
            print("File dropped:", filepath)
            self.metadata = dict(MP4(filepath)) if filepath else {}
            print("Metadata:", self.metadata)
            self.setWindowTitle("Editing file: " + filepath)
            self.fileDropped.emit(self.metadata)
        
        
            
    
    # open file dialog when widget is clicked        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")
            if file_path:
                self.setText(f"File selected: {file_path}")
                self.filepath = file_path
                self.metadata = MP4(file_path) if file_path else {}
                
                
    def get_file_path(self):
        return self.filepath if self.filepath else None
    
    
    def get_metadata(self):
        return self.metadata

        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = ""
        self.description = ""
        self.comment = ""
        self.date = "" 
        
        self.setWindowTitle("Metadata Editor")
        self.setFixedWidth(800)
        
        self.file_dialog = DragDropLabel()
        self.file_dialog.fileDropped.connect(self.update_metadata)
        metadata = self.file_dialog.get_metadata()
        
        self.setGeometry(500, 500, 800, 600)
        
        # Create a label and input field for the title
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Times", 20))
        self.title_label.setText("Title: ")
        
        self.title_input = QTextEdit(self)
        self.title_input.setAcceptRichText(True)
        self.title_input.setPlaceholderText(metadata['\xa9nam'][0] if '\xa9nam' in metadata else "")
        self.title_input.setFixedHeight(100)
        self.title_input.setFixedWidth(350)
        self.title_input.setMinimumWidth(700)
        self.title_input.setFont(QFont("Segoe UI Emoji", 12))
        # allow tabbing out when widget is focused
        self.title_input.setTabChangesFocus(True)
        
        
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_input)
        
        # Create a label and input field for the description
        self.description_label = QLabel()
        self.description_label.setFont(QFont("Times", 20))
        self.description_label.setText("Description: ")
        
        self.description_input = QTextEdit(self)
        self.description_input.setFont(QFont("Segoe UI Emoji", 12))
        self.description_input.setAcceptRichText(True)
        self.description_input.setPlaceholderText(metadata['desc'][0] if 'desc' in metadata else "")
        self.description_input.setFixedHeight(100)
        self.description_input.setFixedWidth(350)
        self.description_input.setMinimumWidth(620)
        # allow tabbing out when widget is focused
        self.description_input.setTabChangesFocus(True)
        
        description_layout = QHBoxLayout()
        description_layout.addWidget(self.description_label)
        description_layout.addWidget(self.description_input)
        
        
        # create a label and input field for the comments field
        self.comment_label = QLabel()
        self.comment_label.setFont(QFont("Times", 20))
        self.comment_label.setText("Comment: ")
        
        self.comment_input = QTextEdit(self)
        self.comment_input.setFont(QFont("Segoe UI Emoji", 12))
        self.comment_input.setAcceptRichText(True)
        self.comment_input.setPlaceholderText(metadata['\xa9cmt'][0] if '\xa9cmt' in metadata else "")
        self.comment_input.setFixedHeight(100)
        self.comment_input.setFixedWidth(350)
        self.comment_input.setMinimumWidth(620)
        # allow tabbing out when widget is focused
        self.comment_input.setTabChangesFocus(True)
        
        comment_layout = QHBoxLayout()
        comment_layout.addWidget(self.comment_label)
        comment_layout.addWidget(self.comment_input)
        
        # Create a label and date input field for the date
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Times", 20))
        self.date_label.setText("Date: ")
        
        
        self.date_input = QDateEdit(self)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)
        self.date_input.setFixedHeight(40)
        self.date_input.setFixedWidth(150)
        # self.date_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        date = datetime.strptime(self.date, "%Y-%m-%d") if self.date else datetime.now()
        self.date_input.setDate(date)
        
        self.clear_date = QCheckBox("Clear Date")
        self.clear_date.setToolTip("Check this box to clear the date field when saving")
        self.clear_date.setChecked(False)
        self.clear_date.setFont(QFont("Times", 8))
        
        self.ignore_date = QCheckBox("Ignore Date")
        self.ignore_date.setToolTip("Check this box to ignore the date field when saving")
        self.ignore_date.setChecked(False)
        self.ignore_date.setFont(QFont("Times", 8))
        
        
        # self.date_force_button = QCheckBox("Force Overwrite Date")
        # self.date_force_button.setChecked(False)
        # self.date_force_button.setFont(QFont("Times", 10))
        
        
        # create the date layout
        date_layout = QHBoxLayout()
        date_layout.setSpacing(20)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_input, alignment=Qt.AlignmentFlag.AlignLeft)
        # date_layout.addWidget(self.date_force_button, alignment=Qt.AlignmentFlag.AlignLeft)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        date_layout.addWidget(self.clear_date, alignment=Qt.AlignmentFlag.AlignLeft)
        date_layout.addWidget(self.ignore_date, alignment=Qt.AlignmentFlag.AlignLeft)
        
        
        # Create the save button
        self.save_button = QPushButton("Save", self)
        self.save_button.setFixedHeight(40)
        self.save_button.setFixedWidth(100)
        self.save_button.clicked.connect(self.save_metadata)
        
        # create clear all button
        self.clear_all_button = QPushButton("Clear All", self)
        self.clear_all_button.setFixedHeight(40)
        self.clear_all_button.setFixedWidth(100)
        self.clear_all_button.clicked.connect(self.clear_all)
        
        # create the save button layout
        button_row = QHBoxLayout()
        button_row.addWidget(self.save_button)
        button_row.addWidget(self.clear_all_button)
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        # Create the main layout of the window
        layout = QVBoxLayout()
        layout.addWidget(self.file_dialog)
        layout.addLayout(title_layout)
        layout.addLayout(description_layout)
        layout.addLayout(comment_layout)
        layout.addLayout(date_layout)
        layout.addLayout(button_row)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
        container = QWidget()
        container.setLayout(layout)
        

        self.tabs = QTabWidget()
        self.tabs.addTab(container, "Edit Single File")
        self.tabs.addTab(EditMultipleWindow(), "Edit Multiple Files")
        self.tabs.addTab(CopyWindow(), "Copy to")
        
        
        # Set the central widget of the Window.
        self.setCentralWidget(self.tabs)

        
        # allow tabbing between the widgets
        container.setTabOrder(self.title_input, self.description_input) 
        container.setTabOrder(self.description_input, self.comment_input)
        container.setTabOrder(self.comment_input, self.date_input)
        container.setTabOrder(self.date_input, self.save_button)
        
    
    def update_metadata(self, metadata):
        # save the new metadata to the instance variables
        self.title = metadata['\xa9nam'][0] if '\xa9nam' in metadata else ""
        self.description = metadata['desc'][0] if 'desc' in metadata else ""
        self.comment = metadata['\xa9cmt'][0] if '\xa9cmt' in metadata else ""
        self.date = metadata['\xa9day'][0] if '\xa9day' in metadata else ""
        
        # update UI with new metadata
        self.title_input.setText(self.title)
        self.description_input.setText(self.description)
        self.comment_input.setText(self.comment)
        if self.date and '\xa9day' in metadata:
            date = self.date.split("T")[0]
            self.date_input.setDate(datetime.strptime(date, "%Y-%m-%d"))
            
        # elif '\xa9day' not in metadata:
        else:
            return
            
        # else:
        #     self.date_input.setDate(datetime.now())
            
        self.setWindowTitle("Editing file: " + self.file_dialog.get_file_path())
    
    
    def clear_all(self):
        filepath = self.file_dialog.get_file_path()
        v = MP4(filepath)
        # clear all metadata fields
        self.title_input.clear()
        self.description_input.clear()
        self.comment_input.clear()
        self.date_input.clear()
        
        del v['\xa9nam']
        del v['desc']
        del v['\xa9cmt']
        del v['\xa9day']
        v.save()
        # reset the window title
        self.setWindowTitle("Metadata Editor")
    
    
    # write the new metadata to the file
    def save_metadata(self):
        # ensure filepath is set
        filepath = self.file_dialog.get_file_path()
        if not filepath:
            print("No file selected")
            return
        
        # load the media file
        v = MP4(filepath)
        
        # update metadata fields
        if self.title_input.toPlainText() != self.title:
            v['\xa9nam'] = self.title_input.toPlainText()
        if self.description_input.toPlainText() != self.description:
            v['desc'] = self.description_input.toPlainText()
        if self.comment_input.toPlainText() != self.comment:
            v['\xa9cmt'] = self.comment_input.toPlainText()
        if self.clear_date.isChecked():
            del v['\xa9day']
        if self.date_input.text() and not self.ignore_date.isChecked():
            v['\xa9day'] = self.date_input.date().toString("yyyy-MM-dd")
            
        # save the updated metadata
        try: 
            v.save()
            print(f"Metadata saved successfully to {filepath}: {v}")
            self.setWindowTitle("Metadata saved successfully")
        
        except Exception as e:
            print(f"Error saving metadata: {e}")


class CopyWindow(QWidget):
    def __init__(self):
        super().__init__()
        pass


class EditMultipleWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        page_layout = QVBoxLayout(self)
        self.file_dialog = DragDropLabel(self)
        page_layout.addWidget(self.file_dialog, alignment=Qt.AlignmentFlag.AlignTop)
        page_layout.addWidget(MainWindow())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())