from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep

def create_driver():
    socks5_proxy = "socks5://127.0.0.1:9050"
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={socks5_proxy}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

driver = create_driver()
driver.get("https://check.torproject.org/")
print("Page chargée")
sleep(5)
driver.quit()
