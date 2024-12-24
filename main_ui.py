import json
import sys
import request_resource
import save_user_info
from PyQt5.QtWidgets import *


class MainWindow(QWidget) :
    def __init__(self):
        super().__init__()
        self.saved_data = save_user_info.load_data()
        self.figma_token = QLineEdit()
        self.res_path = QLineEdit()
        self.export_btn = QPushButton()
        self.res_link_form = QFormLayout()
        self.res_link = QLineEdit()
        self.file_name = QLineEdit()
        self.log_form = QTextEdit()
        self.log_form.setReadOnly(True)
        self.android_btn = QRadioButton('Android')
        self.ios_btn = QRadioButton('iOS')
        self.current_os = ""

        self.android_btn.toggled.connect(lambda : self.set_current_os("android"))
        self.ios_btn.toggled.connect(lambda : self.set_current_os("iOS"))

        self.figma_token.setText(save_user_info.get_saved_token(self.saved_data))
        self.res_path.setText(save_user_info.get_saved_path(self.saved_data))

        if save_user_info.get_saved_os(self.saved_data) == "android":
            self.current_os = "android"
            self.android_btn.setChecked(True)
            self.ios_btn.setChecked(False)

        elif save_user_info.get_saved_os(self.saved_data) == "iOS":
            self.current_os = "iOS"
            self.android_btn.setChecked(False)
            self.ios_btn.setChecked(True)

        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)
        self.init_ui()

    def init_ui(self):
        platform_label = QLabel('os 선택: ')

        platform_hbox = QHBoxLayout()
        platform_hbox.addStretch(1)
        platform_hbox.addWidget(platform_label)
        platform_hbox.addSpacing(20)
        platform_hbox.addWidget(self.android_btn)
        platform_hbox.addSpacing(100)
        platform_hbox.addWidget(self.ios_btn)
        platform_hbox.addStretch(1)

        file_path_form = QFormLayout()

        self.figma_token.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #d4d4d4;")
        self.res_path.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #d4d4d4;")

        info_save_btn = QPushButton()
        info_save_btn.setFixedWidth(200)
        info_save_btn.setFixedHeight(60)
        info_save_btn.setText("Save")
        info_save_btn.setStyleSheet("background-color: white; border-radius: 10px; border:1px solid #d4d4d4;")
        info_save_btn.clicked.connect(
            lambda :save_user_info.save_user_data
                (json.dumps(
                {"token": self.figma_token.text(),
                        "os": self.current_os,
                        "path": self.res_path.text()},
                indent=2)))

        info_hbox = QHBoxLayout()
        info_hbox.addStretch(1)
        info_hbox.addWidget(info_save_btn)
        info_hbox.addStretch(1)

        file_path_form.addRow("피그마 토큰", self.figma_token)
        file_path_form.addRow("폴더 경로", self.res_path)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color:#d4d4d4;")

        self.log_form.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #d4d4d4;")
        self.res_link.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #d4d4d4;")
        self.file_name.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #d4d4d4;")

        self.res_link_form.addRow("리소스 링크", self.res_link)
        self.res_link_form.addRow("파일 이름", self.file_name)

        self.export_btn.setFixedWidth(200)
        self.export_btn.setFixedHeight(60)
        self.export_btn.setText("Export")
        self.export_btn.setStyleSheet("background-color: white; border-radius: 10px; border:1px solid #d4d4d4;")
        self.export_btn.clicked.connect(self.update_selected_os)

        export_hbox = QHBoxLayout()
        export_hbox.addStretch(1)
        export_hbox.addWidget(self.export_btn)
        export_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(platform_hbox)
        vbox.addStretch(1)
        vbox.addLayout(file_path_form)
        vbox.addStretch(1)
        vbox.addLayout(info_hbox)
        vbox.addStretch(1)
        vbox.addWidget(divider)
        vbox.addStretch(1)
        vbox.addWidget(self.log_form)
        vbox.addStretch(1)
        vbox.addLayout(self.res_link_form)
        vbox.addSpacing(50)
        vbox.addLayout(export_hbox)
        vbox.addStretch(1)


        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet('background-color:#fafafa;')
        self.show()
        self.setWindowTitle('Figma Resource Saver')


    def update_selected_os(self):
        if self.android_btn.isChecked():
            request_resource.export_resource(
                window= self,
                platform="android",
                token=self.figma_token.text(),
                paths=[f'{self.res_path.text()}\\drawable-mdpi', f'{self.res_path.text()}\\drawable-hdpi',
                       f'{self.res_path.text()}\\drawable-xhdpi', f'{self.res_path.text()}\\drawable-xxhdpi',
                       f'{self.res_path.text()}\\drawable-xxxhdpi'
                       ],
                res_link=self.res_link.text(),
                res_name=self.file_name.text()
            )


        elif self.ios_btn.isChecked():
            request_resource.export_resource(
                window= self,
                platform="iOS",
                token=self.figma_token.text(),
                paths=[f'{self.res_path.text()}\\'],
                res_link=self.res_link.text(),
                res_name=self.file_name.text()
            )


    def set_current_os(self, os):
        self.current_os = os


    def print_log(self, log):
        self.log_form.append(str(log))
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())