import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QComboBox, QGridLayout, QGroupBox, QSpacerItem, QSizePolicy, QFrame,
                             QMenuBar, QAction, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QSettings

class App(QMainWindow):

    OPERATORS = [
        "any", "019", "activ", "altel", "beeline", "claro", "ee", "globe", "kcell", 
        "lycamobile", "matrix", "megafon", "mts", "orange", "pildyk", "play", 
        "redbullmobile", "rostelecom", "smart", "sun", "tele2", "three", "tigo", 
        "tmobile", "tnt", "virginmobile", "virtual2", "virtual4", "virtual5", 
        "virtual7", "virtual8", "virtual12", "virtual15", "virtual16", "virtual17",
        "virtual18", "virtual19", "virtual20", "virtual21", "virtual22", "virtual23",
        "virtual24", "virtual25", "virtual26", "virtual27", "virtual28", "vodafone", 
        "yota", "zz"
    ]

    SERVICES = [
        "1688", "23red", "32red", "99app", "ace2three", "adidas", "agroinform", 
        "airbnb", "airtel", "aitu", "akelni", "alfa", "algida", "alibaba", "aliexpress", 
        "alipay", "amasia", "amazon", "aol", "astropay", "auchan", "avito", "avon",
        "azino", "b4ucabs", "baidu", "banqi", "bigolive", "billmill", "bisu", "bitaqaty",
        "bitclout", "bittube", "blablacar", "blizzard", "blockchain", "blued", "bolt", "brand20ua",
        "burgerking", "bykea", "cafebazaar", "caixa", "careem", "carousell", "cdkeys", "cekkazan",
        "citaprevia", "citymobil", "clickentregas", "cliqq", "clubhouse", "cmtcuzdan", "coinbase",
        "coinfield", "craigslist", "cryptocom", "dbrua", "deliveroo", "delivery", "dent", "dhani",
        "didi", "digikala", "discord", "disneyhotstar", "divar", "dixy", "dodopizza", "domdara",
        "dominospizza", "dostavista", "douyu", "dream11", "drom", "drugvokrug", "dukascopy", "easypay",
        "ebay", "ebikegewinnspiel", "edgeless", "electroneum", "eneba", "ezbuy", "faberlic", "facebook",
        "fiqsy", "fiverr", "foodpanda", "foody", "forwarding", "freecharge", "galaxy", "gamearena",
        "gameflip", "gamekit", "gamer", "gcash", "get", "getir", "gett", "gg", "gittigidiyor",
        "global24", "globaltel", "globus", "glovo", "google", "grabtaxi", "green", "grindr",
        "hamrahaval", "happn", "haraj", "hepsiburadacom", "hezzl", "hily", "hopi", "hqtrivia",
        "humblebundle", "humta", "huya", "icard", "icq", "icrypex", "ifood", "immowelt", "imo",
        "inboxlv", "indriver", "ininal", "instagram", "iost", "iqos", "ivi", "iyc", "jd", "jkf",
        "justdating", "justdial", "kakaotalk", "karusel", "keybase", "komandacard", "kotak811",
        "kucoinplay", "kufarby", "kvartplata", "kwai", "lazada", "lbry", "lenta", "lianxin", "line",
        "linkedin", "livescore", "magnit", "magnolia", "mailru", "mamba", "mcdonalds", "meetme",
        "mega", "mercado", "michat", "microsoft", "miloan", "miratorg", "mobile01", "momo",
        "monese", "monobank", "mosru", "mrgreen", "mtscashback", "myfishka", "myglo", "mylove",
        "mymusictaste", "mzadqatar", "nana", "naver", "ncsoft", "netflix", "nhseven", "nifty",
        "nike", "nimses", "nrjmusicawards", "nttgame", "odnoklassniki", "offerup", "offgamers",
        "okcupid", "okey", "okta", "olacabs", "olx", "onlinerby", "openpoint", "oraclecloud",
        "oriflame", "other", "ozon", "paddypower", "pairs", "papara", "paxful", "payberry",
        "paycell", "paymaya", "paypal", "paysend", "paytm", "peoplecom", "perekrestok", "pgbonus",
        "picpay", "pof", "pokec", "pokermaster", "potato", "powerkredite", "prajmeriz2020",
        "premiumone", "prom", "proton", "protonmail", "protp", "pubg", "pureplatfrom", "pyaterochka",
        "pyromusic", "q12trivia", "qiwiwallet", "quipp", "rakuten", "rambler", "rediffmail", "reuse",
        "ripkord", "rosakhutor", "rsa", "rutube", "samokat", "seosprint", "sheerid", "shopee",
        "signal", "sikayetvar", "skout", "snapchat", "snappfood", "sneakersnstuff", "socios",
        "sportmaster", "spothit", "ssoidnet", "steam", "surveytime", "swvl", "taksheel", "tango",
        "tantan", "taobao", "telegram", "tencentqq", "ticketmaster", "tiktok", "tinder", "tosla",
        "totalcoin", "touchance", "trendyol", "truecaller", "twitch", "twitter", "uber", "ukrnet",
        "uploaded", "vernyi", "vernyj", "viber", "vitajekspress", "vkontakte", "voopee", "wechat",
        "weibo", "weku", "weststein", "whatsapp", "wildberries", "wingmoney", "winston", "wish",
        "wmaraci", "wolt", "yaay", "yahoo", "yalla", "yandex", "yemeksepeti", "youdo", "youla",
        "youstar", "zalo", "zoho", "zomato"
    ]

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
        self.apiKeyEdit.setText(self.settings.value("api_key", ""))
        self.apiKeyEdit.textChanged.connect(self.saveApiKey)
        
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
        # Страны
        self.countryLabel = QLabel('Страна:')
        self.countryCombo = QComboBox(self)
        self.load_countries()
    
        # Оператор
        self.operatorLabel = QLabel('Оператор:')
        self.operatorCombo = QComboBox(self)
        self.operatorCombo.addItems(self.OPERATORS)

        # Продукт
        self.productLabel = QLabel('Продукт:')
        self.productCombo = QComboBox(self)
        self.productCombo.addItems(self.SERVICES)

        self.buyButton = QPushButton('Купить номер', self)
        
        self.load_settings()

        self.countryCombo.currentIndexChanged.connect(self.save_settings)
        self.operatorCombo.currentIndexChanged.connect(self.save_settings)
        self.productCombo.currentIndexChanged.connect(self.save_settings)

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

    def saveApiKey(self):
        api_key = self.apiKeyEdit.text()
        self.settings.setValue("api_key", api_key)

    def load_countries(self):
        api_key = self.apiKeyEdit.text()
        headers = {
            'Authorization': 'Bearer ' + api_key,
            'Accept': 'application/json',
        }
        response = requests.get('https://5sim.net/v1/guest/countries', headers=headers)
        if response.status_code == 200:
            countries = response.json()
            self.countryCombo.addItems(countries)
        else:
            pass


    def save_settings(self):
        self.settings.setValue("selected_country", self.countryCombo.currentText())
        self.settings.setValue("selected_operator", self.operatorCombo.currentText())
        self.settings.setValue("selected_service", self.productCombo.currentText())

    def load_settings(self):
        selected_country = self.settings.value("selected_country", "")
        selected_operator = self.settings.value("selected_operator", "")
        selected_service = self.settings.value("selected_service", "")

        if selected_country:
            index_country = self.countryCombo.findText(selected_country)
            if index_country != -1:
                self.countryCombo.setCurrentIndex(index_country)

        if selected_operator:
            index_operator = self.operatorCombo.findText(selected_operator)
            if index_operator != -1:
                self.operatorCombo.setCurrentIndex(index_operator)

        if selected_service:
            index_service = self.productCombo.findText(selected_service)
            if index_service != -1:
                self.productCombo.setCurrentIndex(index_service)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
    