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
api_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
#chrome browser = x, chromedriver = y; making global variables for them
x , y = "" , ""
filename = "chromedriver.exe"
def chrome_browser_version():
# Get Chrome browser version via subprocess
    output = subprocess.check_output(r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value', shell = True)
# sets chrome browser version to a variable to compare
    x = output.decode('utf-8').strip()
    print(x, "chrome browser")  
    return x

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

def download_file(url, filename):
    # Send a HTTP request to the URL
    print("inside download_file(url, filename)")
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in write mode
        with open(filename, 'wb') as file:
            # Write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File downloaded successfully: {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def main():

    response = requests.get(api_url)
    data = response.json()
    versions_list = data['versions']  

    for version_info in versions_list:
        version_number = version_info['version']
        downloads = version_info['downloads']

        for download_type, download_info in downloads.items():

                if download_type == 'chromedriver':
                    download_info = str(download_info).replace ("'", '"')
                    download_info = json.loads(download_info)

                    for platform_and_url in download_info:
                        platform = platform_and_url['platform']
                        url = platform_and_url['url']

                        if platform == 'win64':
                            print(f"Version: {version_number},\n URL: {url}\n")
                            urlz = url
                            if version_number==z:
                                print("Version ", z, "found")
                                try:download_file(urlz, filename)
                                except:print("download_file failed")
                                print(urlz)
                                input()
                                


#cleans the x and y variable to proper comparing size; identical to method below
def clean_stringXY_variable(x):
    # Remove all non-integer characters except "."
    cleaned = ''.join(c for c in x if c.isdigit() or c == '.')
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10] #this is intended to keep 10 digits only for the comparison as the two variables x and y have different lengths due to minor differences
    
    return (cleaned)


def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request fails
    with open(filename, 'wb') as file:
        file.write(response.content)

# Call the function to set the value global variables to x and y and print versions to cmd
x = chrome_browser_version()
get_chromedriver_version()
y = chromedriver_version


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
    print("Versions are incompatible; Proceeding to obtain correct ChromeDriver version")
    z = cleaned_x

    try:main()
    except:print("main method failed")

print("Version Check for Chrome Scraping Setup complete, Press enter to continue")
#input()
print("Proceeding to next step.")