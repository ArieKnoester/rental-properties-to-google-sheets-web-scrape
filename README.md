# rental-properties-to-google-sheets-web-scrape

## Description
This program uses BeautifulSoup to scrape a Zillow site for available properties for rent. The URL for 
the Zillow site contains all search filters within the URL (price range,area of town, etc...). For each 
listing the rent, address and url are parsed and entered into a Google Form using Selenium. From
the Google Form, the user can export a Google Sheet containing the data for each listing.

### Note:
This code works as of 2024-01-05, but keep in mind that Zillow may change the structure of their site 
which will cause this implementation of BeautifulSoup's find_all() method to fail.