import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """登录页面"""

    # 元素定位
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def login(self, username: str, password: str):
        """
        登录系统（支持成功/失败场景，不强制等待跳转，解决锁定用户超时问题）
        """
        logger.info(f"登录系统，用户名: {username}")

        # 等待用户名输入框可见
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )

        # 输入账号密码
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

        # 🔥 关键修复：
        # 不等待跳转！让测试用例自己判断是成功还是失败
        # 锁定用户、错误密码都不会再超时

    def get_error_message(self) -> str:
        """获取登录错误信息"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self, expected_error: str) -> bool:
        """断言错误信息是否正确"""
        return expected_error in self.get_error_message()









