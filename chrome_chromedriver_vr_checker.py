from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import subprocess
import os
import re

# Get Chrome browser version via subprocess
output = subprocess.check_output(r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value', shell = True)

# sets chrome browser version to a variable to compare
x = output.decode('utf-8').strip()
print(x, "chrome browser")

# set version as a global variable so it can be used to compare
version = ""

# Get Chromedriver version via subprocess; this program assumes chromedriver.exe is in the same folder as the program itself
def get_chromedriver_version():
    chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
    if os.path.exists(chromedriver_path):
        try:
            service = Service(executable_path=chromedriver_path)
            temp_driver = webdriver.Chrome(service=service)
            version = temp_driver.capabilities["chrome"]["chromedriverVersion"]
            # print(type(version))
            temp_driver.quit()
            print(f"Chromedriver version: {version}")
        except Exception as e:
            print(f"Error getting Chromedriver version: {e}")
    else:
        print("Chromedriver not found. Please download and place it in the same directory.")

#this method removes excess chars from the version variable
def remove_non_numeric(c_driverversion):
    # Use regular expression to replace non-numeric cSharacters with an empty string
    cleaned_string = re.sub(r"[^0-9]", "", c_driverversion)
    return cleaned_string

# method for obtaining driver version
get_chromedriver_version()

#method for removing extra stuff from variable
version_2 = remove_non_numeric(version)
print(f"Cleaned string:{version_2}", " ***chromedriver variable without excess strings")

# sets chrome driver version to a simpler variable to compare
y = version
# print(y) only uncomment if additional print is needed

# compares the 2 outputs of version to see if they are the same 
if x == y:(
    print("Versions are compatible for Scraping with Google Chrome")
)
else:(
    print("Versions are incompatible; proceeding to obtain correct ChromeDriver version")
    # access api here to find correct version of chrome driver to match the version of chrome browser
)
    



    