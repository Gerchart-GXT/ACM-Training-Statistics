from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Browser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
        
        chrome_options.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
        chrome_options.add_argument("no-sandbox")  # 取消沙盒模式
        chrome_options.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
        chrome_options.add_argument("about:histograms")
        chrome_options.add_argument("about:cache")
        
        chrome_options.add_argument("disable-extensions")  # 禁用扩展
        chrome_options.add_argument("disable-glsl-translator")  # 禁用GLSL翻译
        
        chrome_options.add_argument("disable-translate")  # 禁用翻译
        chrome_options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片, 提升速度
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10) 

    def __del__(self):
        self.driver.quit()

    def openPage(self, url):
        self.driver.get(url)

    def closePage(self):
        self.driver.close()

    def getElement(self, css):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=css)

    def getElements(self, css):
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=css)