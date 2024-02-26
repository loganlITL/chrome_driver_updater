import requests
import os 
import zipfile
import shutil
url_master = "https://storage.googleapis.com/chrome-for-testing-public/122.0.6254.0/win64/chromedriver-win64.zip"
filename = "chromedriver.exe"
script_dir = os.path.dirname(os.path.realpath(__file__))

def download_file(url, filename):
    # Send a HTTP request to the URL
    print("inside download_file(urlz, filename)")
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


download_file(url_master, filename)