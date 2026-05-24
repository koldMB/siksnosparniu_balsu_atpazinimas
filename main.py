import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from configparser import ConfigParser
from Balso_Atradimas import *


input_path = os.path.join(os.path.dirname(__file__), "Input_Image.png")

arguments = ConfigParser()
arguments.read('args.ini')

class ArgumentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Isvestis")
        self.setMinimumSize(480, 360)
        layout = QVBoxLayout()

        self.warning = QLabel("Aargumentai bus pakeisti tik uždarius šį langą")
        layout.addWidget(self.warning)

        self.MinAukstisLabel = QLabel("minimalus paveikslėlio aukštis nuo kurio apdirbamas paveiklsėlis:")
        self.MinAukstis = QSpinBox(self)
        self.MinAukstis.setRange(0, 256)
        self.MinAukstis.setValue(arguments.getint('Arguments', 'MinAukstis'))
        self.MinAukstis.setSuffix(" px")
        layout.addWidget(self.MinAukstisLabel)
        layout.addWidget(self.MinAukstis)

        self.MaxAukstisLabel = QLabel("maksimalus paveikslėlio aukštis nuo kurio apdirbamas paveiklsėlis (negali būti mažesnis už minimalią vertę):")
        self.MaxAukstis = QSpinBox(self)
        self.MaxAukstis.setRange(0, 256)
        self.MaxAukstis.setValue(arguments.getint('Arguments', 'MaxAukstis'))
        self.MaxAukstis.setSuffix(" px")
        layout.addWidget(self.MaxAukstisLabel)
        layout.addWidget(self.MaxAukstis)

        self.AukscioTolerancijaLabel = QLabel("Aukščio tolerancija (minimalus aukštis kad būtų fiksuojama koordinatės):")
        self.AukscioTolerancija = QSpinBox(self)
        self.AukscioTolerancija.setValue(arguments.getint('Arguments', 'AukscioTolerancija'))
        self.AukscioTolerancija.setSuffix(" px")
        layout.addWidget(self.AukscioTolerancijaLabel)
        layout.addWidget(self.AukscioTolerancija)

        self.IlgioTolerancijaLabel = QLabel("Ilgio tolerancija (minimalus Ilgis kad būtų fiksuojama koordinatės):")
        self.IlgioTolerancija = QSpinBox(self)
        self.IlgioTolerancija.setValue(arguments.getint('Arguments', 'IlgioTolerancija'))
        self.IlgioTolerancija.setSuffix(" px")
        layout.addWidget(self.IlgioTolerancijaLabel)
        layout.addWidget(self.IlgioTolerancija)

        self.PlocioTolerancijaLabel = QLabel("Kiek procentų pločio turi būti padengta, kad nebebūtų fiksuojamos koordinatės")
        self.PlocioTolerancija = QSpinBox(self)
        self.PlocioTolerancija.setValue(arguments.getint('Arguments', 'PlocioTolerancija'))
        self.PlocioTolerancija.setSuffix("%")
        layout.addWidget(self.PlocioTolerancijaLabel)
        layout.addWidget(self.PlocioTolerancija)

        self.setLayout(layout)
    def closeEvent(self, event):
        arguments.set('Arguments', 'MinAukstis', str(self.MinAukstis.value()))
        arguments.set('Arguments', 'MaxAukstis', str(self.MaxAukstis.value()))
        arguments.set('Arguments', 'AukscioTolerancija', str(self.AukscioTolerancija.value()))
        arguments.set('Arguments', 'IlgioTolerancija', str(self.IlgioTolerancija.value()))
        arguments.set('Arguments', 'PlocioTolerancija', str(self.PlocioTolerancija.value()))
        with open('args.ini', 'w') as args:
            arguments.write(args)
        event.accept

class Error_NoImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Įvyko klaida")
        self.setMinimumSize(480, 360)

        layout = QVBoxLayout()
        self.ErrorLabel = QLabel("Įvyko klaida, nerastas paveikslėlis")
        layout.addWidget(self.ErrorLabel)
        self.setLayout(layout)

class OutputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Isvestis")
        self.setMinimumSize(480, 360)

        self.ImageLabel = QLabel(self)
        self.ImageLabel.setMinimumSize(480, 360)
        self.refreshtimer = QTimer(self)
        self.refreshtimer.timeout.connect(self.refresh_image)
        self.refreshtimer.start(1000)
        self.refresh_image()
        
    def refresh_image(self):
        self.OutputImage = QPixmap(os.path.join(os.path.dirname(__file__), "BWlygmuo.png"))
        self.ImageLabel.setPixmap(self.OutputImage)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("siksnosparniu balsu atpazinimas")
        self.setMinimumSize(640, 480)
        self.ArgWindow = ArgumentWindow()
        self.OutWindow = OutputWindow()
        self.ErrorWindow = None
        Toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Toolbar)
        Toolbar_Argument_Button = QAction("Argumentai", self)
        Toolbar_Argument_Button.triggered.connect(self.Show_Argument_window)
        Toolbar.addAction(Toolbar_Argument_Button)

        Toolbar_Output_Button = QAction("Ribu Radimas", self)
        Toolbar_Output_Button.triggered.connect(self.Ribu_Radimas)
        Toolbar.addAction(Toolbar_Output_Button)

        Toolbar_Output_Button = QAction("Isvestis", self)
        Toolbar_Output_Button.triggered.connect(self.Show_Output_window)
        Toolbar.addAction(Toolbar_Output_Button)



        ImageLabel = QLabel(self)
        InputImage = QPixmap(input_path)
        ImageLabel.setPixmap(InputImage)
        self.setCentralWidget(ImageLabel)
    def Show_Error_Window(self):
        self.ErrorWindow = Error_NoImage()
        self.ErrorWindow.show()

    def Show_Argument_window(self, checked):
        self.ArgWindow.show()
    
    def Show_Output_window(self, checked):
        output = Balsu_atpazinimas(input_path)
        if output == -1:
            self.Show_Error_Window()
        else:
            self.OutWindow.show()
    
    def Ribu_Radimas(self, checked):
        output = RaskRibas(input_path)
        if output == -1:
            self.Show_Error_Window()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
