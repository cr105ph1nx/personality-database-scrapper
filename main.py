from selenium import webdriver
from bs4 import BeautifulSoup
import re

def ConfigSelenium(driver_location, binary_location):
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location # adding the binary location of the browser 
    options.add_argument('--ignore-certificate-errors') # accessing the Chrome browser driver while ignoring certificate errors
    options.add_argument('--incognito') # accessing the Chrome browser driver in incognito mode
    options.add_argument('--headless') # accessing the Chrome browser driver without opening a browser window

    driver = webdriver.Chrome(executable_path = driver_location, options = options)

    return driver

def TraverseDOM(driver, PDB_url):
    driver.get(PDB_url) # specifying the URL of the webpage
    page_source = driver.page_source

    return page_source

def ExtractData(page_source, personality_types):
    soup = BeautifulSoup(page_source, 'lxml')
    for card_profile in soup.findAll('div', attrs={'id': re.compile('card-profile-\d+')}):
        # Get MBTI personality type
        personality_class = card_profile.find('div', class_='card-container-personality')
        mbti = personality_class.find(text=True)

        print('\n')

    return personality_types


def main():
    PDB_url = 'https://www.personality-database.com/trending'
    personality_types = []
    driver_location = '/usr/bin/chromedriver'
    binary_location = '/usr/bin/google-chrome'

    # Configuring Selenium webdriver
    driver = ConfigSelenium(driver_location, binary_location)
    # Traversing through the DOM of the PDB webpage
    page_source = TraverseDOM(driver, PDB_url)
    # Extracting the data with bs4
    personality_types = ExtractData(page_source, personality_types)
    

if __name__ == "__main__":
    main()