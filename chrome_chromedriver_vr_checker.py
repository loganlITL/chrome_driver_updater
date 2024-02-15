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


# this method is searching for any matches that may be present and reports back if a match is found
def extract_and_compare(url, z):
    try:
        print("extract_and_compare is now running")
        # Fetch the JSON data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request fails
        print("Initiating phase, entered try for json extraction")
            # Parse the JSON content
        data = json.loads(response.content.decode("utf-8"))
        print("json data extracted, headed towards 'for loop'")
        # Loop through all the versions        
        for version_key, version_value in data.items():
                print("version_key =", version_key)
                if version_key == "versions": # Compare the version with the api json tag "versions"
                    print("step 1, versions")
                    if "version" in version_value: # Check if "version" is a key in the version_value dictionary
                        print(f"step 2, Version {z} found in the JSON data.")
                        if version_value["version"] == z: # Checking version of google chrome against the value of the json api; havent limited comparisons to 10 chars - will throw off results
                            print("step 3, Entered value if statement")
                        # Assuming the "platform" key is in the next level of the JSON data
                            for platform_key, platform_value in version_value.items():
                                print("step 4, in platform for loop, for debugging only")
                                if platform_key == "platform": # enters and compares value to get right type of chrome driver, windows 64bit needed
                                    platform_value = data["platform"]
                                    if platform_value == "win64":
                                        # Extract the "url" value
                                        url_value = data.get("url")
                                        if url_value:
                                            print(f"Download URL for win64: {url_value}")
                                            # Add download logic here
                                            try:
                                                response = requests.get(url)
                                                filename = "chromedriver"
                                                with open(filename, 'wb') as file:
                                                    file.write(response.content)
                                            except:print("failure to download new chrome driver")
                                        else:
                                            print("No URL found for win64.")
                    else:
                        print(f"Version {z} not found in the JSON data.")
                        # Uncomment the next line to see the version_value
                        # print("version_value =", version_value)
                        print("z =", z)
                        # Add other actions if needed
                        # ...
                else:
                    print("Version checker failed. Make this code go to 'versions' first, then 'version', then 'platform', and obtain the 'url' from the JSON file.")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")

#this method was made based off 'extract_and_compare' as an improvement;it doesnt seem to go any different due to error at "version" key
def extract_and_compare2(url, z):
    try:
        print("extract_and_compare2 is now running")
        # Fetch the JSON data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request fails
        print("Initiating phase, entered try for json extraction")
        # Parse the JSON content
        data = json.loads(response.content.decode("utf-8"))
        print("json data extracted, headed towards 'for loop'")
        # Check the presence of keys in the JSON data
        if "versions" in data:
            print("step 1, versions")
            print("versions" in data["versions"], "is 'versions' in data from versions?")
            print("113.0.5672.0" in data["versions"], "is '113.0.5672.0' in data from versions?")
            print('versions' in data["versions"], "is versions in data from versions?")
            print('version' in data["versions"], "is version in data from versions?")
            print('version' in data,"is version in data?")
            print('revision' in data["versions"], "is revision in data from versions?")
            print('downloads' in data["versions"], "is downloads in data from versions?")
            print('chrome' in data["versions"], "is chrome in data from versions?")
            #print(data["versions"])
            if 'version' in data:
                print(f"step 2, 'version' key found in the JSON data.")
                if data["versions"]["version"] == z:
                    print("step 3, searching for ",z ," as value of the 'version' key")
                    # Proceed to the nested keys
                    if "revision" in data["versions"]["version"]:
                        print("step 4, entered revision key sector")
                        if "downloads" in data["versions"]["version"]["revision"]:
                            print("step 5, entered downloads key sector")
                            if "chrome" in data["versions"]["version"]["revision"]["downloads"]:
                                print("step 6, entered chrome key sector")
                                if "platform" in data["versions"]["version"]["revision"]["downloads"]["chrome"] and "url" in data["versions"]["version"]["revision"]["downloads"]["chrome"]:
                                    print("step 7, entered platform and url key sector")
                                    if data["versions"]["version"]["revision"]["downloads"]["chrome"]["platform"] == "win64":  
                                        url_value = data["versions"]["version"]["revision"]["downloads"]["chrome"]["url"]
                                        print(f"Download URL for win64: {url_value}")
                                        print("step 8, platform win64 found")
                                        # Add download logic here
                                        try:
                                            response = requests.get(url)
                                            filename = "chromedriver"
                                            with open(filename, 'wb') as file:
                                                file.write(response.content)
                                        except:print("Failure to download new chromedriver. Failed after step 7.")
                                    else:
                                        print("Platform is not win64. Failed after step 6")
                                else:
                                    print("No platform or url key found in the chrome dictionary. Failed after step 5")
                            else:
                                print("No chrome key found in the downloads dictionary. Failed after step 4")
                        else:
                            print("No downloads key found in the revision dictionary. Failed after step 3")
                else:
                    print(f"Version {z} not found in the JSON data. Failed after step 2")
            else:
                print("No 'version' key found in the data. Failed after step 1")
        else:
            print("No 'versions' key found in the JSON data.")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")

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
cleaned_x = "113.0.5672.0"
print("cleaned_x has been changed to ",cleaned_x, "for debugging purposes for incompatable versions")

