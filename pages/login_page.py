
###   登录页   ###

##  编写具体页面对象

#  做什么 1.
# 针对被测网站的页面，封装元素定位和业务操作

###  为什么这么做
#  页面元素和操作集中管理，当UI变懂事只需修改对应页面的定位符
#  测试用例只关心“做什么”，不关心“怎么找到这个按钮”

## 作用
#  构建业务层抽象，让测试用例想操作真是页面一样调用login（）、get_page_title()

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    #  1.先在这里定义元素定位器
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def enter_username(self, username):
        """输入用户名"""
        self.input_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """输入密码"""
        self.input_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """登录操作，针对不同用户场景优化"""
        # 问题用户单独设置更长的超时
        #  2.这里调用self。username——input
        if username == "problem_user":
            self.input_text(self.USERNAME_INPUT, username, timeout=20)
            self.input_text(self.PASSWORD_INPUT, password, timeout=20)
        else:
            self.enter_username(username)
            self.enter_password(password)

        self.click_login()

    def is_error_displayed(self, expected_text):
        """
        检查错误提示是否显示正确
        """
        # 错误提示元素的定位器（根据你的页面调整）
        error_message = (By.CLASS_NAME, "error-message-container")
        element = self.find_element(error_message)
        return expected_text in element.text


    # 终极方法：不依赖定位符，直接判断页面里是否包含错误文本
   #def is_error_displayed(self, expected_text):
        #return expected_text in self.driver.page_source





"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # 元素定位器/定位符
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def enter_username(self, username):
        self.input_text(self.USERNAME_INPUT,username)

    def enter_password(self, password):
        self.input_text(self.PASSWORD_INPUT,password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)  
"""













