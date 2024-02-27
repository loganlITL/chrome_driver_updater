from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import subprocess
import requests
import zipfile
import shutil
import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
#api url link below
api_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
#chrome browser = x, chromedriver = y;
global x , y , z 
x , y , z = "" , "" , ""
filename = "chromedriver.exe"
chromedriver_version = ""


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

#cleans the x and y variable to proper comparing size; identical to method below
def clean_stringXY_variable(x):
    # Remove all non-integer characters except "."
    cleaned = ''.join(c for c in x if c.isdigit() or c == '.')
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10] #this is intended to keep 10 digits only for the comparison as the two variables x and y have different lengths due to minor differences
    
    return (cleaned)

def truncate_string(input_string):
    # Truncate the string to the first 10 characters
    truncated_string = input_string[:10]
    return truncated_string

def api_parser():

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
                            #print(f"Version: {version_number},\n URL: {url}\n")
                            
                            if truncate_string(version_number)==truncate_string(z):
                                print("Version ", z, "found")
                                global url_master
                                url_master = url
                                print(url_master)
                                try:download_file(url_master, filename)#runs download method for specific chrome driver version
                                except:print("failed to download file")
                                return #terminate method after 1 match is found
                            
def download_file(url, filename):
    # Send a HTTP request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Set the output directory to your desired location(script dir for chromedriver.exe)
        output_directory = os.path.dirname(os.path.realpath(__file__))   
        # Create a file path by joining the directory name with the desired file name
        zip_path = os.path.join(script_dir, filename + ".zip")
        # Open the file in write mode
        with open(zip_path, 'wb') as file:
            # Write the contents of the response to the file
            file.write(response.content)
            print(f"Zip file downloaded successfully: {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all the contents of the zip file in the output directory
            zip_ref.extractall(script_dir)
            print(f"File extracted successfully: {filename}")
        # Move the chromedriver.exe from the 'chromedriver-win64' folder to the top level of the script directory
        extracted_folder = os.path.join(output_directory, 'chromedriver-win64')
        shutil.move(os.path.join(extracted_folder, filename), os.path.join(output_directory, filename))
        print(f"File moved to script directory: {output_directory}/{filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
class Version:
    def main():

        # Call the function to set the value global variables to x and y and print versions to cmd
        x = chrome_browser_version()
        get_chromedriver_version()
        y = chromedriver_version

        # This cluster runs the methods for cleaning x and y to 10 digit strings
        cleaned_x = clean_stringXY_variable(x)
        cleaned_y = clean_stringXY_variable(y)

        #for testing path where versions dont match, leave commented otherwise
        #cleaned_x = "122.0.6254.0"
        #print("cleaned_x has been changed to ",cleaned_x, "for debugging purposes for incompatable versions")

        #version id comparison between current chrome browser and chrome driver versions
        #print(cleaned_x," x val, ",cleaned_y, " y val")
        if cleaned_x == cleaned_y:(
            print("Versions are compatible for Scraping with Google Chrome")
        )
        else:  #access api here to find correct version of chrome driver to match the version of chrome browser
            print("Versions are incompatible; Proceeding to obtain correct ChromeDriver version")
            global z
            z = cleaned_x

            try:api_parser()
            except:print("main method failed")

        print("Version Check for Chrome Scraping Setup complete, Press enter to continue")
        input()
        print("Proceeding to next step.")


if __name__ == '__main__':
    Version.main()