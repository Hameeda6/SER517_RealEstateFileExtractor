import unittest
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from HomePage import MainWindow
from HomePage import welcomeWindow
from HomePage import autoUploadWindow


class TestHomePage(unittest.TestCase):


    def test_buttonClicked(self):
        app = QtWidgets.QApplication([])
        checkwin = MainWindow()
        checkbox = QtWidgets.QMessageBox()
        checkbox.setWindowTitle("WELCOME")
        checkbox.setText("WELCOME TO HOMEPAGE")
        with self.assertLogs() as log: checkwin.buttonClicked()
        self.assertIn("INFO:root:WELCOME", log.output)
        self.assertTrue(checkbox.exec() == QtWidgets.QMessageBox.Ok)

    def setUp(self):
        app = QApplication([])
        self.welcome_window = welcomeWindow()

    def test_window_title(self):
        app = QApplication([])
        self.assertEqual(self.welcome_window.windowTitle(), "Welcome Window")

    def test_init(self):
        app = QApplication([])
        window = autoUploadWindow()
        self.assertEqual(window.windowTitle(), "AUTO UPLOAD WINDOW")
    
    def test_autoUploadFunction(self):
        app = QApplication([])
        window = autoUploadWindow()
        window.tokentextbox.setPlainText("YOUR_DROPBOX_TOKEN")
        window.foldertextbox.setPlainText("TEST_FOLDER")
        window.autoUploadFunction()

if __name__ == '__main__':
    unittest.main()
