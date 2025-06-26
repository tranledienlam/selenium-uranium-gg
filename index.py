
import argparse
import time
import math
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility
from googl import Setup as GoogleSetup, Auto as GoogleAuto

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        self.google_setup = GoogleSetup(node, profile)
        
    def _run(self):
        self.google_setup._run()
        self.node.new_tab('https://www.geturanium.io?ref=0x7f9d6a031e669c59d31b4ead83abd5507b036085', method="get")

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.profile_name = profile.get('profile_name')
        self.email = profile.get('email')
        self.password = profile.get('password')
        self.google_auto = GoogleAuto(node, profile)

    def is_popup(self):
        if not self.node.find(By.XPATH, '//h2[contains(text(), "Welcome to Uranium Miner!")]'):
            return False
        else:
            if not self.node.find_and_click(By.XPATH, '//div[span[contains(text(), "Terms & Conditions")]]/div'):
                self.node.log('Không tìm thấy Terms & Conditions')
            self.node.find_and_click(By.XPATH, '//button[contains(text(), "Next")]')

        if not self.node.find(By.XPATH, '//h2[contains(text(), "How to Play")]'):
            return False
        else:
            self.node.find_and_click(By.XPATH, '//button[contains(text(), "Next")]')

        if not self.node.find(By.XPATH, '//h2[contains(text(), "Create Your Game Account")]'):
            return False
        else:
            self.node.find_and_click(By.XPATH, '//button[contains(text(), "Connect")]')
            self.node.find_and_click(By.CSS_SELECTOR, '[aria-label*="google"]')
            self.node.find_and_click(By.CSS_SELECTOR, f'[data-email="{self.email}"]')

    def is_login(self):
        text_el = self.node.get_text(By.CSS_SELECTOR, '[class="relative"]', wait=10)
        if text_el:
            parts = text_el.split('/')
            if len(parts) >= 2:
                try:
                    number = int(parts[0])
                    if number > 0:
                        self.node.log(f'Đăng nhập thành công. exp: {number}')
                        return True
                    else:
                        self.node.log('Chưa đăng nhập')
                        return False
                except Exception as e:
                    self.node.log(f'Lỗi chuyển đổi chuỗi exp thành số: {e}')
        else:
            self.node.snapshot('CSS_SELECTOR [class="relative"] xác nhận đăng nhập đã thay đổi')

    def shards_get(self):
        text = self.node.get_text(By.XPATH, '//div[div[div[@class="relative"]]]//span')
        shards = None
        try:
            if text and ',' in text:
                shards = int(text.replace(',',''))
            elif text and '.' in text:
                shards = int(text.replace('.',''))
            elif text:
                shards = int(text)
        except Exception as e:
            self.node.log(f'Lỗi chuyển đổi chuỗi shards thành số: {e}')
        return shards

    def earn_button(self):
        buttons = self.node.find_all(By.TAG_NAME, 'button', timeout=20)
        button_earn = None
        for button in buttons:
            if 'Start Refining'.lower() in button.text.lower():
                button_earn = button
        return button_earn

    def earn_click(self):
        self.node.find_and_click(By.XPATH, '//span[contains(text(), "Earn")]')

        button_earn = self.earn_button()
        if button_earn:
            self.node.scroll_to(button_earn)
            self.node.click(button_earn)
            if self.earn_button():
                self.node.snapshot(f'Click earn thất bại', False)
                return False
            else:
                self.node.snapshot(f"Đã bắt đầu earn", False)
                return True
        else:
            el_text = self.node.get_text(By.XPATH, '//div[div[contains(text(), "remaining")]]')
            # match = re.search(r"(\d{2})\s*hr.*?(\d{2})\s*min.*?(\d{2})\s*sec", el_text)
            if el_text:
                parts = el_text.split('\n')
                try:
                    hours = parts[1]
                    minutes = parts[4]
                    seconds = parts[7]
                    self.node.snapshot(f"Quay lại earn sau {hours}:{minutes}:{seconds}", False)
                    return True
                except IndexError:
                    self.node.snapshot(f"Không kiểm tra được còn bao lâu. Chuỗi không đúng định dạng.", False)
            return False

    def mine(self):
        booster_buttons = []
        is_mine = False
        self.node.find_and_click(By.XPATH, '//span[contains(text(), "Mine")]')
        buttons = self.node.find_all(By.TAG_NAME, 'button')
        for button in buttons:
            if button.is_enabled():
                if "Auto Collector".lower() in button.text.lower():
                    booster_buttons.append(button)
                elif "Shard Multiplier".lower() in button.text.lower():
                    booster_buttons.append(button)
                elif "Conveyor Booster".lower() in button.text.lower():
                    booster_buttons.append(button)
            
        for button in booster_buttons:
            if self.node.click(button):
                is_mine = True

        return is_mine
    
    def upgrade(self):
        self.node.find_and_click(By.XPATH, '//span[contains(text(), "Upgrades")]', timeout=15)
        upgrade_buttons = self.node.find_all(By.XPATH, '//button[contains(text(),"Upgrade")]')

        if upgrade_buttons:
            self.node.scroll_to(upgrade_buttons[0])
            for button in upgrade_buttons:
                self.node.click(button)
            return True
        else:
            return False
        
    def _run(self):
        jobs = []
        self.google_auto._run()
        self.node.new_tab('https://www.geturanium.io?ref=0x7f9d6a031e669c59d31b4ead83abd5507b036085', method="get")
        
        #connect
        self.is_popup()
        if not self.node.wait_for_disappear(By.XPATH, '//p[contains(text(), "Connecting...")]'):
            self.node.snapshot(f'Bị lỗi mạng')
        if not self.is_login():
            self.node.log('Đăng nhập thất bại')
            return
        
        #earn
        shards = self.shards_get()
        if shards and shards > 135000:
            self.node.log(f"Đủ trên 100k để Earn")
            if self.earn_click():
                jobs.append('earn')
        
        #mine
        shards = self.shards_get()
        if shards and shards < 15000:
            self.node.snapshot(f'Cần click tay để kiếm thêm shards')
        
        time_end = time.time() + 630
        while time_end - time.time() > 0:
            if self.mine():
                if "mine" not in jobs:
                    jobs.append("mine")
            Utility.wait_time(15)

        #upgrade
        shards = self.shards_get()
        if shards and math.modf(shards / 100000)[0] > 15000:
            while True:
                if self.upgrade():
                    if "upgrade" not in jobs:
                        jobs.append("upgrade")
                else:
                    break
        self.node.snapshot(f'Hoàn thành công việc {jobs}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.read_data('profile_name', 'email', 'password')
    if not profiles:
        print("Không có dữ liệu để chạy")
        exit()

    browser_manager = BrowserManager(AutoHandlerClass=Auto, SetupHandlerClass=Setup)
    
    browser_manager.run_terminal(
        profiles=profiles,
        max_concurrent_profiles=4,
        block_media=False,
        auto=args.auto,
        headless=args.headless,
        disable_gpu=args.disable_gpu,
    )