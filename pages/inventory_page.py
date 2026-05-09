
###  商品列表页  ###

##  编写具体页面对象

#  做什么 2.
# 针对被测网站的页面，封装元素定位和业务操作

###  为什么这么做
#  页面元素和操作集中管理，当UI变懂事只需修改对应页面的定位符
#  测试用例只关心“做什么”，不关心“怎么找到这个按钮”

## 作用
#  构建业务层抽象，让测试用例想操作真是页面一样调用login（）、get_page_title()

from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME,'title')
    def get_page_title(self):
        return self.get_text(self.TITLE)







