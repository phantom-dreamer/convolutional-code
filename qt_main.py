import sys
import os

from qt_form import Ui_Form
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox

from convolutional_code import convolutional_communication_channel


class ConvolutionalWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config_file_name = ""
        self.file_to_encode = ""
        self.decoder_path = ""
        self.pushButton.clicked.connect(self.open_config_files)
        self.pushButton_2.clicked.connect(self.open_file_to_encode)
        self.pushButton_3.clicked.connect(self.open_dir_to_decode)
        self.pushButton_4.clicked.connect(self.run)


    def open_config_files(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выбрать json-файл конфигурации', r".", "Json файлы (*.json)")
        self.config_file_name = os.path.normpath(file_name)

    def open_file_to_encode(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выбрать файл для отправки в канал связи', r".",)
        self.file_to_encode = os.path.normpath(file_name)

    def open_dir_to_decode(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Выбрать директорию для', r".", )
        self.decoder_path = os.path.normpath(dir_name)

    def run(self):
        msg = QMessageBox()
        if self.file_to_encode and self.config_file_name and self.decoder_path:
            try:
                convolutional_communication_channel(
                    file=self.file_to_encode, config_name=self.config_file_name, dir_to_write=self.decoder_path
                )
            except ValueError as e:
                msg.setWindowTitle("Канал связи завершил работу с ошибкой")
                msg.setText(f"Неверные параметры {e}")
                msg.setIcon(QMessageBox.Warning)

            else:
                msg.setWindowTitle("Канал связи закончил свою работу")
                msg.setText(f"Декодированный файл находится по адресу {self.decoder_path}")
                msg.setIcon(QMessageBox.Information)
            finally:
                msg.exec_()
        else:
            msg.setWindowTitle("Канал связи закончил свою работу c ошибкой")
            msg.setText(f"Вы не выбрали файл")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()


def create_window():
    app = QApplication(sys.argv)
    window = ConvolutionalWidget()
    window.show()
    app.exec_()


def main():
    create_window()


if __name__ == '__main__':
    main()