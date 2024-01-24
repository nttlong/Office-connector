import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton,QVBoxLayout
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

# Create the application and window
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec_())