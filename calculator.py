import sys
from PyQt5.QtWidgets import ( # type: ignore
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QFileDialog, QLabel
)
from PyQt5.QtCore import Qt # type: ignore

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Calculator")
        self.setFixedSize(500, 500)

        self.init_ui()
        self.load_history()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # === Top bar with toggle button ===
        top_bar = QHBoxLayout()
        self.toggle_btn = QPushButton("☀️ History")
        self.toggle_btn.clicked.connect(self.toggle_history)
        self.toggle_btn.setStyleSheet("background-color: #FDCB6E; font-weight: bold;")
        top_bar.addStretch()
        top_bar.addWidget(self.toggle_btn)
        self.main_layout.addLayout(top_bar)

        # === Input field ===
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter expression")
        self.input_field.setStyleSheet("font-size: 24px; padding: 10px;")
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.returnPressed.connect(self.evaluate_expression)
        self.main_layout.addWidget(self.input_field)

        # === Buttons ===
        self.create_buttons()

        # === Layout for calculator and history ===
        body_layout = QHBoxLayout()

        self.history = QListWidget()
        self.history.setStyleSheet("background-color: #2C2F33; color: white; font-size: 16px;")
        self.history.setFixedWidth(180)

        self.calc_buttons_layout = QVBoxLayout()
        for row in self.button_rows:
            row_layout = QHBoxLayout()
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setFixedHeight(60)
                btn.setStyleSheet("font-size: 20px;")
                btn.clicked.connect(self.button_clicked)
                row_layout.addWidget(btn)
            self.calc_buttons_layout.addLayout(row_layout)

        body_layout.addLayout(self.calc_buttons_layout)
        body_layout.addWidget(self.history)

        self.main_layout.addLayout(body_layout)

        self.history.setVisible(False)

    def create_buttons(self):
        self.button_rows = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

    def button_clicked(self):
        sender = self.sender()
        text = sender.text()
        current = self.input_field.text()

        if text == "=":
            self.evaluate_expression()
        elif text == "C":
            self.input_field.clear()
        else:
            self.input_field.setText(current + text)

    def evaluate_expression(self):
        expression = self.input_field.text()
        try:
            result = str(eval(expression))
            self.input_field.setText(result)
            log = f"{expression} = {result}"
            self.history.addItem(log)
            with open("history.txt", "a") as f:
                f.write(log + "\n")
        except Exception:
            self.input_field.setText("Error")

    def toggle_history(self):
        self.history.setVisible(not self.history.isVisible())

    def load_history(self):
        try:
            with open("history.txt", "r") as f:
                for line in f:
                    self.history.addItem(line.strip())
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())
# git remote add origin https://github.com/<aryan711lee>/pyqt-calculator.git
