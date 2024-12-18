from itertools import repeat
from playwright.sync_api import sync_playwright
import time
import json

import traceback

from pyparsing import C

def wait_images(page):
    page.evaluate("""
                () => {
                    return new Promise((resolve) => {
                        const images = Array.from(document.images);
                        const loaded = images.map(img => img.complete);
                        if (loaded.every(Boolean)) {
                            resolve();
                        } else {
                            const onLoad = () => {
                                if (images.every(img => img.complete)) {
                                    resolve();
                                }
                            };
                            images.forEach(img => img.addEventListener('load', onLoad));
                        }
                    });
                }
                """)
    print("All images loaded.")

def list_event_listeners(page):
    try:
        # Run JavaScript in the page context to list event listeners
        listeners = page.evaluate("""
        () => {
            const elements = document.querySelectorAll('*');
            const listeners = [];
            elements.forEach(element => {
                const clone = element.cloneNode(false);
                const eventListeners = getEventListeners(element);
                if (Object.keys(eventListeners).length > 0) {
                    listeners.push({
                        element: clone.outerHTML,
                        events: eventListeners
                    });
                }
            });
            return listeners;
        }
        """)
        # Print event listeners
        for listener in listeners:
            print(f"Element: {listener['element']}")
            print("Events:")
            for event, handlers in listener['events'].items():
                print(f"  {event}:")
                for handler in handlers:
                    print(f"    Handler: {handler.listener}")
    except Exception as e:
        print("Error fetching event listeners:", e)

def execute_xpath(page, xpath):
    try:
        # Use query_selector with the xpath prefix
        element = page.query_selector(f"xpath={xpath}")
        if element:
            print("Element found!")
            return element
        else:
            print("Element not found.")
            return None
    except Exception as e:
        print(f"Error executing XPath: {xpath}")
        print(str(e))
        return None

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

def scrape_brands_names(context):
   
        
        # Launch a headless browser
        #browser = p.chromium.launch(headless=True)
        #print("browser launching")
        #browser_context = browser.new_context()
       # browser_context.set_default_timeout(60000)
        #main_page = browser.new_page()
        
        main_page = context.new_page()
        #print("page created")
        # Navigate to the brands page
        main_page.goto("https://www.goldenscent.com/en/brands.html",timeout=60000)
        
        # Close pop-up message if present
        close_message(main_page)
        click_stay_on_web_button(main_page)
        # Select all brand elements
        brands = main_page.query_selector_all('.brands--list-li a')
        print("brands elements collected")
        brand_names_li=[]
        print(f"all elements collected {len(brands)}")
        #for brand in brands:
        main_page.wait_for_load_state('networkidle')
        brand_names_li= [brand.query_selector('span').inner_text() for brand in brands]
        print(f"all names collected {len(brand_names_li)}")
        main_page.close()
        # Cache is automatically cleared when a new context is created. No explicit `clear_cache` method is required.
        #browser_context.close()  # Close context to free resources
        # Close the browser
        return brand_names_li
        
def scrape_brands_links_by_name(brand_name_to_find,context):
    
        try:
            
             # Find the brand element using XPath
            xpath1 = f"//a[@class=\"block no-underline product-link\"][span[normalize-space(text())=\"{brand_name_to_find}\"]]"
            
             # Find the perfume count using XPath
            xpath2 = f"//label[@class='ais-RefinementList-label'][span[normalize-space(text())='Perfume']]"

           
            brand_element=False
            brand_link="-"
            C=False
            while not C:
                
                try:
                    
                   # browser_context = browser.new_context()
                    
                    main_page = context.new_page()
                    main_page.goto("https://www.goldenscent.com/en/brands.html", timeout=20000)
                    print("context launched")
                    # Wait for all images to load
                    #wait_images(main_page)
                
                    #list_event_listeners(page)
                    # Close pop-up message if present
                    close_message(main_page)
                    click_stay_on_web_button(main_page)
                    print("Page loaded")
                    brand_element = main_page.query_selector(xpath1)
                    
                    with main_page.expect_navigation(wait_until="networkidle",timeout=30000):
                        brand_element.click(force=True)
                        #brand_element.evaluate("element => element.click()")
                        print("Element clicked!")
                    time.sleep(3)
                    brand_link=main_page.url
                    
                    if (brand_link =="-") or (brand_link.endswith(".html")):
                        main_page.close()
                        #browser_context.close()  
                        continue
                    try:
                        Perfume_element = main_page.locator(xpath2)
                        # Now you can interact with the brand_element
                        count_text = Perfume_element.locator("span.ais-RefinementList-count").inner_text()                      
                        count=int(count_text)
                    except:
                        count=0
                  
                    
                except:
                    main_page.close()
                   # browser_context.close()  
                    continue
                
                C=True
                print(f"Brand clicked: {brand_name_to_find}")
                print(f"After URL: {brand_link}")
                
            main_page.close()
           # browser_context.close()  # Close context to free resources
            print("Finished seccussfully")
            
            return brand_link, count
            
        except Exception as e:
            #print(f"Generated XPath: {xpath}")
            print(f"Error loading page or interacting with it: {str(e)}")
            print("Detailed traceback:")
            traceback.print_exc()  # This prints the full stack trace of the exception
            main_page.close()
            #browser_context.close()  # Close context to free resources
            print("Except")
            return "-",count
           
  
        
                

     
        
        
with sync_playwright() as p:
     # Launch a headless browser
      # Specify Chrome executable path
     # Launch Chrome
     browser_context = p.chromium.launch_persistent_context(
        user_data_dir="/tmp/playwright",
        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
        headless=False
    )
     print("Browser launched")
    
     # Run the scraping function
     brand_names_li=scrape_brands_names(browser_context)
     print(len(brand_names_li))
     all_b_dict={}
     
     for i, name in enumerate(brand_names_li, start=1):
         while True:
             brand_link,count=scrape_brands_links_by_name(name,browser_context)
             print(f"{i}-{name}-{brand_link}-{count}") 
             if brand_link!="-":
                 brand_dict={}
                 brand_dict["Name"]=name
                 brand_dict["link"]=brand_link
                 brand_dict["Count"]=count
                 all_b_dict[i]=brand_dict
                 break
         #if i==3:
             #break   
         
        

     browser_context.close()
     print("Browser closed")
    
    

# Save all_data_dict as a JSON file
with open("brand_links.json", "w", encoding="utf-8") as file:
    json.dump(all_b_dict, file, ensure_ascii=False, indent=4)

