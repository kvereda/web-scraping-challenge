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
    #requested data
    news_title = news_soup.find_all('div', class_='content_title').a.text
    news_p = news_soup.find_all('div', class_='article_teaser_body').text

    #scraping images
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url) 
    html = browser.html
    img_soup = bs(html, "html.parser")
    image = img_soup.find("li", class_="slide").a["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    #scraping facts
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts_df = table[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_html_table = mars_facts_df.to_html()
    

