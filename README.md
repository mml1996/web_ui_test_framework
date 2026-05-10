# Web UI 自动化测试框架（Python + Selenium + Pytest + Allure）

> 基于 Python 的 Web UI 自动化测试项目，集成了 Selenium、Pytest 和 Allure 报告，支持参数化用例和持续集成。

---

## 📌 项目简介
本项目以 `https://www.saucedemo.com` 为被测站点，主要实现了以下功能：
- 核心登录模块的自动化测试
- 支持多组用户数据的参数化用例
- 自动生成可视化 Allure 测试报告
- 可接入 GitHub Actions 实现持续集成

---

## 🛠️ 技术栈
- **语言**：Python 3.11
- **自动化工具**：Selenium
- **测试框架**：Pytest
- **测试报告**：Allure-pytest
- **持续集成**：GitHub Actions（配置已就绪）

---

## 📊 Allure 测试报告效果

项目集成了 Allure 可视化测试报告，实现了用例的分层管理、参数化展示与完整执行记录：

### 用例分层与执行详情
![Allure 用例详情](./2231778414742_.pic.jpg)

### 参数化用例场景验证
![Allure 参数化用例](./2241778414775_.pic.jpg)

支持按 feature/story 分层展示用例
自动统计通过率、失败用例与执行时长

---

## 📁 项目结构
web_ui_test_framework/
├── config/          # 配置文件（环境、浏览器、路径等）
├── core/            # 核心封装（DriverFactory、基础页面对象）
├── tests/           # 测试用例
├── utils/           # 工具类（日志、文件处理等）
├── conftest.py      # pytest 全局配置
├── requirements.txt # 依赖清单
└── .github/workflows/
    └── ci.yml       # GitHub Actions CI 配置

---

## 🚀 本地运行
# 1. 安装依赖
pip install -r requirements.txt

# 2. 执行测试并生成 Allure 结果
pytest --alluredir=allure-results

# 3. 本地查看报告
allure serve allure-results
