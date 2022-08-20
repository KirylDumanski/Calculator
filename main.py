import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow

from PyQt5.QtGui import QFontDatabase

from typing import Text, Optional, Union

from operator import add, sub, mul, truediv

import config

operations = {
    '+': add,
    '−': sub,
    '×': mul,
    '÷': truediv
}


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_length = self.ui.entry.maxLength()

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        # Digits
        for button in config.NUM_BUTTONS:
            getattr(self.ui, button).clicked.connect(self.add_digit)

        # Math operations
        for button in config.MATH_OPERATIONS:
            getattr(self.ui, button).clicked.connect(self.math_operation)

        # Calculate
        self.ui.btn_calc.clicked.connect(self.calculate)

        # C, CE
        self.ui.btn_c.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)

        # Point
        self.ui.btn_point.clicked.connect(self.add_point)

        # Negative
        self.ui.btn_negative.clicked.connect(self.negate)

    def add_digit(self) -> None:
        """Add digit to entry line by clicking digit button"""
        self.clear_temp_if_equal()
        btn = self.sender()

        if btn.objectName() in config.NUM_BUTTONS:
            if self.ui.entry.text() == '0':
                self.ui.entry.setText(btn.text())
            else:
                self.ui.entry.setText(self.ui.entry.text() + btn.text())

    def clear_all(self) -> None:
        """Clear all (entry line and temp label)"""
        self.ui.entry.setText('0')
        self.ui.temp.clear()
        self.clear_temp_if_equal()
        self.set_max_length()
        self.disable_buttons(False)

    def clear_entry(self) -> None:
        """Clear entry line"""
        self.ui.entry.setText('0')
        self.clear_temp_if_equal()
        self.set_max_length()
        self.disable_buttons(False)

    def add_point(self) -> None:
        """Add point to entry line"""
        self.clear_temp_if_equal()
        if '.' not in self.ui.entry.text():
            self.ui.entry.setText(self.ui.entry.text() + '.')

    def add_temp(self) -> None:
        """Add an expression to the temp label"""
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.ui.entry.text())

        if not self.ui.temp.text() or self.get_math_sign() == '=':
            self.ui.temp.setText(entry + f" {btn.text()} ")
            self.ui.entry.setText('0')
            self.set_max_length()

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
        temp = self.ui.temp.text()
        entry = self.ui.entry.text()

        try:
            result = self.remove_trailing_zeros(
                operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num())
            )
            self.ui.temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
            self.ui.entry.setText(result)
            return result

        except KeyError:
            pass

        except ZeroDivisionError:
            self.show_zero_division_error()

    def replace_temp_sign(self) -> None:
        """Change the math sign in the temp label"""
        btn = self.sender()
        self.ui.temp.setText(self.ui.temp.text()[:-2] + f"{btn.text()} ")

    def math_operation(self) -> None:
        """Application logic"""
        btn = self.sender()

        if not self.ui.temp.text():
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:
                    self.replace_temp_sign()
            else:
                try:
                    self.ui.temp.setText(self.calculate() + f" {btn.text()} ")

                except TypeError:
                    pass

                except ZeroDivisionError:
                    self.show_zero_division_error()

    def negate(self) -> None:
        """Add a minus sign to the number in entry line"""
        self.clear_temp_if_equal()
        entry = self.ui.entry.text()
        if '-' not in entry:
            if entry != '0':
                self.ui.entry.setMaxLength(self.entry_max_length + 1)
                self.ui.entry.setText('-' + entry)
        else:
            self.ui.entry.setText(entry[1:])
            self.set_max_length()

    def set_max_length(self) -> None:
        """Set max length to the entry line"""
        self.ui.entry.setMaxLength(self.entry_max_length)

    def clear_temp_if_equal(self) -> None:
        """Clear the temp label if it contains '=' """
        if self.get_math_sign() == '=':
            self.ui.temp.clear()

    def show_zero_division_error(self) -> None:
        """Show zero division error"""
        self.ui.entry.setMaxLength(len(config.ERROR_ZERO_DEV))
        self.ui.entry.setText(config.ERROR_ZERO_DEV)
        self.disable_buttons(True)

    def disable_buttons(self, disable: bool) -> None:
        """Disable buttons"""
        for button in config.BUTTONS_TO_DISABLE:
            getattr(self.ui, button).setDisabled(disable)

        color = 'color: #A1A1A1' if disable else 'color: black'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str) -> None:
        """Change buttons color"""
        for button in config.BUTTONS_TO_DISABLE:
            getattr(self.ui, button).setStyleSheet(css_color)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
