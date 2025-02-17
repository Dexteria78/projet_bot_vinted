from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def create_driver():
    socks5_proxy = "socks5://127.0.0.1:9050"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Mode headless pour Chrome
    chrome_options.add_argument("--disable-gpu")  # Désactive le GPU
    chrome_options.add_argument("--no-sandbox")  # Bypass les restrictions sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")  # Réduit les plantages liés à /dev/shm
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging port
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Contourne la détection
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")  # Utilise Tor
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--disable-software-rasterizer")

    # Chemin du ChromeDriver
    service = Service("/usr/local/bin/chromedriver")
    
    # Initialisation du WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Test simple
if __name__ == "__main__":
    driver = create_driver()
    driver.get("https://check.torproject.org/")
    print("Page chargée via Tor avec Chrome.")
    driver.quit()
