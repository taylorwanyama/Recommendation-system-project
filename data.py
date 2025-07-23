import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

baseurl = 'https://www.kilimall.co.ke/'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image:apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

product_links = []

print("--- Initializing Selenium WebDriver for Category Pages ---")
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless') # Uncomment this line to run in headless mode (no browser UI)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('--incognito') 
chrome_options.add_argument('--disable-dev-shm-usage')

# Adding Arguments to bypass Selenium detection ---
chrome_options.add_argument('--disable-blink-features=AutomationControlled') # Disables 'navigator.webdriver'
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # Removes 'Chrome is being controlled by automated test software' infobar
chrome_options.add_experimental_option('useAutomationExtension', False) # Disables automation extension

# Sets a human-like User-Agent which ensures that this matches what a real Chrome browser uses)
chrome_options.add_argument(f"user-agent={headers['User-Agent']}")

driver = None
try:
    # If chromedriver is in PATH, simply:
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute JavaScript to override navigator.webdriver, even if flag is set
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    print("Selenium WebDriver initialized successfully for category page scraping.")
except WebDriverException as e:
    print(f"❌ Error initializing WebDriver: {e}")
    print("Please ensure chromedriver is installed and its path is correctly configured.")
    print("You can download chromedriver from: https://googlechromelabs.github.io/chrome-for-testing/")
    exit()

print("\n--- Scraping Category Pages (using Selenium) ---")
for i in range(1, 21): # Attempting up to 20 pages
    category_url = f"https://www.kilimall.co.ke/category/health-beauty?id=482&form=category&source=category|allCategory|Health+&+Beauty&page={i}"
    print(f"Fetching category page: {category_url}")
    try:
        driver.set_page_load_timeout(40) 
        driver.get(category_url)

        # Wait for products to load. Use a more robust selector if 'product-item' is too broad.
        # Sometimes, waiting for a specific part of the product item (like the link itself) is better.
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-item a[href]"))
        )
        
        # Scroll down to ensure all products on the page are loaded, if it's a lazy-loading page
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) # Give time for new content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


        products = driver.find_elements(By.CSS_SELECTOR, "div.product-item a[href]")
        if not products:
            print(f"No product links found on page {i}. This might be the last page or an issue with the selector.")
            break

        for product_element in products:
            link = product_element.get_attribute('href')
            if link and not link.startswith('http'):
                link = baseurl.rstrip('/') + '/' + link.lstrip('/')
            if link and link not in product_links:
                product_links.append(link)

        print(f"  Collected {len(products)} links from page {i}. Total unique links: {len(product_links)}")
        time.sleep(random.uniform(1.5, 3.5)) # Longer delay between pages to be gentle

    except TimeoutException:
        print(f"❌ Timeout fetching category page {i}. Page took too long to load or elements not found.")
        continue # Try next page
    except Exception as e:
        print(f"❌ Unexpected Error processing category page {i}: {e}")
        break # Stop if a general error occurs

print(f"Collected {len(product_links)} unique product links in total from category pages.")

