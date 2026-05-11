
###  商品列表页  ###

##  编写具体页面对象

#  做什么 2.
# 针对被测网站的页面，封装元素定位和业务操作

###  为什么这么做
#  页面元素和操作集中管理，当UI变懂事只需修改对应页面的定位符
#  测试用例只关心“做什么”，不关心“怎么找到这个按钮”

## 作用
#  构建业务层抽象，让测试用例想操作真是页面一样调用login（）、get_page_title()

#class InventoryPage(BasePage):
 #   TITLE = (By.CLASS_NAME,'title')
  #  def get_page_title(self):
   #     return self.get_text(self.TITLE)

import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class InventoryPage(BasePage):
    """商品列表页面（Inventory Page）"""

    # ----- 元素定位 -----
    PAGE_TITLE = (By.CLASS_NAME, 'title')  # 页面标题
    INVENTORY_ITEMS = (By.CLASS_NAME, 'inventory_item')  # 所有商品项
    ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')  # 商品名称
    ITEM_PRICE = (By.CLASS_NAME, 'inventory_item_price')  # 商品价格
    SHOPPING_CART_LINK = (By.CLASS_NAME, 'shopping_cart_link')  # 购物车图标
    SHOPPING_CART_BADGE = (By.CLASS_NAME, 'shopping_cart_badge')  # 购物车数量徽章

    # ----- 页面操作方法 -----
    def is_inventory_page(self) -> bool:
        """验证当前是否是商品列表页面"""
        try:
            title_element = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
            return title_element.text == "Products"
        except TimeoutException:
            return False

    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.get_text(self.PAGE_TITLE)

    def get_all_item_names(self) -> list:
        """获取所有商品的名称列表"""
        items = self.find_elements(self.ITEM_NAME)
        return [item.text for item in items]

    def get_item_price(self, item_name: str) -> float:
        """根据商品名称获取商品价格"""
        item_locator = (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']")
        item_element = self.find_element(item_locator)
        price_text = item_element.find_element(*self.ITEM_PRICE).text
        return float(price_text.replace('$', ''))

    def add_to_cart_by_name(self, item_name: str):
        """根据商品名称将商品添加到购物车（最终稳定版）"""
        logger.info(f"添加商品到购物车: {item_name}")
        # 1. 先把商品名转换成 kebab-case
        data_test_value = item_name.lower().replace(' ', '-')
        # 2. 直接匹配完整的 data-test 属性
        add_btn_locator = (
            By.XPATH,
            f"//button[@data-test='add-to-cart-{data_test_value}']"
        )
        self.click(add_btn_locator)

    def remove_from_cart_by_name(self, item_name: str):
        """根据商品名称从购物车移除商品"""
        logger.info(f"从购物车移除商品: {item_name}")
        data_test_value = item_name.lower().replace(' ', '-')
        remove_btn_locator = (
            By.XPATH,
            f"//button[@data-test='remove-{data_test_value}']"
        )
        self.click(remove_btn_locator)

    def get_cart_item_count(self) -> int:
        """获取购物车右上角的商品数量"""
        try:
            badge_element = self.find_element(self.SHOPPING_CART_BADGE)
            return int(badge_element.text)
        except Exception:
            return 0  # 如果购物车为空，返回0

    def click_shopping_cart(self):
        """点击购物车图标，进入购物车页面"""
        logger.info("点击购物车图标，进入购物车页面")
        self.click(self.SHOPPING_CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)







