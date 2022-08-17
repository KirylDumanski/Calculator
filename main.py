import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow

from PyQt5.QtGui import QFontDatabase


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        # Digits
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        # C, CE
        self.ui.btn_c.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)

        # Point
        self.ui.btn_point.clicked.connect(self.add_point)

        # Temp

        # Negative

        # Math operations

    def add_digit(self) -> None:
        """Adds digit to entry line by clicking digit button"""
        btn = self.sender()

        if self.ui.entry.text() == '0':
            self.ui.entry.setText(btn.text())
        else:
            self.ui.entry.setText(self.ui.entry.text() + btn.text())

    def clear_all(self) -> None:
        """Clears all (entry line and temp label)"""
        self.ui.entry.setText('0')
        self.ui.temp.clear()

    def clear_entry(self) -> None:
        """Clears entry line"""
        self.ui.entry.setText('0')

    def add_point(self) -> None:
        """Adds point to entry line"""
        if '.' not in self.ui.entry.text():
            self.ui.entry.setText(self.ui.entry.text() + '.')

    def add_temp(self) -> None:
        """Adds an expression to the temporary content field"""
        btn = self.sender()

        if not self.ui.temp.text():
            self.ui.temp.setText(self.ui.entry.text() + f" {btn.text()}")
            self.ui.entry.setText('0')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
