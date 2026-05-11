
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class CheckoutPage(BasePage):
    """结算信息填写页面（Checkout: Your Information）"""

    # ----- 结算页面元素定位 -----
    PAGE_TITLE = (By.CLASS_NAME, 'title')
    FIRST_NAME_INPUT = (By.ID, 'first-name')
    LAST_NAME_INPUT = (By.ID, 'last-name')
    POSTAL_CODE_INPUT = (By.ID, 'postal-code')
    CONTINUE_BTN = (By.ID, 'continue')
    CANCEL_BTN = (By.ID, 'cancel')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    # ----- 页面操作方法 -----
    def is_checkout_page(self) -> bool:
        """
        验证当前是否是结算信息填写页面
        捕获页面加载超时、元素不存在等异常
        """
        try:
            title_element = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
            return title_element.text == "Checkout: Your Information"
        except TimeoutException:
            return False

    def input_customer_info(self, first_name: str, last_name: str, postal_code: str):
        """
        填写结算信息：姓名+姓氏+邮编
        """
        logger.info(f"填写结算信息：{first_name} {last_name}, 邮编：{postal_code}")
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)

    def get_error_message(self) -> str:
        """获取表单验证错误提示信息"""
        return self.get_text(self.ERROR_MESSAGE)

    def click_continue(self):
        """
        点击继续按钮，跳转到订单概览页面
        """
        logger.info("点击【继续】按钮")
        self.click(self.CONTINUE_BTN)
        # 先注释掉，等创建overview_page.py后再打开
        # from pages.overview_page import OverviewPage
        # return OverviewPage(self.driver)

    def click_cancel(self):
        """
        点击取消按钮，返回购物车页面
        """
        logger.info("点击【取消】按钮")
        self.click(self.CANCEL_BTN)
        from pages.cart_page import CartPage
        return CartPage(self.driver)