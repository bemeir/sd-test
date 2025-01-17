import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Configuration
HOSTNAME = "gate.smartproxy.com"  # Proxy host:port configuration
PORT = "7000"
DRIVER = "CHROME"  # Select 'CHROME' or 'FIREFOX'
SCREENSHOT_DIR = "screenshots"  # Directory to save screenshots
ROTATIONS_PER_URL = 5  # Number of rotations per URL
TARGET_URLS = [
    "https://whatismyipaddress.com/",
    "https://dev-docker.sdbullion.com/1-oz-american-silver-eagle-coins-random-year",
    "https://dev-docker.sdbullion.com/silver/us-mint-american-silver-eagle-coins",
]


def smartproxy():
    """Selects appropriate driver and sets up proxy."""
    if DRIVER == "FIREFOX":
        options = FirefoxOptions()
    elif DRIVER == "CHROME":
        options = ChromeOptions()
    else:
        raise ValueError("Invalid driver specified")

    proxy_str = f"{HOSTNAME}:{PORT}"
    options.add_argument(f"--proxy-server={proxy_str}")

    return options


def setup_browser():
    """Installs and returns the latest WebDriver with Smartproxy settings."""
    if DRIVER == "FIREFOX":
        browser = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()), options=smartproxy()
        )
    elif DRIVER == "CHROME":
        browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=smartproxy()
        )
    return browser


def visit_website(url, rotation):
    """Visits the target website, captures a screenshot, and prints page source."""
    browser = setup_browser()
    try:
        print(f"Visiting {url} (Rotation: {rotation})...")
        browser.get(url)
        time.sleep(5)  # Wait for the page to load

        # Save screenshot
        url_label = url.replace("https://", "").replace("http://", "").replace("/", "_")
        screenshot_path = (
            f"{SCREENSHOT_DIR}/screenshot_{url_label}_rotation_{rotation}.png"
        )
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
        browser.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"Error visiting {url} (Rotation: {rotation}): {e}")
    finally:
        browser.quit()


def main():
    """Main function to visit multiple URLs with proxy rotations."""
    for rotation in range(1, ROTATIONS_PER_URL + 1):
        for url in TARGET_URLS:
            visit_website(url, rotation)
            time.sleep(2)  # Optional delay between visits


if __name__ == "__main__":
    main()
