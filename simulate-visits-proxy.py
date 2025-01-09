import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import choice
import os

# Configuration
TARGET_URL = "https://example.com"  # Replace with your target URL
PROXIES = [
    "http://username:password@proxy1:port",
    "http://proxy2:port",
    "http://username:password@proxy3:port",
]  # Replace with your proxy list
SCREENSHOT_DIR = "screenshots"  # Directory to save screenshots

# Ensure screenshot directory exists

if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)


def setup_browser(proxy=None):
    """Sets up and returns a Selenium WebDriver instance with optional proxy."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy:
        print(f"Using proxy: {proxy}")
        chrome_options.add_argument(f"--proxy-server={proxy}")

    return webdriver.Chrome(options=chrome_options)


def visit_website(proxy):
    """Visits the target website using a proxy and captures a screenshot."""
    browser = setup_browser(proxy)
    try:
        print(f"Visiting {TARGET_URL} with proxy {proxy}...")
        browser.get(TARGET_URL)
        time.sleep(3)  # Wait for the page to load

        # Save screenshot
        proxy_label = proxy.replace("http://", "").replace(":", "_").replace("@", "_")
        screenshot_path = f"{SCREENSHOT_DIR}/screenshot_{proxy_label}.png"
        browser.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
    except Exception as e:
        print(f"Error visiting {TARGET_URL} with proxy {proxy}: {e}")
    finally:
        browser.quit()


def main():
    """Main function to test website with multiple proxies."""
    for proxy in PROXIES:
        visit_website(proxy)
        time.sleep(5)  # Delay between visits


if __name__ == "__main__":
    main()
