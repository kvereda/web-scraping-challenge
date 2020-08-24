from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import time
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    browser = init_browser()
    #scraping the news
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, "html.parser")
    news_data = news_soup.find("li", class_="slide")
    news_title = news_data.find_all('div', class_='content_title').a.text
    news_p = news_data.find_all('div', class_='article_teaser_body').text

    #scraping images
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url) 
    html = browser.html
    img_soup = bs(html, "html.parser")
    image = img_soup.find("li", class_="slide").a["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    #scraping facts
    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    mars_facts_df = table[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_html_table = mars_facts_df.to_html()
    
    #scraping hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    hemispheres_soup = bs(html, "html.parser")
    data = hemispheres_soup.find_all("div", class_="item")
    hemisphere_img_urls = []

    for d in data:
    
        title = d.find("h3").text

        img_url = d.a["href"]
        url = "https://astrogeology.usgs.gov" + img_url
        response = requests.get(url)
        
        soup = bs(response.text,"html.parser")
        mars_url = soup.find("img", class_="wide-image")["src"]
        full_url = "https://astrogeology.usgs.gov" + mars_url
        
        hemisphere_img_urls.append({"title": title, "img_url": full_url})

    #dictionary
    mars_data = {
        "news_title": news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "mars_html_table": mars_html_table,
        "hemisphere_img_urls": hemisphere_img_urls
    }

    browser.quit()
    return mars_data
