import requests
import json

api_url = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'




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


if __name__ == '__main__':
    main()