# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests

def scrape():
    # %%
    # Necessary for Mac
    # !which chromedriver


    # Mac executable path
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    # Windows executable path(comment out '!which chromedrive' to make it work)
    executable_path = {'executable_path': 'chromedriver.exe'}

    browser = Browser('chrome', **executable_path, headless=True)


    # %%
    # define url and visit
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    sleep(2)


    # %%
    # create dictinary
    scrape_mars = {}

    # %% [markdown]
    # <h1>NASA Mars News</h1>

    # %%

    # html parser boiler plate
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # have to dig into article before pulling news title to avoid conflict in navbar
    articles = soup.find('div', class_='image_and_description_container')
    scrape_mars['news_title'] = articles.find('div', class_='content_title').get_text()
    scrape_mars['news_p'] = articles.find('div', class_='article_teaser_body').get_text()


    # %%
    scrape_mars

    # %% [markdown]
    # <h1>JPL Mars Space Images - Featured Image</h1>

    # %%

    # define url and visit
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    sleep(1)


    # %%

    # html parser boiler plate
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    base_url= 'https://www.jpl.nasa.gov'

    # have to click image to see source
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(1)


    # %%
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('div', id='fancybox-lock')
    scrape_mars['featured_image_url'] = base_url+image.find('img')['src']
    print(scrape_mars)

    # %% [markdown]
    # <h1>Mars Weather</h1>

    # %%

    # define url and visit
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    sleep(1)


    # %%
    # html parser boiler plate
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweets = soup.find_all('div',lang="en",dir='auto')

    # tweet = tweets[2].find('span').get_text()
    # print(tweet)

    # loop through recent tweets to find the first weather tweet
    for tweet in tweets:
        output = tweet.find('span').get_text()
        if 'InSight' in output:
            print(output)
            scrape_mars['mars_weather'] = output
            break

    # %% [markdown]
    # <h1>Mars Facts</h1>

    # %%

    # define url and visit
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    sleep(1)

    #  html parser boiler plate
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # %%

    # https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]
    mars_facts = df.to_html(index=False,header=False, classes='table-striped')
    scrape_mars['mars_facts']=mars_facts

    # %% [markdown]
    # <h1>Mars Hemispheres</h1>

    # %%
    # define url and visit
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    sleep(1)

    #  html parser boiler plate
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    og_url= 'https://astrogeology.usgs.gov/'

    # /cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg
    # 


    # %%
    images = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    for image in images:

        # declare  html parser(for secomnd time going through loop and beyond)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # get url to main image
        thumb_url = image.find('a')['href']
        
        # set image title for hemisphere_image_urls
        image_title = image.find('h3').get_text()
        
        # visit site for main image and restart html parser
        browser.visit(og_url+thumb_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        sleep(1)

        # grab full image url
        img_url = soup.find('img',class_='wide-image')['src']

        # add title and image url to hemisphere_image_urls
        hemisphere_image_urls.append({'title':image_title,'url':og_url+img_url})

        # go back to main page
        browser.back()

        
    scrape_mars['hemisphere_image_urls'] = hemisphere_image_urls

    alt_url_list = {'Cerberus Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg',
 'Schiaparelli Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg',
 'Syrtis Major Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg',
 'Valles Marineris Hemisphere Enhanced': 'https://astrogeology.usgs.gov//cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}

    alt_image_url_list = []

    for k,v in alt_url_list.items():
        alt_image_url_list.append({'title':k,'url':v})

    scrape_mars['alt_img_url']=alt_image_url_list

    # Close the browser after scraping
    browser.quit()

    # Return results
    return scrape_mars


