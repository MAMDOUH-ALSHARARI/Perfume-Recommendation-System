from itertools import repeat
from playwright.sync_api import sync_playwright
import time
import json
import pandas as pd


import traceback

from pyparsing import C

def scrape_perfume_info(url,context):
    # Initialize a dictionary to store the perfume information
    product_info = {}
    try:
        main_page = context.new_page()
        main_page.goto(url, timeout=20000)
        print("context launched")
        close_message(main_page)
        click_stay_on_web_button(main_page)   
        print("Page loaded")
        
        # Scroll to load all items
        scroll_amount = 1400                     
        last_height = 0 
        """
        while True:
            main_page.evaluate(f"window.scrollBy(0, {scroll_amount});")
            main_page.evaluate(f"window.scrollBy({scroll_amount}, -200);")
            print(f"scrolled {scroll_amount}")
            scroll_amount+=1400
            time.sleep(2)  # Allow content to load
            new_height = main_page.evaluate("document.body.scrollHeight")
            print(f"last_height: {last_height}, new_height: {new_height}")
            if new_height == last_height:
                break
            last_height = new_height
        """
        #main_page.query_selector
        # Loop through each unique href and navigate to it
        
        try:
            
            

            # Extract the name
           # name_element = main_page.query_selector('div', {'class': "col-xs-12"})
            # Extract perfume details
            name_element = main_page.query_selector('h1')
            product_info['name'] = name_element.inner_text().strip() if name_element else None
            
            rating_element = main_page.query_selector('div.rc-midcontent h4')
            product_info['rating'] = rating_element.inner_text().strip() if rating_element else None
            
            total_ratings_element = main_page.query_selector('div.rc-midcontent span')
            product_info['total_ratings'] = total_ratings_element.inner_text().strip() if total_ratings_element else None


            img_element = main_page.query_selector('div.thumbnails__block.active img')
            product_info['img'] = img_element.get_attribute('src') if img_element else None

            
        
            

            
            #savings
            # Extract price details
            price_element = main_page.query_selector_all('div.savings')

           # price_element = main_page.query_selector('div.price-content span.special')
            product_info['final_price'] = (
            price_element[0].inner_text()
            #.strip().replace(',', '')
            if price_element else None
        
           )
            
            # Extract the final price (discounted or regular)
           # price_content = main_page.query_selector('div', {'class': 'price-content'})
           # final_price = None
            
           # if price_content:
                # Check if there is a discount (look for 'savings' class)
            #    savings_div = price_content.find('div', {'class': 'savings'})
              #  if savings_div:
                    # Extract the discounted price from the second span within 'savings'
                 #   spans = savings_div.find_all('span')
                 #   if len(spans) > 1:
                #        final_price = re.search(r'\d+', spans[1].get_text(strip=True)).group()
               # else:
                   #if there's no discount, use the regular price in 'special'
               #    special_price = price_content.find('span', {'class': 'special'})
                #   if special_price:
                 #      final_price = re.search(r'\d+', special_price.get_text(strip=True)).group()

            # Store the final price if found
        #    if final_price:
         #       product_info["final_price"] = int(final_price)  # Convert to integer for consistency
         #   else:
          #      product_info["final_price"] = None
           #     print(f"Price not found on perfume")
     
            # Extract additional attributes
            #rows = main_page.query_selector_all('li', {'class': 'row'})
            # Extract additional attributes
            rows = main_page.query_selector_all('li.row')
            for row in rows:
                label_element = row.query_selector('div.col-md-2.p0')
                value_element = row.query_selector('div.col-md-5.p0')
                label = label_element.inner_text().strip() if label_element else None
                value = value_element.inner_text().strip() if value_element else None
                if label and value:
                    product_info[label] = value

            print(f"Scraped: {product_info['name']}")
            main_page.close()
            return product_info

        except Exception as e:
            print(f"Error on perfume info: {e}")
            main_page.close()
            return {}
    except Exception as e:
        print(f"Error on loading perfume page: {e}")
        main_page.close()
        return {}
    return product_info
           
