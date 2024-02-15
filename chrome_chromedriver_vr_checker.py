from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import subprocess
import os
import requests
import json
import re


#establish chromedriver_version as a global variable
chromedriver_version = None
#api url link below
url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
#chrome browser = x, chromedriver = y; making global variables for them
x , y = "" , ""


#def get_chromebrowser_version(): #attempted make this code below a method and broke the program
# Get Chrome browser version via subprocess
output = subprocess.check_output(r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value', shell = True)

# sets chrome browser version to a variable to compare
x = output.decode('utf-8').strip()
print(x, "chrome browser")  

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


#cleans the x and y variable to proper comparing size; identical to method below
def clean_stringXY_variable(x):
    # Remove all non-integer characters except "."
    cleaned = ''.join(c for c in x if c.isdigit() or c == '.')
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10] #this is intended to keep 10 digits only for the comparison as the two variables x and y have different lengths due to minor differences
    
    return (cleaned)

# Call the function to set the value global variables and print versions to cmd
get_chromedriver_version()
# sets chrome driver version to a simpler variable to clean and compare
y = chromedriver_version

#this comment cluster pertain to "x" and chromebrowser version being a method than loose code at the top of program
#print(x,"after calling chrome browser version method when implemented")
#get_chromebrowser_version() this is commented due to failed attempt to make method at the top of program
#print(f"Global Chromedriver version: {chromedriver_version}")


# This cluster runs the methods for cleaning x and y to 10 digit strings
cleaned_x = clean_stringXY_variable(x)
#print(cleaned_x,"clean chrome browser variable x")
cleaned_y = clean_stringXY_variable(y)
#print(cleaned_y,"clean chrome driver variable y")

#for testing path where versions dont match, leave commented otherwise
cleaned_x = "122.0.6254.0"
print("cleaned_x has been changed to ",cleaned_x, "for debugging purposes for incompatable versions")

#version id comparison between current chrome browser and chrome driver versions
if cleaned_x == cleaned_y:(
    print("Versions are compatible for Scraping with Google Chrome")
)
else:  #access api here to find correct version of chrome driver to match the version of chrome browser
    print("Versions are incompatible; proceeding to obtain correct ChromeDriver version")
    #this cluster should make z an acceptable variable type and value for the api comparison; should it be string
    z = cleaned_x 
    print("z as chromebrowser version id complete")

    try:
        print("4th attempt to parse json file started")
        
        # Fetch the JSON data from the URL       
        response = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
        response.raise_for_status()  # Raise an exception if the request fails
        # Parse the JSON content
        data = json.loads(response.content.decode("utf-8"))
        #print lines to see what data spits up
        print("line 251")
        print(data['versions'][0])
        print("line 263")
        # Now you can access elements in the JSON data
        i = 0
        for i in range(len(data['versions'])): 
            first_version = data['versions'][0]['version']
            print("first_version = ", first_version)
            if data['versions'][i]['version'] == z:
                print(f"Match found at index {i}")
                break  # This will exit the loop immediately
            i = i + 1
        else:print("no match found")

    except:print("4th attempt to parse json file failed")

print("Version Check for Chrome Scraping Setup complete, Press enter to continue")
#input()
print("Proceeding to next step.")