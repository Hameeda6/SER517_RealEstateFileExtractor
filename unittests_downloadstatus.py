import unittest
import os
import time
from datetime import datetime, timedelta
from TenantCloud import check_download

class TestCheckDownload(unittest.TestCase):
    
    download_directory = os.path.join(os.path.expanduser("~"), "Desktop", "TenantCloudFiles")
    os.makedirs(download_directory, exist_ok=True)
    test_file_name = "test_file.txt"
    test_file_path = os.path.join(download_directory, test_file_name)
    with open(test_file_path, 'w') as f:
        f.write("test content")
    modified_time = time.time() - 3600
    os.utime(test_file_path, (modified_time, modified_time))
    test_file_name_1= "test_file_1.txt"
    test_file_path_1 = os.path.join(download_directory, test_file_name_1)
    with open(test_file_path_1, 'w') as f:
        f.write("test content")
    

    def test_check_download(self):
        start_time = datetime.fromtimestamp(os.path.getmtime(self.test_file_path))
        print(start_time)
        num_files, downloaded_files = check_download(start_time)

        self.assertEqual(num_files, 1)
        self.assertEqual(downloaded_files[0][0], self.test_file_name_1)
        self.assertEqual(downloaded_files[0][1], os.path.getsize(self.test_file_path))

    def tearDown(self):
        os.remove(self.test_file_path)
        os.remove(self.test_file_path_1)

if __name__ == '__main__':
    unittest.main()
