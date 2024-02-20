import requests
import os 

url_master = "https://storage.googleapis.com/chrome-for-testing-public/122.0.6254.0/win64/chromedriver-win64.zip"
filename = "chromedriver.exe"

def download_file(url, filename):
    # Send a HTTP request to the URL
    print("inside download_file(urlz, filename)")
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Set the output directory to your desired location (Downloads folder)
        output_directory = os.path.expanduser("~/Downloads")     
        # Create a file path by joining the directory name with the desired file name
        file_path = os.path.join(output_directory, filename)
        # Open the file in write mode
        with open(file_path, 'wb') as file:
            # Write the contents of the response to the file
            file.write(response.content)
            print(f"File downloaded successfully: {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


download_file(url_master, filename)