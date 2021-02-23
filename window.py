# pyinstaller --onefile --windowed window.py
import os
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QLabel, QApplication, QFileDialog, QMessageBox)
from sort import *
from tkinter import *


class Example(QWidget):
    dirlist = ''
    readdir = ''
    writedir = ''
    def __init__(self):
        super().__init__()
        self.initUI()

    def myf1(self):
        if len(Example.dirlist) < 2:
            QMessageBox.about(self, "Error", "Please, choose a directory")
            return 0
        files0 = []
        for run in os.listdir(Example.dirlist):
            if os.path.isfile(Example.dirlist + "/" + run) == True:
                files0.append(run)
        self.myf(files0)
        nominal_path_towrite = Example.writedir
        for run in os.listdir(Example.dirlist):
            if os.path.isdir(Example.dirlist + "/" + run) == True:
                Example.readdir = Example.dirlist + "/" + run + "/"
                print(Example.readdir)
                Example.writedir = nominal_path_towrite + '_'.join(run.split('_')[:-1]) + '/'
                shutil.rmtree(Example.writedir, ignore_errors=True)
                os.makedirs(Example.writedir)
                print(Example.writedir)
                self.myf(os.listdir(Example.readdir))


    def finalpath(self):
        fdir = ''
        if len(Example.readdir.split('/')[-1].split('_')) < 2:
            Example.writedir = Example.readdir + '/'
            return 0
        for one in (Example.readdir.split('_'))[:-2]:
            fdir = fdir + one + "_"
        fdir = fdir + str((Example.readdir.split('_'))[-2]) + '/'
        shutil.rmtree(fdir, ignore_errors=True)
        os.makedirs(fdir)
        Example.writedir = fdir
        return 0

    def myf(self,spisok):
        ij = 0
        for run in spisok:
            with open(str(Example.readdir+'/'+run), "r", encoding='cp1251', errors='ignore') as f_obj:
                if str(Example.readdir+'/'+run)[-1] != 'v':
                    continue
                csv_reader(f_obj,Example.writedir,ij)
                ij+=1

    def getDirectory(self):
        Example.dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        Example.readdir = Example.dirlist

    def labe(self):
        self.ql.setText(Example.dirlist)
        self.ql2.setText("")

    def labe1(self):
        self.ql1.setText("Writing to  " + Example.writedir)
        self.ql1.setStyleSheet("QLabel { color: green; text-decoration: underline; }");

    def labe2(self):
        self.ql2.setText("Обработка завершена ")
        self.ql2.setStyleSheet("QLabel { color: red; text-decoration: underline; }");


    def initUI(self):

        openDirButton = QPushButton("Выбрать папку", self)
        openDirButton.move(50,50)
        openDirButton.clicked.connect(self.getDirectory)

        btn1 = QPushButton("Обработать", self)
        btn1.move(50, 150)

        list = []
        for i in range(100000):
            list.append(' ')
        self.ql = QLineEdit(str(''.join(list)),self)
        self.ql.setGeometry(1000,1000,400,25)
        self.ql.move(220,50)
        openDirButton.clicked.connect(self.labe)

        self.ql1 = QLabel(str(''.join(list)),self)
        self.ql1.move(220,150)
        openDirButton.clicked.connect(self.finalpath)
        openDirButton.clicked.connect(self.labe1)
        btn1.clicked.connect(self.myf1)

        self.ql2 = QLabel(str(''.join(list)), self)
        self.ql2.move(220, 350)
        btn1.clicked.connect(self.labe2)

        self.setGeometry(100, 100, 650, 650)
        self.setWindowTitle('Обработчик')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()