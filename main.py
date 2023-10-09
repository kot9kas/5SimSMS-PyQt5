import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QComboBox, QGridLayout, QGroupBox, QSpacerItem, QSizePolicy, QFrame,
                             QMenuBar, QAction, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QSettings

class App(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.settings = QSettings("Kot9k", "5sim SMS Receiver") 
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)

        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('5Sim SMS Receiver')
        self.setGeometry(100, 100, 400, 350)

        mainLayout = QVBoxLayout()

        self.themeSwitchButton = QPushButton(self)
        self.themeSwitchButton.setIcon(QIcon('light_icon.png'))
        self.themeSwitchButton.setIconSize(QSize(32, 32))
        self.themeSwitchButton.clicked.connect(self.toggle_theme)
        mainLayout.addWidget(self.themeSwitchButton)

        groupBoxStyle = """
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            border: 1px solid gray;
            border-radius: 10px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #555;
        }
        """
        
        apiGroupBox = QGroupBox("Детали API")
        apiGroupBox.setStyleSheet(groupBoxStyle)
        apiLayout = QGridLayout()

        self.apiKeyLabel = QLabel('API Ключ:')
        self.apiKeyEdit = QLineEdit(self)
        
        self.balanceLabel = QLabel("Баланс: -")
        balanceFont = QFont()
        balanceFont.setPointSize(14)
        balanceFont.setBold(True)
        self.balanceLabel.setFont(balanceFont)
        self.balanceLabel.setAlignment(Qt.AlignCenter)
        
        self.separatorFrame = QFrame()
        self.separatorFrame.setFrameShape(QFrame.HLine)
        self.separatorFrame.setFrameShadow(QFrame.Sunken)
        
        self.checkBalanceButton = QPushButton('Проверить баланс', self)
        self.checkBalanceButton.setFixedSize(150, 40)
        self.checkBalanceButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.checkBalanceButton.clicked.connect(self.checkBalance)

        apiLayout.addWidget(self.apiKeyLabel, 0, 0)
        apiLayout.addWidget(self.apiKeyEdit, 0, 1)
        apiLayout.addWidget(self.separatorFrame, 1, 0, 1, 2)
        apiLayout.addWidget(self.balanceLabel, 2, 0, 1, 2)
        apiLayout.addWidget(self.checkBalanceButton, 3, 0, 1, 2, Qt.AlignCenter)

        apiGroupBox.setLayout(apiLayout)
        mainLayout.addWidget(apiGroupBox)

        numGroupBox = QGroupBox("Детали номера")
        numGroupBox.setStyleSheet(groupBoxStyle)
        numLayout = QGridLayout()

        self.countryLabel = QLabel('Страна:')
        self.countryCombo = QComboBox(self)
        self.countryCombo.addItems(['Afghanistan'])
        self.operatorLabel = QLabel('Оператор:')
        self.operatorCombo = QComboBox(self)
        self.operatorCombo.addItems(['Any', 'iTelecom'])
        self.productLabel = QLabel('Продукт:')
        self.productCombo = QComboBox(self)
        self.productCombo.addItems(['Amazon'])
        self.buyButton = QPushButton('Купить номер', self)
        self.buyButton.setStyleSheet("""
            QPushButton {
                background-color: #3f51b5;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #344495;
            }
        """)
        self.buyButton.clicked.connect(self.buyNumber)

        numLayout.addWidget(self.countryLabel, 0, 0)
        numLayout.addWidget(self.countryCombo, 0, 1)
        numLayout.addWidget(self.operatorLabel, 1, 0)
        numLayout.addWidget(self.operatorCombo, 1, 1)
        numLayout.addWidget(self.productLabel, 2, 0)
        numLayout.addWidget(self.productCombo, 2, 1)
        numLayout.addWidget(self.buyButton, 3, 1, Qt.AlignRight)

        numGroupBox.setLayout(numLayout)
        mainLayout.addWidget(numGroupBox)

        smsGroupBox = QGroupBox("Детали SMS")
        smsGroupBox.setStyleSheet(groupBoxStyle)
        smsLayout = QVBoxLayout()

        self.smsLabel = QLabel('Полученное SMS:')
        self.smsTextEdit = QLineEdit(self)
        self.smsTextEdit.setStyleSheet("padding: 5px; border-radius: 5px;")
        self.checkButton = QPushButton('Проверить SMS', self)
        self.checkButton.setStyleSheet("""
            QPushButton {
                background-color: #ff5722;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e54d13;
            }
        """)
        self.checkButton.clicked.connect(self.checkSMS)

        smsLayout.addWidget(self.smsLabel)
        smsLayout.addWidget(self.smsTextEdit)
        smsLayout.addWidget(self.checkButton)

        smsGroupBox.setLayout(smsLayout)
        mainLayout.addWidget(smsGroupBox)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        mainLayout.addItem(spacer)

        centralWidget = QWidget(self)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)


    def buyNumber(self):
        api_key = self.apiKeyEdit.text()
        country = self.countryCombo.currentText().lower() 
        operator = self.operatorCombo.currentText().lower() 
        product = self.productCombo.currentText().lower() 

        headers = {
            'Authorization': 'Bearer ' + api_key,
            'Accept': 'application/json',
        }
    
        url = f'https://5sim.net/v1/user/buy/activation/{country}/{operator}/{product}'

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            order_id = data.get('id')
            phone_number = data.get('phone')
            self.order_id = order_id
            self.smsTextEdit.setText(f'Bought phone number: {phone_number}')
        elif response.status_code == 400:
            error_message = response.text
            if error_message == "not enough user balance":
                self.smsTextEdit.setText('Insufficient balance. Please top up your account.')
            elif error_message == "not enough rating":
                self.smsTextEdit.setText('Insufficient rating.')
            elif error_message == "select country":
                self.smsTextEdit.setText('Please select a country.')
            elif error_message == "select operator":
                self.smsTextEdit.setText('Please select an operator.')
            elif error_message == "bad country":
                self.smsTextEdit.setText('Invalid country selected.')
            elif error_message == "bad operator":
                self.smsTextEdit.setText('Invalid operator selected.')
            elif error_message == "no product":
                self.smsTextEdit.setText('No product available.')
            elif error_message == "server offline":
                self.smsTextEdit.setText('Server is offline. Please try again later.')
            else:
                self.smsTextEdit.setText('Error buying number.')
        else:
            self.smsTextEdit.setText('Error buying number.')


    def checkSMS(self):
        api_key = self.apiKeyEdit.text()

        if hasattr(self, 'order_id'):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            }
            url = f'https://5sim.net/v1/user/check/{self.order_id}'
            response = requests.get(url, headers=headers)
        
            if response.status_code == 200:
                data = response.json()
                sms_list = data.get('sms', [])
            
                if sms_list:
                    latest_sms = sms_list[-1]
                    sms_text = latest_sms.get('text', '')
                    self.smsTextEdit.setText(sms_text)
                else:
                    self.smsTextEdit.setText('No SMS yet.')
            else:
                self.smsTextEdit.setText('Error checking SMS.')
        else:
            self.smsTextEdit.setText('No order ID available.')

      
    def checkBalance(self):
        api_key = self.apiKeyEdit.text()
        headers = {
            'Authorization': 'Bearer ' + api_key,
            'Accept': 'application/json',
        }
        response = requests.get('https://5sim.net/v1/user/profile', headers=headers)
        if response.status_code == 200:
            data = response.json()
            balance = data.get('balance', '-')
            self.balanceLabel.setText(f"Balance: $ {balance}")
        else:
            self.balanceLabel.setText("Balance: Error fetching")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.apply_dark_theme()
            self.themeSwitchButton.setIcon(QIcon('light_icon.png'))
        else:
            self.apply_light_theme()
            self.themeSwitchButton.setIcon(QIcon('dark_icon.png'))

        self.settings.setValue("dark_mode", self.dark_mode)


    def apply_light_theme(self):
        light_style = """
            QMainWindow, QWidget, QMenuBar, QMenu, QComboBox, QLineEdit, QGroupBox, QPushButton {
                background-color: #f2f2f2;
                color: black;
                border: 1px solid #dcdcdc;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #dcdcdc;
            }
            QLabel, QVBoxLayout {
                color: black;
                background-color: #f2f2f2;
            }
            QPushButton {
                background-color: #e6e6e6;
            }
            QPushButton:hover {
                background-color: #d4d4d4;
            }
        """
        self.setStyleSheet(light_style)

    def apply_dark_theme(self):
        dark_style = """
            QMainWindow, QWidget, QMenuBar, QMenu, QComboBox, QLineEdit, QGroupBox, QPushButton {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #555;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #555;
            }
            QLabel, QVBoxLayout {
                color: white;
                background-color: #2c2c2c;
            }
            QPushButton {
                background-color: #404040;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """
        self.setStyleSheet(dark_style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
    