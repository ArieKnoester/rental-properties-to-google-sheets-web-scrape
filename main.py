# https://www.selenium.dev/documentation/
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os
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
    rentals = []

    for listing in listings:
        rental_tuple = (listing.span.text, listing.address.text, listing.a.get("href"))
        rentals.append(rental_tuple)

    return rentals


rentals_list = get_zillow_listings()
pp.pprint(rentals_list)
