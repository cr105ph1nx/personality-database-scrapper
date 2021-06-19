from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import requests

def DownloadImage(dirname, url):
    # Change directory to corresponding mbti personality folder
    os.chdir(dirname)
    # We can split the file based upon / and extract the last split within the python list below:
    file_name = url.split('/')[-1]
    print(f"This is the file name: {file_name}")
    # let's send a request to the image URL:
    r = requests.get(url, stream=True)
    # We can check that the status code is 200 before doing anything else:
    if r.status_code == 200:
        # This command below will allow us to write the data to a file as binary:
        with open(file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        print("Oops... must be a bad url!")
    # Return to absolute path
    os.chdir('../')

def CreateFolder(dirname):
    # Create target Directory if don't exist
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        print("Directory " , dirname ,  " Created ")
    else:    
        print("Directory " , dirname ,  " already exists")

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

def ExtractData(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    for card_profile in soup.findAll('div', attrs={'id': re.compile('card-profile-\d+')}):
        # Get MBTI personality type
        personality_class = card_profile.find('div', class_='card-container-personality')
        mbti = personality_class.find(text=True)
        CreateFolder(mbti)

        # Get MBTI personality type
        id = re.search('(?<=profile\-).*', card_profile.get('id'))[0] # get current element ID
        image_url = "https://www.personality-database.com/profile_images/"+ id +".png"
        DownloadImage(mbti, image_url)

def main():
    PDB_url = 'https://www.personality-database.com/trending'
    driver_location = '/usr/bin/chromedriver'
    binary_location = '/usr/bin/google-chrome'

    # Change directory to database/
    os.chdir('database/')
    # Configuring Selenium webdriver
    driver = ConfigSelenium(driver_location, binary_location)
    # Traversing through the DOM of the PDB webpage
    page_source = TraverseDOM(driver, PDB_url)
    # Extracting the data with bs4
    ExtractData(page_source)
    # Closing browser
    driver.close()
    

if __name__ == "__main__":
    
    main()