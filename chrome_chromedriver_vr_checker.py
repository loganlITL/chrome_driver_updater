from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import subprocess
import os
import requests
import re

# Get Chrome browser version via subprocess
output = subprocess.check_output(r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value', shell = True)

# sets chrome browser version to a variable to compare
x = output.decode('utf-8').strip()
print(x, "chrome browser")


chromedriver_version = None
# Get Chromedriver version via subprocess; this program assumes chromedriver.exe is in the same folder as the program itself
def get_chromedriver_version():
    global chromedriver_version  # Declare the variable as global
    chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
    if os.path.exists(chromedriver_path):
        try:
            service = Service(executable_path=chromedriver_path)
            temp_driver = webdriver.Chrome(service=service)
            version = temp_driver.capabilities["chrome"]["chromedriverVersion"]
            # Extract the integer part from the version string
            version_parts = version.split('.')
            major_version = int(version_parts[0])
            minor_version = int(version_parts[1])
            build_version = int(version_parts[2])
            chromedriver_version = f"{major_version}.{minor_version}.{build_version}"
            print(f"Chromedriver version: {chromedriver_version}")
            temp_driver.quit()
        except Exception as e:
            print(f"Error getting Chromedriver version: {e}")
    else:
        print("Chromedriver not found. Please download and place it in the same directory.")

# Call the function to set the global variable and for obtaining driver version
get_chromedriver_version()

# Now you can use 'chromedriver_version' elsewhere in your code
print(f"Global Chromedriver version: {chromedriver_version}")


# sets chrome driver version to a simpler variable to clean and compare
y = chromedriver_version


#cleans the x variable to proper comparing size; identical to method below
def clean_intX_variable(x):
    # Remove all non-integer characters except "."
    cleaned = ''.join(c for c in x if c.isdigit() or c == '.')
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10] #this is intended to keep 10 digits only for the comparison as the two variables x and y have different lengths due to minor differences
    
    return (cleaned)

#cleans the y variable to proper comparing size; identical to method above
def clean_intY_variable(y):
    # Remove all non-integer characters except "."
    cleaned = ''.join(c for c in x if c.isdigit() or c == '.')
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10] #this is intended to keep 10 digits only for the comparison as the two variables x and y have different lengths due to minor differences
    
    return (cleaned)


# This cluster runs the methods for cleaning x and y
# I couldnt get the two to run under the same method; got errors for running an identical method with a different variable
cleaned_x = clean_intX_variable(x)
print(cleaned_x,"clean chrome browser variable x")
cleaned_y = clean_intY_variable(y)
print(cleaned_y,"clean chrome driver variable y")


#this was for debugging because I kept getting incompatible data types
print(cleaned_x,cleaned_y,"compare check started")
print("X is a ",type(cleaned_x), "Y is a ",type(cleaned_y))


#for testing path where versions dont match, leave commented otherwise
cleaned_x = "113.0.5672.0"
print("cleaned_x has been changed to ",cleaned_x, "for debugging purposes for incompatable versions")


#this compares the two to see if chrome driver needs to be updated
if cleaned_x == cleaned_y:(
    print("Versions are compatible for Scraping with Google Chrome")
)
else:  # access api here to find correct version of chrome driver to match the version of chrome browser
    print("Versions are incompatible; proceeding to obtain correct ChromeDriver version")
   
    #api link below
    api_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    
    #this cluster provides a clean str of the chrome browser version so the api can read and compare
    print(type(cleaned_x))
    z = str(cleaned_x)
    #z = str(z)
    #print(type(z)) this line is testing the variable type of z in terminal for debugging
    
    # this method is searching for any matches that may be present and reports back if a match is found
    def find_identical_version(api_url, z):
        try:
            response = requests.get(api_url)
            data = response.json()

            for version_info in data:
                #print(data) do not uncomment this unless you want to see the whole json page blow up the terminal
                version = version_info["version"]  # Corrected usage
                if version == z:
                    return version_info

            return None  # No identical version found
        except Exception as e:
            print(f"Error fetching data from the API: {e}")
            return None
       
    result = find_identical_version(api_url, z) 

    if result:
        print(f"Identical version found: {result['version']}")
    # You can access other information from 'result' as needed
    else:
        print(f"No identical version found for {cleaned_x}")

print("Version Check for Chrome Scraping Setup complete, Press enter to continue")
input()
print("Proceeding to next step.")