
###   登录页   ###

##  编写具体页面对象

#  做什么 1.
# 针对被测网站的页面，封装元素定位和业务操作

###  为什么这么做
#  页面元素和操作集中管理，当UI变懂事只需修改对应页面的定位符
#  测试用例只关心“做什么”，不关心“怎么找到这个按钮”

## 作用
#  构建业务层抽象，让测试用例想操作真是页面一样调用login（）、get_page_title()

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    username_input = (By.ID, 'user-name')
    password_input = (By.ID, 'password')
    login_button = (By.ID, 'login-button')
    error_message = (By.CLASS_NAME, 'error-message-container')

    # 输入用户名
    def enter_username(self, username):
        self.input_text(self.username_input, username)

    # 输入密码
    def enter_password(self, password):
        self.input_text(self.password_input, password)

    # 点击登录
    def click_login(self):
        self.click(self.login_button)

        # 登录方法（已修复：删除错误的 timeout 参数）
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

        # ✅ 修复：添加用例需要的错误提示判断方法
    def is_error_displayed(self, *args, **kwargs):
            return self.find_element(self.error_message).is_displayed()
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













