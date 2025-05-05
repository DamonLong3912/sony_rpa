import asyncio
from playwright.async_api import async_playwright

async def main():
    # 启动 playwright
    async with async_playwright() as p:
        # 启动浏览器（这里使用 chromium）
        browser = await p.chromium.launch(headless=False)  # headless=False 表示可以看到浏览器界面
        
        # 创建新页面
        page = await browser.new_page()
        
        # 访问百度
        await page.goto('https://www.baidu.com')
        print("成功访问百度首页")
        
        # 在搜索框中输入文字
        await page.fill('#kw', '自动化测试')
        print("输入搜索关键词")
        
        # 点击搜索按钮
        await page.click('#su')
        print("点击搜索按钮")
        
        # 等待搜索结果加载
        await page.wait_for_load_state('networkidle')
        

        
        # 等待3秒后关闭浏览器
        await asyncio.sleep(3)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main()) 