# The rest of the code for scraping individual product pages (using the same driver)
# and data processing remains largely the same.
scraped_products = []
print("\n--- Scraping Individual Product Pages (using Selenium) ---")
for i, link in enumerate(product_links):
        
    print(f"Fetching product page: {link}")
    try:
        driver.set_page_load_timeout(40) 
        time.sleep(random.uniform(1, 2)) #Small random delay before navigating
        driver.get(link)

        time.sleep(random.uniform(1, 3)) # Gives the page some time to initially load

        # Wait for the product title to ensure the main content is loaded
        # Product name must be extracted BEFORE category for proper filtering
        product_name = "N/A"
        try:
            name_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "product-title"))
            )
            product_name = name_element.text.strip()
        except TimeoutException:
            print(f"  Warning: Product name not found (Timeout) for {link}")

        # Scroll down to ensure all dynamic content loads, especially for reviews/ratings
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);") 
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2) 

        # --- REVISED CODE FOR CATEGORY AND SUB-CATEGORY EXTRACTION ---
        main_category = "N/A"
        sub_category = "N/A"
        try:
            # Find all breadcrumb items' name divs
            breadcrumb_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.breadcrumbs-item div.b-name.name"))
            )
            
            all_breadcrumb_texts = [elem.text.strip() for elem in breadcrumb_elements]
            
            # Filter out "Home", the specific product_name, and empty strings
            filtered_breadcrumbs = [
                text for text in all_breadcrumb_texts 
                if text.lower() != "home" and text != product_name and text != ""
            ]
            
            # If the path starts with "Health & Beauty", remove it for more specific categorization
            if filtered_breadcrumbs and filtered_breadcrumbs[0] == "Health & Beauty":
                filtered_breadcrumbs = filtered_breadcrumbs[1:]

            # Now, attempt to extract based on specific request and then general position
            beauty_index = -1
            fragrance_index = -1
            
            try:
                beauty_index = filtered_breadcrumbs.index("Beauty")
            except ValueError:
                pass
            
            try:
                fragrance_index = filtered_breadcrumbs.index("Fragrance")
            except ValueError:
                pass

            if beauty_index != -1 and fragrance_index != -1 and fragrance_index == beauty_index + 1:
                # Specific case: Beauty followed by Fragrance
                main_category = "Beauty"
                sub_category = "Fragrance"
            elif beauty_index != -1:
                # If only Beauty is found, make it the main category and take the next if available
                main_category = "Beauty"
                if beauty_index + 1 < len(filtered_breadcrumbs):
                    sub_category = filtered_breadcrumbs[beauty_index + 1]
                else:
                    sub_category = "N/A"
            elif fragrance_index != -1:
                # If only Fragrance is found, make it sub-category and set main to Health & Beauty
                main_category = "Health & Beauty" # Default parent category if not found above
                sub_category = "Fragrance"
            else:
                # Fallback: take the last two meaningful categories if specific ones aren't found
                if len(filtered_breadcrumbs) >= 2:
                    main_category = filtered_breadcrumbs[-2]
                    sub_category = filtered_breadcrumbs[-1]
                elif len(filtered_breadcrumbs) == 1:
                    main_category = filtered_breadcrumbs[0]
                    sub_category = "N/A"
                elif "Health & Beauty" in all_breadcrumb_texts: # If nothing more specific was found, but H&B was in original path
                    main_category = "Health & Beauty"
                    sub_category = "N/A"

        except TimeoutException:
            print(f"  Warning: Breadcrumb elements not found (Timeout) for {link}")
        except NoSuchElementException:
            print(f"  Warning: Breadcrumb elements not found (NoSuchElement) for {link}")
        # --- END REVISED CODE ADDITION ---


        # Using Selenium to find elements directly for critical data (product_name is already found above)
        product_price = "N/A"
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "sale-price"))
            )
            product_price = price_element.text.strip()
        except TimeoutException:
            print(f"  Warning: Product price not found (Timeout) for {link}")

        product_discount_rate = "N/A"
        try:
            discount_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "discount-rate"))
            )
            product_discount_rate = discount_element.text.strip()
        except TimeoutException:
            try:
                discount_element = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "discount"))
                )
                product_discount_rate = discount_element.text.strip()
            except TimeoutException:
                pass 

        
        product_rating = "N/A"
        rating_element = None
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.rate"))
            )
            product_rating = rating_element.text.strip()

            start_time = time.time()
            while product_rating == '5.0' and (time.time() - start_time < 5):
                time.sleep(0.5) 
                product_rating = rating_element.text.strip()
                if product_rating != '5.0': 
                    break
            
            if product_rating == '5.0' and "perfume" in product_name.lower(): 
                 print(f"  Note: Rating for '{product_name}' remained '5.0' after extended wait, might be default or missing actual reviews.")

        except TimeoutException:
            print(f"  Warning: Rating element not found (Timeout) for {link}")
        except NoSuchElementException:
            print(f"  Warning: Rating element not found (NoSuchElement) for {link}")


        product_reviews = "0 Customer reviews" 
        reviews_element = None
        try:
            reviews_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='#pc__product-detail__reviews'] span.reviews"))
            )
            product_reviews = reviews_element.text.strip()

            start_time = time.time()
            while product_reviews == '0 Customer reviews' and (time.time() - start_time < 5):
                time.sleep(0.5) 
                product_reviews = reviews_element.text.strip()
                if product_reviews != '0 Customer reviews': 
                    break
            
            if product_reviews == '0 Customer reviews' and "perfume" in product_name.lower():
                print(f"  Note: Customer reviews for '{product_name}' remained '0 Customer reviews' after extended wait, might be default or missing actual reviews.")

        except TimeoutException:
            print(f"  Warning: Reviews element not found (Timeout) for {link}")
        except NoSuchElementException:
            print(f"  Warning: Reviews element not found (NoSuchElement) for {link}")
        
            
        if product_name and product_price and product_name != "N/A" and product_price != "N/A":
            product_info = {
                "Product_name": product_name,
                "Rating": product_rating,
                "Price": product_price,
                "Discount_rate": product_discount_rate,
                "Customer_reviews": product_reviews,
                "Category": main_category, 
                "Sub_Category": sub_category, 
                #"URL": link 
            }
            scraped_products.append(product_info)
            print(f"✅ Scraped: {product_name} - {product_price} - Rating: {product_rating} - Category: {main_category}, Sub-Category: {sub_category}") 
        else:
            print(f"❌ Skipped (missing essential data or errors): {link}")

        time.sleep(random.uniform(0.8, 2.5)) 

    except TimeoutException:
        print(f"❌ Timeout fetching product details for {link}. Page took too long to load or elements not found within the specified time.")
    except Exception as e:
        print(f"❌ Unexpected Error processing {link}: {e}")

