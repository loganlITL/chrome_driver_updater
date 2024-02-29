*********************Chrome Driver Automatic Updater************************** WINDOWS 11
This program automatically updates chromedriver.exe for selenium webscraping to make automating the process faster than having to manually update the chrome driver everytime your browser updates, which may result in incompatable versions.

The program uses python with selenium for pulling the chromedriver version, in order to compare it to the chrome browser version.
If the 2 versions are not identical, then the program will access the json api to obtain and download the correct version of chromedriver.exe for webscraping and put into the same directory as the script.

class Version holds the main method which runs the program.

If the program fails to download the new version of ChromeDriver, it still attempts to post a link to the terminal for manual download.

******************HOW TO USE*****************

how to import: 
from chrome_chromedriver_vr_checker import Version as chk
chk.main()

DEPENDENCIES:
selenium
os
zipfile
requests
json
shutil
subprocess

*All of these need to be installed through pip for this program to run without issues
This program has been tested and developed for Windows 11 with selenium 4 and python 3.12


You must have this program in the same folder as your own program since chromedriver.exe is programmed to go to the same directory as this program after it is unzipped.
You also must have your program find chromedriver.exe from the same directory.
This program does not take into consideration other platforms which may have chrome browser installed differently ie:(linux, mac, ect)

The 'seperate methods' folder is for prototyping another type of webscraper version checker for a different platform ie:(edge, firefox, safari ect.) These files are only for development purposes.