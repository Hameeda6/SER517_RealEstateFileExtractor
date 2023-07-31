from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QMessageBox, QTextEdit, QFileDialog, QScrollArea, QProgressDialog
from PyQt6.QtCore import Qt, QDir, QTimer, QThread, pyqtSignal, QObject, pyqtSlot
import os
from PyQt6.QtGui import QFont
from dropbox.exceptions import AuthError
import dropbox.exceptions
import dropbox
from pathlib import Path
from datetime import datetime
import glob
from selenium.common.exceptions import NoSuchElementException


global check_if_clicked
check_if_clicked = 0


class uiMainWindow(object):
    def setupui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)


class menuWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('MENU WINDOW')
        self.setGeometry(50, 50, 800, 300)
        self.setStyleSheet("background-color: #C4A568;")
        label = QLabel(self)
        label.setText("MENU WINDOW")
        label.setGeometry(10, 10, 0, 0)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: blue; font-size: 20px;")

        textedit = QTextEdit(self)
        textedit.setGeometry(50, 50, 700, 280)
        textedit.setStyleSheet("color: Black; font-size: 20px;")
        textedit.setReadOnly(True)
        textedit.setText("WELCOME - Shows briefly about MB Property Management \n\nUPLOAD - helps to upload the files into dropbox with the help of dropbox access token \n\nDOWNLOAD - helps to download files from tenant cloud \n\nHELP - shows how to get access token for a drop box \n\n QUIT - Closes the Application ")


class dropWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('HOW TO ACCESS THE ACCESS TOKEN FROM DROP BOX')
        self.setGeometry(50, 50, 800, 300)
        self.setStyleSheet("background-color: #C4A568;")
        label = QLabel(self)
        label.setText("HOW TO ACCESS THE ACCESS TOKEN FROM DROP BOX")
        label.setGeometry(10, 10, 0, 0)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: blue; font-size: 20px;")

        textedit = QTextEdit(self)
        textedit.setGeometry(50, 50, 700, 280)
        textedit.setStyleSheet("color: Black; font-size: 20px;")
        textedit.setReadOnly(True)
        textedit.setText("\n STEPS TO ACCESS THE ACCESS TOKEN FROM DROPBOX \n\n 1. Visit the website '<a href=\"https://www.dropbox.com/developers\">https://www.dropbox.com/developers</a>' and sign in to your account. \n2. Click on the APP CONSOLE \n3. Choose the app where the files have to be uploaded if not create an app. \n4. Under the PERMISSIONS tab, under 'Files and folders', select 'files.content.write' and 'files.content.read' to enable permission.\n5. Under the SETTINGS tab, click on GENERATE to get your Dropbox Access Token. ")


class helpWindow(QDialog):
    def menu_clicked(self):
        menu_window = menuWindow()
        menu_window.exec()

    def drop_clicked(self):
        drop_window = dropWindow()
        drop_window.exec()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('HELP WINDOW')
        self.setGeometry(50, 50, 800, 300)
        self.setStyleSheet("background-color: #C4A568;")
        label = QLabel(self)
        label.setText("HELP WINDOW")
        label.setGeometry(10, 10, 0, 0)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: blue; font-size: 20px;")

        buttonmenu = QPushButton("MENU", self)
        buttonmenu.setGeometry(50, 50, 500, 100)
        buttonmenu.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")
        buttonmenu.clicked.connect(self.menu_clicked)

        buttondrop = QPushButton("ACCESS TOKEN FROM DROP BOX", self)
        buttondrop.setGeometry(50, 180, 500, 100)
        buttondrop.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")
        buttondrop.clicked.connect(self.drop_clicked)


class viewWindow(QDialog):

    def __init__(self):
        super().__init__()
        global check_if_clicked
        self.setWindowTitle('VIEW THE BROWSED FILES')
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #C4A568;")

        label = QLabel(self)
        label.setText("THE FILES BROWSED ARE:")
        label.setGeometry(150, 20, 400, 40)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: black; font-size: 20px; margin-bottom: 10px;font-weight: bold;")

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setGeometry(60, 80, 600, 360)
        scroll.setStyleSheet("background-color: white;")

        scroll_content = QWidget(scroll)
        scroll.setWidget(scroll_content)

        layout = QVBoxLayout(scroll_content)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        for filenames in filename:
            font = QFont("Courier New", 12)
            for index, filenames in enumerate(filename):
                file_label = QLabel(scroll_content)
                file_label.setText(str(index+1) + ". " + filenames)
                file_label.setStyleSheet("background-color: #F0F0F0; padding: 5px; border-radius: 5px; font-size: 16px;")
                file_label.setFont(font)
                layout.addWidget(file_label)


