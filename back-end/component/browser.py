from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Browser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10) 

    def openPage(self, url):
        self.driver.get(url)

    def getElement(self, css):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=css)

    def getElements(self, css):
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=css)