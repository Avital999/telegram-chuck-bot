from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time



def html_info():
    # Using selenium
    options = webdriver.ChromeOptions()
    options.add_argument("webdriver\chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    url = "https://parade.com/968666/parade/chuck-norris-jokes/"
    driver.get(url)
    print("STARTTTTTTTTT")
    time.sleep(10)
    page_source = driver.page_source
    print(page_source)
    soup = BeautifulSoup(page_source, "lxml")
    print("second")
    driver.quit()
