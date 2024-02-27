from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chrome_chromedriver_vr_checker import Version as chk
import os
import time

chk.main()

# Get the script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the path to chromedriver.exe (using the script directory)
chromedriver_path = os.path.join(script_dir, 'chromedriver.exe')

# Initialize the ChromeDriver service
service = Service(chromedriver_path)

# Start the service
service.start()

# Create a new ChromeDriver instance
driver = webdriver.Chrome(service=service)

try:
    website = 'https://www.google.com/'
    driver.get(website)
    driver.fullscreen_window()

    # Wait for the search input field to appear
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "q")))

    # Enter a search query (e.g., "fluffy puppies") and press Enter
    input_element = driver.find_element(By.NAME, "q")
    input_element.clear()
    input_element.send_keys("fluffy puppies" + Keys.ENTER)

    # Wait for the search results page to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Fluffy Puppies")))

    # Click on the link related to fluffy puppies
    link = driver.find_element(By.PARTIAL_LINK_TEXT, "Fluffy Puppies")
    link.click()

    # Wait for some time (e.g., 10 seconds) to observe the page
    time.sleep(10)

finally:
    # Quit the driver and stop the service
    driver.quit()
    service.stop()