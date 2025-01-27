import pickle
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

class ShoppingBot:
    def __init__(self):
        self.driver = self.setup_driver()

    def setup_driver(self):
        """
        配置并启动 Chrome 浏览器驱动
        :return: 浏览器驱动实例
        """
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 无头模式，适用于没有GUI的环境
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def load_shopping_agents(self):
        """
        加载保存的 shopping_agents 并刷新页面使 shopping_agents 生效
        """
        try:
            with open("shopping_agents.pkl", "rb") as f:
                shopping_agents = pickle.load(f)
                for shopping_agent in shopping_agents:
                    self.driver.add_shopping_agent(shopping_agent)
        except FileNotFoundError:
            print("未找到保存的 shopping_agents，请先登录并保存 cookies。")
            self.driver.quit()
        self.driver.refresh()
        time.sleep(2)

    def search_product(self, keyword):
        """
        在搜索框中输入关键词并进行搜索
        :param keyword: 搜索关键词
        """
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.doubleCardWrapperAdapt--mEcC7olq')))
        sleep(3)

    def collect_product(self):
        """
        将商品收藏
        """
        collect_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'collectBtn'))
        )
        # 使用 ActionChains 模拟鼠标点击
        actions = ActionChains(self.driver)
        actions.move_to_element(collect_button).click().perform()

    def add_product_to_cart(self):
        """
        将商品加入购物车中
        """
        add_cart_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-usage="/pc-tb.pc-tb-detail2.addCartClick"]')
        add_cart_button.click()

    def choose_product(self):
        """
        点击搜索结果中的第一个商品链接
        """
        item_link = self.driver.find_element(By.CSS_SELECTOR, 'a.doubleCardWrapperAdapt--mEcC7olq')
        current_window = self.driver.current_window_handle
        # 点击链接，打开新标签页
        item_link.click()
        self.driver.implicitly_wait(2)
        all_windows = self.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                break

    def shopping(self, item):
        self.driver.get("https://world.taobao.com")
        self.load_cookies()
        self.search_product(item)
        self.choose_product()
        try:
            # self.collect_product()
            # sleep(2)
            self.add_product_to_cart()
            sleep(2)
        except Exception as e:
            self.driver.save_screenshot('error_screenshot.png')
            # import traceback
            # traceback.print_exc()
        finally:
            self.driver.quit()

def main():
    item = "请帮我购买一个红色的iphone16"
    bot = ShoppingBot()
    bot.shopping(item)

if __name__ == "__main__":
    main()