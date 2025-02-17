from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def create_driver():
    # Configuration du proxy Tor
    socks5_proxy = "socks5://127.0.0.1:9050"

    # Options du navigateur
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={socks5_proxy}")
    chrome_options.add_argument("--headless")  # Mode sans interface graphique
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialisation de ChromeDriver
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Test Tor avec Selenium
try:
    driver = create_driver()
    driver.get("https://check.torproject.org")
    print("Page chargée : ", driver.title)
    if "Congratulations" in driver.page_source:
        print("Tor est configuré correctement avec Selenium.")
    else:
        print("Tor ne semble pas fonctionner correctement.")
finally:
    driver.quit()
