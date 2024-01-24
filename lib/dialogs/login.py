import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QOpenGLVertexArrayObject


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        # Create the label
        website_label = QLabel("Enter your website:", self)

        # Create the text box
        self.website_textbox = QLineEdit(self)

        # Create the button
        login_button = QPushButton("Login", self)

        # Arrange the elements using a layout (optional but recommended)
        layout = QVBoxLayout()
        layout.addWidget(website_label)
        layout.addWidget(self.website_textbox)
        layout.addWidget(login_button)
        self.setLayout(layout)
        login_button.clicked.connect(self.handle_login_click)

    def handle_login_click(self):
        import webbrowser
        website = self.website_textbox.text()  # Get the entered website
        # Perform actions based on the entered website
        print("User entered:", website)  # Example action
        webbrowser.open(website)