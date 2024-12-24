import json
from PyQt5.QtWidgets import *

def save_user_data(data, filename="./data.json"):
    try:
        with open(filename, "w") as file:
            json.dump(data, file)
        show_message_box("저장을 완료했습니다.")
    except Exception as e:
        show_message_box(f"저장에 실패했습니다. \n {e}")
        print(e)


def load_data(filename="./data.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_saved_token(data):
    return json.loads(data)['token']

def get_saved_path(data):
    return json.loads(data)['path']

def get_saved_os(data):
    return json.loads(data)['os']


def show_message_box(message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("안내")
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)

    msg_box.exec_()