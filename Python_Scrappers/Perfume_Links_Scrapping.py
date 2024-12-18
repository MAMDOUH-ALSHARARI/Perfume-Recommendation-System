from itertools import repeat
from playwright.sync_api import sync_playwright
import time
import json

import traceback

from pyparsing import C

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
    

def get_links_of_brands():
    
    # Load the JSON file
    file_path = 'brand_links_sorted.json'  # Replace with the path to your JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    names_list = [item['Name'] for item in data.values()]
    links_list = [item['link'] for item in data.values()]
    count_list = [item['Count'] for item in data.values()]

    return names_list,links_list,count_list

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
        
def scrape_perfume_links_by_brand(url,context):
    
        try:
            
            C=False
            while not C:
                
                try:
                    
                   # browser_context = browser.new_context()
                    
                    main_page = context.new_page()
                    main_page.goto(url, timeout=20000)
                    print("context launched")
                    close_message(main_page)
                    click_stay_on_web_button(main_page)
                    # Click "Perfume" category
                    
                    print("Page loaded")
                    scroll_amount = 1400
                   # Scroll to load all items
                  
                    last_height = 0
                    click_perfume(main_page)
                    while True:
                     
                        
                        #Scroll to load all items
                       # last_height = main_page.execute_script("return document.body.scrollHeight")
                       # scroll_up_step = 400  # Amount to scroll up after scrolling down
                       # scroll_step = 8000  # Amount to scroll down in each iteration
                       # main_page.execute_script(f"window.scrollBy({scroll_amount}, {50});")
                       # main_page.evaluate("window.scrollBy(0, {scroll_amount});")
                        main_page.evaluate(f"window.scrollBy(0, {scroll_amount});")
                        main_page.evaluate(f"window.scrollBy({scroll_amount}, -200);")
                        print(f"scrolled {scroll_amount}")
                        scroll_amount+=1400
                        time.sleep(2)  # Allow content to load
                       
                        new_height = main_page.evaluate("document.body.scrollHeight")
                        #main_page.execute_script(f"window.scrollBy({scroll_amount}, {100});")
                        #scroll_amount += 100
                        #time.sleep(1)
                       # main_page.execute_script(f"window.scrollBy({scroll_amount}, {200});")
                       # scroll_amount += 200
                       # time.sleep(1)
                       # new_height = main_page.execute_script("return document.body.scrollHeight")
                        time.sleep(2)
 
                        print(f"last_height: {last_height}, new_height: {new_height}")
                        if new_height == last_height:                   
                       
                           break
                        last_height = new_height
                    #Collect links for the category
                    # Collect links for the category
                    golden_links = main_page.query_selector_all("a[href*='/p/']")
                    golden_hrefs = [link.get_attribute('href') for link in golden_links]
                    print(f"perfumes collected  {len(golden_hrefs)} ")

                    C=True
                    main_page.close()
                    
                except:
                    C=True
                    main_page.close()
                    return []
                return golden_hrefs  
        except Exception as e:
            #print(f"Generated XPath: {xpath}")
            print(f"Error loading page or interacting with it: {str(e)}")
            print("Detailed traceback:")
            traceback.print_exc()  # This prints the full stack trace of the exception
            main_page.close()
            #browser_context.close()  # Close context to free resources
            print("OuterExcept")
            return []
           
  
               
with sync_playwright() as p:
     # Launch a headless browser
      # Specify Chrome executable path
     # Launch Chrome
     brand_name_li, brand_links_li,brand_counts_li=get_links_of_brands()
     
     print(brand_name_li[0])
     print(brand_links_li[0])
     print(brand_counts_li[0])
     all_p_dict={}
     print("finshied test")
     
     browser_context = p.chromium.launch_persistent_context(
        user_data_dir="/tmp/playwright",
        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
        headless=False
    )
     print("Browser launched")
    
    
     
     for i, url in enumerate(brand_links_li, start=0):
         print(f"{i+1}-{brand_name_li[i]}-{url}-{brand_counts_li[i]}") 
             
         if int(brand_counts_li[i])==0:
              print("continue") 
              continue
              
                                
                 
                 #if perfume_link_li =="-":
                    
         while True:
             perfume_link_li=scrape_perfume_links_by_brand(url,browser_context)
             if perfume_link_li:
                 print(f"perfumes collected for {brand_name_li[i]} ")
                 break
             print(f"repeat, perfumes not collected for {brand_name_li[i]}")
             
         all_p_dict[brand_name_li[i]]=perfume_link_li
        
         #if i>=1:
          #   print("End loop")
          #   break   
         
        

     browser_context.close()
     print("Browser closed")
    
    

# Save all_data_dict as a JSON file
with open("all_p_dict.json", "w", encoding="utf-8") as file:
    json.dump(all_p_dict, file, ensure_ascii=False, indent=4)

    