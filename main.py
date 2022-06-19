from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3
from win32api import GetSystemMetrics
import datetime

date = datetime.datetime.now()

time_string = date.strftime("%Y-%m-%d")
anlik =datetime.datetime.strptime(time_string, "%Y-%m-%d")






font = QFont("Times", 16)
font1 = QFont("Times", 30)
font2 = QFont("Elephant", 10)
kume = []
db = sqlite3.connect("veritabanı.db")
kalem = db.cursor()


def ustkisim(mevcutsayfa):
    print("Width =", GetSystemMetrics(0))
    print("Height =", GetSystemMetrics(1))


    kpt = QPushButton("X", mevcutsayfa)
    kpt.setFont(font1)
    kpt.setGeometry(GetSystemMetrics(0)-50, 10, 40, 40)
    kpt.clicked.connect(pencere.cikisfonk)

    geri = QPushButton("<", mevcutsayfa)
    geri.setFont(font1)
    geri.setGeometry(10, 10, 40, 40)
    geri.clicked.connect(mevcutsayfa.gerifonk)


class iadesyf(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        text = QLabel()
        text.setText("Please select returner")
        liste = QListWidget()
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        a = kalem.execute("SELECT * FROM ogrenciler")
        for b in a.fetchall():
            if b[5] == "0":
                pass
            else:
                liste.addItem(b[1])

        text.setFont(font)
        dikey.addWidget(text)
        dikey.addWidget(liste)

        liste.itemClicked.connect(self.iadespencere)
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def iadespencere(self, item):

        self.iade = iadebilgi(item.text())
        self.iade.show()




    def gerifonk(self):
        self.close()



class iadebilgi(QWidget):
    def __init__(self,item):
        super().__init__()

        self.item=item

        self.veri = kalem.execute("SELECT * FROM ogrenciler WHERE ad=?", (self.item,)).fetchall()
        self.veriodunc = kalem.execute("SELECT * FROM odunc_tablo WHERE ogrenci_ad=? and durum=?", (self.item,1)).fetchall()
        zaman=self.veriodunc[-1][4]
        mevcutzaman =datetime.datetime.strptime(zaman, "%Y-%m-%d")







        self.setWindowTitle("Student information")
        self.setGeometry(400, 200, 300, 200)



        self.gecen_zaman= anlik-mevcutzaman




        l1 = QLabel()
        l1.setFont(font)
        l1.setText(self.veri[0][1])

        l2 = QLabel()
        l2.setFont(font)
        l2.setText("Number:  " + str(self.veri[0][3]))

        l3 = QLabel()
        l3.setFont(font)
        l3.setText("Date of take:  " + str(zaman))


        l4 = QLabel()
        l4.setFont(font)
        l4.setText("Elapsed time:  " + str(self.gecen_zaman.days) + "  day")


        if str(self.veri[0][5])=="0":
            l5 = QLabel()
            l5.setFont(font)
            l5.setText("Book:  No book" )
        else:
            l5 = QLabel()
            l5.setFont(font)
            l5.setText("Book:  " + str(self.veri[0][5]))



        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()










        self.devam = QPushButton("Continue")
        self.devam.setFont(font)
        self.devam.clicked.connect(self.iadeal)

        yatay2.addWidget(l1)


        dikey.addLayout(yatay2)
        dikey.addWidget(l2)
        dikey.addWidget(l5)
        dikey.addWidget(l3)
        dikey.addWidget(l4)

        dikey.addWidget(self.devam)



        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def iadeal(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Receive')
        box.setText('Are you sure that?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Yes')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('No')
        box.exec_()

        if box.clickedButton() == buttonY:
            kalem.execute("UPDATE  ogrenciler SET Kitap=0  WHERE ad =?", (self.veri[0][1],))
            kalem.execute("UPDATE  odunc_tablo SET durum=0  WHERE ogrenci_ad =? and durum=1", (self.veri[0][1],))

            kalem.execute('''INSERT INTO iade_tablo(ogrenci,kitap,tarih,tutma_suresi) VALUES (?,?,?,?)''',(self.veri[0][1],self.veri[0][5], time_string, self.gecen_zaman.days))

            db.commit()
            self.close()
            pencere.iade.close()
            pencere.iadefonk()


        elif box.clickedButton() == buttonN:
            pass


class pencere(QWidget):
    def __init__(self):
        super().__init__()

        kpt = QPushButton("X", self)
        kpt.setFont(font1)
        kpt.setGeometry(GetSystemMetrics(0)-50, 10, 40, 40)
        kpt.clicked.connect(self.cikisfonk)

        self.logo = QLabel()
        self.text = QLabel()
        self.odunc = QPushButton("loan transactions")
        self.iade = QPushButton("return procedures")
        self.ktp = QPushButton("List of books ")
        self.ogrnc = QPushButton("List of students")
        self.hmda = QPushButton("About us")
        self.cikis = QPushButton("Exit")
        self.logo.setPixmap(QPixmap("indir.png"))

        self.odunc.setFont(font)
        self.iade.setFont(font)
        self.ktp.setFont(font)
        self.ogrnc.setFont(font)
        self.hmda.setFont(font)
        self.cikis.setFont(font)
        self.text.setFont(font)
        self.text.setText("Library system app")

        self.cikis.clicked.connect(self.cikisfonk)
        self.ktp.clicked.connect(self.ktplst)
        self.ogrnc.clicked.connect(self.ogrenci)
        self.odunc.clicked.connect(self.odunc1)
        self.iade.clicked.connect(self.iadefonk)
        self.hmda.clicked.connect(self.hakkimizda)

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()

        dikey.addStretch()
        dikey.addWidget(self.text)
        dikey.addWidget(self.logo)
        dikey.addStretch()
        dikey.addWidget(self.odunc)
        dikey.addWidget(self.iade)
        dikey.addWidget(self.ktp)
        dikey.addWidget(self.ogrnc)
        dikey.addWidget(self.hmda)
        dikey.addWidget(self.cikis)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

        self.showFullScreen()
        self.show()

    def cikisfonk(self):
        QApplication.closeAllWindows()

    def ktplst(self):
        self.kitap = kitaplst()
        self.kitap.showFullScreen()

    def ogrenci(self):
        self.ogren = ogrencilst()
        self.ogren.showFullScreen()

    def odunc1(self):
        self.v = oduncsayfası()
        self.v.showFullScreen()

    def iadefonk(self):
        self.iade = iadesyf()
        self.iade.showFullScreen()

    def hakkimizda(self):

        self.hak = hakkımızdasyf()
        self.hak.showFullScreen()


class oduncsayfası(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        text = QLabel()
        text.setText("Click book which you'll give")
        liste = QListWidget()
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()






        a = kalem.execute("SELECT * FROM kitaplar")
        for b in a.fetchall():

            a = kalem.execute("SELECT * FROM ogrenciler WHERE Kitap=?", (b[1],))
            self.adet = len(a.fetchall())
            if b[2]-self.adet == 0:
                pass
            else:
                liste.addItem(b[1])

        text.setFont(font)
        dikey.addWidget(text)
        dikey.addWidget(liste)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        liste.itemClicked.connect(self.oduncislem)

        self.setLayout(yatay)

    def oduncislem(self, item):
        self.kitapadi = item.text()

        kume.append(self.kitapadi)
        print(kume[0])
        self.a = oduncbilgi(self.kitapadi)
        self.a.show()


    def gerifonk(self):
        self.close()

class oduncbilgi(QWidget):
    def __init__(self,item):
        super().__init__()

        self.kitapadı = item
        a = kalem.execute("SELECT * FROM kitaplar WHERE kitap_adi=?", (self.kitapadı,))
        self.veri = a.fetchall()

        a = kalem.execute("SELECT * FROM ogrenciler WHERE Kitap=?", (self.kitapadı,))






        self.setWindowTitle("Book informations")
        self.setGeometry(400, 200, 300, 200)
        width = 300
        height = 250

        l1 = QLabel()
        l1.setFont(font)
        l1.setText("Name:  "+self.veri[0][1])

        l2 = QLabel()
        l2.setFont(font)
        l2.setText("Writer:  " + self.veri[0][5])

        l3 = QLabel()
        l3.setFont(font)
        l3.setText("date of upload:  " + str(self.veri[0][8]))

        l4 = QLabel()
        l4.setFont(font)
        l4.setText("Number of pages:  " + str(self.veri[0][4]))

        l5 = QLabel()
        l5.setFont(font)
        l5.setText("Location:  " + self.veri[0][6])

        l6 = QLabel()
        l6.setFont(font)
        l6.setText("Number:  " + str(self.veri[0][2]))


        l7 = QLabel()
        l7.setFont(font)
        l7.setText("Cost:  " + str(self.veri[0][7]))

        l7 = QLabel()
        l7.setFont(font)
        l7.setText("Cost:  " + str(self.veri[0][7]))

        l8 = QLabel()
        l8.setFont(font)
        l8.setText("Who have these:   " )

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()

        dikey.addWidget(l1)
        dikey.addWidget(l2)
        dikey.addWidget(l3)
        dikey.addWidget(l4)
        dikey.addWidget(l6)
        dikey.addWidget(l7)
        dikey.addWidget(l5)
        dikey.addWidget(l8)


        self.i = 0
        for b in a.fetchall():
            l9 = QLabel()
            l9.setFont(font)
            l9.setText(b[1])
            dikey.addWidget(l9)
            self.i=self.i+1

        l10 = QLabel()
        l10.setFont(font)
        l10.setText("Available:   " + str(self.veri[0][2]-self.i))
        dikey.addWidget(l10)

        self.edit = QPushButton("Continue")
        self.edit.setFont(font)
        self.edit.clicked.connect(self.devam)





        dikey.addWidget(self.edit)




        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def devam(self):
        self.page = kisiletisiodunc(self.veri)
        self.page.show()
        self.close()

class hakkımızdasyf(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        dikey= QVBoxLayout()
        yatay= QHBoxLayout()

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo.jpg"))


        self.text= QLabel("Since 2022")
        self.text.setFont(font2)

        dikey.addStretch()
        dikey.addWidget(self.logo)
        dikey.addWidget(self.text)
        dikey.addStretch()
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()


        self.setLayout(yatay)
        self.showFullScreen()
    def gerifonk(self):
        self.close()

class kisiletisiodunc(QWidget):
    def __init__(self,item):
        super().__init__()
        self.kitap=item
        list = QListWidget()
        text = QLabel("Who will take this book")
        text.setFont(font)
        a = kalem.execute("SELECT * FROM ogrenciler")
        for b in a.fetchall():
            if b[5] == "0":
                list.addItem(b[1])
            else:
                pass

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        dikey.addWidget(text)
        dikey.addWidget(list)
        yatay.addLayout(dikey)
        list.itemClicked.connect(self.sorgu)

        self.setLayout(yatay)

    def sorgu(self,item):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Add?')
        box.setText('Are you sure that?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Yes')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('No')
        box.exec_()

        if box.clickedButton() == buttonY:
            self.kayit(item)

        elif box.clickedButton() == buttonN:
            pass

    def kayit(self, item):
        ogrenci = item.text()
        kitap = self.kitap


        kalem.execute('''INSERT INTO odunc_tablo(ogrenci_ad,kitap_ad,durum,tarih) VALUES (?,?,?,?)''', (ogrenci,kitap[0][1],1,time_string))
        kalem.execute("UPDATE  ogrenciler SET Kitap=?  WHERE ad =?", (kitap[0][1],ogrenci))
        db.commit()
        self.close()
        kume.clear()
        pencere.v.close()
        self.v = oduncsayfası()
        self.v.showFullScreen()







class kitaplst(QWidget):
    def __init__(self):
        super().__init__()
        a = kalem.execute("SELECT * FROM kitaplar")
        baslık = QLabel()
        ustkisim(self)
        baslık.setText("List of books")
        baslık.setFont(font)
        kitapeklebtn = QPushButton("Add book")
        kitapeklebtn.setFont(font)
        liste = QListWidget()

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()

        liste.itemClicked.connect(self.durum)

        for b in a.fetchall():
            liste.addItem(b[1])

        dikey.addWidget(baslık)
        dikey.addWidget(liste)
        dikey.addWidget(kitapeklebtn)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        kitapeklebtn.clicked.connect(self.kitapeklemek)

        self.setLayout(yatay)
        self.show()

    def durum(self, item):

        self.bilgi = oduncbilgi(item.text())
        self.bilgi.show()











    def kitapeklemek(self):

        self.kitapek = kitapekleme()
        self.kitapek.show()

    def gerifonk(self):
        self.close()


class ogrencilst(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        text = QLabel()
        text.setText("List of students")

        text.setFont(font)
        liste = QListWidget()
        yatay = QHBoxLayout()
        dikey = QVBoxLayout()
        ogrencieklebtn = QPushButton("Add student")
        ogrencisilbtn = QPushButton("Delete student")
        ogrencisilbtn.setFont(font)
        ogrencieklebtn.setFont(font)

        ogrencieklebtn.clicked.connect(self.ogrenciek)
        liste.itemClicked.connect(self.uzrindekitapvar)
        c = kalem.execute('''SELECT * FROM ogrenciler ''')

        for b in c.fetchall():
            liste.addItem(b[1])

        dikey.addWidget(text)
        dikey.addWidget(liste)
        dikey.addWidget(ogrencieklebtn)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)

    def gerifonk(self):
        self.close()

    def ogrenciek(self):
        self.a = ogrenciekleme()
        self.a.show()


    def uzrindekitapvar(self, item):
        self.a = ogrencibilgi(item)
        self.a.show()


class ogrenciekleme(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add student")
        self.setGeometry(400, 200, 300, 200)
        width = 300
        height = 350

        self.sex=""

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.person_name = QLineEdit()
        self.person_name.setPlaceholderText("Person's name")

        self.person_number = QLineEdit()
        self.person_number.setPlaceholderText("Person's phonenumber")

        self.adress = QLineEdit()
        self.adress.setPlaceholderText("Person's adress")

        self.gender = QLineEdit()
        self.gender.setPlaceholderText("Person's gender")

        self.gendergrid = QGridLayout()
        self.label = QLabel("What's Your Gender?")
        self.r1 = QRadioButton("Male")
        self.r2 = QRadioButton("Female")
        self.r1.setFont(font)
        self.r2.setFont(font)
        self.label.setFont(font)
        self.gendergrid.addWidget(self.label, 0, 0)
        self.gendergrid.addWidget(self.r1, 1, 0)
        self.gendergrid.addWidget(self.r2, 1, 1)


        self.person_date = QLineEdit()
        self.person_date.setPlaceholderText("Person's birthday")










        kaydetbtn = QPushButton("Add")
        kaydetbtn.setFont(font)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()



        self.person_date.setFont(font)
        self.person_name.setFont(font)
        self.gender.setFont(font)
        self.person_number.setFont(font)
        self.adress.setFont(font)

        self.r2.toggled.connect(self.femaleselected)
        self.r1.toggled.connect(self.maleselected)



        kaydetbtn.clicked.connect(self.ekle)



        dikey.addWidget(self.person_name)
        dikey.addLayout(self.gendergrid)
        dikey.addWidget(self.person_number)
        dikey.addWidget(self.adress)
        dikey.addWidget(self.person_date)
        dikey.addWidget(kaydetbtn)






        yatay.addLayout(dikey)

        self.setWindowTitle("Öğrenci Ekle")
        self.setGeometry(400, 200, 300, 200)
        self.setLayout(yatay)

    def ekle(self):
        try:
            datetime.datetime.strptime(self.person_date.text(), '%Y-%m-%d')
            a = self.person_name.text()
            if a== '' or self.person_date.text()==''or self.person_number.text()==0 or self.adress.text()=='':
                box = QMessageBox()
                box.setIcon(QMessageBox.Question)
                box.setWindowTitle('Wrong!')
                box.setText('Please fill everyhere')
                box.setStandardButtons(QMessageBox.Ok)
                buttonY = box.button(QMessageBox.Ok)
                buttonY.setText('Ok')
                box.exec_()
            else:
                kalem.execute('''INSERT INTO ogrenciler(ad,cinsiyet,Tel_no,adres,dogum_gunu,eklenme_tarihi) VALUES (?,?,?,?,?,?)''', (a,self.sex,self.person_number.text(),self.adress.text(),self.person_date.text(),time_string))
                db.commit()
                self.close()
                pencere.ogrenci()
        except ValueError:
            box = QMessageBox()
            box.setIcon(QMessageBox.Question)
            box.setWindowTitle('Wrong?!')
            box.setText('Incorrect date format, should be YYYY-MM-DD"')
            box.setStandardButtons(QMessageBox.Ok)
            buttonY = box.button(QMessageBox.Ok)
            buttonY.setText('Ok')
            box.exec_()

    def maleselected(self, selected):
        if selected:
            self.sex= "Male"

    def femaleselected(self, selected):
        if selected:
            self.sex="Female"
    def deleteperson(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Delete?!')
        box.setText('Are you sure that?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Evet')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('Iptal')
        box.exec_()

        if box.clickedButton() == buttonY:
            kalem.execute("Delete  From kitaplar where kitap_adi = ?", (self.kitapadı,))
            db.commit()
            self.close()
            pencere.kitap.close()
            pencere.ktplst()

        elif box.clickedButton() == buttonN:
            pass


class ogrencibilgi(QWidget):
    def __init__(self,item):
        super().__init__()

        self.item=item.text()

        self.veri = kalem.execute("SELECT * FROM ogrenciler WHERE ad=?", (item.text(),)).fetchall()







        self.setWindowTitle("Student information")
        self.setGeometry(400, 200, 300, 200)


        l1 = QLabel()
        l1.setFont(font)
        l1.setText(self.veri[0][1])

        l2 = QLabel()
        l2.setFont(font)
        l2.setText("Number:  " + str(self.veri[0][3]))

        l3 = QLabel()
        l3.setFont(font)
        l3.setText("Adress:  " + self.veri[0][6])

        l4 = QLabel()
        l4.setFont(font)
        l4.setText(self.veri[0][2])

        if str(self.veri[0][5])=="0":
            l5 = QLabel()
            l5.setFont(font)
            l5.setText("Book:  No book" )
        else:
            l5 = QLabel()
            l5.setFont(font)
            l5.setText("Book:  " + str(self.veri[0][5]))



        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()








        self.edit = QPushButton("Edit")
        self.edit.setFont(font)
        self.edit.clicked.connect(self.ogrenguncelleme)

        self.delete = QPushButton("Delete this person")
        self.delete.setFont(font)
        self.delete.clicked.connect(self.delete1)

        yatay2.addWidget(l1)
        yatay2.addWidget(l4)


        dikey.addLayout(yatay2)
        dikey.addWidget(l2)
        dikey.addWidget(l3)
        dikey.addWidget(l5)

        dikey.addWidget(self.edit)
        dikey.addWidget(self.delete)



        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def ogrenguncelleme(self):
        self.page = ogrenciduzen(self.veri)
        self.page.show()
    def delete1(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Delete?!')
        box.setText('Are you sure that?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Yes')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('No')
        box.exec_()

        if box.clickedButton() == buttonY:
            kalem.execute("Delete  From ogrenciler where ad = ?", (self.item,))
            db.commit()
            self.close()
            pencere.ogren.close()
            pencere.ogrenci()

        elif box.clickedButton() == buttonN:
            pass

class kitapekleme(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kitap ekleme")
        self.setGeometry(400, 200, 300, 200)
        width = 300
        height = 275

        l1 = QLabel()
        l1.setFont(font)
        l1.setText("Adet:  ")

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.kitapadi = QLineEdit()
        self.kitapadi.setPlaceholderText("kitabın adını yazınız")

        self.yazar = QLineEdit()
        self.yazar.setPlaceholderText("Kitabın yazarını yazınız")

        self.adet = QSpinBox()
        self.adet.setValue(0)

        self.sayfa = QLineEdit()
        self.sayfa.setPlaceholderText("kitabın sayfa sayısını")

        self.fiyat = QLineEdit()
        self.fiyat.setPlaceholderText("kitabın fiyatını yazınız")

        self.konum = QLineEdit()
        self.konum.setPlaceholderText("kitabın konumunu yazınız")



        self.eklebtn = QPushButton("EKLE")
        self.eklebtn.clicked.connect(self.kitapkaydi)


        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()

        self.kitapadi.setFont(font)
        self.yazar.setFont(font)
        self.sayfa.setFont(font)
        self.fiyat.setFont(font)
        self.adet.setFont(font)
        self.konum.setFont(font)

        self.eklebtn.setFont(font)


        yatay2.addWidget(l1)
        yatay2.addWidget(self.adet)
        dikey.addWidget(self.kitapadi)
        dikey.addWidget(self.yazar)
        dikey.addWidget(self.sayfa)
        dikey.addLayout(yatay2)
        dikey.addWidget(self.konum)
        dikey.addWidget(self.fiyat)


        dikey.addWidget(self.eklebtn)
        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def kitapkaydi(self):
        kitap = self.kitapadi.text()
        adet = self.adet.text()
        sayfa = self.sayfa.text()
        yazar = self.yazar.text()
        fiyat = self.fiyat.text()
        konum= self.konum.text()
        kalem.execute('''INSERT INTO kitaplar(kitap_adi,adet,sayfa,yazar,eklenme_tarih,fiyat,konum,durum) VALUES (?,?,?,?,?,?,?,?)''', (kitap,adet,sayfa,yazar,time_string,fiyat,konum,adet))

        db.commit()
        self.close()
        pencere.kitap.close()
        pencere.ktplst()


class kitapbilgi(QWidget):
    def __init__(self,item):
        super().__init__()

        self.kitapadı = item
        a = kalem.execute("SELECT * FROM kitaplar WHERE kitap_adi=?", (self.kitapadı,))
        self.veri = a.fetchall()

        a = kalem.execute("SELECT * FROM ogrenciler WHERE Kitap=?", (self.kitapadı,))






        self.setWindowTitle("kitap bilgi")
        self.setGeometry(400, 200, 300, 200)
        width = 300
        height = 250

        l1 = QLabel()
        l1.setFont(font)
        l1.setText("Name:  "+self.veri[0][1])

        l2 = QLabel()
        l2.setFont(font)
        l2.setText("Writer:  " + self.veri[0][5])

        l3 = QLabel()
        l3.setFont(font)
        l3.setText("date of upload:  " + self.veri[0][8])

        l4 = QLabel()
        l4.setFont(font)
        l4.setText("Number of pages:  " + str(self.veri[0][4]))

        l5 = QLabel()
        l5.setFont(font)
        l5.setText("Location:  " + self.veri[0][6])

        l6 = QLabel()
        l6.setFont(font)
        l6.setText("Number:  " + str(self.veri[0][2]))


        l7 = QLabel()
        l7.setFont(font)
        l7.setText("Cost:  " + str(self.veri[0][7]))

        l7 = QLabel()
        l7.setFont(font)
        l7.setText("Cost:  " + str(self.veri[0][7]))

        l8 = QLabel()
        l8.setFont(font)
        l8.setText("Who have these:   " )

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()

        dikey.addWidget(l1)
        dikey.addWidget(l2)
        dikey.addWidget(l3)
        dikey.addWidget(l4)
        dikey.addWidget(l6)
        dikey.addWidget(l7)
        dikey.addWidget(l5)
        dikey.addWidget(l8)


        i = 0
        for b in a.fetchall():
            l9 = QLabel()
            l9.setFont(font)
            l9.setText(b[1])
            dikey.addWidget(l9)
            self.i=i+1

        l10 = QLabel()
        l10.setFont(font)
        l10.setText("Available:   " + str(self.veri[0][2]-self.i))
        dikey.addWidget(l10)

        self.edit = QPushButton("Edit")
        self.edit.setFont(font)
        self.edit.clicked.connect(self.kitapgun)

        self.delete = QPushButton("Delete this person")
        self.delete.setFont(font)
        self.delete.clicked.connect(self.delete1)




        dikey.addWidget(self.edit)
        dikey.addWidget(self.delete)



        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def kitapgun(self):
        self.page = Kitapduzenleme(self.veri)
        self.page.show()
    def delete1(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Delete?!')
        box.setText('Are you sure that?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Evet')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('Iptal')
        box.exec_()

        if box.clickedButton() == buttonY:
            kalem.execute("Delete  From kitaplar where kitap_adi = ?", (self.kitapadı,))
            db.commit()
            self.close()
            pencere.kitap.close()
            pencere.ktplst()

        elif box.clickedButton() == buttonN:
            pass

class ogrenciduzen(QWidget):
    def __init__(self,item):
        super().__init__()
        self.item=item
        self.setWindowTitle("Student editing")
        self.setGeometry(400, 200, 300, 200)
        width = 350
        height = 300
        self.veri = kalem.execute("SELECT * FROM ogrenciler WHERE ad=?", (item[0][1],)).fetchall()

        self.l1 = QLabel()
        self.l1.setFont(font)
        self.l1.setText("Please write new version:  ")

        self.l2 = QLineEdit()
        self.l2.setFont(font)
        self.l2.setText(str(self.veri[0][4]))

        self.l3 = QLineEdit()
        self.l3.setFont(font)
        self.l3.setText(str(self.veri[0][3]))

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.guncelle = QPushButton("Update")
        self.guncelle.clicked.connect(self.upgrade)


        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()

        self.l1.setFont(font)
        self.l2.setFont(font)
        self.l3.setFont(font)

        self.guncelle.setFont(font)

        dikey.addWidget(self.l1)
        dikey.addWidget(self.l2)
        dikey.addWidget(self.l3)







        dikey.addWidget(self.guncelle)
        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def upgrade(self):


        try:
            kalem.execute("UPDATE ogrenciler SET adres = ? WHERE ad = ? ",(self.l2.text(),str(self.item[0][1]),))
            kalem.execute("UPDATE ogrenciler SET Tel_no = ? WHERE ad = ? ",(self.l3.text(),str(self.item[0][1]),))
            db.commit()
            QMessageBox.question(self, "Complate", "Successfull", QMessageBox.Ok)

        except:
            QMessageBox.question(self, "Uncomplated", "Unsuccesful", QMessageBox.Ok)




        pencere.ogren.close()
        pencere.ogrenci()

class Kitapduzenleme(QWidget):
    def __init__(self,item):
        super().__init__()
        self.item=item
        self.setWindowTitle("Edit book")
        self.setGeometry(400, 200, 300, 200)
        width = 350
        height = 300

        l1 = QLabel()
        l1.setFont(font)
        l1.setText("Amount::  ")

        l2 = QLabel()
        l2.setFont(font)
        l2.setText("Location:  ")

        l3 = QLabel()
        l3.setFont(font)
        l3.setText("Cost:  ")

        self.setFixedWidth(width)
        self.setFixedHeight(height)


        self.adet = QSpinBox()
        self.adet.setValue(item[0][2])

        self.fiyat = QLineEdit()
        self.fiyat.setText(str(item[0][7]))

        self.konum = QLineEdit()
        self.konum.setText(str(item[0][2]))



        self.guncelle = QPushButton("Update")
        self.guncelle.clicked.connect(self.kitapduzenle)


        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        yatay2 = QHBoxLayout()

        self.fiyat.setFont(font)
        self.adet.setFont(font)
        self.konum.setFont(font)

        self.guncelle.setFont(font)

        dikey.addWidget(l2)
        dikey.addWidget(self.konum)
        dikey.addWidget(l3)
        dikey.addWidget(self.fiyat)
        dikey.addWidget(l1)
        dikey.addWidget(self.adet)




        dikey.addWidget(self.guncelle)
        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def kitapduzenle(self):

        adet = self.adet.text()
        fiyat = self.fiyat.text()
        konum= self.konum.text()

        kalem.execute("UPDATE kitaplar SET adet = ? WHERE kitap_adi = ? ",(adet,str(self.item[0][1]),))
        kalem.execute("UPDATE kitaplar SET fiyat = ? WHERE kitap_adi = ? ",(fiyat,str(self.item[0][1]),))
        kalem.execute("UPDATE kitaplar SET konum = ? WHERE kitap_adi = ? ",(konum,str(self.item[0][1]),))


        db.commit()
        pencere.kitap.close()
        pencere.ktplst()





uygulama = QApplication(sys.argv)
pencere = pencere()
sys.exit(uygulama.exec_())
