
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
from utils.config_reader import config
import logging
#from loguru import logger

#初始化日志
logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        #  初始化页面基类
        self.driver = driver
        # 从配置文件读取超时时间，不再写死
        self.timeout = config.get('timeout')
        self.wait = WebDriverWait(self.driver, self.timeout)
        #self.timeout = 10

    def find_element(self, locator):
        """
        查找单个元素（确保可见且可交互）
        : param locator: 元素定位器，格式为（By.ID,'xxx）
        : return: WebElement 对象
        """

        try:
            # 改用 element_to_be_clickable,确保元素可见且可点击
            element = self.wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"找到元素: {locator}")
            return element
        except TimeoutException:
            logger.error(f"定位元素超时: {locator}")
            raise


    def find_elements(self, locator):
        """
        查找多个元素
        : param locator: 元素定位器
        : return: 元素列表
        """
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator))
            logger.info(f'找到多个元素: {locator}')
            return elements
        except TimeoutException:
            logger.error(f'定位多个元素超时: {locator}')
            raise


    def click(self, locator):
        """
        点击元素
        : param locator: 元素定位器
        """
        self.find_element(locator).click()
        logger.info(f'点击了元素: {locator}')

        # element = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator))
        # element.click()
        # logger.info(f'Clicked on element: {locator}')

    def input_text(self, locator, text):
        """
        向输入框输入文本（先清空再输入）

        : param locator: 元素定位器
        : return: text: 要输入的文本
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f'在 {locator} 输入了文本: {text}')

    def get_text(self, locator):
        """
        获取元素文本
        : param locator: 元素定位器
        : return: 元素文本
        """
        return self.find_element (locator).text

    def get_title(self):
        """
        获取页面标题
        : return: 页面标题
        """
        return self.driver.title

