import sys
from PyQt4 import QtGui, QtCore
import socket

class FTP(QtGui.QWidget):
    def __init__(self, s):
        super(FTP, self).__init__()
        ss = s
        print(s)
        self.setGeometry(50, 50, 600, 500)
        self.setWindowTitle("FTP - Interface")
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))
        self.home()

    def soquetes(self, s):
        s.send(bytes('TYPE A\r\n', 'ascii'))
        msg = s.recv(1024)
        print(msg)

        s.send(bytes('PASV\r\n', 'ascii'))
        msg = s.recv(1024)
        print(msg)

        msg = str(msg)

        start = msg.find("(")
        end = msg.find(")")
        tp = msg[start + 1:end].split(',')
        port = int(tp[4]) * 256 + int(tp[5])
        print(port)


        s.send(bytes('CWD html\r\n', 'ascii'))
        msg1 = s.recv(2048)
        print(msg1)

        s.send(bytes('PWD oi\r\n', 'ascii'))
        msg1 = s.recv(2048)
        a = str(msg1).split()
        print(a[1][1:-1])
        # msg2 = soc.recv(2048)
        # print(msg2)

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(('192.168.43.241', port))
        s.send(bytes('LIST\r\n', 'ascii'))
        msg2 = self.soc.recv(2048)
        msg2 = ' '.join(str(msg2).split('1000')).split('\\r\\n')
        print(msg2)
        self.styleChoice1 = QtGui.QLabel("Diretório atual:" + a[1][1:-1], self)
        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.move(100,0)
        for i in msg2:
            self.comboBox.addItem(i[(i.find('May') + 13):])
        self.comboBox.view().pressed.connect(self.seleciona_arquivo)

    def seleciona_arquivo(self, index):
        item = self.comboBox.model().itemFromIndex(index).text()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.43.241', 21))

        msg = s.recv(1024)
        print(msg)

        s.send(bytes('USER boreu\r\n', 'ascii'))
        msg = s.recv(1024)
        print(msg)

        s.send(bytes('PASS ap4zx647\r\n', 'ascii'))
        msg = s.recv(1024)
        print(msg)

        s.send(bytes('TYPE A\r\n', 'ascii'))
        msg = s.recv(1024)
        print(msg)

        s.send(bytes('PASV\r\n', 'ascii'))
        msg = s.recv(1024)
        print(msg)

        msg = str(msg)

        start = msg.find("(")
        end = msg.find(")")
        tp = msg[start + 1:end].split(',')
        port = int(tp[4]) * 256 + int(tp[5])
        print(port)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('192.168.43.241', port))

        s.send(bytes('CWD html\r\n', 'ascii'))
        msg1 = s.recv(2048)
        print(msg1)

        s.send(bytes('RETR '+ item + '\r\n', 'ascii'))
        f = open(item, 'wb')
        msg2 = soc.recv(2048)
        f.write(msg2)
        while len(msg2) > 0:
            msg2 = soc.recv(2048)
            f.write(msg2)
        f.close()

    def home(self):
        self.styleChoice1 = QtGui.QLabel("Usuário:", self)
        self.styleChoice1.move(200, 150)
        self.username = QtGui.QLineEdit(self)
        self.username.setPlaceholderText("username")
        self.username.move(250, 150)

        self.styleChoice2 = QtGui.QLabel("Senha:", self)
        self.styleChoice2.move(200, 200)
        self.password = QtGui.QLineEdit(self)
        self.password.setPlaceholderText("password")
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.move(250, 200)

        # btn = QtGui.QPushButton("Conectar", self)
        # btn.clicked.connect(self.conectar)
        # btn.resize(100, 50)
        # btn.move(250, 250)


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 600, 500)
        self.setWindowTitle("FTP - Interface")
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))
        self.home()

    def home(self):
        self.styleChoice1 = QtGui.QLabel("Usuário:", self)
        self.styleChoice1.move(200,150)
        self.username = QtGui.QLineEdit(self)
        self.username.setPlaceholderText("username")
        self.username.move(250,150)


        self.styleChoice2 = QtGui.QLabel("Senha:", self)
        self.styleChoice2.move(200, 200)
        self.password = QtGui.QLineEdit(self)
        self.password.setPlaceholderText("password")
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.move(250, 200)

        btn = QtGui.QPushButton("Conectar", self)
        btn.clicked.connect(self.conectar)
        btn.resize(100, 50)
        btn.move(250,250)


        self.show()

    def conectar(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.43.241', 21))
        msg = s.recv(1024)

        self.user = self.username.text()

        s.send(bytes('USER ' + self.user + '\r\n', 'ascii'))
        msg = s.recv(1024)

        self.passw = self.password.text()

        s.send(bytes('PASS ' + self.passw + '\r\n', 'ascii'))
        msg = s.recv(1024)

        if 'Login successful' in str(msg):
            self.login(s)
        else:
            self.invalido()

    def login(self, s):
        popup = QtGui.QMessageBox.question(self, 'FTP', 'Login realizado com sucesso', QtGui.QMessageBox.Yes)
        pro.soquetes(s)
        pro.show()
        pro.s = s

    def invalido(self):
        popup = QtGui.QMessageBox.question(self, 'FTP', 'Credenciais invalidas', QtGui.QMessageBox.Yes)

    def close_application(self):

        sys.exit()



app = QtGui.QApplication(sys.argv)
pro = FTP(150)
GUI = Window()
sys.exit(app.exec_())

run()
