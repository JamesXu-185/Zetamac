# menu_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from game_window import GameWindow

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Arithmetic Game - Menu')
        self.setGeometry(300, 300, 500, 500)
        
        layout = QVBoxLayout()
        
        title_label = QLabel('Arithmetic Game', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)

        self.time_input = QLineEdit(self)
        self.time_input.setValidator(QIntValidator(1, 3600))
        self.time_input.setText('60')
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel('Time (seconds):'))
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)

        range_layout = QGridLayout()
        self.range_inputs = {}
        operations = ['+', '-', '×', '÷']
        for i, op in enumerate(operations):
            min_input = QLineEdit(self)
            max_input = QLineEdit(self)
            min_input.setValidator(QIntValidator())
            max_input.setValidator(QIntValidator())
            min_input.setText('0' if op != '÷' else '1')
            max_input.setText('100' if op in ['+', '-'] else '12')
            range_layout.addWidget(QLabel(f'{op} Range:'), i, 0)
            range_layout.addWidget(min_input, i, 1)
            range_layout.addWidget(QLabel('to'), i, 2)
            range_layout.addWidget(max_input, i, 3)
            self.range_inputs[op] = (min_input, max_input)
        layout.addLayout(range_layout)

        start_button = QPushButton('Start Game', self)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def start_game(self):
        try:
            time = int(self.time_input.text())
            if time <= 0:
                raise ValueError("Time must be a positive integer")

            ranges = {}
            for op, (min_input, max_input) in self.range_inputs.items():
                min_val = int(min_input.text())
                max_val = int(max_input.text())
                if min_val >= max_val:
                    raise ValueError(f"Invalid range for {op}")
                ranges[op] = {'min': min_val, 'max': max_val}

            self.game_window = GameWindow(time, ranges)
            self.game_window.show()
            self.close()

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
