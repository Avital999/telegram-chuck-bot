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
    pretty_soup = soup.prettify()
    div_elements = div_elements = soup.find_all('div')
    div_info_list = []
    for div in div_elements:
        div_info = div.text  # Get the text content of the <div> element
        if re.match(r'^\s*\d+\.\s', div_info):  # Check if the text matches the pattern
            div_info_list.append(short_div(div_info))
    div_info_list=div_info_list[2:]
    for div_info in div_info_list:
        print("next:")
        print(div_info)
    print(f"finished, div info list is:{len(div_info_list)}")


