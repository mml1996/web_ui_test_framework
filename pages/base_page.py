
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # 全局强制 30 秒等待，彻底解决 GitHub 超时
        self.timeout = 30
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"找到元素: {locator}")
            return element
        except TimeoutException:
            logger.error(f"定位元素超时: {locator}")
            raise

    def find_elements(self, locator):
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator))
            logger.info(f'找到多个元素: {locator}')
            return elements
        except TimeoutException:
            logger.error(f'定位多个元素超时: {locator}')
            raise

    def click(self, locator):
        self.find_element(locator).click()
        logger.info(f'点击了元素: {locator}')

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f'在 {locator} 输入了文本: {text}')

    def get_text(self, locator):
        return self.find_element(locator).text

    def get_title(self):
        return self.driver.title