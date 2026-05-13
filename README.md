# SauceDemo Web UI 自动化测试框架（Python + Selenium + Pytest + Allure）
企业级生产可用版本 | 全流程覆盖 | 开箱即用 | 所有用例 100% 通过
> 基于 Python 的 Web UI 自动化测试项目，集成了 Selenium、Pytest 和 Allure 报告，支持参数化用例和持续集成，完整覆盖 SauceDemo 电商网站核心业务流程，遵循 Page Object 设计模式，具备完善的日志、失败自动截图、可视化报告和异常处理能力。

---

## 📌 项目简介
本项目以官方演示站点 `https://www.saucedemo.com` 为被测对象，完整实现电商核心流程自动化回归测试：
- 多场景登录用例 + YAML 参数化数据驱动
- 商品列表浏览、加入购物车、移除商品
- 购物车数量校验、信息匹配、刷新数据持久化
- 继续购物、跳转结算页面全流程验证
- 全局智能显式等待，彻底解决本地/CI 网络加载超时
- 集成 `pytest-xdist` 并发执行，测试耗时从 10min 压缩至 2~4min
- 用例失败自动截图 + Loguru 完整日志记录
- Allure 高颜值可视化测试报告
- 内置 GitHub Actions 配置，提交代码自动并发跑测试

**当前状态：16 条测试用例本地、GitHub Actions 均 100% 稳定通过**

---

## 🛠️ 技术栈
- **开发语言**：Python 3.11+
- **UI 自动化**：Selenium
- **测试框架**：Pytest
- **并发加速**：pytest-xdist
- **可视化报告**：Allure-pytest
- **日志管理**：Loguru
- **数据驱动**：PyYAML
- **持续集成**：GitHub Actions
- **设计模式**：Page Object Model（PO）

---

## 📊 Allure 测试报告能力
- 按 Epic/Feature/Story 分层管理测试用例
- 自动统计通过率、执行时长、失败用例归类
- 失败用例自动嵌入截图、错误堆栈、完整运行日志
- 展示运行环境、浏览器、Python 版本信息
- 支持在线服务预览 & 静态 HTML 报告导出归档

---

## 📊 Allure 测试报告效果

项目集成了 Allure 可视化测试报告，实现了用例的分层管理、参数化展示与完整执行记录：
### 用例报告总览
![Allure 用例总览](/images/测试用例总览.jpg)

### 用例分层与执行详情
![Allure 用例详情](/images/用例分级与执行.jpg)

### 参数化用例场景验证
![Allure 参数化用例](/images/参数化用例.jpg)

## 🚀 核心功能（最新完整版）
### 1. 完整业务流程覆盖
- 用户登录（正常 / 异常 / 锁定用户 / 参数化）
- 商品列表浏览
- 添加商品到购物车
- 购物车商品数量、名称、价格校验
- 删除 / 清空购物车
- 购物车数据刷新持久化
- 继续购物、去结算
### 2. 超高稳定性（解决 CI 超时问题）
- 全流程 显式等待
- 页面跳转强制等待 URL 匹配
- 添加商品后强制等待购物车数量更新
- 彻底解决 GitHub 网络慢导致的用例失败
### 3. 并发执行（速度提升 3~5 倍）
- 支持 pytest-xdist 多进程并发
- 本地：10 分钟 → 1 分钟内
- GitHub CI：10 分钟 → 2~4 分钟
### 4. 自动化报告与异常捕获
- Allure 可视化报告
- 用例失败自动截图
- 完整运行日志
- 报告包含截图、堆栈、执行时间、用例分级
### 5. 开箱即用 CI/CD
- 提交代码自动触发测试
- GitHub Actions 并发执行
- 环境自动配置、依赖自动安装
- 稳定不随机失败

## 报告核心能力：
  按 Epic/Feature/Story/Title 四层结构展示用例
  自动统计通过率、失败用例、执行时长与历史趋势
  失败用例自动关联截图、错误堆栈与完整执行日志
  展示运行环境信息（浏览器版本、系统、Python 版本）
  支持导出静态 HTML 报告，便于归档与分享

