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

def short_div(str):
    match = re.search(r'[a-zA-Z]', str)

    if match:
        start_index = match.start()
        str1 = str[start_index:]
        print(str1)
        return str1
    else:
        print("No English letter found in the string.")


def html_info():
    page_source = scrape_page_source(URL)
    soup = BeautifulSoup(page_source, "lxml")
    # Find the relevant elements and save them in a list
    div_elements = soup.find_all('div', id=lambda x: x and x.startswith('list-sc-item_'))
    div_text_list = [div.get_text() for div in div_elements]
    result_list = [s[next((i for i, c in enumerate(s) if c.isalpha()), 0):] for s in div_text_list]
    for d in result_list:
        print("the result:")
        print(d)
    print("finished")