if driver: 
    driver.quit()
    print("\n--- Selenium WebDriver closed. ---\n")

# --- NEW FUNCTION TO REFINE CATEGORIES (Now working on Sub_Category too) ---
def refine_categories(df):
    df_copy = df.copy()
    
    # Define mapping rules for generic sub-categories based on product name
    category_mapping_rules = {
        'Sets': [
            {'keywords': ['perfume', 'fragrance'], 'new_sub_category': 'Perfume Sets'},
            {'keywords': ['shampoo', 'conditioner', 'hair growth'], 'new_sub_category': 'Hair Care Sets'},
            {'keywords': ['skincare', 'serum', 'cream'], 'new_sub_category': 'Skincare Sets'},
            {'keywords': ['makeup', 'cosmetic'], 'new_sub_category': 'Makeup Sets'},
        ],
        'Hair Clippers & Accessories': [
            {'keywords': ['clipper', 'trimmer', 'shaver'], 'new_sub_category': 'Hair Clippers & Trimmers'},
        ],
        'Irons': [
            {'keywords': ['straightener', 'straightening'], 'new_sub_category': 'Hair Straighteners'},
            {'keywords': ['curling', 'curler'], 'new_sub_category': 'Curling Irons'},
        ],
        'Hair Combs': [
            {'keywords': ['brush', 'brushes'], 'new_sub_category': 'Hair Brushes & Combs'},
        ],
        "Men's": [ 
            {'keywords': ['perfume', 'fragrance'], 'new_sub_category': "Men's Fragrance"},
            {'keywords': ['shaving', 'grooming'], 'new_sub_category': "Men's Grooming"},
        ]
    }

    for index, row in df_copy.iterrows():
        current_sub_category = row['Sub_Category']
        product_name = row['Product_name'].lower()

        # Prioritize refining Sub_Category first
        if current_sub_category in category_mapping_rules:
            for rule in category_mapping_rules[current_sub_category]:
                if any(kw in product_name for kw in rule['keywords']):
                    df_copy.loc[index, 'Sub_Category'] = rule['new_sub_category']
                    break 
        
    return df_copy



if scraped_products:
    df = pd.DataFrame(scraped_products)
    print("\n--- Scraped Data Head (Before Refinement) ---\n", df.head())

    if 'Price' in df.columns:
        df['Price'] = df['Price'].astype(str).str.replace('KSh', '').str.replace(',', '').astype(float)
    if 'Rating' in df.columns:
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Apply the category refinement
    df = refine_categories(df) 

    print("\n--- Data with Numeric Price and Rating (and REFINE CATEGORY/SUB-CATEGORY) ---\n", df[['Product_name', 'Category', 'Sub_Category', 'Price', 'Rating', 'Customer_reviews']].head())

    output_filename = "kilimall_beauty_health_products_scraped.csv" # Updated output name
    df.to_csv(output_filename, index=False)
    print(f"\n--- Data saved to {output_filename} ---")
else:
    print("\nNo products were scraped.")