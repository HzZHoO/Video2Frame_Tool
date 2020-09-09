import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from OneVideo2Frames import video2frames


import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class V2FTool(QWidget):
    def __init__(self):
        super(V2FTool, self).__init__()
        width = 670
        height = 122
        self.setFixedSize(width, height)  # fix the size of my tool

        # the button for choosing a directory containing videos
        self.btn = QPushButton("选择视频文件夹", self)
        self.btn.move(20, 19)  # x,y position of button
        self.btn.clicked.connect(self.choice_dir)  # only pass the method name to the .connect, no parentheses

        # the button for activating the transformation
        self.start_btn = QPushButton("启动视频转换", self)
        self.start_btn.setGeometry((width - 100) // 2, 60, 100, 40)
        self.start_btn.setEnabled(False)  # disable the start button at initial
        self.start_btn.clicked.connect(self.start_video2frames)

        # the line for showing some prompts and information
        self.le = QLineEdit(self)  # input line
        # self.le.move(130, 22)  # x,y position
        self.le.setFocusPolicy(Qt.NoFocus)  # forbid editing
        self.le.setPlaceholderText("这里将显示您选择的文件夹的完整路径以及一些提示信息")  # prompt
        self.le.setGeometry(150, 22, 500, 20)  # x, y, w, h

        self.dir_path = ""  # path of the directory we choose
        self.path_flag = False  # whether current directory path is valid

        self.working_flag = False  # whether the script is working
        self.work = WorkThread()  # thread for working
        self.work.finished.connect(self.work_finished)  # working thread finished signal and corresponding action
        self.work.trigger.connect(self.update_prompt)  # for showing the progress

        self.setWindowTitle("视频转换工具v1.0   by ZHZ")
        self.setWindowIcon(QIcon(r'C:\Users\张昊卓\OneDrive\Video2Frames\icons\128.ico'))
        self.show()

    def choice_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(
            self,
            "请选择存储一系列视频的一个文件夹（注意路径必须纯英文，不得有中文字符）",
            "C:\\"
        )
        self.le.setText(self.dir_path)
        # print(self.dir_path)

        if not all(ord(c) < 128 for c in self.dir_path):  # if the directory path is invalid
            print("路径不是纯英文！提示错误！选择的路径无效！")
            self.path_flag = False
            self.le.clear()
            self.le.setPlaceholderText("刚才选择的路径无效，请重新选择纯英文路径的文件夹！")
            self.start_btn.setEnabled(False)  # disable the start button
            # self.start_btn.setStyleSheet("color: gray")  # set the start button to gray
            QMessageBox.warning(self, "警告", "不得选择非纯英文路径！")  # activate a warning message
        elif self.dir_path != "":
            self.path_flag = True
            self.start_btn.setEnabled(True)
            # self.start_btn.setStyleSheet("color: black")

    def start_video2frames(self):
        self.start_btn.setEnabled(False)
        # self.start_btn.setStyleSheet("color: gray")
        self.working_flag = True

        print("开始将所选文件夹下的视频转换为图片并保存在对应文件夹下")
        self.le.clear()
        self.le.setPlaceholderText("正在将所选文件夹下的视频转换为图片并保存在对应文件夹下......")  # prompt

        self.work.update_dir(self.dir_path)  # tell the dir_path to work thread
        self.work.start()  # start working! run the working thread

    def update_prompt(self, prompt):
        self.le.setPlaceholderText(prompt)  # new prompt for current working progress

    def work_finished(self):
        self.working_flag = False
        QMessageBox.information(self, "提示", "成功完成所选文件夹下所有视频的转换")
        self.le.clear()
        self.le.setPlaceholderText("选择下一个文件夹进行视频转换，或关闭程序退出")  # prompt

    def closeEvent(self, event):  # for avoiding accident exit
        if self.working_flag:  # only work during the transformation
            quitMsgBox = QMessageBox()
            quitMsgBox.setWindowTitle('退出确认窗口')
            quitMsgBox.setText('当前脚本正在工作，您确定要退出吗？')
            buttonY = QPushButton('确定')
            buttonN = QPushButton('取消')
            quitMsgBox.addButton(buttonY, QMessageBox.YesRole)
            quitMsgBox.addButton(buttonN, QMessageBox.NoRole)
            quitMsgBox.exec_()
            if quitMsgBox.clickedButton() == buttonY:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


class WorkThread(QThread):
    """
        Thread for working: N video ---> N directories containing frames
    """
    trigger = pyqtSignal(str)

    def __int__(self):
        super(WorkThread, self).__init__()
        self._dir = ""

    def get_dir(self):
        return self._dir

    def update_dir(self, new_dir):
        self._dir = new_dir

    @staticmethod
    def is_video_file(filename):
        assert isinstance(filename, str)
        extensions = ['.mp4', '.avi', '.mkv']
        return any([filename.endswith(extension) for extension in extensions])

    def run(self):
        print("转换视频线程工作中")
        tic = time.time()

        # get video names
        videos = []
        video_dir = self.get_dir()  # video root dir
        dirs_and_files = os.listdir(video_dir)
        for filename in dirs_and_files:
            if self.is_video_file(filename):
                videos.append(filename)

        # transform every video in the list
        for i, video in enumerate(videos):
            prompt = "已选文件夹下共{:d}个视频，正在转换第{:d}个...".format(len(videos), i + 1)
            self.trigger.emit(prompt)  # send the prompt string to the main widget

            basename = video.split('.')[0]
            this_frames_dir = os.path.join(video_dir, basename)
            this_video = os.path.join(video_dir, video)
            video2frames(this_video, this_frames_dir)  # do the tranformation!

        toc = time.time()
        print("视频转换完成，耗时{:.2f}分钟".format((toc - tic) / 60))
        prompt = "已选文件夹下{:d}个视频转换完成，共耗时{:.2f}分钟".format(len(videos), (toc - tic) / 60)
        self.trigger.emit(prompt)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    v2ftool = V2FTool()
    sys.exit(app.exec_())