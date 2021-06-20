from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import os
import requests

def WaitDriver(driver, xpath):
    try:
        # wait 10 seconds before looking for element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print("Failed to wait for driver.")

def DownloadImage(dirname, url):
    # Change directory to corresponding mbti personality folder
    os.chdir(dirname)
    # We can split the file based upon / and extract the last split within the python list below:
    file_name = url.split('/')[-1]
    # let's send a request to the image URL:
    r = requests.get(url, stream=True)
    # We can check that the status code is 200 before doing anything else:
    if r.status_code == 200:
        # This command below will allow us to write the data to a file as binary:
        with open(file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        print(f"Downloaded image: {file_name} to {dirname} folder")
    else:
        print("Oops... must be a bad url!")
    # Return to absolute path
    os.chdir('../')

def CreateFolder(dirname):
    # Create target Directory if it doesn't exist
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def ConfigSelenium(driver_location, binary_location):
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location # adding the binary location of the browser 
    options.add_argument('--ignore-certificate-errors') # accessing the Chrome browser driver while ignoring certificate errors
    options.add_argument('--incognito') # accessing the Chrome browser driver in incognito mode
    options.add_argument('--headless') # accessing the Chrome browser driver without opening a browser window
    driver = webdriver.Chrome(executable_path = driver_location, options = options)

    return driver

def ExtractData(driver, PDB_url):
    # Specifying the URL of the webpage 
    driver.get(PDB_url)
    while True:
        WaitDriver(driver, '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[4]') # Wait for driver until class is present in DOM
        # Fetch page source
        page_source = driver.page_source
        # Parse page source
        soup = BeautifulSoup(page_source, 'lxml')
        # Fetch profile cards from current page
        cards_profile = soup.findAll('div', attrs={'id': re.compile('card-profile-\d+')})
        # Browse current page
        for card_profile in cards_profile:
            # Get MBTI personality type
            personality_class = card_profile.find('div', class_='card-container-personality')
            mbti = personality_class.find(text=True)
            # Check if MBTI personality type is known
            if(mbti != "XXXX"):
                CreateFolder(mbti)
                # Get face image
                id = re.search('(?<=profile\-).*', card_profile.get('id'))[0] # get current element ID
                image_url = "https://www.personality-database.com/profile_images/"+ id +".png"
                DownloadImage(mbti, image_url)

        # Direct to next page 
        WaitDriver(driver, '//a[text()=">>>"]') # Wait for driver until next button is present in DOM
        next_button = driver.find_element_by_xpath('//a[text()=">>>"]')            
        driver.execute_script('arguments[0].click();', next_button)
        # Check if current page empty
        if(len(cards_profile)>0):
            print("\nOff to the next page we go!")
        else:
            print("\nSeems like you got everything here!")
            # writing handled url to file 
            file2 = open('../urls_handled.txt', 'a')
            file2.write(PDB_url)
            file2.close()
            break

def main():
    # Set location of driver and binary
    driver_location = '/usr/bin/chromedriver'
    binary_location = '/usr/bin/google-chrome'
    # Change directory to database/
    os.chdir('database/')
    # Configuring Selenium webdriver
    driver = ConfigSelenium(driver_location, binary_location)
    # Read urls.txt
    file1 = open('../urls.txt', 'r')
    urls = file1.readlines()
    # Strips the newline character
    for url in urls:
        # Display current url
        print(format(url.strip()))
        # Extracting the data with bs4
        ExtractData(driver, url)
    # Closing browser
    driver.close()

if __name__ == "__main__":
    main()