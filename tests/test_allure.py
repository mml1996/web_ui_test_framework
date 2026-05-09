import allure
import pytest


@allure.epic('saucedemo电商Web UI自动化测试框架')
@allure.feature('登录模块')
@allure.story('标准用户登录')
@allure.title('验证标准用户可以成功登录系统')
@pytest.mark.ut
def test_a():
    pass


@allure.epic('saucedemo电商Web UI自动化测试框架')
@allure.feature('登录模块')
@allure.story('锁定用户登录')
@allure.title('验证锁定用户无法登录，会显示锁定提示')
@pytest.mark.ut
def test_b():
    pass

@allure.epic('saucedemo电商Web UI自动化测试框架')
@allure.feature('登录模块')
@allure.story('多账号登录场景验证')
@allure.title('参数化登录用例: {case[name]}')
@pytest.mark.ut
def test_c():
    pass




