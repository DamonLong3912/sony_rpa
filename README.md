# Playwright 浏览器自动化示例

这是一个使用 Playwright 进行浏览器自动化的简单示例项目。

## 环境准备

1. 确保已安装 Python 3.7 或更高版本
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 安装 Playwright 浏览器：
   ```bash
   playwright install
   ```

## 运行示例

执行以下命令运行示例脚本：
```bash
python browser_demo.py
```

## 功能说明

示例脚本将会：
1. 打开一个 Chromium 浏览器
2. 访问百度首页
3. 在搜索框中输入"Playwright 自动化测试"
4. 点击搜索按钮
5. 等待搜索结果加载完成
6. 保存搜索结果截图
7. 等待 3 秒后自动关闭浏览器 