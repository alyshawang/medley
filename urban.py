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

# display = Display(visible=0, size=(1920, 1080))

# Generate a random user-agent
def get_random_user_agent():
    user_agents = [
        # Windows-based browsers
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
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    ]
    return random.choice(user_agents)

def scroll_to_end(driver):
    # Scroll to the end of the page to load more items dynamically
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for a short period to allow the page to load the new items
    time.sleep(2)

def scrape_urban(category_url):
    try:
        options = ChromeOptions()
        # options.add_argument("--headless")  # Run Chrome in headless mode (without a visible window)
        options.add_argument("--no-sandbox")  # Disable sandboxing for compatibility with some systems

        # Set the path to the Chrome driver executable
        # Download the driver that matches your Chrome browser version from: https://sites.google.com/a/chromium.org/chromedriver/downloads
        driver_path = "/Users/alyshawang/Downloads/chromedriver"  # Replace with the actual path to the chromedriver executable

        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        headers = {'User-Agent': get_random_user_agent()}
        driver.get(category_url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".o-pwa-product-tile"))
        )
        # Wait for the page to load (you can increase the wait time if needed)
        # time.sleep(10)

        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".c-pwa-tile-grid-inner"))
        # )

        # Get the page source after JavaScript rendering
        page_source = driver.page_source

        # scroll_to_end(driver)

        prev_page_height = 0
        new_page_height = driver.execute_script("return document.body.scrollHeight")

        # Keep scrolling until no more new items are loaded
        while prev_page_height != new_page_height:
            prev_page_height = new_page_height
            scroll_to_end(driver)
            new_page_height = driver.execute_script("return document.body.scrollHeight")
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".o-pwa-product-tile"))
            )
            time.sleep(2)  # Wait for 2 seconds after scrolling

        # Get the final page source after loading all items
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find the elements that contain product titles
        product_tiles = soup.select(".o-pwa-product-tile")

        # Extract and store the product titles and image URLs in separate lists
        product_data = []

        for tile in product_tiles:
            title_element = tile.select_one(".o-pwa-product-tile__heading")
            image_element = tile.select_one(".o-pwa-product-tile__media img[srcset]")
            price_element = tile.select_one(".c-pwa-product-price__current.s-pwa-product-price__current")


            if title_element and image_element and price_element:

                title_text = title_element.text.strip()
                image_url = image_element.get("src")
                price_text = price_element.text.strip()


                product_data.append({"title": title_text, "image_url": image_url, "price": price_text})  # Include price

        # print(product_data)  # Print the product data for debugging purposes

        return product_data

    except Exception as e:
        print(f"Error while fetching Brandy Melville data: {e}")
        return []

def scrape_all_categories():
    # List of URLs for different Brandy Melville categories
    category_urls = [
        "https://www.urbanoutfitters.com/en-ca/brands/kimchi-blue"
        # Add more URLs for other categories if needed
    ]

    print("Brandy Melville Products:")
    for url in category_urls:
        product_data = scrape_urban(url)
        for product in product_data:
            print(f"Title: {product['title']}")
            print(f"Image URL: {product['image_url']}")
            print(f"Price: {product['price']}")
            print("\n")
   
    # for url in category_urls:
    #     product_data_list = []  # List to store product data

    #     print(f"Scraping products from {url}")
    #     product_data = scrape_urban(url)
    #     product_data_list.extend(product_data)  # Extend the list with scraped data

    #     # Convert the list of dictionaries to a DataFrame
    #     df = pd.DataFrame(product_data_list)

    #     # Create a unique filename based on the hash of the URL
    #     url_hash = hashlib.md5(url.encode()).hexdigest()
    #     filename = f"{url_hash}.csv"
        
    #     # Save the DataFrame to a CSV file
    #     df.to_csv(filename, index=False)
    #     print(f"Scraped data saved to '{filename}'")

if __name__ == "__main__":
    scrape_all_categories()