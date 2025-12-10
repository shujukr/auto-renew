"""
GitHub Actions 自动续期脚本
"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime

def setup_driver():
    """配置 Chrome 浏览器"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def add_cookies(driver, cookie_string):
    """添加 Cookie 到浏览器"""
    if not cookie_string:
        return False
    
    try:
        # 先访问域名以设置 Cookie
        driver.get("https://dashboard.katabump.com")
        time.sleep(2)
        
        # 解析并添加 Cookie
        cookies = cookie_string.split(';')
        for cookie in cookies:
            cookie = cookie.strip()
            if '=' in cookie:
                name, value = cookie.split('=', 1)
                driver.add_cookie({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': 'dashboard.katabump.com'
                })
        
        print(f"✓ 已添加 {len(cookies)} 个 Cookie")
        return True
    except Exception as e:
        print(f"❌ 添加 Cookie 失败: {e}")
        return False

def login(driver, username, password):
    """登录网站"""
    if not username or not password:
        print("⚠️  未提供登录凭证")
        return False
    
    try:
        # 等待登录表单加载
        wait = WebDriverWait(driver, 10)
        
        # 尝试常见的登录表单选择器
        username_selectors = [
            (By.ID, "username"),
            (By.NAME, "username"),
            (By.ID, "email"),
            (By.NAME, "email"),
            (By.XPATH, "//input[@type='text' or @type='email']")
        ]
        
        password_selectors = [
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.XPATH, "//input[@type='password']")
        ]
        
        login_button_selectors = [
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Login')]"),
            (By.XPATH, "//input[@type='submit']")
        ]
        
        # 查找并填写用户名
        username_field = None
        for by, selector in username_selectors:
            try:
                username_field = wait.until(EC.presence_of_element_located((by, selector)))
                break
            except:
                continue
        
        if not username_field:
            print("❌ 未找到用户名输入框")
            return False
        
        username_field.clear()
        username_field.send_keys(username)
        print("✓ 已填写用户名")
        
        # 查找并填写密码
        password_field = None
        for by, selector in password_selectors:
            try:
                password_field = driver.find_element(by, selector)
                break
            except:
                continue
        
        if not password_field:
            print("❌ 未找到密码输入框")
            return False
        
        password_field.clear()
        password_field.send_keys(password)
        print("✓ 已填写密码")
        
        # 查找并点击登录按钮
        login_button = None
        for by, selector in login_button_selectors:
            try:
                login_button = driver.find_element(by, selector)
                break
            except:
                continue
        
        if login_button:
            login_button.click()
            print("✓ 已点击登录按钮")
            time.sleep(5)  # 等待登录完成
            return True
        else:
            print("❌ 未找到登录按钮")
            return False
            
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return False

def click_renew(driver):
    """点击续期按钮"""
    try:
        wait = WebDriverWait(driver, 15)
        
        # 多种可能的 Renew 按钮选择器
        renew_selectors = [
            (By.XPATH, "//button[contains(translate(., 'RENEW', 'renew'), 'renew')]"),
            (By.XPATH, "//a[contains(translate(., 'RENEW', 'renew'), 'renew')]"),
            (By.XPATH, "//input[@value='Renew' or @value='renew']"),
            (By.ID, "renew"),
            (By.ID, "renewButton"),
            (By.CLASS_NAME, "renew-button"),
            (By.CLASS_NAME, "btn-renew"),
        ]
        
        button = None
        for by, selector in renew_selectors:
            try:
                button = wait.until(EC.element_to_be_clickable((by, selector)))
                print(f"✓ 找到 Renew 按钮: {selector}")
                break
            except:
                continue
        
        if button:
            # 滚动到按钮位置
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            
            # 尝试点击
            try:
                button.click()
            except:
                # 如果普通点击失败，使用 JavaScript 点击
                driver.execute_script("arguments[0].click();", button)
            
            print("✓ 成功点击 Renew 按钮")
            time.sleep(3)
            return True
        else:
            print("❌ 未找到 Renew 按钮")
            return False
            
    except Exception as e:
        print(f"❌ 点击失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print(f"开始执行续期任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 从环境变量获取配置
    url = os.getenv('RENEW_URL', 'https://dashboard.katabump.com/servers/edit?id=166361&renew=success')
    cookies = os.getenv('COOKIES')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    
    driver = None
    success = False
    
    try:
        # 设置浏览器
        print("\n1️⃣  正在启动浏览器...")
        driver = setup_driver()
        print("✓ 浏览器启动成功")
        
        # 优先使用 Cookie 方式
        if cookies:
            print("\n2️⃣  使用 Cookie 登录方式")
            add_cookies(driver, cookies)
            
            # 访问页面
            print(f"正在访问: {url}")
            driver.get(url)
            time.sleep(3)
        else:
            # 访问页面
            print(f"\n2️⃣  正在访问: {url}")
            driver.get(url)
            time.sleep(3)
            
            # 检查是否需要登录
            print("\n3️⃣  检查登录状态...")
            if "login" in driver.current_url.lower() or driver.find_elements(By.XPATH, "//input[@type='password']"):
                print("需要使用用户名密码登录")
                login_success = login(driver, username, password)
                
                if login_success:
                    driver.save_screenshot(f"step2_logged_in_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    print("✓ 登录成功")
                    
                    # 登录后重新访问续期页面
                    driver.get(url)
                    time.sleep(3)
                else:
                    print("❌ 登录失败，尝试继续...")
            else:
                print("✓ 无需登录或已通过 Cookie 登录")
        
        # 保存初始截图
        driver.save_screenshot(f"step1_initial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        print("✓ 已保存初始截图")
        
        # 点击续期按钮
        print("\n4️⃣  正在查找并点击 Renew 按钮...")
        success = click_renew(driver)
        
        # 保存最终截图
        driver.save_screenshot(f"step3_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        print("✓ 已保存最终截图")
        
    except Exception as e:
        print(f"\n❌ 执行过程中出错: {e}")
        if driver:
            driver.save_screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    
    finally:
        if driver:
            driver.quit()
            print("\n5️⃣  浏览器已关闭")
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 续期任务完成")
    else:
        print("⚠️  续期任务可能未成功，请检查截图")
    print("=" * 60)
    
    # 如果失败，退出码为1，触发 GitHub Actions 的失败通知
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