class UploadWindow(QDialog):

    completed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setWindowTitle('UPLOAD THE FILE TO DROPBOX')
        self.setGeometry(100, 100, 750, 500)

        self.setStyleSheet("background-color: #C4A568;")

        label_name = QLabel("UPLOAD WINDOW", self)
        label_name.setGeometry(150, 20, 400, 30)
        label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_name.setStyleSheet("color: Black; font-size: 16px;font-weight: bold;")

        label_token = QLabel("ENTER THE DROPBOX ACCESS TOKEN", self)
        label_token.setGeometry(150, 50, 450, 50)
        label_token.setStyleSheet("color: Black; font-size: 16px;font-weight: bold;")

        help_button = QPushButton("?", self)
        help_button.setGeometry(450, 65, 20, 20)
        help_button.setStyleSheet("background-color: black; color: white;")
        help_button.clicked.connect(self.helpbuttonFunction)

        self.tokentextbox = QTextEdit(self)
        self.tokentextbox.setGeometry(150, 100, 450, 40)
        self.tokentextbox.setStyleSheet("font-size: 14px;")

        label_file_textbox = QLabel("ENTER THE FOLDER NAME TO BE CREATED IN DROPBOX \nTO UPLOAD THE BROWSED FILES", self)
        label_file_textbox.setGeometry(150, 150, 450, 50)

        label_file_textbox.setStyleSheet("color: black; font-size: 16px;font-weight: bold;")

        self.textbox = QTextEdit(self)
        self.textbox.setGeometry(150, 200, 450, 40)
        self.textbox.setStyleSheet("font-size: 14px;")

        button_explore = QPushButton("BROWSE FILES", self)
        button_explore.setStyleSheet("background-color: Black; color: white;")
        button_explore.setGeometry(250, 280, 200, 30)

        global check_if_clicked
        check_if_clicked = 0

        def on_button_explore_clicked():
            global check_if_clicked
            check_if_clicked = 1
            global filename
            # code for browsing 1 or multiple files after clicking button
            filename, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files ();;Text Files (.txt)")

            if len(filename) == 0:
                QMessageBox.information(self, "Message", "File is not clicked, Select 1 or more files to upload")
            if len(filename) > 0:
                QMessageBox.information(self, "Message", "Files are browsed,view the files selected and upload them")
            return filename

        def on_button_upload_clicked():
            global check_if_clicked
            inp = self.textbox.toPlainText()
            dropbox_access_token = self.tokentextbox.toPlainText()
            if check_if_clicked == 0:
                QMessageBox.information(self, "Message", "Browse a file to upload to dropbox")
            if dropbox_access_token == "":
                QMessageBox.information(self, "Message", "Dropbox Access Token is missing!!!")
            else:
                countfile = 0

                for i in range(len(filename)):
                    lastindex = Path(filename[i]).stem
                    extension_extract = os.path.splitext(filename[i])
                    extention_type = extension_extract[1]
                    if inp == "":
                        dropbox_path = "/" + lastindex + extention_type
                    else:
                        dropbox_path = "/" + inp + "/" + lastindex + extention_type
                    if filename == '':
                        QMessageBox.information(self, "Message", "Please select a file to upload")
                    else:
                        computer_path = filename[i]
                        client = dropbox.Dropbox(dropbox_access_token)

                        # try-catch block when the refresh token gets expired
                        try:
                            print("try")
                            client.files_upload(open(computer_path, "rb").read(), dropbox_path)
                            print("[UPLOADED] {}".format(computer_path))
                            countfile += 1
                        except dropbox.exceptions.AuthError as e:
                            print(f"Error uploading {computer_path} to Dropbox: {e}")
                            QMessageBox.information(self, "Error", "Unable to refresh access token without refresh token and app key. Please generate a new access token manually.", parent=self)

                        except Exception as e:
                            print(f"Error uploading {computer_path}")

                if countfile == len(filename):
                    if inp is not None:
                        QMessageBox.information(self, "Message", "All the files have been uploaded into the dropbox in the folder name specified")
                    else:
                        QMessageBox.information(self, "Message", "All the files have been uploaded into the dropbox main directory")
                else:
                    QMessageBox.information(self, "Message", "Unable to refresh access token without refresh token and app key. Please generate a new access token manually.")

        def viewbrowsedfiles():
            print("view files clicked")
            if check_if_clicked != 0:
                view_window = viewWindow()
                view_window.exec()
            else:
                QMessageBox.information(self, "Message", "Browse a file to view")

        button_explore.clicked.connect(on_button_explore_clicked)

        button_upload = QPushButton("UPLOAD FILES TO DROPBOX", self)
        button_upload.setGeometry(250, 340, 200, 30)
        button_upload.setStyleSheet("background-color: Black; color: white;")
        button_upload.clicked.connect(on_button_upload_clicked)

        button_viewfiles = QPushButton("VIEW THE BROWSED FILES", self)
        button_viewfiles.setGeometry(250, 400, 200, 30)
        button_viewfiles.setStyleSheet("background-color: Black; color: white;")
        button_viewfiles.clicked.connect(viewbrowsedfiles)

        button_exit = QPushButton("EXIT", self)
        button_exit.setStyleSheet("background-color: Black; color: white;")
        button_exit.setGeometry(250, 460, 200, 30)
        button_exit.clicked.connect(self.close)

    def helpbuttonFunction(self):
        help_windows = helpWindow()
        help_windows.exec()


class welcomeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WELCOME WINDOW')
        self.setGeometry(50, 50, 800, 300)
        self.setStyleSheet("background-color: #C4A568;")
        label = QLabel(self)
        label.setText("WELCOME WINDOW")
        label.setGeometry(10, 10, 0, 0)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: blue; font-size: 20px;")

        textedit = QTextEdit(self)
        textedit.setGeometry(50, 50, 700, 280)
        textedit.setStyleSheet("color: Black; font-size: 20px;")
        textedit.setReadOnly(True)
        textedit.setText("    Greetings and thank you for accessing the MB property management application. \n    This tool provides you with a range of capabilities, including the ability to upload \n    text files of any format to Dropbox,  as well as download multiple files from the \n    tenant cloud. If you require further information, please consult the help button,\n    and if you wish to exit the application, you can do so by clicking on the quit \n    button. ")


class MainWindow(QtWidgets.QMainWindow, uiMainWindow):
    def __init__(self):
        super().__init__()
        self.setupui(self)

        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("logo.png").scaled(300, 100)
        label.setPixmap(pixmap)
        label.setGeometry(600, 50, pixmap.width(), pixmap.height())

        text_label = QtWidgets.QLabel("MB Property Management Inc. is a solution-driven company specializing in managing real estate \n\ninvestment properties. \n\nWe are located in Toronto, Ontario, and we serve the Greater Toronto Area (GTA) as well as surrounding \n\ncities, such as Hamilton and Barrie. \n\nOur dedicated multilingual team cultivates deep relationships with people throughout the real estate \n\nindustry and within the communities we serve.", self)
        text_label.setGeometry(50, 250, 800, 400)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        text_label.setFont(font)
        text_label.setStyleSheet("color: #C4A568;")

        buttonwelcome = QPushButton("WELCOME", self)
        buttonwelcome.setGeometry(900, 240, 300, 50)
        buttonwelcome.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")
        buttonwelcome.clicked.connect(self.welcome_clicked)

        button = QPushButton("UPLOAD", self)
        button.setGeometry(900, 340, 300, 50)
        button.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")
        button.clicked.connect(self.upload_button_clicked)

        download_button = QPushButton("DOWNLOAD", self)
        download_button.setGeometry(900, 440, 300, 50)
        download_button.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")
        download_button.clicked.connect(self.downloadButtonClicked)

        button = QPushButton("HELP", self)
        button.setGeometry(900, 540, 300, 50)
        button.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")
        button.clicked.connect(self.setting_button_clicked)

        quit_button = QPushButton("QUIT", self)

        quit_button.setGeometry(900, 640, 300, 50)
        quit_button.setStyleSheet("background-color: #C4A568; color: Black; font-size: 20px;font-weight: bold;")

        quit_button.clicked.connect(self.close)
        self.setGeometry(100, 100, 700, 500)

        self.setStyleSheet("background-color: #161616;")
        self.showMaximized()

    def downloadButtonClicked(self):

        download_window = downloadWindow()
        download_window.exec()

    def welcome_clicked(self):
        welcome_window = welcomeWindow()
        welcome_window.exec()

    def upload_button_clicked(self):
        upload_window = UploadWindow()
        upload_window.exec()

    def setting_button_clicked(self):
        setting_window = helpWindow()
        setting_window.exec()


class ErrorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Error")
        self.setFixedSize(578, 80)
        self.downloadlabel = QLabel("User not logged in, Please close the TenantCloud chrome window and retry!", self)
        self.downloadlabel.move(8, 25)
        self.setStyleSheet("background-color: #C4A568; font-size: 16px;font-weight:bold")