---

## 📁 项目结构
web_ui_test_framework/
#### ├── pages/                  # 页面对象层（Page Object）
#### │   ├── base_page.py        # 基础页面类，封装所有通用Selenium操作
#### │   ├── login_page.py       # 登录页面元素与业务方法
#### │   ├── inventory_page.py   # 商品列表页面元素与业务方法
#### │   ├── cart_page.py        # 购物车页面元素与业务方法
#### │   └── checkout_page.py    # 结算流程页面元素与业务方法
#### ├── tests/                  # 测试用例层
#### │   ├── test_login.py       # 登录模块测试用例
#### │   ├── test_cart_page.py   # 购物车模块测试用例
#### │   └── test_checkout_page.py # 结算模块测试用例
#### ├── data/                   # 测试数据层
#### │   └── login_data.yaml     # 登录模块参数化测试数据
#### ├── utils/                  # 公共工具层
#### │   ├── logger.py           # 全局日志配置
#### │   └── file_utils.py       # 文件处理工具
#### ├── reports/                # 测试报告输出目录
#### │   ├── screenshots/        # 失败用例自动截图
#### │   └── logs/               # 运行日志文件
#### ├── .github/workflows/
#### │   └── ci.yml              # GitHub Actions 自动执行配置
#### ├── conftest.py             # Pytest 全局配置与Fixture
#### ├── pytest.ini              # Pytest 运行参数配置
#### ├── requirements.txt        # 项目依赖清单
#### └── README.md               # 项目说明文档


---

## 🚀 本地环境部署 & 运行
  ### 1. 克隆项目
    git clone https://github.com/mml1996/web_ui_test_framework.git
    cd web_ui_test_framework
  ### 2. 安装依赖
    pip install -r requirements.txt
  ### 3. 常用执行命令
    ## 1. 普通串行执行所有用例
       pytest tests/ -v
  
    ## 2. 并发执行（推荐，速度提升3~5倍）
       pytest tests/ -v -n auto

    ## 3. 生成 Allure 报告数据
       pytest tests/ -v -n auto --alluredir=reports/allure-results

    ## 4. 本地自动打开 Allure 报告
       allure serve reports/allure-results

    ## 5. 仅执行单个模块
       pytest tests/test_login.py -v
       pytest tests/test_cart_page.py -v

---

## 🏗️ 框架核心亮点 & 稳定性优化

### 1. 标准 PO 设计模式
页面元素定位与测试业务逻辑完全分离，新增 / 维护用例无需改动底层元素封装。
### 2. 全链路智能等待
摒弃强制 time.sleep()，统一封装显式等待：
等待元素存在、可见、可点击
页面跳转强制等待 URL 加载完成
购物车加购后强制等待徽章数字变为 2，彻底解决 GitHub CI 网络延迟导致购物车为空、断言失败问题
### 3. 并发执行能力
集成 pytest-xdist，支持多进程并行执行：
本地：10 分钟 → 1 分钟左右
GitHub Actions：10 分钟 → 2~4 分钟
Fixture 为 function 级别，天然兼容多进程并发无冲突
### 4. 完善异常机制
用例执行失败自动截图保存至 reports/screenshots
Loguru 分级日志，控制台 + 文件双输出
全局浏览器生命周期管理，执行完毕自动关闭驱动，无残留进程
### 5. 数据驱动测试
基于 YAML 外部文件管理测试数据，参数化用例易维护、易扩展。

---

## 🔄 GitHub Actions 持续集成
项目已内置 .github/workflows/UI Test CI.yml，已配置并发执行：
每次推送代码自动触发 CI 流程
自动搭建 Python 环境、安装所有依赖
自动以 pytest tests/ -v -n auto 并发执行测试
保留运行日志与失败截图记录
无需额外配置，开箱即用
每次提交代码后，可在仓库的 Actions 页面查看执行结果和报告链接。