def click_perfume(main_page):
    print("clicking Perfume")
    try:
        xpath = f"//label[@class='ais-RefinementList-label'][span[normalize-space(text())='Perfume']]"
        Perfume_element = main_page.locator(xpath)    
        Perfume_element.click(force=True)
        time.sleep(2) 
        print("perfume choice clicked")
    except:
        print("perfume choice not clicked")
    
def get_links_of_perfumes():
    
    # Load the JSON file
    file_path = 'all_p_dict.json'  # Replace with the path to your JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Define the base URL
    base_url = "https://www.goldenscent.com"

    # Collect all perfumes into a single list using list comprehension
    # all_perfumes = [perfume for perfume_list in data.values() for perfume in perfume_list]
    all_perfume_links = [f"{base_url}{perfume}" for perfume_list in data.values() for perfume in perfume_list]


    # Check the length of the collected list
    print(f"Total perfumes collected: {len(all_perfume_links)}")

    return all_perfume_links

def click_stay_on_web_button(page):
    try:
        # Check if the button exists and click it
        button_selector = "button.c-t-w"
        page.wait_for_selector(button_selector, timeout=10000)
        
        button = page.query_selector(button_selector)
        if button:
            button.click()
            print("Clicked 'STAY ON THE WEB' button successfully.")
        else:
            print("'STAY ON THE WEB' button not found.")
    except Exception as e:
        print("Error interacting with 'STAY ON THE WEB' button")
              #: {str(e)}")
        #print("Detailed traceback:")
        #traceback.print_exc()  # This prints the full stack trace of the exception

def close_message(page):
    try:
        # Wait for the close button to appear
        page.wait_for_selector(".ab-close-button[aria-label='Close Message']", timeout=10000)

        close_button = page.query_selector(".ab-close-button[aria-label='Close Message']")
        if close_button:
            close_button.click()
            print("Message closed successfully.")
            time.sleep(2)  # Add a short delay to ensure the message is fully dismissed
        else:
            print("No close message found.")
    except Exception as e:
        print("Could not close the message:")
              #, str(e))
        #print("Detailed traceback:")
        #traceback.print_exc()  # This prints the full stack trace of the exception
                   
  
# Record the start time
start_time = time.time()

with sync_playwright() as p:
     # Launch a headless browser
      # Specify Chrome executable path
     # Launch Chrome
     perfume_links_li=get_links_of_perfumes()
     perfume_links_li_not=[]
     print(len(perfume_links_li))
     # Initialize a list to store perfume details with both name and price
     perfume_details = []
     product_info={}
     print("finshied test")
     
     
     

        
     browser_context = p.chromium.launch_persistent_context(
        user_data_dir="/tmp/playwright",
        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
        headless=False
    )
     print("Browser launched")
    
    
     
     for i, url in enumerate(perfume_links_li, start=0):
         print(f"{i+1}-{perfume_links_li[i]}") 
        
                    
         while True:
             product_info=scrape_perfume_info(url,browser_context)
             if product_info:
                 
                 print("perfume info scrapped for")
                 break
             print("repeat, perfume info not scrapped")
             perfume_links_li_not.append(url)
             break
            # break
             
         # Append the perfume information to the list
         perfume_details.append(product_info)
         # Convert the list of perfume details to a DataFrame
         golden_df = pd.DataFrame(perfume_details)
         # Display the DataFrame with perfume names and final prices
         #print(golden_df[:1])
        
        # if i>=1:
          #   print("End loop")
          #   break   
         
        

     browser_context.close()
     print("Browser closed")
    
    
     #Save the DataFrame to a CSV file
     golden_df.to_csv("golden_scent_perfumes4.csv", index=False, encoding="utf-8-sig")
 
# Record the end time
end_time = time.time()

# Calculate the total time spent
total_time_seconds = end_time - start_time
hours, remainder = divmod(total_time_seconds, 3600)
minutes, seconds = divmod(remainder, 60)

# Print the total time in hours, minutes, and seconds
print(f"Time spent: {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds")