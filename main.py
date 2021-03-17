from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
from pandas import ExcelWriter
from urllib.request import urlopen
import ssl
import shutil
import os


if __name__ == "__main__":
    user = input('Input login: ')
    password = input('Input password: ')
    
    URL = "https://www.vk.com/"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    user_input = driver.find_elements_by_name("email")[1]
    user_input.send_keys(user)
    password_input = driver.find_elements_by_name("pass")[1]
    password_input.send_keys(password)

    submit = driver.find_element_by_id("index_login_button")
    submit.click()
    url = driver.command_executor._url
    session_id = driver.session_id
    driver = webdriver.Remote(command_executor=url,desired_capabilities={})
    driver.close()
    driver.session_id = session_id

    driver.get("https://www.vk.com/feed")
    news_page = driver.page_source
    soup = bs(news_page, 'html.parser')

    basedir_path = os.getcwd()
    images_path = os.path.join(basedir_path, 'images/')
    title = 2
    news_feed = soup.find_all("div", class_="_post post page_block post--with-likes deep_active")

    authors_list, dates_list, texts_list, likes_list, shares_list, views_list = [], [], [], [], [], []

    for item in news_feed:
        authors_list.append(item.find("a", class_="author").text)

        date = item.find("span", {"class":"rel_date rel_date_needs_update"})
        dates_list.append(datetime.fromtimestamp(int(date['time'])).strftime('%d.%m.%y'))

        text = item.find("div", class_="wall_post_text")
        if text:
            texts_list.append(text.text)
        else:
            texts_list.append('')

        likes = item.find("a", {"class":"like_btn like _like"})
        if likes:
            likes_list.append(likes['data-count'])
        else:
            likes_list.append('0')

        shares = item.find("a", {"class":"like_btn share _share"})
        if shares:
            shares_list.append(shares['data-count'])
        else:
            shares_list.append('0')

        views = item.find("div", class_="like_views _views")
        if views:
            views_list.append(views.text)
        else:
            views_list.append('0')

        img = item.find("a", {"aria-label":"фотография"})
        if img:
            a = img['onclick']
            image = (f"{a[(a.find('https:')):(a.find('.jpg'))]}.jpg")
            image = image.replace('\\', '')
            print(image)
            try:
                context = ssl._create_unverified_context()
                jpg = urlopen(image, context=context).read()
                out = open(images_path+"/{}.jpg".format(title), 'wb') 
                out.write(jpg)
                out.close()
            except Exception:
                print('Unsupported link type')
            title+=1
        else:
            print('No photo')
            title+=1

    driver.quit()

    df = pd.DataFrame({
        'Group': authors_list,
        'Date': dates_list,
        'Contents': texts_list,
        'Liked': likes_list,
        'Shared': shares_list,
        'Views': views_list
    })

    writer = ExcelWriter('stats.xlsx')
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

    shutil.make_archive('images', 'zip', 'images')

    print('\Done!')
