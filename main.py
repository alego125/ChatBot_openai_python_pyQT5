import sys
import openai
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox, QAction, QInputDialog


class ChatWindow(QMainWindow):
    """Main window class that defines the chat interface"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configure main window
        self.setWindowTitle('ChatGPT')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")

        # Configure menu bar
        menubar = self.menuBar()
        menubar.setStyleSheet("color: black")
        filemenu = menubar.addMenu('Archivo')

        # Add "Enter API key" action
        apikey_action = QAction('Ingresar API key', self)
        apikey_action.setShortcut('Ctrl+A')
        apikey_action.triggered.connect(self.show_apikey_dialog)
        filemenu.addAction(apikey_action)

        # Add "Exit" action
        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        filemenu.addAction(exit_action)

        # Configure central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Configure labels, text fields and buttons
        self.history_label = QLabel('Historial de chat:', self.central_widget)
        self.history_label.move(20, 10)
        self.history_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.history = QTextEdit(self.central_widget)
        self.history.setReadOnly(True)
        self.history.setGeometry(20, 40, 760, 400)
        self.history.setStyleSheet("background-color: #f2f2f2; color: black; border: 2px solid #cccccc;")

        self.message_label = QLabel('Escriba su mensaje:', self.central_widget)
        self.message_label.move(20, 450)
        self.message_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.message = QLineEdit(self.central_widget)
        self.message.setGeometry(20, 480, 600, 30)
        self.message.setStyleSheet("background-color: white; color: black; border: 2px solid #cccccc; font-size: 16px;")

        self.send_button = QPushButton('Enviar', self.central_widget)
        self.send_button.setGeometry(640, 480, 140, 30)
        self.send_button.setStyleSheet("background-color: #007bff; color: white; border: none; font-size: 16px;")
        self.send_button.clicked.connect(self.send_message)

        # Add menu bar to main window
        self.setMenuBar(menubar)

    def show_apikey_dialog(self):
        """Method that generates a popup window to enter the OpenAI API key"""

        text, ok = QInputDialog.getText(self, 'Ingresar API key', 'Ingrese su API key:')
        if ok:
            self.apikey = text            
            QMessageBox.information(self, 'API key', 'API key ingresada correctamente.')

    def send_message(self):
        """Function that sends the prompt message to OpenAI's GPT-3 model and displays the response in the chat history"""

        # Check if the API key has been entered; if not, show the API key dialog
        if not hasattr(self, 'apikey'):        
            self.show_apikey_dialog()
            return

        message = self.message.text()

        # If the user entered a message, send it to OpenAI and ChatGPT for a response
        if message:
            # Set the OpenAI API key
            openai.api_key = self.apikey
            # Set api config
            response = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=message,
                            max_tokens=1024,
                            n=1,
                            stop=None,
                            temperature=0.3,
                        )
            if response:                
                self.history.setStyleSheet('font-weight: bold; font-size: 18px;')
                self.history.append('<font color="blue">\nYo: \n\n</font>' + message)
                # We use html to modify color text into textbox   
                self.history.append('<font color="red">\nChatGPT: </font>' + response.choices[0].text)
                # Append line to separete conversation dialogs
                self.history.append('---------------------------------------------')
            else:
                QMessageBox.warning(self, 'Error', 'Ocurrió un error al enviar el mensaje.')
            self.message.clear()


if __name__ == '__main__':
    # Create instances and call them
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())
