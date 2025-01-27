import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 初始化浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，适用于没有GUI的环境
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 访问网页
url = 'https://www.53ai.com/news/LargeLanguageModel/2024073097084.html'  # 替换成你需要访问的网页
url = 'https://awtmt.com/articles/3740087'
url = 'https://blog.csdn.net/u011511601/article/details/80628273'
url = 'https://mp.weixin.qq.com/s/lcROuJHOg-C3UkFHHv452Q'
driver.get(url)

# 等待页面加载
time.sleep(2)

# 获取整个页面的高度
page_height = driver.execute_script("return document.body.scrollHeight")
page_width = driver.execute_script("return document.body.scrollWidth")

# 尝试查找网页中的 <main> 部分
try:
    main_element = driver.find_element(By.TAG_NAME, 'main')  # 查找 <main> 标签
except:
    print("页面没有找到 <main> 标签，使用默认布局")
    main_element = None

if main_element:
    # 获取主体部分的位置和尺寸
    main_location = main_element.location
    main_size = main_element.size

    # 计算裁剪区域的左、上、右、下边界
    left = main_location['x']
    top = main_location['y']
    right = left + main_size['width']
    bottom = top + main_size['height']
else:
    # 如果页面没有 <main> 标签，默认裁剪页面的中间部分
    left = 0
    top = 100  # 假设页面顶部100px为导航栏
    right = page_width
    bottom = page_height - 100  # 假设页面底部100px为页脚

# 设置窗口大小为页面大小
driver.set_window_size(page_width, page_height)

# 截取整个页面的截图
driver.save_screenshot('full_page_screenshot.png')

# 打开截图并加载成图片对象
image = Image.open('full_page_screenshot.png')

# 裁剪截图为主体区域
cropped_image = image.crop((left, top, right, bottom))

# 保存裁剪后的图片
cropped_image.save('main_content_screenshot.png')

# 关闭浏览器
driver.quit()
