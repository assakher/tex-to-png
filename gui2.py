import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

import TeXProcessor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("TeX to PNG")

        self.create_menu()
        self.create_central_widget()
        self.create_status_bar()

    def create_menu(self):
        pass

    def create_central_widget(self):
        central_widget = CentralWidget()
        self.setCentralWidget(central_widget)
        self.central_widget = central_widget

    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Loaded")

    def update_status_bar(self, message):
        self.status_bar.showMessage(message)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()

        self.tooltips = Tooltips()
        self.workspace = Workspace()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tooltips)
        layout.addWidget(self.workspace)
        self.setLayout(layout)


class Tooltips(QtWidgets.QTabBar):
    def __init__(self):
        super(Tooltips, self).__init__()


class Workspace(QtWidgets.QWidget):
    def __init__(self):
        super(Workspace, self).__init__()

        self.display = Display()
        self.controls = Controls()
        self.user_input = UserInput()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.display, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.controls)
        layout.addWidget(self.user_input)
        self.setLayout(layout)


class Display(QtWidgets.QLabel):
    def __init__(self):
        super(Display, self).__init__()
        self.setGeometry(0, 0, 200, 200)
        self.setMinimumSize(200, 200)
        self.image = QtGui.QPixmap()
        self.image.load('greeting.png')
        self.setPixmap(self.image)

        self.resize(200, 200)

    def update(self):
        self.image.load("temp.png")
        self.setPixmap(self.image)
        self.resize(200, 200)


class Controls(QtWidgets.QWidget):
    def __init__(self):
        super(Controls, self).__init__()

        self.preview_btn = PreviewBtn()
        self.reset_btn = ResetBtn()
        self.save_btn = SaveBtn()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.preview_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)


class PreviewBtn(QtWidgets.QPushButton):
    def __init__(self):
        super(PreviewBtn, self).__init__()
        self.setText("Preview")
        self.clicked.connect(self.commit_text)

    def commit_text(self):
        text = self.parentWidget().parentWidget().user_input.get_input()
        window.update_status_bar('Creating preview')
        try:
            TeXProcessor.latex_to_pdf(text)
            TeXProcessor.pdf_to_png()
            window.update_status_bar('Created preview')
            self.parentWidget().parentWidget().display.update()
        except RuntimeError:
            window.update_status_bar('Improper expression entered')


class ResetBtn(QtWidgets.QPushButton):
    def __init__(self):
        super(ResetBtn, self).__init__()
        self.setText("Reset")
        self.clicked.connect(self.clear_user_input)

    def clear_user_input(self):
        self.parentWidget().parentWidget().user_input.clear()


class SaveBtn(QtWidgets.QPushButton):
    def __init__(self):
        super(SaveBtn, self).__init__()
        self.setText("Save")
        self.clicked.connect(self.save_file_dialog)

    def save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            "Save", "untitled", "PNG Image (*.png)",
                                                            options=options)
        if filename:
            try:
                TeXProcessor.pdf_to_png(output_file=filename)
            except PermissionError:
                pass


class UserInput(QtWidgets.QTextEdit):
    def __init__(self):
        super(UserInput, self).__init__()

    def get_input(self):
        return self.toPlainText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())