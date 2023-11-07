
from torch import device, hub

from numpy.random import randint
from random import sample

def c_hashed(symbol='QWUYERIPOFGSHKJLVZBXNMqwertyuiopkhdfslkxzcbnm1234567890'): return "".join(sample(symbol, randint(8, 16)))
language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000  # 48000
speaker = 'aidar'  # aidar, baya, kseniya, xenia, random, ruslan, irina
put_accent = True
put_yo = True
device = device('cpu')  # cpu или gpu
model, _ = hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)
from soundfile import write
def va_speak(what: str, speak, rate, accent, yo):
    audio = model.apply_tts(text=what + "..",
                            speaker=speak,
                            sample_rate=rate,
                            put_accent=accent,
                            put_yo=yo)
    return audio
def downloadAudio(what, speak, rate, accent, yo, path):
    write((path+c_hashed()+"-Atutum-convertil"+'.mp3'), va_speak(what=what, speak=speak, rate=rate, accent=accent, yo=yo), sample_rate)

from numba import jit
from numba.experimental import jitclass
from numpy.random import randint
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from compiler import Ui_MainWindow

class Thread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(str)

    def __init__(self, status, parent=None):
        super(Thread, self).__init__(parent)
        self.status = status
        self.i = 0

    @jit(fastmath=True)
    def run(self):
        while True:
            self.updateSignal.emit(f'{self.status}{self.i}')
            self.i += randint(1, 10)
            self.msleep(1000)


class GUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, status):
        super().__init__()
        self.setupUi(self)
        self.params = {
            'dictor': 'aidar',
            'Rate': 48000
        }
        self.setWindowTitle("Atutum Convertil")
        self.setWindowIcon(QIcon("LogoSmall.png"))
        self.status = status
        self.ready = 1
        self.text = ''
        self.premium = False
        self.selectedPremiumVoice = 0
        self.selectedPremiumSpeed = 0
        self.Dialog = QMessageBox()
        self.Dialog.setWindowTitle("Audio Downloader")
        self.Dialog.setWindowIcon(QIcon("LogoSmall.png"))
        self.Dialog.setFixedSize(400, 400)
        self.lineEdit.textEdited.connect(self.responce)
        self.pushButton_4.clicked.connect(self.convert)
        self.pushButton_3.clicked.connect(self.download)
        self.comboBox_2.currentIndexChanged.connect(self.change)
        self.comboBox.currentIndexChanged.connect(self.change)
        self.pushButton.clicked.connect(self.activate)
        self.label_3.setText('👑')

    def activate(self):
        if self.lineEdit_2.text() == '1234':
            self.premium = True
            self.groupBox.setTitle('Текст в аудио Pro👑')

    def change(self):
        if self.comboBox_2.currentIndex() == 0:
            self.params['dictor'] = 'aidar'
            self.selectedPremiumVoice = 0
        elif self.comboBox_2.currentIndex() == 1:
            self.params['dictor'] = 'baya'
            self.selectedPremiumVoice = 0
        elif self.comboBox_2.currentIndex() == 2:
            self.params['dictor'] = 'xenia'
            self.selectedPremiumVoice = 0
        elif self.comboBox_2.currentIndex() == 3:
            self.params['dictor'] = 'random'
            self.selectedPremiumVoice = 0
        elif self.comboBox_2.currentIndex() == 4:
            self.selectedPremiumVoice =1
            # self.params['dictor'] = 'ksenia'
        elif self.comboBox_2.currentIndex() == 5:
            self.selectedPremiumVoice = 1
        if self.comboBox.currentIndex() == 1:
            self.params['Rate'] = 48000
        elif self.comboBox.currentIndex() == 2:
            self.params['Rate'] = 8000
        elif self.comboBox.currentIndex() == 3:
            self.params['Rate'] = 24000
        if self.comboBox_3.currentIndex() == 0:
            self.selectedPremiumSpeed = 0
        elif self.comboBox_3.currentIndex() == 1:
            self.selectedPremiumSpeed = 1

    def statusUpgrader(self, status):
        if self.comboBox_3.currentIndex() == 1:
            if self.premium:
                self.progressBar.setValue(100)
        else:
            if self.progressBar.value() > 90:
                self.progressBar.setValue(100)
            self.progressBar.setValue(int(status))

    def convert(self):
        if self.text != '':
            if self.premium:
                self.start_thread()
                self.statusUpgrader(self.status)
            else:
                if self.selectedPremiumVoice == 1 or self.selectedPremiumSpeed == 1:
                    if self.lineEdit_2.text() == '1234':
                        self.selectedPremiumSpeed = 0
                        self.selectedPremiumVoice = 0
                        self.premium = True
                    else:
                        self.Dialog.show()
                        self.Dialog.setText("Ваш статус аккаунта досжен быть премиум(👑)")
                else:
                    self.start_thread()
                    self.statusUpgrader(self.status)


    def start_thread(self):
        self.thread = Thread(self.status)
        self.thread.updateSignal.connect(self.statusUpgrader)
        self.thread.start()

    def responce(self, text):
        self.text = text

    def download(self):
        print(self.progressBar.value())
        if self.progressBar.value() == 100:
            workdir = QFileDialog.getExistingDirectory()
            if workdir != '' and workdir is not None:
                downloadAudio(what=self.text, speak=self.params['dictor'], rate=self.params['Rate'], yo=True,
                              accent=True, path=workdir+'/')


status = 0
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = GUI(status=status)
    w.show()
    sys.exit(app.exec())
