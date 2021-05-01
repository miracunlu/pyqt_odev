import sys

import serial
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QLineEdit

arduino = serial.Serial('COM3', 9600, timeout=0.1)  # Arduino ile serşal bağlantı oluşturuyoruz


class MyArea(QtWidgets.QWidget):
    def __init__(self):
        super(MyArea, self).__init__()

        # Süre Saydırmak için Kullanılan Elemanlar
        self.txtTime = QtWidgets.QLabel('time', self)
        self.txtTime.move(15, 20)
        self.txtInput = QLineEdit('Sayı Giriniz', self)
        self.txtInput.move(15, 50)
        self.buttonStart = QtWidgets.QPushButton("Start", self)
        self.buttonStart.move(200, 50)
        self.buttonStart.setCheckable(True)
        self.txtMessageInfo = QtWidgets.QLabel('Message: ', self)
        self.txtMessageInfo.move(15, 100)
        self.txtSend = QtWidgets.QLabel('Send ', self)
        self.txtSend.move(200, 100)
        self.txtSend.setVisible(False)
        self.txtReceive = QtWidgets.QLabel('Receive ', self)
        self.txtReceive.move(100, 100)
        self.txtReceive.setVisible(False)

        # LED Yakmak İçin Kulanılan Elemanlar
        self.txtLed = QtWidgets.QLabel('LED', self)
        self.txtLed.move(15, 150)
        self.buttonLedOn = QtWidgets.QPushButton("ON", self)
        self.buttonLedOn.move(15, 175)
        self.buttonLedOn.setCheckable(True)
        self.buttonLedOff = QtWidgets.QPushButton("OFF", self)
        self.buttonLedOff.move(200, 175)
        self.buttonLedOff.setCheckable(True)
        self.txtLedStatus = QtWidgets.QLabel('LED:', self)
        self.txtLedStatus.move(15, 250)
        self.txtLedOn = QtWidgets.QLabel('ON', self)
        self.txtLedOn.move(50, 250)
        self.txtLedOn.setVisible(True)
        self.txtLedOff = QtWidgets.QLabel('OFF', self)
        self.txtLedOff.move(50, 250)
        self.txtLedOff.setVisible(False)
        self.setGeometry(1000, 1000, 500, 500)
        self.setWindowTitle('My Area')
        self.show()

        # butonlara tıklandıgında gidilmesi gereken fonksiyonlar
        self.buttonStart.clicked.connect(self.sure)
        self.buttonLedOn.clicked.connect(self.Led_On)
        self.buttonLedOff.clicked.connect(self.Led_Off)

    def Led_On(self):  # buttonLedOn butonuna tıklandığında çalışan fonksiyon

        self.txtLedOn.setVisible(True)  # buttonLedOn butonuna tıklandığında  ON yazısını görünür yapıyoruz
        self.txtLedOff.setVisible(False)  # buttonLedOn butonuna tıklandığında  FFF yazısını görünmez yapıyoruz
        arduino.write(
            str.encode("0,1\n")
        )  # buttonLedOn butonuna tıklandığında  Arduinoya veri göndermek için kullandığımız kod satırı

    def Led_Off(self):  # buttonLedOff butonuna tıklandığında çalışan fonksiyon
        self.txtLedOn.setVisible(False)  # buttonLedOff butonuna tıklandığında  ON yazısını görünmez yapıyoruz
        self.txtLedOff.setVisible(True)  # buttonLedOff butonuna tıklandığında  OFF yazısını görünür yapıyoruz
        arduino.write(
            str.encode("0,0\n")
        )  # buttonLedOff butonuna tıklandığında  Arduinoya veri göndermek için kullandığımız kod satırı

    def sure(self):  # buttonStart butonuna tıklandığımız zaman çalışan fonksiyon

        self.buttonStart.setUpdatesEnabled(
            False
        )  # butona tıklandığında zaman süre dolana kadar buttonStart işlevsiz hale geliyor
        self.txtInput.setUpdatesEnabled(
            False
        )  # butona tıklandığında zaman süre dolana kadar txtInput işlevsiz hale geliyor
        self.txtSend.setVisible(True)  # butona tıklandığında zaman arayüzde Send yazısını görünür yapıyoruz
        self.txtReceive.setVisible(False)  # butona tıklandığında zaman arayüzde Reveive yazısını görünür yapıyoruz
        arduino.write(
            str.encode(self.txtInput.text() + ",2\n")
        )  # buttonStart butonuna tıklandığında  Arduinoya veri göndermek için kullandığımız kod satırı
        # self.txtInput.text() ile text input bölümüne yazılan sayı değerini çekiyoruz
        deger = 1  # while döngüsünü kırmak için kullandığım değişken
        while deger == 1:

            msg = arduino.readline()  # arduinodan gelen veriyi okumak için kullandığım kod satırı
            print(msg)
            if msg == b'a':  # Eger gelen msj bytes türündeki 'a' ya eşitse if blogunun içine giriyor
                self.buttonStart.setUpdatesEnabled(True)  # buttobStart butonunu aktif ediyor
                self.txtInput.setUpdatesEnabled(True)  # txtInput aktif oluyor
                self.txtSend.setVisible(False)  # Send yazısı görünmez oluyor
                self.txtReceive.setVisible(True)  # Receive yazısı görünür oluyor
                deger = 0


app = QApplication(sys.argv)

mainWindow = MyArea()
status = app.exec_()
sys.exit(status)
