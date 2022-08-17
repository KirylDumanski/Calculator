import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow

from PyQt5.QtGui import QFontDatabase

from typing import Text, Optional, Union

from operator import add, sub, mul, truediv

operations = {
    '+': add,
    '−': sub,
    '×': mul,
    '÷': truediv,
}


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

        # Calculate

    def add_digit(self) -> None:
        """Add digit to entry line by clicking digit button"""
        btn = self.sender()

        if self.ui.entry.text() == '0':
            self.ui.entry.setText(btn.text())
        else:
            self.ui.entry.setText(self.ui.entry.text() + btn.text())

    def clear_all(self) -> None:
        """Clear all (entry line and temp label)"""
        self.ui.entry.setText('0')
        self.ui.temp.clear()

    def clear_entry(self) -> None:
        """Clear entry line"""
        self.ui.entry.setText('0')

    def add_point(self) -> None:
        """Add point to entry line"""
        if '.' not in self.ui.entry.text():
            self.ui.entry.setText(self.ui.entry.text() + '.')

    def add_temp(self) -> None:
        """Add an expression to the temp label"""
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.ui.entry.text())

        if not self.ui.temp.text():
            self.ui.temp.setText(entry + f" {btn.text()} ")
            self.ui.entry.setText('0')

    @staticmethod
    def remove_trailing_zeros(num: Text) -> str:
        """Remove trailing zeros"""
        n = str(float(num))
        return n.replace('.0', '') if n.endswith('.0') else n

    def get_entry_num(self) -> Union[int, float]:
        """Return number from entry line"""
        entry = self.ui.entry.text()
        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float]:
        """Return number from temp label """
        if self.ui.temp.text():
            temp = self.ui.temp.text().split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        """Return math sign from temp label"""
        if self.ui.temp.text():
            return self.ui.temp.text().split()[-1]

    def calculate(self) -> Optional[str]:
        """Perform a calculation, displays and returns the result of a mathematical operation"""
        try:
            temp = self.ui.temp.text()
            entry = self.ui.entry.text()
            result = self.remove_trailing_zeros(
                operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num())
            )
            self.ui.temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
            self.ui.entry.setText(result)
            return result

        except KeyError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
