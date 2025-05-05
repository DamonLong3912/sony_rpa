import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    # 创建一个测试文件
    test_file_path = os.path.join(os.getcwd(), 'test_upload.txt')
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write('这是一个测试上传的文件内容')
    
    print(f"已创建测试文件: {test_file_path}")

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 访问文件上传测试网站
        await page.goto('https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_fileupload_get')
        print("已打开测试网站")

        # 切换到包含上传控件的 iframe
        frame = page.frame_locator('#iframeResult')

        # 上传文件
        # 注意：set_input_files 方法会自动处理文件选择对话框
        await frame.locator('#myFile').set_input_files(test_file_path)
        print("已选择要上传的文件")

        # 等待一会儿以便查看结果
        await asyncio.sleep(3)

        # 获取上传的文件名（在这个示例网站中可以看到）
        file_name = await frame.locator('#myFile').input_value()
        print(f"上传的文件名: {file_name}")

        # 清理测试文件
        os.remove(test_file_path)
        print("已清理测试文件")

        # 关闭浏览器
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main()) 