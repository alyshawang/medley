import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from fake_useragent import UserAgent
import time
import random
from time import sleep

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.31 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.31 Safari/537.36",
        # macOS-based browsers
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Safari/537.36",
        # Linux-based browsers
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",    ]
    return random.choice(user_agents)

def scroll_to_end(driver):
    # Scroll to the end of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the content to load

def scrape_ssense(category_url):
    try:
        options = ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode (without a visible window)
        options.add_argument("--no-sandbox")  # Disable sandboxing for compatibility with some systems

        # Set the path to the Chrome driver executable
        # Download the driver that matches your Chrome browser version from: https://sites.google.com/a/chromium.org/chromedriver/downloads
        driver_path = "/Users/alyshawang/Downloads/chromedriver"  # Replace with the actual path to the chromedriver executable

        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        headers = {'User-Agent': get_random_user_agent()}
        driver.get(category_url)

        # Wait for the page to load (you can increase the wait time if needed)
        time.sleep(5)

        # Get the page source after JavaScript rendering
        page_source = driver.page_source
        

        scroll_to_end(driver)

        prev_page_height = 0
        new_page_height = driver.execute_script("return document.body.scrollHeight")

        # Keep scrolling until no more new items are loaded
        while prev_page_height != new_page_height:
            prev_page_height = new_page_height
            scroll_to_end(driver)
            new_page_height = driver.execute_script("return document.body.scrollHeight")

        # Get the final page source after loading all items
        page_source = driver.page_source
        print(page_source)  # Print the product data for debugging purposes

        soup = BeautifulSoup(page_source, "html.parser")

        # Find the elements that contain product titles
        product_tiles = soup.select(".itemContainer ng-scope")

        # Extract and store the product titles and image URLs in separate lists
        product_data = []

        for tile in product_tiles:
            title_element = tile.select_one(".itemTitle ng-binding")
            image_element = tile.select_one(".itemCover img[src]")

            if title_element and image_element:
                title_text = title_element.text.strip()
                image_url = "https:" + image_element.get("srcset")
                if image_url:
                    image_url = image_url.split(", ")[-1].split(" ")[0]

                product_data.append({"title": title_text, "image_url": image_url})

        print(product_data)  # Print the product data for debugging purposes

        return product_data

    except Exception as e:
        print(f"Error while fetching Brandy Melville data: {e}")
        return []

def scrape_all_ssense():
    # List of URLs for different Brandy Melville categories
    category_urls = [
        # "https://us.brandymelville.com/",
        # "https://www.brandymelvilleusa.com/collections/clothing",
        # "https://www.brandymelvilleusa.com/collections/basics",
        # "https://www.brandymelvilleusa.com/collections/graphics",
        "https://www.yesstyle.com/en/women-tops/list.html/bcc.14090_bpt.46#/sb=136&s=10&bpt=46&bcc=14090&l=1&pn=4&bt=37"
        # Add more URLs for other categories if needed
    ]

    print("SSENSE Products:")
    for url in category_urls:
        product_data = scrape_ssense(url)
        for product in product_data:
            print(f"Title: {product['title']}")
            print(f"Image URL: {product['image_url']}")
            print("\n")

if __name__ == "__main__":
    # scrape_all_categories()
    scrape_all_ssense()