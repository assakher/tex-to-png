from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
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
        super(Tooltips,self).__init__()


class Workspace(QtWidgets.QWidget):
    def __init__(self):
        super(Workspace, self).__init__()

        self.display = Display()
        self.controls = Controls()
        self.user_input = UserInput()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.display)
        layout.addWidget(self.controls)
        layout.addWidget(self.user_input)
        self.setLayout(layout)


class Display(QtWidgets.QLabel):
    def __init__(self):
        super(Display, self).__init__()
        self.setGeometry(0, 0, 200, 200)
        self.image = QtGui.QPixmap()
        self.image.load('1.png')
        self.setPixmap(self.image)

        self.resize(200, 200)

    def update(self) -> None:
        self.image.load("temp.png")
        self.setPixmap(self.image)


class Controls(QtWidgets.QWidget):
    def __init__(self):
        super(Controls, self).__init__()

        self.cancel_btn = CancelBtn()
        self.reset_btn = ResetBtn()
        self.preview_btn = PreviewBtn()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.preview_btn)
        self.setLayout(layout)


class CancelBtn(QtWidgets.QPushButton):
    def __init__(self):
        super(CancelBtn, self).__init__()
        self.setText("Preview")
        self.clicked.connect(self.commit_text)

    def commit_text(self):
        text = self.parentWidget().parentWidget().user_input.get_input()
        window.update_status_bar('Creating preview')
        TeXProcessor.create_png(text)
        window.update_status_bar('Created preview')
        self.parentWidget().parentWidget().display.update()


class ResetBtn(QtWidgets.QPushButton):
    def __init__(self):
        super(ResetBtn, self).__init__()
        self.setText("Reset")


class PreviewBtn(QtWidgets.QPushButton):
    def __init__(self):
        super(PreviewBtn, self).__init__()
        self.setText("Save")


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