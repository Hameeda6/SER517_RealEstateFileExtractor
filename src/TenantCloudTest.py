import unittest
from unittest.mock import patch, MagicMock
from TenantCloud import *

prg = './TenantCloud.py'

class TestMyModule(unittest.TestCase):

    def setUp(self):
        # initialize the webdriver and open the TenantCloud login page
        self.driver = webdriver.Chrome()
        self.driver.get('https://app.tenantcloud.com/')

    def test_file_manager(self):
        driver = MagicMock()
        file_manager_button_xpath = '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/home-main/div/div/div[1]/div[15]/widget-source/widget-file-manager/div/div[2]/div[2]/a'
        file_manager(driver, file_manager_button_xpath)
        driver.find_element.assert_called_once_with('xpath', file_manager_button_xpath)
        driver.find_element().click.assert_called_once()

    def test_check_box(self):
        driver = MagicMock()
        checkbox_xpath = '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/file-manager-table/div/div/div[1]/control-checkbox/div/label'
        check_box(driver, checkbox_xpath)
        driver.find_element.assert_called_once_with('xpath', checkbox_xpath)
        driver.find_element().click.assert_called_once()

    def test_file_exists(self):
        assert os.path.isfile(prg)

    @patch('requests.get')
    @patch('builtins.open', new_callable=MagicMock)
    def test_fetch_files(self, mock_open, mock_get):
        url = 'https://tenantcloud.s3.us-west-2.amazonaws.com/assets/file_manager_download/n/w/k/nwklfgmnn1qk7pwz/original.zip?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS7C4YD3EA2G3N4GR%2F20230404%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230404T160000Z&X-Amz-SignedHeaders=host&X-Amz-Expires=10800&X-Amz-Signature=980de0ca1d792e31fef38e8f35b1dcfd459ced63385087e8e76e85e3e0f69fb4'
        mock_response = MagicMock()
        mock_response.text = '<html><body><a href="file_manager 10 files.zip">PDF File</a></body></html>'
        mock_get.return_value = mock_response
        mock_file_content = b'zip file content'
        mock_file_response = MagicMock()
        mock_file_response.content = mock_file_content
        with patch('builtins.open', mock_open):
            fetch_files(url)
        mock_get.assert_called_once_with('https://tenantcloud.s3.us-west-2.amazonaws.com/assets/file_manager_download/n/w/k/nwklfgmnn1qk7pwz/original.zip?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS7C4YD3EA2G3N4GR%2F20230404%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230404T160000Z&X-Amz-SignedHeaders=host&X-Amz-Expires=10800&X-Amz-Signature=980de0ca1d792e31fef38e8f35b1dcfd459ced63385087e8e76e85e3e0f69fb4')
        mock_open.assert_called_once_with('file_manager 10 files.zip', 'wb')
        mock_open().write.assert_called_once_with(mock_file_content)

    def test_enabled(self):
        # test the enabled function to ensure it correctly identifies whether the next page is available
        driver = self.driver
        driver.get('https://app.tenantcloud.com/files')
        self.assertTrue(enabled())
        driver.get('https://app.tenantcloud.com/files?page=10')
        self.assertFalse(enabled())

    def test_check_download(self):
        # test the check_download function to ensure it correctly identifies whether a file has been downloaded
        self.assertEqual(check_download(), 'Download successful')


    def test_new_page(self):
        page_no = 2
        expected_url = 'https://home.tenantcloud.com/ng2/settings/file_manager?page=2'
        new_page(page_no, self.driver, self.wait)
        self.driver.get.assert_called_once_with(expected_url)
        self.wait.assert_called_once()


    def test_pagination(self):
        self.driver.current_url = 'https://home.tenantcloud.com/ng2/settings/file_manager'
        self.assertTrue(enabled())
        self.assertTrue(check_box())
        self.assertTrue(action_menu())
        self.assertTrue(download_button())

        expected_url_list = ['https://home.tenantcloud.com/ng2/settings/file_manager?page=2', 'https://home.tenantcloud.com/ng2/settings/file_manager?page=3', 'https://home.tenantcloud.com/ng2/settings/file_manager?page=4']
        url_list = []
        page_no = 2
        while enabled():
            pagination(page_no, self.driver, self.wait)
            url_list.append(self.driver.current_url)
            page_no += 1
        self.assertEqual(url_list, expected_url_list)


    def tearDown(self):
        # close the webdriver instance after each test
        self.driver.quit()


    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    def test_default_action_menu(self, mock_find_element):
        # Mock the find_element method to simulate finding the default action menu button
        mock_find_element.return_value = MagicMock()

        # Call the function
        action_menu()

        # Assert that the default action menu button was clicked
        mock_find_element.assert_called_with('xpath',
                                             '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/div/div/file-manager-table-action/menu/button/menu-btn')

    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    def test_alternate_action_menu(self, mock_find_element):
        # Mock the find_element method to simulate not finding the default action menu button,
        # but finding the alternate action menu button instead
        mock_find_element.side_effect = [NoSuchElementException, MagicMock()]

        # Call the function
        action_menu()

        # Assert that the alternate action menu button was clicked
        mock_find_element.assert_any_call('xpath',
                                          '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/div/div/file-manager-table-action/menu/button/menu-btn')
        mock_find_element.assert_called_with('xpath',
                                             '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/settings-file-manager-layout/settings-file-manager-layout-main/panel/section/panel-body/div/settings-file-manager-list2/div/div/div[2]/dots/div/a/div/i')


    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    def test_default_download_button(self, mock_find_element):
        # Mock the find_element method to simulate finding the default download button
        mock_find_element.return_value = MagicMock()

        # Call the function
        download_button()

        # Assert that the default download button was clicked
        mock_find_element.assert_called_with('xpath', '/html/body/div[2]/div/div/menu-content/div/button')

    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
    def test_alternate_download_button(self, mock_find_element):
        # Mock the find_element method to simulate not finding the default download button,
        # but finding the alternate download button instead
        mock_find_element.side_effect = [NoSuchElementException, NoSuchElementException, MagicMock()]

        # Call the function
        download_button()

        # Assert that the alternate download button was clicked
        mock_find_element.assert_any_call('xpath', '/html/body/div[2]/div/div/menu-content/div/button')
        mock_find_element.assert_any_call('xpath', '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/settings-file-manager-layout/settings-file-manager-layout-main/panel/section/panel-body/div/settings-file-manager-list2/div/div/div[2]/dots/div/div/div[2]/div/div/div/ul/li[1]/permission-action-popover/div/a')
        mock_find_element.assert_called_with('xpath', '/html/body/div[3]/div/div/menu-content/div/button')


    def test_download_success(self):
        # Create a temporary file in the download directory
        download_directory = os.path.join(os.path.expanduser("~"), "Desktop", "TenantCloudFiles")
        test_file_path = os.path.join(download_directory, "file_manager 10 files.zip")
        with open(test_file_path, "w") as f:
            f.write("Test file content")
        # Check if the file exists in the download directory
        self.assertEqual(check_download(), "Download successful")
        # Remove the temporary file
        os.remove(test_file_path)

    def test_download_not_successful(self):
        # Delete all files in the download directory
        download_directory = os.path.join(os.path.expanduser("~"), "Desktop", "TenantCloudFiles")
        for file_name in os.listdir(download_directory):
            file_path = os.path.join(download_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        # Check if there are no files in the download directory
        self.assertEqual(check_download(), "Download not successful")

    def test_download_location_not_found(self):
        # Remove the download directory
        download_directory = os.path.join(os.path.expanduser("~"), "Desktop", "TenantCloudFiles")
        os.rmdir(download_directory)
        # Check if the function returns the expected message
        self.assertEqual(check_download(), "Download successful. check downloads location")


if __name__ == '__main__':
    unittest.main()


# Since this scraper is built using Selenium, which is a testing framework by itself, some tests are integrated inherently in the code.
