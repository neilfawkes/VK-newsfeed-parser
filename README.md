# VK newsfeed parser

This script is parsing the newsfeed of vk.com using Selenium.
The input is login and password to vk.com, the output (author of the post, date, text, number of likes, shares and views) is saved in Excel file.
Also this script saves photos from posts (if there are some; in case of several photos it saves the first one) and creates the archive "images.zip".

Libraries used in this project:
- selenium
- chromedriver_binary
- BeautifulSoup
- datetime
- pandas
- urllib.request
- ssl
- shutil
- os
