from bs4 import BeautifulSoup
import time
from selenium import webdriver
import random

URL = "https://www.liveabout.com/top-chuck-norris-jokes-2307758"


def scrape_page_source(url):
    """ Given an url, scrape the page source using Selenium and return it."""

    options = webdriver.ChromeOptions()
    options.add_argument("webdriver\chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # sleep random time between 1 and 2 seconds
    random_sleeping_time = round(random.uniform(1, 2), 3)
    time.sleep(random_sleeping_time)

    page_source = driver.page_source

    driver.quit()

    return page_source


def clean_text(jokes):
    # removes leading and trailing white spaces
    jokes = [s.lstrip().rstrip() for s in jokes]
    # extract the portion of each joke starting from the first alphabetical char
    jokes = [s[next((i for i, c in enumerate(s) if c.isalpha()), 0):] for s in jokes]
    return jokes


def soup_to_jokes(soup):
    """Receiving the soup returned from beautifulSoup package and return a list of jokes."""
    div_elements = soup.find_all('div', id=lambda x: x and x.startswith('list-sc-item_'))
    div_text_list = [div.get_text() for div in div_elements]
    return clean_text(div_text_list)


def jokes_list():
    page_source = scrape_page_source(URL)
    soup = BeautifulSoup(page_source, "lxml")
    jokes = soup_to_jokes(soup)
    jokes.reverse()
    return jokes


def chuck_joke(joke_number: int) -> str:
    return jokes_list()[joke_number-1]


