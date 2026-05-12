import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


# 获取一个logger实例，用来记录测试过程中的信息
logger = logging.getLogger(__name__)

class CartPage(BasePage):
    #-----元素定位器（Page Locators）-----
    PAGE_TITLE = (By.CLASS_NAME, 'title')     # 页面标题
    CART_ITEMS = (By.CLASS_NAME, 'cart_item')  # 所有商品项目的列表

    # 单个商品项目内部元素的定位方式，基于商品项来查找
    ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')  # 商品名称
    ITEM_DESC = (By.CLASS_NAME, 'inventory_item_desc')  # 商品描述
    ITEM_PRICE = (By.CLASS_NAME, 'inventory_item_price') # 商品价格
    ITEM_QUANTITY_SELECT = (By.TAG_NAME, 'select')  # 数量选择下拉框
    ITEM_REMOVE_BTN = (By.XPATH, "//button[text()='Remove']")  # 商品的"Remove"按钮

    # 页面操作元素
    CHECKOUT_BTN = (By.ID, 'checkout')  # 修正：ID大小写错误
    CONTINUE_SHOPPING_BTN = (By.ID, 'continue-shopping') # 修正：删除重复定义和拼写错误

    #------页面方法------
    def is_cart_page(self) -> bool:
        """
        验证当前是否是购物车页面
        捕获页面加载超时、元素不存在等异常
        """
        try:
            # 等待页面标题元素出现，并检查其文本是否为 "Your Cart"
            title_element = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
            return title_element.text == "Your Cart"
        except TimeoutException:  # 修正：捕获具体的 超时异常
            return False

    def get_cart_items_count(self) -> int:
        """
        获取购物车中的商品个数
        """
        # 等待至少一个商品项存在，或直接找所有商品项，如果找不到则返回空列表
        try:
            items = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
            return len(items)
        except TimeoutException:
            import time
            time.sleep(2)
            try:
                items = self.driver.find_elements(*self.CART_ITEMS)
                return len(items)
            except:
                return 0

    def get_cart_item_name(self) -> list:
        """
        获取购物车中所有商品的名称，返回一个列表
        """
        # 为复用性，调用一个通用的内部方法_get_all_cart_items_info
        return [item_info['name'] for item_info in self._get_all_cart_items_info()]

    def get_cart_item_descriptions(self) -> list:
        """
        获取购物车中所有商品的描述，返回一个列表
        """
        return [item_info['desc'] for item_info in self._get_all_cart_items_info()]

    def get_cart_item_prices(self) -> list:
        """
        获取购物车中所有商品的价格（转换为浮点数），返回一个列表
        """
        return [item_info['price'] for item_info in self._get_all_cart_items_info()]

    def get_cart_item_info(self) -> list:
        """
        返回购物车中所有商品的完整信息（描述、价格、数量、移除按钮），以字典列表形式
        """
        return self._get_all_cart_items_info()

    def update_item_quantity(self, item_index: int, quantity: int):
        """
        修改指定位置（索引）商品的数量
        """
        cart_items = self.find_elements(self.CART_ITEMS)
        if item_index < len(cart_items):
            try:
                quantity_select = cart_items[item_index].find_element(*self.ITEM_QUANTITY_SELECT)
                quantity_select.find_elements(By.TAG_NAME, 'option')[quantity-1].click()
                logger.info(f'Updated quantity for item {item_index+1} to {quantity}.')
            except Exception as e:
                logger.warning(f'修改商品数量失败，SauceDemo 不支持此操作:{str(e)}')
        else:
            logger.error('Item index out of range.')

    def remove_item(self, item_index: int):
        """
        从购物车中移除指定位置（索引）的商品
        """
        cart_items = self.find_elements(self.CART_ITEMS)
        if item_index < len(cart_items):
            # 修正：复用已经定义的ITEM_REMOVE_BTN，不用硬编码
            remove_btn = cart_items[item_index].find_element(*self.ITEM_REMOVE_BTN)
            remove_btn.click()
            logger.info(f'Removed item {item_index+1} from cart.')
        else:
            logger.error('Item index out of range.')

    def click_checkout(self):
        """
        点击结算按钮，跳转到结算信息填写页面
        """
        logger.info(f"点击结算按钮")
        self.click(self.CHECKOUT_BTN)
        from pages.checkout_page import CheckoutPage # 延迟导入，避免循环依赖
        return CheckoutPage(self.driver)

    def click_continue_shopping(self):
        """
        点击继续购物按钮，返回商品列表页面
        """
        self.click(self.CONTINUE_SHOPPING_BTN)
        from pages.inventory_page import InventoryPage  # 延迟导入，避免循环依赖
        return InventoryPage(self.driver)

    #-------内部辅助方法--------
    def _get_all_cart_items_info(self) -> list[dict]:
        """
        内部方法：获取购物车中所有商品的完整信息
        """
        items_info = []
        cart_items = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))

        for item in cart_items:
            #  在每个商品项的上下文中查找子元素，并获取其文本
            name = item.find_element(*self.ITEM_NAME).text
            desc = item.find_element(*self.ITEM_DESC).text
            price_text = item.find_element(*self.ITEM_PRICE).text
            # 从 "$29.99" 这种格式的文本中提取数字部分，并转换为浮点数
            price = float(price_text.replace('$', ''))

            current_quantity = 1
            try:
                quantity_select = item.find_element(*self.ITEM_QUANTITY_SELECT)
                current_quantity = int(quantity_select.get_attribute('value'))
            except:
                pass

            #  检查移除按钮是否存在
            remove_btn_displayed = False
            try:
                remove_btn = item.find_element(*self.ITEM_REMOVE_BTN)
                remove_btn_displayed = remove_btn.is_displayed()
            except:
                pass

            items_info.append({
                'name': name,
                'desc': desc,
                'price': price,
                'quantity': current_quantity,
                'remove_btn': remove_btn_displayed
            })
        return items_info







