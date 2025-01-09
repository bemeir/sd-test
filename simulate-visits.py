import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuration
TARGET_URL = "https://example.com"  # Replace with your target URL
COUNTRIES = ["us", "uk", "de", "fr", "au"]  # List of NordVPN countries to test
SCREENSHOT_DIR = "screenshots"  # Directory to save screenshots

# Ensure screenshot directory exists
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)


def switch_vpn(country):
    """Connects to a NordVPN server in the specified country."""
    print(f"Connecting to NordVPN server in {country}...")
    os.system(f"nordvpn connect {country}")
    time.sleep(5)  # Wait for the VPN to connect
    print(f"Connected to {country}.")


def disconnect_vpn():
    """Disconnects from NordVPN."""
    print("Disconnecting NordVPN...")
    os.system("nordvpn disconnect")
    time.sleep(2)
    print("Disconnected.")


def setup_browser():
    """Sets up and returns a Selenium WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)


def visit_website(country, browser):
    """Visits the target website and captures a screenshot."""
    print(f"Visiting {TARGET_URL} with IP from {country}...")
    browser.get(TARGET_URL)
    time.sleep(3)  # Wait for the page to load

    # Save screenshot
    screenshot_path = f"{SCREENSHOT_DIR}/screenshot_{country}.png"
    browser.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")


def main():
    """Main function to test website with NordVPN and Selenium."""
    for country in COUNTRIES:
        try:
            # Switch VPN to the target country
            switch_vpn(country)

            # Set up Selenium browser
            browser = setup_browser()

            # Visit the target website
            visit_website(country, browser)

        except Exception as e:
            print(f"Error testing with country {country}: {e}")
        finally:
            # Quit the browser and disconnect VPN
            browser.quit()
            disconnect_vpn()


if __name__ == "__main__":
    main()
