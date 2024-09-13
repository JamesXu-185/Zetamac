# results_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ResultsWindow(QWidget):
    def __init__(self, score, total_questions, total_time):
        super().__init__()
        self.score = score
        self.total_questions = total_questions
        self.total_time = total_time
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Results')
        self.setGeometry(300, 300, 400, 350)
        
        layout = QVBoxLayout()
        
        title_label = QLabel('Game Results', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)
        
        score_label = QLabel(f'Score: {self.score}/{self.total_questions}', self)
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setFont(QFont('Arial', 18))
        layout.addWidget(score_label)
        
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            percentage_label = QLabel(f'Percentage: {percentage:.2f}%', self)
            percentage_label.setAlignment(Qt.AlignCenter)
            percentage_label.setFont(QFont('Arial', 18))
            layout.addWidget(percentage_label)
            
            avg_time = self.total_time / self.total_questions
            avg_time_label = QLabel(f'Average time per question: {avg_time:.2f} seconds', self)
            avg_time_label.setAlignment(Qt.AlignCenter)
            avg_time_label.setFont(QFont('Arial', 18))
            layout.addWidget(avg_time_label)
        else:
            no_questions_label = QLabel('No questions were answered.', self)
            no_questions_label.setAlignment(Qt.AlignCenter)
            no_questions_label.setFont(QFont('Arial', 18))
            layout.addWidget(no_questions_label)
        
        self.play_again_button = QPushButton('Play Again', self)
        self.play_again_button.setFont(QFont('Arial', 18))
        self.play_again_button.clicked.connect(self.play_again)
        layout.addWidget(self.play_again_button)
        
        self.setLayout(layout)

    def play_again(self):
        from menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()