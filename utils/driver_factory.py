###  封装浏览器驱动工厂  ###

#from pytest_selenium.drivers.chrome import chrome_options

###  做什么

###  根据配置动态创建webdriver实例，并自动下载驱动。

###  为什么这么做
###  工厂模式统一浏览器创建逻辑，用例只需调用get_driver()即可
###  切换浏览器只需改yaml配置
###  自动处理驱动版本匹配，再无chromedriver版本不对的痛

###  作用
###  同意入口，屏蔽细节，让测试代码不关心驱动从哪来，如何配置

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from utils.config_reader import config

class DriverFactory:
    @staticmethod
    def get_driver():
        browser = config.get('browser')
        if browser == 'chrome':
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif browser == 'firefox':
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        driver.maximize_window()
        driver.implicitly_wait(config.get('timeout'))
        return driver

