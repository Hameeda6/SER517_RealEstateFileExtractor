import time
from selenium import webdriver
from selenium.common import NoSuchElementException
import os
import getpass

from datetime import datetime
import glob
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
import glob
from PyQt6.QtWidgets import QMessageBox


options = webdriver.ChromeOptions()
username = getpass.getuser()
# options.add_argument("user-data-dir=/Users/" + username + "/Library/Application Support/Google/Chrome")
# uncomment the above line to use a user profile for chrome

download_directory = str(os.path.join(os.path.expanduser("~"), "Desktop")) + "/TenantCloudFiles"
prefs = {"download.default_directory": download_directory}
options.add_experimental_option("prefs", prefs)
# To download the files in a specified directory

driver = webdriver.Chrome(options = options)
driver.maximize_window()
URL = "https://home.tenantcloud.com/login"
file_managers = "https://home.tenantcloud.com/ng2/settings/file_manager"
checkbox_xpath = '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/settings-file-manager-layout/settings-file-manager-layout-main/panel/section/panel-body/div/settings-file-manager-list2/div/settings-file-manager-table/div/div/div[1]/custom-checkbox/div/label'
driver.get(URL)
page_no = 2
start_time = datetime.now()


def wait():
    time.sleep(3)


def waiting(second):
    time.sleep(second)


def short_wait():
    time.sleep(2)


def download_wait():
    time.sleep(10)


def file_manager():
    driver.find_element('xpath',
                        '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/home-main/div/div/div[1]/div[15]/widget-source/widget-file-manager/div/div[2]/div[2]/a').click()
    # file manager homepage
    print("Found the file manager button on dashboard")


def check_box():
    try:
        time.sleep(3)
        driver.find_element('xpath',
                            '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/file-manager-table/div/div/div[1]/control-checkbox/div/label').click()
        # select all files checkbox
        short_wait()
        print("Found default checkbox")
    except NoSuchElementException:
        driver.find_element('xpath',
                            checkbox_xpath).click()
        short_wait()
        print("alternate checkbox found")


def long_wait():
    time.sleep(20)


def new_page(page_no):
    url2 = file_managers + '?page=' + str(page_no)
    driver.get(url2)
    wait()


def enabled():
    try:
        driver.find_element('xpath',
                            '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/file-manager-table/div/div/div[1]/control-checkbox/div/label')
        # select all files checkbox
        print('next page')
    except NoSuchElementException:
        print("trying alternate page")
        try:
            driver.find_element('xpath',
                                checkbox_xpath)
            print('Next page handled')
        except NoSuchElementException:
            print("Unable to go to next page")
            return False
    return True


def pagination(page_no):
    url_list = []
    url_list.append(driver.current_url)
    while enabled():
        try:
            time.sleep(5)
            new_page(page_no)
            print(page_no)
            page_no += 1
            wait()
            curr_url = driver.current_url
            url_list.append(curr_url)
            if len(url_list) > 1:
                if url_list[-1] == url_list[-2]:
                    print("All pages traversed and all files downloaded.")
                    break
            check_box()
            action_menu()
            wait()
            download_button()
            download_wait()
        except NoSuchElementException:
            print("All files downloaded.")
            break
    num_files, downloaded_files = check_download(start_time)
    print(f"{num_files} files downloaded after {start_time}:")
    for file in downloaded_files:
        print(file)


def login_manual():
    wait()
    waiting(60)
    file_manager()



def action_menu():
    try:
        driver.find_element('xpath',
                            '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/div/div/file-manager-table-action/menu/button/menu-btn').click()
        # actions menu.
        short_wait()
        print('default action menu found')
    except NoSuchElementException:
        driver.find_element('xpath',
                            '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/settings-file-manager-layout/settings-file-manager-layout-main/panel/section/panel-body/div/settings-file-manager-list2/div/div/div[2]/dots/div/a/div/i').click()
        short_wait()
        print("alternate action menu button found")


def download_button():
    try:
        driver.find_element('xpath', '/html/body/div[2]/div/div/menu-content/div/button').click()
        print("download button found auto")
    except NoSuchElementException:
        print("trying alternate download button")
        try:
            driver.find_element('xpath', '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/settings-file-manager-layout/settings-file-manager-layout-main/panel/section/panel-body/div/settings-file-manager-list2/div/div/div[2]/dots/div/div/div[2]/div/div/div/ul/li[1]/permission-action-popover/div/a').click()
            print("alternate download button found next page")
        except NoSuchElementException:
            driver.find_element('xpath', '/html/body/div[3]/div/div/menu-content/div/button').click()
            print("download button found manual")


def check_download(start_time):
    # get the file name which is downloaded
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
    print(f"Downloaded {num_files} files with total size of {total_size} bytes after {start_time}:")
    for file in downloaded_files:
        print(f"{file[0]} ({file[1]} bytes) - modified {file[2]}")
    return num_files, downloaded_files


def download():
    # use when chrome user profile is available
    wait()
    check_box()
    action_menu()
    download_button()
    long_wait()
    pagination(page_no)


# handling login
try:
    wait()
    file_manager()
    print("Logged in already")
except NoSuchElementException:
    print("Logging in")
    login_manual()


# being downloading after logging in
def initiate():
    download()
    wait()
    driver.quit()


def verify_login():
    driver.find_element('xpath', '/html/body/div[2]/div/div/menu-content/div/button').click()
    driver.find_element('xpath',
                        '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/settings-file-manager-layout/settings-file-manager-layout-main/panel/section/panel-body/div/settings-file-manager-list2/div/div/div[2]/dots/div/a/div/i').click()
    short_wait()
    driver.find_element('xpath',
                        '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/ui-view-ng-upgrade/ui-view/app/div/ng-component/div/file-manager-list/panel/panel-body/file-manager-table/div/div/div[1]/control-checkbox/div/label')
    # select all files checkbox
    driver.find_element('xpath',
                        '/html/body/ui-view/app-root/div[3]/landlord-dashboard/div/div/div/div[2]/landlord-app-component/div/home-main/div/div/div[1]/div[15]/widget-source/widget-file-manager/div/div[2]/div[2]/a').click()
    # file manager homepage
    short_wait()
    download()
