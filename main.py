# https://beautiful-soup-4.readthedocs.io/en/latest/#
# https://www.selenium.dev/documentation/
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_all_elements_located
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os
import re
import pprint as pp

load_dotenv()
ZILLOW_URL = os.environ['ZILLOW_URL']
GOOGLE_FORM_URL = os.environ['GOOGLE_FORM_URL']
ZILLOW_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
}


def get_zillow_content():
    response = requests.get(url=ZILLOW_URL, headers=ZILLOW_HEADER)
    response.raise_for_status()
    return response.text


def get_zillow_listings():
    zillow_content = get_zillow_content()
    soup = BeautifulSoup(zillow_content, "html.parser")
    listings = soup.find_all("article", attrs={"data-test": "property-card"})
    addresses = []
    rents = []
    urls = []

    for listing in listings:

        # print(listing.address.text)
        address = listing.address.text.replace(" - ", ",").strip()
        address = re.split(r'[,|]', address)

        if address[0][0].isdigit():
            addresses.append(address[0].strip())
        else:
            addresses.append(address[1].strip())

        # print(listing.span.text)
        rents.append(listing.span.text.replace("+", "").replace("/", "").replace("mo", "").split()[0])

        url = listing.a.get("href")
        if "https://www.zillow.com" not in url:
            url = "https://www.zillow.com" + url
        urls.append(url)

    # print(f"addresses: {len(addresses)}, rents: {len(rents)}, urls: {len(urls)}")
    # pp.pprint(addresses)
    # pp.pprint(rents)
    # pp.pprint(urls)
    add_rentals_to_form(addresses, rents, urls)


def add_rentals_to_form(addresses, rents, urls):
    driver = webdriver.Firefox()
    driver.get(url=GOOGLE_FORM_URL)

    for i in range(len(addresses)):
        WebDriverWait(driver, timeout=10).until(presence_of_all_elements_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
        inputs = driver.find_elements(By.CSS_SELECTOR, value=".whsOnd.zHQkBf")
        inputs[0].send_keys(addresses[i])
        inputs[1].send_keys(rents[i])
        inputs[2].send_keys(urls[i])
        submit = driver.find_element(By.CSS_SELECTOR, value=".NPEfkd.RveJvd.snByac")
        submit.click()
        WebDriverWait(driver, timeout=10).until(element_to_be_clickable((By.CSS_SELECTOR, ".c2gzEf>a"))).click()

    driver.quit()


get_zillow_listings()
