HOW TO USE

how to import: from chrome_chromedriver_vr_checker import Version as chk

Calling this class allows the full program to check versions for the chrome browser and chrome driver, compares the 2 against one another and if no match occurs, access api to obtain correct version of webdriver to match chrome browser version.
This is designed to be imported into another program to keep chromedriver.exe updated automatically in the script directory.
You must have this program in the same folder as your own and search for the chromedriver.exe in the same directory

The 'seperate methods' folder is for prototyping another type of webscraper version checker for a different platform ie:(edge, firefox, safari ect.) These files are only for development purposes.


UPDATE LOG
date 2\12\24
this is to check the program google chrome and chrome driver and compare the 2.
if compatable, then proceed to web scraping
if not compatible or not present(webdriver), it should automatically go to the api and download the chromedriver to the same folder this program is in.

the program also limits version numbers up to 10 digits, including "." in the method "clean_intX_variable" and "clean_intY_variable"
this may cause issues when it comes to scaling; not too sure how it will affect future releases.

there are some parts in which are incomplete as of 2\13\24
- api access and download of correct chromedriver version
- proper organization of code into clear methods

DATE: 2/20/24
finished functionality, downloads the chromedriver.exe to the downloads folder.
try and excepts included to handle errors gracefully
cleaned up code and elimnated unnessecary lines & excess print lines

fixed bug where version in api was not matching length of z
fixed bug where chromedriver was not checking version correctly

issues:api download obtains faulty file from url.
however, if done manually, the link gets the correct version
idea: maybe the chrome driver isnt extracted properly and is still compressed, hence it is smaller and errors occur?

DATE: 2/26/24
json api download corrected by adding zip extraction and file was put in same dir as script
made program callable outside of itself by putting code calls inside a main method
organized code and left comments

DATE: 2/27/24
updated program to make class Version available to import into other web scraping programs.
made an example of that process in 'import class test.py'
