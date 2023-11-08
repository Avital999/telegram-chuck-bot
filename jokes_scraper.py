from bs4 import BeautifulSoup
import time
from selenium import webdriver
import random

URL = "https://www.liveabout.com/top-chuck-norris-jokes-2307758"


def scrape_page_source(url):
    min_sleep = 1
    max_sleep = 2

    options = webdriver.ChromeOptions()
    options.binary_location = "/bin/google-chrome"  # Replace with the actual path to your Chrome executable
    chrome_driver_path = "chromedriver" # Replace with the actual path to your ChromeDriver executable

    # Use the 'service' argument to specify the path to the ChromeDriver executable
    chrome_service = webdriver.chrome.service.Service(executable_path=chrome_driver_path)

    # Pass the 'service' and 'options' to the Chrome WebDriver constructor
    driver = webdriver.Chrome(service=chrome_service, options=options)

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




