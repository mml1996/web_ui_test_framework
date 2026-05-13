import time
import sys
import os
import pytest
from pathlib import Path
from datetime import datetime
import allure
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.driver_factory import DriverFactory
from utils.config_reader import config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 日志配置
logger.remove()
logger.add(sys.stderr, level='INFO')
logger.add('logs/test_{time}.log', rotation='1 day', level='DEBUG', encoding='utf-8')


# 1. 浏览器驱动 fixture（终极稳定版）
@pytest.fixture(scope='function')
def driver():
    logger.info('=== 开始初始化浏览器驱动 ===')
    driver = None
    try:
        driver = DriverFactory.get_driver()

        # 延长所有超时时间
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.implicitly_wait(config.get('timeout', 20))
        driver.wait = WebDriverWait(driver, 20)

        base_url = config.get('base_url')
        driver.get(base_url)
        logger.info(f'成功访问基础URL: {base_url}')

        yield driver

    except Exception as e:
        logger.error(f'浏览器初始化失败: {str(e)}', exc_info=True)
        raise

    finally:
        if driver:
            logger.info('=== 关闭浏览器驱动 ===')
            driver.quit()


# 2. 购物车页面预加载 fixture（修复重复登录问题）
@pytest.fixture
def cart_page(driver):
    logger.info('=== 开始执行cart_page fixture ===')
    try:
        # 1. 登录
        logger.info('1. 开始登录系统')
        from pages.login_page import LoginPage
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        logger.info('已使用用户 standard_user 登录成功')
        time.sleep(1)

        # 2. 清空购物车
        logger.info('2. 开始清空购物车')
        driver.get("https://www.saucedemo.com/cart.html")
        try:
            remove_buttons = driver.find_elements(By.XPATH, "//button[text()='Remove']")
            for btn in remove_buttons:
                btn.click()
        except Exception as e:
            logger.warning(f'清空购物车时出现警告: {str(e)}')
        logger.info('已清空购物车')
        time.sleep(0.5)

        logger.info('3. 开始进入商品列表页')
        driver.get("https://www.saucedemo.com/inventory.html")
        time.sleep(1)

        # --------------------------
        # 关键修复：加购逻辑改为「点击+验证」，确保GitHub一定生效
        # --------------------------
        # 加购1：Backpack
        logger.info('添加商品：Sauce Labs Backpack')
        backpack_btn = wait_clickable(driver, (By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-backpack']"))
        # 用JavaScript强制点击，绕过无界面模式的拦截
        driver.execute_script("arguments[0].click();", backpack_btn)
        time.sleep(1)
        # 验证是否成功加入：按钮文字变成"Remove"
        assert wait_element(driver, (By.XPATH, "//button[@data-test='remove-sauce-labs-backpack']")), "Backpack 未成功加入购物车"

        # 加购2：Bolt T-Shirt
        logger.info('添加商品：Sauce Labs Bolt T-Shirt')
        shirt_btn = wait_clickable(driver, (By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-bolt-t-shirt']"))
        driver.execute_script("arguments[0].click();", shirt_btn)
        time.sleep(1)
        # 验证是否成功加入
        assert wait_element(driver, (By.XPATH, "//button[@data-test='remove-sauce-labs-bolt-t-shirt']")), "Bolt T-Shirt 未成功加入购物车"

        # 4. 进入购物车
        logger.info('4. 开始进入购物车页面')
        # 进入购物车（JS强制点击，保证GitHub必生效）
        cart_button = wait_clickable(driver, (By.CLASS_NAME, "shopping_cart_link"))
        driver.execute_script("arguments[0].click();", cart_button)
        logger.info('已进入购物车页面')
        time.sleep(1)

        #  最终验证：必须2个商品
        from pages.cart_page import CartPage
        cart_page_obj = CartPage(driver)
        real_count = cart_page_obj.get_cart_items_count()
        logger.info(f'✅ 购物车最终商品数量：{real_count}')
        assert real_count == 2, f"夹具失败！购物车数量应为2，实际是 {real_count}"

        logger.info('=== cart_page fixture执行成功 ===')
        return cart_page_obj

    except Exception as e:
        logger.error('=== cart_page fixture执行失败 ===', exc_info=True)
        raise

# 3. 失败自动截图钩子
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 仅在用例执行失败时截图
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                screenshot_dir = Path('reports/screenshots')
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                file_name = f'{item.name}_{timestamp}.png'
                file_path = screenshot_dir / file_name

                driver.save_screenshot(str(file_path))
                logger.error(f'用例 {item.name} 失败，截图已保存: {file_path}')

                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f'失败截图_{item.name}',
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                logger.error(f'截图保存失败: {str(e)}', exc_info=True)


# ==================== 通用等待工具（不影响业务）====================
def wait_element(driver, locator):
    return driver.wait.until(EC.presence_of_element_located(locator))

def wait_clickable(driver, locator):
    return driver.wait.until(EC.element_to_be_clickable(locator))

