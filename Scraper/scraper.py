from bs4 import BeautifulSoup
import time
from selenium import webdriver

def html_info():
    # Using selenium
    options = webdriver.ChromeOptions()
    options.add_argument("webdriver\chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    url = "https://www.liveabout.com/top-chuck-norris-jokes-2307758"
    driver.get(url)
    time.sleep(10.23)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    print(soup)
    driver.quit()
