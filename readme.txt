date 2\12\24
this is to check the program google chrome and chrome driver and compare the 2.
if compatable, then proceed to web scraping
if not compatible or not present(webdriver), it should automatically go to the api and download the chromedriver to the same folder this program is in.

the program also limits version numbers up to 10 digits, including "." in the method "clean_intX_variable" and "clean_intY_variable"
this may cause issues when it comes to scaling; not too sure how it will affect future releases.

there are some parts in which are incomplete as of 2\13\24
- api access and download of correct chromedriver version
- proper organization of code into clear methods