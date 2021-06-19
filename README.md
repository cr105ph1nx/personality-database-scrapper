# PDB Scrapper 
The aim of the project is to scrap the webpage **https://www.personality-database.com/** in order to create a `database/` folder in which are organized folders for each **MBTI personality type**, each folder includes **face images** of public personalities corresponding to their MBTI personality type.

*This data will be used as reference in a ML thesis conducted by a friend of mine, for the objective of **exploring the possible links between the MBTI personality type of a person and their facial features**.*

# Setup 
1. to install python on Debian-based:
```bash
sudo apt install python
```
2. clone this repository
```bash
git clone https://github.com/cr105ph1nx/personality-database-scrapper.git
cd personality-database-scrapper/
```
3. create a python virtual environement
```bash
pip3 install virtualenv 
virtualenv .
source bin/activate
```
4. install the dependencies 
```bash
pip3 install requirements.txt
```

# Usage
1. run the script 
```bash
python main.py
```

# Ressources 
* [requests](https://pypi.org/project/requests/)
* [selenium](https://pypi.org/project/selenium/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
* [lxml](https://pypi.org/project/lxml/)

# Compatibility 
If you have an older version of python, you might run into some compatibility issues. In case of any errors, try updating to the newest stable version of python and pip. Or consult the py documentation for more information.

# Configuring Selenium 
In order to configure selenium 
1. you need to install your favourite browser as well as its corresponding driver.
2. make sure their directory is included in the PATH environment variables of your local machine.
3. replace the variables `driver_location` and `binary_location` by the actual path to your driver and binary.

*You can learn more about how to configure selenium from the library's official [documentation](https://www.selenium.dev/documentation/en/)*