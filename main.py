import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIntValidator
import random

class ZetamacGame(QWidget):
    def __init__(self):
        super().__init__()
        self.time_left = 60  # Default time
        self.score = 0
        self.questions_asked = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Zetamac-like Arithmetic Game')
        self.setGeometry(300, 300, 400, 350)
        
        layout = QVBoxLayout()
        
        self.question_label = QLabel('Set time and press Start to begin!', self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(QFont('Arial', 18))
        layout.addWidget(self.question_label)
        
        self.answer_input = QLineEdit(self)
        self.answer_input.setAlignment(Qt.AlignCenter)
        self.answer_input.setFont(QFont('Arial', 16))
        self.answer_input.returnPressed.connect(self.check_answer)
        layout.addWidget(self.answer_input)
        
        # Time input layout
        time_layout = QHBoxLayout()
        self.time_input_label = QLabel('Time (seconds):', self)
        self.time_input = QLineEdit(self)
        self.time_input.setValidator(QIntValidator(1, 3600))  # Limit input to integers between 1 and 3600
        self.time_input.setText(str(self.time_left))  # Set default value
        time_layout.addWidget(self.time_input_label)
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)
        
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)
        
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)
        
        self.time_label = QLabel(f'Time: {self.time_left}')
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)

    def start_game(self):
        try:
            self.time_left = int(self.time_input.text())
            if self.time_left <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Time", "Please enter a valid positive number for the time.")
            return

        self.score = 0
        self.questions_asked = 0
        self.start_button.setEnabled(False)
        self.time_input.setEnabled(False)
        self.answer_input.setEnabled(True)
        self.answer_input.setFocus()
        self.timer.start(1000)
        self.update_timer()
        self.new_question()

    def new_question(self):
        operations = ['+', '-', '*']
        operation = random.choice(operations)
        a = random.randint(0, 100)
        if operation == '+':
            b = random.randint(0, 100)
        elif operation == '-':
            b = random.randint(0, a)  # Ensure b is not greater than a
        else:  # multiplication
            a = random.randint(0, 12)
            b = random.randint(0, 12)
        
        self.question = f"{a} {operation} {b}"
        self.answer = eval(self.question)
        self.question_label.setText(self.question)
        self.answer_input.clear()

    def check_answer(self):
        user_answer = self.answer_input.text()
        try:
            if int(user_answer) == self.answer:
                self.score += 1
            self.questions_asked += 1
            self.score_label.setText(f'Score: {self.score}')
            self.new_question()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

    def update_timer(self):
        self.time_label.setText(f'Time: {self.time_left}')
        if self.time_left <= 0:
            self.timer.stop()
            self.end_game()
        else:
            self.time_left -= 1

    def end_game(self):
        self.answer_input.setEnabled(False)
        self.start_button.setEnabled(True)
        self.time_input.setEnabled(True)
        self.question_label.setText(f'Game Over! Score: {self.score}/{self.questions_asked}')
        QMessageBox.information(self, "Game Over", f"Time's up!\nYou answered {self.score} out of {self.questions_asked} questions correctly.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ZetamacGame()
    game.show()
    sys.exit(app.exec_())