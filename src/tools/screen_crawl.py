from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import sleep
from webdriver_manager.chrome import ChromeDriverManager

# 初始化浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，适用于没有GUI的环境
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 访问网页
url = 'https://www.53ai.com/news/LargeLanguageModel/2024073097084.html'  # 替换成你需要访问的网页
url = 'https://mp.weixin.qq.com/s/lcROuJHOg-C3UkFHHv452Q'
driver.get(url)

# 等待页面加载
time.sleep(2)

# 获取网页的总高度
page_height = driver.execute_script("return document.body.scrollHeight")

# 设置一个空的列表，用于保存截图
screenshots = []

# 滚动并截取屏幕
scroll_position = 0
while scroll_position < page_height:
    # 滚动页面
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")

    # 等待页面加载
    time.sleep(1)

    # 截取当前视口截图并保存
    screenshot_filename = f"screenshot_{scroll_position}.png"
    driver.save_screenshot(screenshot_filename)
    screenshots.append(screenshot_filename)

    # 更新滚动位置
    scroll_position += driver.execute_script("return window.innerHeight")

# 合并所有截图为一张完整的图片
images = [Image.open(screenshot) for screenshot in screenshots]
total_width = max(image.width for image in images)
total_height = sum(image.height for image in images)
full_image = Image.new('RGB', (total_width, total_height))

y_offset = 0
for image in images:
    full_image.paste(image, (0, y_offset))
    y_offset += image.height

full_image.save('full_page_screenshot.png')

# 关闭浏览器
driver.quit()
