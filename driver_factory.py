"""
###  封装浏览器驱动工厂  ###

###  做什么
###  根据配置动态创建webdriver实例，并自动下载驱动。

###  为什么这么做
###  工厂模式统一浏览器创建逻辑，用例只需调用get_driver()即可
###  切换浏览器只需改yaml配置
###  自动处理驱动版本匹配，再无chromedriver版本不对的痛

###  作用
###  统一入口，屏蔽细节，让测试代码不关心驱动从哪来，如何配置
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from utils.config_reader import config
from webdriver_manager.chrome import ChromeDriverManager

class DriverFactory:
    @staticmethod
    def get_driver():
        browser = config.get('browser')
        timeout = config.get('timeout')

        if browser == 'chrome':
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            chrome_options = ChromeOptions()

            # CI 环境必须加无头模式
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-shared-memory")

            # 设置页面加载策略
            chrome_options.set_capability("pageLoadStrategy", "eager")

            # 最稳定写法，无任何报错
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.maximize_window()
        driver.implicitly_wait(timeout)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)

        return driver
