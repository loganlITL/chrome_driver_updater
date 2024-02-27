from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os

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

get_chromedriver_version()