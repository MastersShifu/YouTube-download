# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=undefined-variable
# pylint: disable=wildcard-import
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QFileDialog
from PySide6.QtGui import QIcon
import sys
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import gc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download video from YouTube")

        layout = QVBoxLayout()

        self.setFixedSize(700, 0)

        # Лейбл для вывода ошибки
        self.label = QLabel()
        self.label.setStyleSheet("color: red")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)


        # Создаем поле для ввода
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter link for video")
        layout.addWidget(self.input)
        self.name = QLineEdit()


        # Создаем выпадающий список
        self.combo_box = QComboBox()
        self.combo_box.addItems(["mp4", "mp3", "mp4 and mp3"])
        layout.addWidget(self.combo_box)

        # Создаем кнопку
        button = QPushButton("Download")
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

        # Создаем виджет и устанавливаем основной макет на него
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on_button_click(self):
        # Получаем значение поля ввода и выпадающего списка
        text = self.input.text()
        combo_box_value = self.combo_box.currentText()

        # Проверяем поле на пустоту
        if not text:
            self.label.setText("Missing string!")
            return

        directory = QFileDialog.getExistingDirectory(self, "Select Directory")

        if combo_box_value == "mp4":
            self.label.setHidden(True)
            link = text
            yt = YouTube(link)
            name = f"{yt.title}.mp3"
            stream = yt.streams.get_by_itag(22)
            stream.download(output_path=directory, filename=f"{name}.mp4")

        elif combo_box_value == "mp3":
            self.label.setHidden(True)
            link = text
            yt = YouTube(link)
            name = f"{yt.title}.mp3"
            stream = yt.streams.get_by_itag(22)
            stream.download(output_path=directory, filename=f"{name}.mp4")

            mp4_file = f"{directory}/{name}.mp4"
            mp3_file = f"{directory}/{name}.mp3"
            videoclip = VideoFileClip(mp4_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)
            audioclip.close()
            videoclip.close()

            os.remove(mp4_file)
        
        elif combo_box_value == "mp4 and mp3":
            self.label.setHidden(True)
            link = text
            yt = YouTube(link)
            name = f"{yt.title}.mp3"
            stream = yt.streams.get_by_itag(22)
            stream.download(output_path=directory, filename=f"{name}.mp4")

            mp4_file = f"{directory}/{name}.mp4"
            mp3_file = f"{directory}/{name}.mp3"
            videoclip = VideoFileClip(mp4_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)
            audioclip.close()
            videoclip.close()
        gc.collect()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    icon = QIcon("ico.jpg")
    window.setWindowIcon(icon)
    window.show()
    app.exec_()