#version id comparison between current chrome browser and chrome driver versions
if cleaned_x == cleaned_y:(
    print("Versions are compatible for Scraping with Google Chrome")
)
else:  #access api here to find correct version of chrome driver to match the version of chrome browser
    print("Versions are incompatible; proceeding to obtain correct ChromeDriver version")
    z = cleaned_x 
    #this cluster should make z an acceptable variable type and value for the api comparison; should it be string
    try:       
        #this was attempt one at trying to get download link from json file        
        print("z as chromebrowser version id complete")
        extract_and_compare(url, z)
        print("extract_and_compare(url, z) was successful")
    except:
        print("method call failed; extract_and_compare(url, z) was unsuccessful")     
    try:
        #this was attempt two at trying to get download link from json file
        extract_and_compare2(url, z)
        print("extract_and_compare2(url, z) was successful")
    except:
        print("method extract_and_compare2(url, z) unsuccessful")

    try: # Fetch the JSON data from the URL
        print("third attempt to parse json file started")
        response = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
        response.raise_for_status()  # Raise an exception if the request fails

        # Parse the JSON content
        data = json.loads(response.content.decode("utf-8"))

        # Now you can access elements in the JSON data
        for version in data['versions']:            
            #print(f"Version: {version['version']}")
            #print(f"Revision: {version['revision']}")
            #print(f"Downloads: {version['downloads']}")
            
            if data[0] == z:
                print("version found")

            else:
                print("Version ",z," not found")    
    except:print("third attempt at json parsing failed")

    try:
        print("4th attempt to parse json file started")
        
    # Fetch the JSON data from the URL
        print("line 244")
        response = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
        response.raise_for_status()  # Raise an exception if the request fails
        print("line 247")
    # Parse the JSON content
        data = json.loads(response.content.decode("utf-8"))
        #print lines to see what data spits up
        print("line 251")
        print(data['versions'][0])
        print("line 263")
    # Now you can access elements in the JSON data
        first_version = data['versions'][0]['version']
        print("first_version = ", first_version)
        if z == first_version:
            print(f"Version {z} matches the first version in the JSON data.")
        else:
            print(f"Version {z} does not match the first version in the JSON data.")

        if url:
            print(f"Download URL for version {z}: {url}")
        else:
            print(f"No download URL found for version {z}")
    except:print("4th attempt to parse json file failed")

print("Version Check for Chrome Scraping Setup complete, Press enter to continue")
#input()
print("Proceeding to next step.")