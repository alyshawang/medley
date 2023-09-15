from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import time
from random import randint
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import hashlib


# generate a random user-agent
def get_random_user_agent():
    user_agents = [
        # windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.31 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.31 Safari/537.36",
        # mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Safari/537.36",
        # linux
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    ]
    return random.choice(user_agents)

def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scrape_brandy_melville(category_url):
    try:
        options = ChromeOptions()
        options.add_argument("--headless")  # chrome in headless mode
        options.add_argument("--no-sandbox")  

        driver_path = "/Users/alyshawang/Downloads/chromedriver" 

        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        headers = {'User-Agent': get_random_user_agent()}
        driver.get(category_url)

        time.sleep(5)

        page_source = driver.page_source

        scroll_to_end(driver)

        prev_page_height = 0
        new_page_height = driver.execute_script("return document.body.scrollHeight")

        while prev_page_height != new_page_height:
            prev_page_height = new_page_height
            scroll_to_end(driver)
            new_page_height = driver.execute_script("return document.body.scrollHeight")

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        product_tiles = soup.select(".card-wrapper")

        product_data = []

        for tile in product_tiles:
            title_element = tile.select_one(".card-information__text.h5")
            image_element = tile.select_one(".media.media--transparent.media--adapt.media--hover-effect img[src]")
            price_element = tile.select_one(".price-item.price-item--regular")
            link_element = tile.select_one(".card-wrapper a[href]")


            if title_element and image_element and price_element:

                title_text = title_element.text.strip()
                image_url = "https:" + image_element.get("src")
                if image_url:
                    image_url = image_url.split(", ")[-1].split(" ")[0]
                price_text = price_element.text.strip()
                link_url = "https://us.brandymelville.com" + link_element.get("href")
                if link_url:
                    link_url = link_url.split(", ")[-1].split(" ")[0]


                product_data.append({"title": title_text, "image_url": image_url, "price": price_text, "link": link_url})  

        # print(product_data) 

        return product_data

    except Exception as e:
        print(f"Error while fetching Brandy Melville data: {e}")
        return []

def scrape_all_categories():
    category_urls = [
        "https://us.brandymelville.com/"
        "https://www.brandymelvilleusa.com/collections/clothing",
        "https://www.brandymelvilleusa.com/collections/basics",
        "https://www.brandymelvilleusa.com/collections/graphics",
        "https://www.brandymelvilleusa.com/collections/accessories"
    ]

    # print("Brandy Melville Products:")
    # for url in category_urls:
    #     product_data = scrape_brandy_melville(url)
    #     for product in product_data:
    #         print(f"Title: {product['title']}")
    #         print(f"Image URL: {product['image_url']}")
    #         print(f"Price: {product['price']}")
    #         print(f"URL: {product['link']}")
    #         print("\n")
   
    for url in category_urls:
        product_data_list = [] 

        print(f"Scraping products from {url}")
        product_data = scrape_brandy_melville(url)
        product_data_list.extend(product_data) 

        df = pd.DataFrame(product_data_list)

        url_hash = hashlib.md5(url.encode()).hexdigest()
        filename = f"{url_hash}.csv"
        
        df.to_csv(filename, index=False)
        print(f"Scraped data saved to '{filename}'")

if __name__ == "__main__":
    scrape_all_categories()