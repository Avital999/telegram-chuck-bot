from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time


def html_info():
    # Using selenium
    options = webdriver.ChromeOptions()
    options.add_argument("webdriver\chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    driver.get("https://parade.com/968666/parade/chuck-norris-jokes/")
    print("STARTTTTTTTTT")
    time.sleep(10)
    driver.quit()
