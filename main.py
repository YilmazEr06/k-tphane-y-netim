from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3
font = QFont("Times",16)
font1 = QFont("Times",30)
kume=[]
db=sqlite3.connect("veritabanı.db")
kalem = db.cursor()
def ustkisim(mevcutsayfa):
    kpt= QPushButton("X",mevcutsayfa)
    kpt.setFont(font1)
    kpt.setGeometry(1200,10,40,40)
    kpt.clicked.connect(pencere.cikisfonk)

    geri = QPushButton("<", mevcutsayfa)
    geri.setFont(font1)
    geri.setGeometry(20, 10, 40, 40)
    geri.clicked.connect(mevcutsayfa.gerifonk)
class iadesyf(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        text = QLabel()
        text.setText("İade Etmek İstediğiniz Kitaba Tıklayınız")
        liste = QListWidget()
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        a = kalem.execute("SELECT * FROM kitaplar")
        for b in a.fetchall():
            if b[2] == 0:
                liste.addItem(b[1])

        text.setFont(font)
        dikey.addWidget(text)
        dikey.addWidget(liste)

        liste.itemClicked.connect(self.iadespencere)
        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()



        self.setLayout(yatay)

    def iadespencere(self,item):
        kitapadi=item.text()
        kalem.execute("UPDATE  odunc_tablo SET durum=0 WHERE kitap_ad=?", (kitapadi,))
        kalem.execute("UPDATE  kitaplar SET durum=1 WHERE kitap_adi=?", (kitapadi,))
        kalem.execute("UPDATE  odunc_tablo SET kitap_ad= '' WHERE kitap_ad=?",(kitapadi,))


        db.commit()



    def gerifonk(self):
        self.close()
class pencere(QWidget):
    def __init__(self):

        super().__init__()

        kpt = QPushButton("X", self)
        kpt.setFont(font1)
        kpt.setGeometry(1200, 10, 40, 40)
        kpt.clicked.connect(self.cikisfonk)

        self.logo= QLabel()
        self.text= QLabel()
        self.odunc= QPushButton("Ödünç İşlemleri")
        self.iade= QPushButton("iade İşlemleri")
        self.ktp= QPushButton("Kitap Kistesi ")
        self.ogrnc= QPushButton("Öğrenci Listesi")
        self.hmd= QPushButton("Hakımmızda")
        self.cikis= QPushButton("Çıkış")
        self.logo.setPixmap(QPixmap("indir.png"))




        self.odunc.setFont(font)
        self.iade.setFont(font)
        self.ktp.setFont(font)
        self.ogrnc.setFont(font)
        self.hmd.setFont(font)
        self.cikis.setFont(font)
        self.text.setFont(font)
        self.text.setText("Kütüphane Sistemi")



        self.cikis.clicked.connect(self.cikisfonk)
        self.ktp.clicked.connect(self.ktplst)
        self.ogrnc.clicked.connect(self.ogrenci)
        self.odunc.clicked.connect(self.odunc1)
        self.iade.clicked.connect(self.iadefonk)



        dikey=QVBoxLayout()
        yatay=QHBoxLayout()

        dikey.addStretch()
        dikey.addWidget(self.text)
        dikey.addWidget(self.logo)
        dikey.addStretch()
        dikey.addWidget(self.odunc)
        dikey.addWidget(self.iade)
        dikey.addWidget(self.ktp)
        dikey.addWidget(self.ogrnc)
        dikey.addWidget(self.hmd)
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
        self.kitap= kitaplst()
        self.kitap.showFullScreen()

    def ogrenci(self):
        self.ogren= ogrencilst()
        self.ogren.showFullScreen()

    def odunc1(self):
        self.v= oduncsayfası()
        self.v.showFullScreen()

    def iadefonk(self):
        self.iade=iadesyf()
        self.iade.showFullScreen()
class oduncsayfası(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        text =QLabel()
        text.setText("ALmak İstediğiniz Kitaba Tıklayınız")
        liste=QListWidget()
        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        a = kalem.execute("SELECT * FROM kitaplar")
        for b in a.fetchall():
            if b[2] == 1:
                liste.addItem(b[1])


        text.setFont(font)
        dikey.addWidget(text)
        dikey.addWidget(liste)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        liste.itemClicked.connect(self.oduncislem)

        self.setLayout(yatay)

    def oduncislem(self,item):
        self.kitapadi= item.text()

        kume.append(self.kitapadi)
        print(kume[0])
        self.a= odunciletisi()
        self.a.show()

    def gerifonk(self):
        self.close()
class odunciletisi(QWidget):
    def __init__(self):
        super().__init__()
        list=QListWidget()
        text=QLabel("Adınızı seçiniz adınız yoksa kayıt oluşturunuz")
        text.setFont(font)
        a = kalem.execute("SELECT * FROM ogrenciler")
        for b in a.fetchall():
            list.addItem(b[1])

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()
        dikey.addWidget(text)
        dikey.addWidget(list)
        yatay.addLayout(dikey)
        list.itemClicked.connect(self.kayit)

        self.setLayout(yatay)

    def kayit(self,item):
        ogrenci=item.text()

        a = kalem.execute("SELECT * FROM odunc_tablo WHERE ogrenci_ad=?",(ogrenci,))
        eski= a.fetchall()[0][2]
        kalem.execute("UPDATE  odunc_tablo SET kitap_ad=?  WHERE ogrenci_ad =?", (kume[0],ogrenci))
        kalem.execute("UPDATE  kitaplar SET durum=1  WHERE kitap_adi =?", (eski,))
        kalem.execute("UPDATE  odunc_tablo SET durum=1  WHERE ogrenci_ad =?", (ogrenci,))
        kalem.execute("UPDATE  kitaplar SET durum=0  WHERE kitap_adi =?", (kume[0],))
        db.commit()
        self.close()
        kume.clear()
class kitaplst(QWidget):
    def __init__(self):
        super().__init__()
        a = kalem.execute("SELECT * FROM kitaplar")
        baslık= QLabel()
        ustkisim(self)
        baslık.setText("kitap listesi")
        baslık.setFont(font)
        kitapeklebtn= QPushButton("Kitap ekle")
        kitapeklebtn.setFont(font)
        liste= QListWidget()

        dikey=QVBoxLayout()
        yatay=QHBoxLayout()

        liste.itemClicked.connect(self.varyok)


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
    def varyok(self,item):
        kitapadı=item.text()
        a = kalem.execute("SELECT * FROM kitaplar WHERE kitap_adi=?",(kitapadı,))
        durum =a.fetchall()[0][2]
        if(durum==1):
            QMessageBox.information(self,"Kitap bilgisi",kitapadı + "  Mevcut")
        else:
            a = kalem.execute("SELECT * FROM odunc_tablo WHERE kitap_ad=?", (kitapadı,))
            kimde=a.fetchall()[0][1]

            QMessageBox.information(self,"Kitap bilgisi",kitapadı+ "adlı kitapın şu anki sahibi " + kimde )


    def kitapeklemek(self):

        self.kitapek=kitapekleme()
        self.kitapek.show()

    def gerifonk(self):
        self.close()
class ogrencilst(QWidget):
    def __init__(self):
        super().__init__()
        ustkisim(self)
        text=QLabel()
        text.setText("Öğrenci Listesi")

        text.setFont(font)
        liste= QListWidget()
        yatay = QHBoxLayout()
        dikey= QVBoxLayout()
        ogrencieklebtn= QPushButton("öğrenci ekle")
        ogrencisilbtn=QPushButton("öğrenci sil")
        ogrencisilbtn.setFont(font)
        ogrencieklebtn.setFont(font)

        ogrencieklebtn.clicked.connect(self.ogrenciek)
        ogrencisilbtn.clicked.connect(self.ogrencisil)
        liste.itemClicked.connect(self.uzrindekitapvar)
        c = kalem.execute('''SELECT * FROM ogrenciler ''')

        for b in c.fetchall():
            liste.addItem(b[1])

        dikey.addWidget(text)
        dikey.addWidget(liste)
        dikey.addWidget(ogrencieklebtn)
        dikey.addWidget(ogrencisilbtn)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()
        self.setLayout(yatay)
    def gerifonk(self):
        self.close()
    def ogrenciek(self):
        self.a=ogrenciekleme()
        self.a.show()
    def ogrencisil(self):
        print("Oğrenci sil")
    def uzrindekitapvar(self,item):
        b=item.text()
        a = kalem.execute("SELECT * FROM odunc_tablo WHERE ogrenci_ad=?", (b,))
        c=a.fetchall()

        if (c[0][3]==1):
            QMessageBox.information(self, "Durum",  "elindeki kitap "+c[0][2] )
            print(c)


        else:
            QMessageBox.information(self, "Durum",  "elinde kitap yok " )
class ogrenciekleme(QWidget):
    def __init__(self):
        super().__init__()
        self.ogrenci=QLineEdit()
        kaydetbtn=QPushButton("Kaydet")
        iptalbtn =QPushButton("İptal")
        yatay =QHBoxLayout()
        dikey =QVBoxLayout()

        self.ogrenci.setPlaceholderText("Öğrenci Adı")
        kaydetbtn.setFont(font)
        iptalbtn.setFont(font)
        self.ogrenci.setFont(font)

        kaydetbtn.clicked.connect(self.ekle)
        iptalbtn.clicked.connect(self.iptalm)



        dikey.addWidget(self.ogrenci)
        dikey.addWidget(kaydetbtn)
        dikey.addWidget(iptalbtn)

        yatay.addLayout(dikey)



        self.setWindowTitle("Öğrenci Ekle")
        self.setGeometry(400,200,300,200)
        self.setLayout(yatay)

    def ekle(self):
        a =self.ogrenci.text()
        kalem.execute('''INSERT INTO ogrenciler(ad) VALUES (?)''',(a,))
        kalem.execute('''INSERT INTO odunc_tablo(ogrenci_ad) VALUES (?)''',(a,))
        db.commit()
        self.close()
    def iptalm(self):
        self.close()
class kitapekleme(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400,200,300,200)
        self.kitapadi=QLineEdit()
        self.kitapadi.setPlaceholderText("kitabın adını yazınız")



        self.eklebtn=QPushButton("EKLE")
        self.eklebtn.clicked.connect(self.kitapkaydi)
        dikey=QVBoxLayout()
        yatay=QHBoxLayout()

        dikey.addWidget(self.kitapadi)
        dikey.addWidget(self.eklebtn)
        yatay.addLayout(dikey)
        self.setLayout(yatay)
    def kitapkaydi(self):
        kitap= self.kitapadi.text()
        kalem.execute('''INSERT INTO kitaplar(kitap_adi) VALUES (?)''',(kitap,))

        db.commit()
        self.close()

class Pencere(QWidget):
    def __init__(self):
        super().__init__()

        mesajKutusu = QMessageBox.question(self,"Mesajımızın Başlığı","Python'ı Sevdin mi?",
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Ok | QMessageBox.Save, QMessageBox.Yes )
        if mesajKutusu == QMessageBox.Yes:
            print("Evet'e Tıkladın!")
        elif mesajKutusu == QMessageBox.No:
            print("Hayır'a Tıkladın!")
        elif mesajKutusu == QMessageBox.Save:
            print("Tamam kaydediyorum !")
        else:
            print("Ok'a tıkladın !")













uygulama = QApplication(sys.argv)
pencere = pencere()
sys.exit(uygulama.exec_())