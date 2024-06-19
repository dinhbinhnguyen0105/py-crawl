import socket, os, sys
from time import sleep
from random import uniform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from PyQt5.QtCore import pyqtSignal, QObject

dir_utils = os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')
sys.path.append(dir_utils)

class SeleniumControl(QObject):
    finished = pyqtSignal()
    event_error = pyqtSignal(str)
    def __init__(self, browsername, parent=None):
        super().__init__(parent)
        if sys.platform == 'linux' or sys.platform == 'linux2':
            pass
        elif sys.platform == 'win32':
            self.dir_driver = os.path.join(os.path.dirname(__file__), os.path.pardir, 'bin', 'driver', 'chromedriver.exe')
            self.dir_chromeapp = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            self.path_chromedriver = os.path.join(os.path.dirname(__file__), os.path.pardir, 'bin', 'driver', 'chromedriver.exe')
            if not os.path.exists(self.dir_driver) or not os.path.exists(self.dir_driver):
                print('Error')
                self.finished.emit()
        elif sys.platform == 'darwin':
            self.dir_driver = os.path.join(os.path.dirname(__file__), 'chromedriver')
            self.dir_chromeapp = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'        
            self.path_chromedriver = os.path.join(os.path.dirname(__file__), os.path.pardir, 'bin', 'driver', 'chromedriver')
            if not os.path.exists(self.dir_driver) or not os.path.exists(self.path_chromedriver):
                self.finished.emit()

        self.browsername = browsername
        self.dir_browser = os.path.join(os.path.dirname(__file__), os.path.pardir, 'bin', 'browsers', browsername)
        if os.path.exists(self.dir_browser) is not True:
            os.mkdir(self.dir_browser)
        self.port = 9923
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', self.port)) == 0:
                    self.port += 1
                else: break

    def initDriver(self):
        options = Options()
        options.add_experimental_option('debuggerAddress', f'localhost:{self.port}')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-notifications')
        service = Service(self.dir_driver)
        os.popen(f'"{self.dir_chromeapp}" --remote-debugging-port={self.port} --user-data-dir="{self.dir_browser}"')
        try:
            return webdriver.Chrome(service=service, options=options)
        except WebDriverException as e:
            return False

    def quitDriver(self):
        if hasattr(self, 'driver') and self.driver:
            if self.driver.current_window_handle in self.driver.window_handles:
                self.driver.close()
                self.driver.quit()
            self.finished.emit()
            