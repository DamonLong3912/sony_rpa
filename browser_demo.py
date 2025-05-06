import asyncio
import os
import sys
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

# 加载.env文件中的环境变量
load_dotenv()

# 获取应用程序的根目录
def get_application_path():
    """获取应用程序所在的目录路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe运行
        return os.path.dirname(sys.executable)
    else:
        # 如果是直接运行python脚本
        return os.path.dirname(os.path.abspath(__file__))

async def test():
    # 启动 playwright
    async with async_playwright() as p:
        # 获取浏览器路径配置
        browser_path = os.getenv('BROWSER_PATH')
        
        # 启动浏览器（这里使用 chromium）
        if browser_path and os.path.exists(browser_path):
            # 如果有配置浏览器路径且文件存在，则使用指定的浏览器
            browser = await p.chromium.launch(
                headless=False,  # headless=False 表示可以看到浏览器界面
                executable_path=browser_path
            )
            print(f"使用配置的浏览器路径: {browser_path}")
        else:
            # 否则使用内置浏览器
            browser = await p.chromium.launch(headless=False)
            print("使用Playwright内置浏览器")
        
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
        
        # 等待搜索结果表格出现并点击第一个链接
        await page.wait_for_selector('table.searchResults')
        first_link = await page.query_selector('table.searchResults a')
        if first_link:
            await first_link.click()
            print("点击了搜索结果中的第一个链接")
        else:
            print("未找到搜索结果中的链接")
        
        # 等待3秒后关闭浏览器
        await asyncio.sleep(3)
        await browser.close()

async def access_sony_dra():
    # 启动 playwright
    async with async_playwright() as p:
        # 获取浏览器路径配置
        browser_path = os.getenv('BROWSER_PATH')
        
        # 启动浏览器（这里使用 chromium）
        if browser_path and os.path.exists(browser_path):
            # 如果有配置浏览器路径且文件存在，则使用指定的浏览器
            browser = await p.chromium.launch(
                headless=False,  # headless=False 表示可以看到浏览器界面
                executable_path=browser_path
            )
            print(f"使用配置的浏览器路径: {browser_path}")
        else:
            # 否则使用内置浏览器
            browser = await p.chromium.launch(headless=False)
            print("使用Playwright内置浏览器")
        
        # 创建新页面
        page = await browser.new_page()

        # 设置cookies
        cookies = [
            {
                'name': 'JSESSIONID',
                'value': os.getenv('JSESSIONID', ''),  # 从环境变量获取JSESSIONID
                'domain': 'dra2.medigitalapps.com',
                'path': '/'
            },
            {
                'name': 'user',
                'value': os.getenv('USER', ''),  # 从环境变量获取user cookie
                'domain': 'dra2.medigitalapps.com',
                'path': '/'
            }
        ]
        await page.context.add_cookies(cookies)
        print("已设置cookies")
        
        # 访问Sony DRA网站
        await page.goto('https://dra2.medigitalapps.com/dra/home.do')
        print("成功访问Sony DRA网站")
        
        # 等待name=criteria的输入框出现
        await page.wait_for_selector('input[name="criteria"]',timeout=120000)
        print("输入框已加载")
        
        # 在搜索框中输入文字
        await page.fill('input[name="criteria"]', 'G0100047358250')
        print("输入搜索关键词")
        
        # 在下拉框中选择raasProductId选项
        await page.select_option('select[name="searchMethod"]', 'raasProductId')
        print("选择下拉框选项raasProductId")
        
        # 点击type=submit, name=searchButton的提交按钮
        await page.click('input[type="submit"][name="searchButton"]')
        print("点击搜索按钮")
        
        # 等待搜索结果加载
        await page.wait_for_load_state('networkidle')
        
        # 等待搜索结果表格出现并点击第一个链接
        await page.wait_for_selector('table.searchResults')
        first_link = await page.query_selector('table.searchResults a')
        if first_link:
            await first_link.click()
            print("点击了搜索结果中的第一个链接")
        else:
            print("未找到搜索结果中的链接")
        
        # 无限等待，保持浏览器窗口打开
        await asyncio.Event().wait()

async def process_product(page, product_id):
    """处理单个产品ID的搜索"""
    # 等待name=criteria的输入框出现
    await page.wait_for_selector('input[name="criteria"]',timeout=120000)
    print(f"开始处理产品ID: {product_id}")
    
    # 清空搜索框并输入新的产品ID
    await page.fill('input[name="criteria"]', '')
    await page.fill('input[name="criteria"]', product_id)
    
    # 在下拉框中选择raasProductId选项
    await page.select_option('select[name="searchMethod"]', 'raasProductId')
    
    # 点击搜索按钮
    await page.click('input[type="submit"][name="searchButton"]')
    
    # 等待搜索结果加载
    await page.wait_for_load_state('networkidle')
    
    # 等待搜索结果表格出现并点击第一个链接
    try:
        await page.wait_for_selector('table.searchResults', timeout=10000)
        first_link = await page.query_selector('table.searchResults a')
        if first_link:
            await first_link.click()
            print(f"成功点击产品 {product_id} 的搜索结果链接")
            return True
        else:
            print(f"未找到产品 {product_id} 的搜索结果链接")
            return False
    except:
        print(f"处理产品 {product_id} 时发生错误")
        return False

async def process_excel():
    # 读取Excel文件
    try:
        # 获取Excel文件的完整路径
        app_path = get_application_path()
        excel_path = os.path.join(app_path, 'SONY_DRA.xlsx')
        
        if not os.path.exists(excel_path):
            print(f"错误：找不到Excel文件，请确保 SONY_DRA.xlsx 文件位于以下目录：\n{app_path}")
            return
            
        df = pd.read_excel(excel_path)
        # 找出完成时间为空的记录
        unfinished_products = df[df['完成时间'].isna()]
        
        if len(unfinished_products) == 0:
            print("没有需要处理的未完成数据")
            return
            
        print(f"共有 {len(unfinished_products)} 条数据需要处理")
        
        # 启动浏览器并处理每条记录
        async with async_playwright() as p:
            browser_path = os.getenv('BROWSER_PATH')
            
            if browser_path and os.path.exists(browser_path):
                browser = await p.chromium.launch(
                    headless=False,
                    executable_path=browser_path
                )
                print(f"使用配置的浏览器路径: {browser_path}")
            else:
                browser = await p.chromium.launch(headless=False)
                print("使用Playwright内置浏览器")
            
            page = await browser.new_page()
            
            # 设置cookies
            cookies = [
                {
                    'name': 'JSESSIONID',
                    'value': os.getenv('JSESSIONID', ''),
                    'domain': 'dra2.medigitalapps.com',
                    'path': '/'
                },
                {
                    'name': 'user',
                    'value': os.getenv('USER', ''),
                    'domain': 'dra2.medigitalapps.com',
                    'path': '/'
                }
            ]
            await page.context.add_cookies(cookies)
            
            # 访问Sony DRA网站
            await page.goto('https://dra2.medigitalapps.com/dra/home.do')
            print("成功访问Sony DRA网站")
            
            # 处理每个未完成的产品
            for index, row in unfinished_products.iterrows():
                product_id = row['Product ID']
                success = await process_product(page, product_id)
                if success:
                    # 更新Excel中的完成时间
                    df.at[index, '完成时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # 保存更新后的Excel
                    df.to_excel(excel_path, index=False)
                    print(f"已更新产品 {product_id} 的完成时间")
                
                # 等待一段时间再处理下一个
                await asyncio.sleep(2)
            
            # 完成后保持浏览器窗口打开
            await asyncio.Event().wait()
            
    except Exception as e:
        print(f"处理Excel文件时发生错误: {str(e)}")
        print(f"请确保Excel文件位于以下目录：\n{app_path}")

if __name__ == '__main__':
    # asyncio.run(test())
    # asyncio.run(access_sony_dra())
    asyncio.run(process_excel()) 