from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import subprocess
import os
import requests
import json
import re

# Get Chrome browser version via subprocess
output = subprocess.check_output(r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value', shell = True)

# sets chrome browser version to a variable to compare
x = output.decode('utf-8').strip()
print(x, "chrome browser")

#establish chromedriver_version as a global variable
chromedriver_version = None
#api link below
url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"


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


#cleans the x and y variable to proper comparing size; identical to method below
def clean_intXY_variable(x):
    # Remove all non-integer characters except "."
    cleaned = ''.join(c for c in x if c.isdigit() or c == '.')
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10] #this is intended to keep 10 digits only for the comparison as the two variables x and y have different lengths due to minor differences
    
    return (cleaned)

# This cluster runs the methods for cleaning x and y to 10 digit strings
cleaned_x = clean_intXY_variable(x)
print(cleaned_x,"clean chrome browser variable x")
cleaned_y = clean_intXY_variable(y)
print(cleaned_y,"clean chrome driver variable y")

#for testing path where versions dont match, leave commented otherwise
cleaned_x = "113.0.5672"
print("cleaned_x has been changed to ",cleaned_x, "for debugging purposes for incompatable versions")

# this method is searching for any matches that may be present and reports back if a match is found
def extract_and_compare(url, z):
    try:
        # Fetch the JSON data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request fails
        print("entered try for json extraction")
            # Parse the JSON content
        data = json.loads(response.content.decode("utf-8"))

        # Loop through all the versions
        for version_key, version_value in data.items():
            print("version_key = ", version_key)
            #print("version_value = ", version_value) do not uncomment otherwise terminal gets exploded with json data
            if version_key == "versions":
                # Compare the version with variable z                
                if version_value == z:
                    print(f"Version {z} found in the JSON data.")
                    if "platform" in data:
                        platform_value = data["platform"]
                        if platform_value == "win64":
                            # Extract the "url" value
                            url_value = data.get("url")
                            if url_value:
                                print(f"Download URL for win64: {url_value}")
                                # Add your download logic here
                                # ...
                            else:
                                print("No URL found for win64.")
                else:
                    print(f"Version {z} not found in the JSON data.")
                    #print("version_value = ", version_value)
                    print("z = ", z)
                    # Add other actions if needed
                    # ...
            else:print("version checker failed")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")

#this compares the two to see if chrome driver needs to be updated
#def compare_and_extract_data():# was going to enclose the if statement below into a method; not sure as of yet - line 110
        

#this was for debugging because I kept getting incompatible data types
#print(cleaned_x,cleaned_y,"compare check started")
#print("X is a ",type(cleaned_x), "Y is a ",type(cleaned_y))        
if cleaned_x == cleaned_y:(
    print("Versions are compatible for Scraping with Google Chrome")
)
else:  #access api here to find correct version of chrome driver to match the version of chrome browser
    print("Versions are incompatible; proceeding to obtain correct ChromeDriver version")
       
    #this cluster should make z an acceptable variable type and value for the api comparison; should it be string
    try:
        print("z = to cleaned_x", " - line 103")
        z = cleaned_x
        print(z, " is ", type(z)," value change succesful  - line 105")
    except:
        print("error occured, data type conversion for api comparison and extraction failed - line 103")
        z = "121.68.6769"
        print(z, " is ", type(z)) # this line is testing the variable type of z in terminal for debugging
    
    try:extract_and_compare(url, z)
    except:print("method call failed")
    
            

print("Version Check for Chrome Scraping Setup complete, Press enter to continue")
#input()
print("Proceeding to next step.")