from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import cloudscraper
import time
from itertools import cycle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from zenrows import ZenRowsClient

URL = "https://parade.com/968666/parade/chuck-norris-jokes/"
API_KEY = open("key.txt").read().strip() if open("key.txt").read().strip() else None

def html_info():
    url = URL
    apikey = API_KEY
    params = {
        'url': url,
        'apikey': apikey,
        'js_render': 'true',
        'antibot': 'true',
        'wait': '1103',
        'json_response': 'true',
        'js_instructions': """[{"click":".selector"},{"wait":500},{"fill":[".input","value"]},{"wait_for":".slow_selector"}]""",
    }
    response = requests.get('https://api.zenrows.com/v1/', params=params)
    print(response.text)
    soup = BeautifulSoup(response.text ,'lxml').prettify()
    print("----------------------")
    print(soup)
