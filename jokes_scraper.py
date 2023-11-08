from bs4 import BeautifulSoup
import time
from selenium import webdriver
import random

URL = "https://www.liveabout.com/top-chuck-norris-jokes-2307758"


def scrape_page_source(url):
    min_sleep = 10
    max_sleep = 12

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    random_sleeping_time = round(random.uniform(min_sleep, max_sleep), 3)
    time.sleep(random_sleeping_time)

    page_source = driver.page_source

    driver.quit()
    return page_source


def clean_text(jokes):
    jokes_result = []
    for joke in jokes:
        joke_striped = joke.lstrip().rstrip()
        joke_itself = extract_alphabetic_characters(joke_striped)
        jokes_result.append(joke_itself)
    return jokes_result


def extract_alphabetic_characters(s):
    for i, c in enumerate(s):
        if c.isalpha():
            return s[i:]
    return s


def extract_jokes_from_soup(soup):
    div_elements = soup.find_all('div', id=lambda x: x and x.startswith('list-sc-item_'))
    div_text_list = [div.get_text() for div in div_elements]
    return clean_text(div_text_list)


def scrape_jokes_from_website():
    page_source = scrape_page_source(URL)
    soup = BeautifulSoup(page_source, "lxml")
    jokes = extract_jokes_from_soup(soup)
    jokes.reverse()
    return jokes




