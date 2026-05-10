###！！！！！！9.编写测试用例
# from unittest import case
import allure
import pytest
###   登录相关用例   ###
##  做什么
# 结合页面对象和fixture，按真实业务写测试

##  为什么这么做
# 用例简介，只描述业务步骤和断言，不包含定位细节
# 使用pytest的断言，报错信息清晰

## 作用
# 用例即文档，让产品、开发也能看懂自动化测试在验证什么

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

@allure.epic('saucedemo电商Web UI自动化测试框架')
@allure.feature('登录模块')
class TestLogin:
    @allure.story('标准用户登录')
    @allure.title('验证标准用户可以成功登录系统')
  #  @pytest.mark.skip
    def test_valid_login(self,driver):
        login_page = LoginPage(driver)

        login_page.login('standard_user','secret_sauce')
        inventory_page = InventoryPage(driver)
        assert inventory_page.get_page_title() == 'Products'

    @allure.story('锁定用户登录')
    @allure.title('验证锁定用户无法登录，会显示锁定提示')
    def test_invalid_login(self,driver):
        login_page = LoginPage(driver)

        #直接判断错误信息是否存在，100%不会超时

        login_page.login('locked_out_user','secret_sauce')
        assert login_page.is_error_displayed('Epic sadface: Sorry, this user has been locked out.')

## 修改测试用例

#12.数据驱动-修改测试用例

import pytest
import yaml
from pathlib import Path

# 读取yaml测试数据
def load_login_data():
    data_path = Path(__file__).parent.parent / 'data'/ 'login_data.yaml'
    with open(data_path, encoding='utf-8') as f:
        return yaml.safe_load(f)

@allure.epic('saucedemo电商Web UI自动化测试框架')
@allure.feature('登录模块')
class TestLoginScenarios:
    @allure.story('多账号登录场景验证')
    @allure.title('参数化登录用例: {case[name]}')
    @pytest.mark.parametrize('case', load_login_data())
    def test_login_scenarios(self,driver,case):
        """
        多账号登录场景验证
        :param driver: 浏览器驱动
        :param case: 测试数据，包含username\\password\\expected_title或expected_error
        """
        login_page = LoginPage(driver)
        login_page.login(case['username'],case['password'])
        # 如果case里有expected_error字段，就执行失败断言；否则执行成功断言
        if 'expected_error' in case:
            assert login_page.is_error_displayed(case['expected_error'])
        else:
            assert InventoryPage(driver).get_page_title() == case['expected_title']











