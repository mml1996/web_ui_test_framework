
###   封装通用页面操作  ###

###  封装基础页面对象（basepage）

###  做什么
#  把所有页面公用的操作（等待、查找、点击、输入、截图等）封装到基类，让具体页面继承

###  为什么这么做

#  避免每个页面重复写等待逻辑、异常处理
#  所有公共操作都在这里维护，修改一处，全局生效
#  继承日志，使操作可追溯

###  作用
# 减少重复代码，提高稳定性和可读性，这是Page Object模式的基础

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from utils.config_reader import config


class DriverFactory:
    @staticmethod
    def get_driver():
        browser = config.get('browser')
        if browser == 'chrome':
            chrome_options = ChromeOptions()

            # 基础防崩溃选项
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # 缓解渲染超时的核心配置
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-software-rasterizer")  # 强制禁用软件光栅化
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")  # 禁用 Viz 合成器
            chrome_options.add_argument("--disable-accelerated-2d-canvas")
            chrome_options.add_argument("--disable-accelerated-jpeg-decoding")

            # 防止长时间加载
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--disable-translate")

            # 页面加载策略（建议用 eager 模式）
            chrome_options.page_load_strategy = 'eager'  # 只等待 DOM 加载，不等待所有资源

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

        elif browser == 'firefox':
            # ... 原有 firefox 代码
            pass
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.maximize_window()
        driver.implicitly_wait(config.get('timeout'))
        return driver