class ErrorDialogDropbox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Error")
        self.setFixedSize(578, 80)
        self.downloadlabel = QLabel("Unable to refresh access token without refresh token and app key. Please generate a new access token manually.", self)
        self.downloadlabel.move(5, 25)
        self.setStyleSheet("background-color: #C4A568; font-size: 16px;font-weight:bold")


class TenantCloudThread(QThread):
    completed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

    def run(self):
        try:
            import TenantCloud
            TenantCloud.initiate()
            self.completed.emit()
        except NoSuchElementException:
            QtCore.QMetaObject.invokeMethod(self.parent, "show_error_dialog", QtCore.Qt.ConnectionType.QueuedConnection)

    @pyqtSlot()
    def show_error_dialog(self):
        error_dialog = ErrorDialog(self.parent)
        error_dialog.exec()
        error_dialog.raise_()
        error_dialog.activateWindow()


class downloadWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Window")
        self.setFixedSize(400, 200)
        self.downloadlabel = QLabel("DO YOU WANT TO AUTO-UPLOAD THE FILES?", self)
        self.downloadlabel.move(20, 50)
        self.setStyleSheet("background-color: #C4A568; font-size: 16px; font-weight:bold")

        self.yes_button = QPushButton("YES", self)
        self.yes_button.move(70, 100)
        self.yes_button.clicked.connect(self.auto_upload)

        self.no_button = QPushButton("NO", self)
        self.no_button.move(170, 100)
        self.no_button.clicked.connect(self.handle_ok_button_click)

        label_wait = QLabel("##On clicking NO, wait for a few seconds \n for Tenant Cloud to open#", self)
        label_wait.setGeometry(50, 150, 400, 50)
        label_wait.setStyleSheet("color: black; font-size: 16px;font-weight:bold")
        self.canceled = False

    def handle_ok_button_click(self):
        self.progress_dialog = QProgressDialog("Initiating the process...", "Close", 0, 0, self)
        self.progress_dialog.setWindowTitle("Download Progress")
        self.progress_dialog.setLabelText("Please wait while Google Chrome is being opened.")
        self.progress_dialog.show()
        self.progress_dialog.canceled.connect(self.progress_dialog.close)
        self.timer = QTimer()
        self.timer.singleShot(10000, self.progress_dialog.close)
        self.thread = TenantCloudThread(parent=self)
        self.thread.completed.connect(self.close_progress_dialog)
        self.thread.start()

    def close_progress_dialog(self):
        self.canceled = True
        self.accept()
        self.close()

    def run_tenant_cloud(self):
        print("dummy func called!!")
        start_time = datetime.now()
        try:
            import TenantCloud
            TenantCloud.initiate()
        except NoSuchElementException:
            QMessageBox.information(self, "Message", "Login again!!!")
        self.canceled = True
        self.progress_dialog.canceled.connect(self.progress_dialog.close)

        download_directory = str(os.path.join(os.path.expanduser("~"), "Desktop")) + "/TenantCloudFiles"
        files = glob.glob(download_directory + "/*")
        downloaded_files = []
        total_size = 0
        num_files = 0
        for file in files:
            file_name = os.path.basename(file)
            file_size = os.path.getsize(file)
            modified_time = os.path.getmtime(file)
            modified_time = datetime.fromtimestamp(modified_time)
            if modified_time > start_time:
                downloaded_files.append((file_name, file_size, modified_time))
                total_size += file_size
                num_files += 1
        downloaded_files = sorted(downloaded_files, key=lambda x: x[2])
        self.show_downloaded_popup(downloaded_files, download_directory)

        self.accept()
        self.close()

    def auto_upload(self):
        autoupload_window = autoUploadWindow()
        autoupload_window.exec()

    def show_downloaded_popup(self, downloaded_files, location):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Downloaded Files")
        msg_box.setText("Files downloaded successfully in {}:\n{}".format(location, ", ".join([file[0] for file in downloaded_files])))
        msg_box.setStyleSheet("background-color: black; color: gold;")
        msg_box.setGeometry(100, 100, 500, 300)
        msg_box.exec()

    @QtCore.pyqtSlot()
    def show_error_dialog(self):
        error_dialog = ErrorDialog(self)
        error_dialog.exec()


class autoUploadWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AUTO UPLOAD WINDOW")
        label_header = QLabel("AUTO UPLOAD WINDOW", self)
        label_header.setGeometry(150, 15, 400, 50)
        label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background-color: #C4A568;")

        label_header.setStyleSheet("color: black; font-size: 20px;font-weight: bold;")
        label_dropboxtoken = QLabel("ENTER THE DROPBOX ACCESS TOKEN", self)
        label_dropboxtoken.setGeometry(150, 50, 450, 50)
        label_dropboxtoken.setStyleSheet("color: black; font-size: 16px;")

        help_button = QPushButton("?", self)
        help_button.setGeometry(450, 65, 20, 20)
        help_button.setStyleSheet("background-color: black; color: white;")
        help_button.clicked.connect(self.helpFunction)

        self.tokentextbox = QTextEdit(self)
        self.tokentextbox.setGeometry(150, 100, 450, 40)
        self.tokentextbox.setStyleSheet("font-size: 14px;")

        label_foldername = QLabel("ENTER THE FOLDER NAME TO BE CREATED IN DROPBOX", self)
        label_foldername.setGeometry(150, 150, 450, 50)
        label_foldername.setStyleSheet("color: black; font-size: 16px;")

        self.foldertextbox = QTextEdit(self)
        self.foldertextbox.setGeometry(150, 200, 450, 40)
        self.foldertextbox.setStyleSheet("font-size: 14px;")

        submit_button = QPushButton("SUBMIT", self)
        submit_button.setGeometry(220, 250, 300, 50)
        submit_button.setStyleSheet("background-color: black; color: white;")
        submit_button.clicked.connect(self.autoUploadFunction)

        label_wait = QLabel("##On clicking submit, wait for a few minutes to process#", self)
        label_wait.setGeometry(150, 300, 400, 50)
        label_wait.setStyleSheet("color: black; font-size: 16px;font-style:italic")

    def helpFunction(self):
        help_windows = helpWindow()
        help_windows.exec()

    def autoUploadFunction(self):
        token = self.tokentextbox.toPlainText()
        if token=='':
            QMessageBox.information(self, "Error", "ENTER A DROPBOX ACCESS TOKEN!!!")
        else:
            try:
                dbx = dropbox.Dropbox(token)
                dbx.users_get_current_account()

                self.thread = QThread()
                self.worker = Worker(token=token, foldername=self.foldertextbox.toPlainText(), parent=self)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run_tenant_cloud)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()
                self.thread.finished.connect(lambda: QMessageBox.information(self, "Message", "All the files are uploaded into the Dropbox", parent=self))
                self.thread.finished.connect(self.accept)
                self.thread.finished.connect(self.close)

            except dropbox.exceptions.AuthError:
                QMessageBox.information(self, "Error", "INVALID DROPBOX ACCESS TOKEN!!!")

            except dropbox.exceptions.BadInputError as e:
                QMessageBox.information(self, "Error", str(e))


class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, token, foldername, parent):
        super().__init__()
        self.token = token
        self.foldername = foldername
        self.parent = parent

    def run_tenant_cloud(self):
        try:
            import TenantCloud
            TenantCloud.initiate()

        except NoSuchElementException:
            print("exception handled")
            #QMessageBox.information(self.parent, "Error", "User not logged in, Please close the TenantCloud chrome window and retry!")
            error_dialog = ErrorDialog(self.parent)
            error_dialog.exec()
            error_dialog.raise_()
            error_dialog.activateWindow()

        dir_path = str(os.path.join(os.path.expanduser("~"), "Desktop")) + "/TenantCloudFiles"
        dir = QDir(dir_path)
        files = dir.entryList([], QDir.Filter.Files)
        file_paths = []
        for file_name in files:
            file_path = dir.filePath(file_name)
            file_paths.append(file_path)

        countfile = 0
        global filename
        if self.token == ' ':
            QMessageBox.information(self, "Error", "ENTER A DROPBOX ACCESS TOKEN!!!")
        if len(file_paths) == 0:
            QMessageBox.information(self, "Error", "Files are not selected")
        for i in range(len(file_paths)):
            lastindex = Path(file_paths[i]).stem
            extension_extract = os.path.splitext(file_paths[i])
            extention_type = extension_extract[1]
            if self.foldername == "":
                dropbox_path = "/" + lastindex + extention_type
            else:
                dropbox_path = "/" + self.foldername + "/" + lastindex + extention_type
            computer_path = file_paths[i]
            client = dropbox.Dropbox(self.token)
            try:
                print("try")
                client.files_upload(open(computer_path, "rb").read(), dropbox_path)
                print("[UPLOADED] {}".format(computer_path))
                countfile += 1
            except dropbox.exceptions.AuthError:
                error_dialog = ErrorDialogDropbox(self.parent)
                error_dialog.exec()
                break

        QMessageBox.information(self.parent, "Message", "All the files are uploaded into the Dropbox")
        self.accept()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
