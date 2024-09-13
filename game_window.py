# game_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import random
from results_window import ResultsWindow

class GameWindow(QWidget):
    def __init__(self, time, ranges):
        super().__init__()
        self.time_left = time
        self.start_time = time
        self.ranges = ranges
        self.score = 0
        self.questions_asked = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.initUI()
        self.new_question()
        self.timer.start(1000)

    def initUI(self):
        self.setWindowTitle('Arithmetic Game')
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        
        self.question_label = QLabel('', self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(QFont('Arial', 24))
        layout.addWidget(self.question_label)
        
        self.answer_input = QLineEdit(self)
        self.answer_input.setAlignment(Qt.AlignCenter)
        self.answer_input.setFont(QFont('Arial', 18))
        self.answer_input.returnPressed.connect(self.check_answer)
        layout.addWidget(self.answer_input)
        
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont('Arial', 18))
        layout.addWidget(self.score_label)
        
        self.time_label = QLabel(f'Time: {self.time_left}', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 18))
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)

    def new_question(self):
        operations = list(self.ranges.keys())
        operation = random.choice(operations)
        min_val = self.ranges[operation]['min']
        max_val = self.ranges[operation]['max']
        
        if operation in ['+', '-']:
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            if operation == '-' and b > a:
                a, b = b, a  # Ensure a >= b for subtraction
        elif operation == '×':
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
        else:  # division
            b = random.randint(min_val, max_val)
            a = b * random.randint(min_val, max_val)
        
        self.question = f"{a} {operation} {b}"
        if operation == '×':
            self.answer = a * b
        elif operation == '÷':
            self.answer = a / b
        else:
            self.answer = eval(f"{a} {'+' if operation == '+' else '-'} {b}")
        
        self.question_label.setText(self.question)
        self.answer_input.clear()
        self.answer_input.setFocus()

    def check_answer(self):
        user_answer = self.answer_input.text()
        try:
            if abs(float(user_answer) - self.answer) < 1e-6:
                self.score += 1
            self.questions_asked += 1
            self.score_label.setText(f'Score: {self.score}')
            self.new_question()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

    def update_timer(self):
        self.time_left -= 1
        self.time_label.setText(f'Time: {self.time_left}')
        if self.time_left <= 0:
            self.timer.stop()
            self.end_game()

    def end_game(self):
        self.results_window = ResultsWindow(self.score, self.questions_asked, self.start_time)
        self.results_window.show()
        self.close()