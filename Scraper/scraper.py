from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re

URL = "https://www.liveabout.com/top-chuck-norris-jokes-2307758"


def scrape_page_source(url):
    options = webdriver.ChromeOptions()
    options.add_argument("webdriver\chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10.11)
    page_source = driver.page_source
    driver.quit()
    return page_source

def get_relevant_elements(soup):
    div_elements = soup.find_all('div', id=lambda x: x and x.startswith('list-sc-item_'))
    div_text_list = [div.get_text() for div in div_elements]
    return div_text_list

def cleaned_elements(elements):
    result_list = [s.lstrip().rstrip() for s in elements]
    result_list = [s[next((i for i, c in enumerate(s) if c.isalpha()), 0):] for s in result_list]
    return result_list


def html_info():
    page_source = scrape_page_source(URL)
    soup = BeautifulSoup(page_source, "lxml")
    elements = get_relevant_elements(soup)
    quotes = cleaned_elements(elements)
    for q in quotes:
        print("the quote:")
        print(q)
    print("finished")



