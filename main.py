from selenium import webdriver

# Global variables 
PDB_url = 'https://www.personality-database.com/trending'
 
# Configuring Selenium webdriver
driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'

options = webdriver.ChromeOptions()
options.binary_location = binary_location

driver = webdriver.Chrome(executable_path = driver_location, options = options)
driver.get(PDB_url)