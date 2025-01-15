import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json

class EventManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_response)

    def initUI(self):
        self.setWindowTitle('Event Manager')
        layout = QVBoxLayout()

        self.label = QLabel('Events List:')
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.refresh_button = QPushButton('Refresh Events')
        self.refresh_button.clicked.connect(self.fetch_events)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.fetch_events()

    def fetch_events(self):
        url = QUrl('http://localhost:8000/events')
        request = QNetworkRequest(url)
        self.manager.get(request)

    def handle_response(self, reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            data = json.loads(str(bytes_string, 'utf-8'))
            self.list_widget.clear()
            for event in data:
                self.list_widget.addItem(f"{event['name']} - {event['rout']}")

        else:
            print('Error occurred:', reply.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EventManager()
    ex.show()
    sys.exit(app.exec_())