#Script to scrape several websites for info about the red planet

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def scrape():
    mars_dict = {}
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)  

    #NASA Mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div',class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_dict['News'] = {'Title':news_title,'Description':news_p}

    #3PL Mars Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_image = soup.find('img',class_='main_image')['src']
    feat_image_url = 'https://www.jpl.nasa.gov' + mars_image
    mars_dict['Featured Image'] = feat_image_url

    #Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find_all('div',class_='content')
    indicators = ['Sol','InSight']
    for tweet in mars_weather:
        twit_user = tweet.find('a',class_='account-group')['data-user-id']
        if twit_user == '786939553':
            weather_text = tweet.find('p', class_='tweet-text').text
            #if weather_text.split()[0] == 'Sol':
            if weather_text.split()[0] in indicators:
                break
        continue
    mars_dict['Weather'] = weather_text
    print(weather_text)

    #Mars Data
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    # df.columns = ['Parameter', 'Value(s)']
    # df.set_index('Parameter',inplace=True)
    web_table = df.to_html(classes='table',index=False)
    mars_dict['Facts'] = web_table
    #print(web_table)

    #Mars Hemispheres
    #First url stopped working, page was changed or deleted, or is down
    #url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url = 'https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # hemispheres = soup.find_all('div',class_='item')
    #hemis_array = []
    #url_front = 'https://astrogeology.usgs.gov'

    hemispheres = soup.find_all('a',class_='item')
    hemis_array = []
    url_front = 'https://astrogeology.usgs.gov'
    skip = [0,2,4,6]
    iter_num = 0
    for item in hemispheres:
        if iter_num in skip:
            iter_num += 1
            continue
        else:
            iter_num += 1
            item_dict = {}
            text_header = item.find('h3').text
            item_dict['Title'] = text_header

            #link = item.find('a',class_='itemLink')['href']
            link = item['href']
            full_url = url_front + link
            browser.visit(full_url)

            html = browser.html
            soup = bs(html, 'html.parser')

            big_link = soup.find('img',class_='wide-image')['src']
            item_dict['img_url'] = url_front + big_link

            hemis_array.append(item_dict)

            browser.back()
    mars_dict['Hemispheres'] = hemis_array
    #print(hemis_array)

#<img class="wide-image" src="/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg">

    # #click functions for elements wouldn't work, apparently a chrome driver issue, so I constructed a full link and used browser.visit
    # for item in hemispheres:
    
    #     item_dict = {}
    #     text_header = item.find('h3').text
    #     item_dict['Title'] = text_header
    
    #     link = item.find('a',class_='itemLink')['href']
    #     full_url = url_front + link
    #     browser.visit(full_url)
    
    #     html = browser.html
    #     soup = bs(html, 'html.parser')
    
    #     big_link = soup.find('img',class_='wide-image')['src']
    #     item_dict['img_url'] = url_front + big_link
    
    #     hemis_array.append(item_dict)
    
    #     browser.back()

    # mars_dict['Hemispheres'] = hemis_array

    return mars_dict
    





   

# <a href="/search/map/Mars/Viking/valles_marineris_unenhanced" class="item" style="height: 117px;">
# 			<img class="thumb description-thumb" src="/cache/images/624683252b31408dabbc5c051b12a777_valles_marineris_unenhanced.tif_thumb.png" alt="Valles Marineris Hemisphere Unenhanced thumbnail">
# 			<div class="description">
# 				<h3>Valles Marineris Hemisphere Unenhanced</h3>
# 	<p>Mosaic of the Valles Marineris hemisphere of Mars projected into…</p>
# 			</div>
# 		</a>

  


