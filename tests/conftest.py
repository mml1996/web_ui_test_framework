
###  10.集成日志系统

##  做什么
# 用loguru替代print，将运行日志输出到文件和控制台
# 在conftest.py顶部配置

## 为什么这么做
# loguru简单强大，不需要复杂的logging.conf
# 日志文件按天轮转，便于问题追溯
# 在BasePage中已嵌入日志，自动记录关键操作

##  作用
# 快速定位失败原因，尤其在CI环境无界面时日志是唯一的线索
import sys
import os
import pytest
from pathlib import Path
from datetime import datetime
import allure
from loguru import logger
from utils.driver_factory import DriverFactory
from utils.config_reader import config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger.remove()
logger.add(sys.stderr, level='INFO')
logger.add('logs/test_{time}.log', rotation='1 day', level='DEBUG')
###   8.编写pytest fixtures 管理Driver生命周期

###   pytest全局 fixtures 和 钩子

##  做什么
#  用conftest.py定义driver的创建和销毁，让所有测试方法自动获得driver

##  为什么这么做
# function级别确保每个用例有独立浏览器实例，互不打扰
# yield之前的代码是前置（打开浏览器并访问URL），之后是后置（关闭浏览器）
# 集中管理生命周期，用例中只需生命driver参数即可使用

##  作用
# 用例隔离、资源自动回收，避免因一个用例失败导致后续用例状态异常


#  1.浏览器驱动 fixture（解决超时和卡死问题）

@pytest.fixture(scope='function')
def driver():
    logger.info('Initializing WebDriver')
    driver = None
    try:
        driver = DriverFactory.get_driver()
        # 设置超时时间，防止无限等待
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.implicitly_wait(config.get('timeout'))

        base_url = config.get('base_url')
        driver.get(base_url)
        logger.info(f'Successfully navigated to base URL: {base_url}')

        yield driver

    except Exception as e:
        logger.error(f'初始化浏览器失败: {str(e)}')
        raise

    finally:
        if driver:
            logger.info('Quitting WebDriver')
            driver.quit()

###  11.失败自动截图

##  做什么
# 利用pytest的钩子pytest_runtest_makereport,在测试失败时自动截图保存

##  为什么这么做
# UI测试失败时，一张截图往往比日志更能直接反映问题
# 全自动触发，不需要在每个用例里写try...except

##  作用
# 提升失败分析的效率，尤其在批量回归时


#  2.失败自动截图钩子（嵌入allure报告）

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 仅在用例执行失败时截图
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                # 1.定义截图目录
                screenshot_dir = Path('reports/screenshots')
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                # 2.定义时间戳和文件名  生成文件名：用例名 + 时间戳
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                file_name = f'{item.name}_{timestamp}.png'
                file_path = screenshot_dir / file_name

                # 3.保存截图到本地
                driver.save_screenshot(str(file_path))
                logger.error(f'用例失败，截图已保存: {file_path}')

                # 4.将截图嵌入allure报告
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f'失败截图_{item.name}',
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                logger.error(f'截图保存失败: {str(e)}')












