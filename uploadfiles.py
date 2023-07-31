from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QFileDialog,QMessageBox
from PyQt6.QtCore import Qt
import sys
import os
import dropbox
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Upload the file to dropbox')
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: white;")
        
        # label_file_explorer = QLabel("Upload the file to dropbox", self)
        self.label_file_explorer = QLabel(self)
        self.label_file_explorer.setText('No file selected')
        self.label_file_explorer.setGeometry(150, 60, 400, 100)
        self.label_file_explorer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_file_explorer.setStyleSheet("color: blue; font-size: 20px;")

        self.label_file_count = QLabel(self)
        self.label_file_count.setText('Count of no. of files selected')
        self.label_file_count.setGeometry(0, 0,700, 100)
        self.label_file_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_file_count.setStyleSheet("color: blue; font-size: 20px;")
        
        label_file_textbox = QLabel("Enter the name of the folder to upload the documents", self)
        label_file_textbox.setGeometry(150, 150, 400, 30)
        label_file_textbox.setStyleSheet("color: blue; font-size: 16px;")
        
        self.textbox = QTextEdit(self)
        self.textbox.setGeometry(150, 200, 400, 60)
        self.textbox.setStyleSheet("font-size: 14px;")
        
        button_explore = QPushButton("Browse Files", self)
        button_explore.setGeometry(300, 300, 100, 30)
        button_explore.clicked.connect(self.browseFiles)
        
        button_upload = QPushButton("Upload the File to Dropbox", self)
        button_upload.setGeometry(250, 350, 200, 30)
        button_upload.clicked.connect(self.upload)
        
        button_exit = QPushButton("Exit", self)
        button_exit.setGeometry(300, 400, 100, 30)
        button_exit.clicked.connect(self.exit)
    
    def browseFiles(self):
        global filename
        #code for browsing 1 or multiple files after clicking button
        filename, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        print(len(filename))
        print(filename[0])
        # print(os.path.basename(filename))
        # filepath= os.path.basename(filename)
        if len(filename)==0:
            print("hoiii")
            self.label_file_explorer.setText("File is not clicked, Select 1 or more files to upload")    
        else:
            self.label_file_count.setText("No of files selected are: "+str(len(filename)))
            self.label_file_explorer.setText("The files selected are: "+str(filename))    
        return filename

    def upload(self):
        inp = self.textbox.toPlainText()
        print("inp", inp)
        countfile = 0
        dropbox_access_token = "sl.Bau3WhHAXrGTYeD9rWSgJ0AQaXPGCa5ExcSLeJQUhsGnZ82ireoipllvozxkqCiFL5Etaus9QAnOCb6BK2HJKcIskUlngLzxUSCdIgXmtOPRdOKFEsbhAjqwKcaZaaQ1WGTW_id9"

        for i in range(len(filename)):
            print('filename[i]', filename[i])
            lastindex = Path(filename[i]).stem
            extension_extract = os.path.splitext(filename[i])
            extention_type = extension_extract[1]
            if inp == "":
                dropbox_path = "/" + lastindex + extention_type
            else:
                dropbox_path = "/" + inp + "/" + lastindex + extention_type
            if filename == '':
                self.label_file_explorer.setText("Please select a file to upload")
            else:
                computer_path = filename[i]
                client = dropbox.Dropbox(dropbox_access_token)
                print("[SUCCESS] dropbox account linked")
                client.files_upload(open(computer_path, "rb").read(), dropbox_path)
                print("[UPLOADED] {}".format(computer_path))
                self.label_file_explorer.setText("Files are uploaded")
                countfile += 1
        if countfile == len(filename):
            if inp is not None:
                QMessageBox.information(self, "Message", "All the files have been uploaded into the dropbox in the folder name specified")
            else:
                QMessageBox.information(self, "Message", "All the files have been uploaded into the dropbox main directory")
        else:
            QMessageBox.information(self, "Message", "All the files are not uploaded into the dropbox")

    
    def exit(self):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


