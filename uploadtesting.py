import unittest
from PyQt6.QtWidgets import QApplication
from HomePage import MainWindow

app = QApplication([])

class TestMainWindow(unittest.TestCase):
    
    def test_window_title(self):
        window = MainWindow()
        self.assertEqual(window.windowTitle(), "517 PROJECT")
    
    def test_button_text(self):
        window = MainWindow()
        self.assertEqual(window.pushButton.text(), "WELCOME")

    def test_button_textupload(self):
        window = MainWindow()
        self.assertEqual(window.pushButton_3.text(), 'UPLOAD')

    def test_button_textdownload(self):
        window = MainWindow()
        self.assertEqual(window.pushButton_2.text(), 'DOWNLOAD')
        
if __name__ == '__main__':
    unittest.main()
