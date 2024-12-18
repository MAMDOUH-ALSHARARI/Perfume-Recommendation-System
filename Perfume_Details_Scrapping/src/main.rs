use playwright::Playwright;
use std::{collections::HashMap, fs};
use tokio;
use serde_json;
use std::path::Path;



// Function to load perfume links from a JSON file
fn get_links_of_perfumes(file_path: &str) -> Vec<String> {
    let file = fs::read_to_string(file_path).expect("Failed to read JSON file");
    let data: HashMap<String, Vec<String>> =
        serde_json::from_str(&file).expect("Failed to parse JSON file");
    let base_url = "https://www.goldenscent.com";

    data.values()
        .flat_map(|perfume_list| {
            perfume_list.iter().map(|perfume| format!("{}{}", base_url, perfume))
        })
        .collect()
}
//async fn scrape_perfume_info(url: &str, page: &playwright::api::Page) -> HashMap<String, String>
async fn scrape_perfume_info(url: &str, context: &playwright::api::BrowserContext) -> HashMap<String, String> 
{
    let mut product_info = HashMap::new();
    //let page = context.new_page().await?;
    let page_result = context.new_page().await;
    // Check if page is created successfully
    if let Ok(page) = page_result 
    
    {
        // Navigate to the product page
        if let Err(err) = page.goto_builder(url).goto().await 
        {
            eprintln!("Failed to load page: {}", err);
        }
        else 
        {
             // Extract product name
             if let Ok(Some(name)) = page.evaluate::<(), Option<String>>("document.querySelector('h1')?.innerText", ()).await
             {
                 product_info.insert("name".to_string(), name);
             }

              // Extract all price details dynamically
              if let Ok(prices) = page.evaluate::<(), String>(r#"(() => {let prices = {};let savingsElement = document.querySelector('.price-content .savings'); if (savingsElement) { let savings = savingsElement.querySelector('span')?.innerText.trim(); let currentPrice = savingsElement.querySelector('span:nth-child(2)')?.innerText.trim(); let originalPrice = savingsElement.querySelector('.striked-price')?.innerText.trim();  prices['savings'] = savings; prices['current_price'] = currentPrice; prices['original_price'] = originalPrice; }  let specialPriceElement = document.querySelector('.price-content .special'); if (specialPriceElement) { prices['special_price'] = specialPriceElement.innerText.trim(); }  return JSON.stringify(prices); })() "#, (), ).await 
              {
              let parsed_prices: serde_json::Value = serde_json::from_str(&prices).unwrap_or_default();
              if let Some(savings) = parsed_prices.get("savings") 
              {
                  product_info.insert("savings".to_string(), savings.as_str().unwrap_or("").to_string());
              }
              if let Some(current_price) = parsed_prices.get("current_price") 
              {
                  product_info.insert("current_price".to_string(), current_price.as_str().unwrap_or("").to_string());
               }
             if let Some(original_price) = parsed_prices.get("original_price") 
             {
                 product_info.insert("original_price".to_string(), original_price.as_str().unwrap_or("").to_string());
             }
            if let Some(special_price) = parsed_prices.get("special_price") 
            {
                product_info.insert("special_price".to_string(), special_price.as_str().unwrap_or("").to_string());
             }
             }

             // Extract size
             if let Ok(Some(size)) = page .evaluate::<(), Option<String>>("document.querySelector('.sizebtn.active')?.innerText", ()) .await { product_info.insert("size".to_string(), size); }

             // Extract delivery notes
             if let Ok(Some(delivery)) = page .evaluate::<(), Option<String>>("document.querySelector('.delivery-notes')?.innerText", ()) .await { product_info.insert("delivery".to_string(), delivery); }


             // Extract fragrance details dynamically
             let detail_keys = vec![ "Brand", "Gender", "Product Type", "Character", "Fragrance Family", "Size", "Ingredients", "Concentration","Top Notes","Middle Notes","Base Notes", ];


             for key in detail_keys { let selector = format!( "Array.from(document.querySelectorAll('li.row')).find(e => e.innerText.includes('{}'))?.querySelector('div:nth-child(2)')?.innerText", key );  if let Ok(Some(value)) = page.evaluate::<(), Option<String>>(selector.as_str(), ()).await { product_info.insert(key.to_string(), value); } }


             // Extract product description
             if let Ok(Some(description)) = page .evaluate::<(), Option<String>>("document.querySelector('.product_description')?.innerText", ()) .await { product_info.insert("description".to_string(), description.trim().to_string()); }



             // Extract image URL
             if let Ok(Some(image_url)) = page .evaluate::<(), Option<String>>("document.querySelector('.hooper-slide img')?.src", ()) .await { product_info.insert("image_url".to_string(), image_url); }


             // Extract average rating
             if let Ok(Some(avg_rating)) = page .evaluate::<(), Option<String>>("document.querySelector('.avg-rating')?.innerText", ()) .await { product_info.insert("average_rating".to_string(), avg_rating); }



             // Extract total reviews
             if let Ok(Some(reviews)) = page .evaluate::<(), Option<String>>("document.querySelector('.rc-midcontent span')?.innerText", ()) .await { product_info.insert("total_reviews".to_string(), reviews); }





        }
            
        // Close the page safely to avoid memory leaks
        if let Err(err) = page.close(Some(false)).await            
        {                
        eprintln!("Failed to close page: {}", err);          
        }
    } 
    else 
    {
        eprintln!("Failed to create a new page");
    }
    product_info
}


    // Navigate to the product page
    //if let Err(err) = page.goto_builder(url).goto().await {
        //eprintln!("Failed to load page: {}", err);
        //return product_info;
    //}

    
    
    // Safely close the page without propagating errors
  //  if let Err(err) = page.close().await {
   // eprintln!("Failed to close page: {}", err);
//}
  //  Ok(product_info)
//}





#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let start_time = std::time::Instant::now();

    let playwright = Playwright::initialize().await?;
    // Initialize Playwright
    let playwright = Playwright::initialize().await?;
    let browser = playwright
        .chromium()
        .launcher()
        .executable(Path::new("C:/Program Files/Google/Chrome/Application/chrome.exe")) // Use Chrome
        .headless(false) // Set to true if you want headless mode
        .launch()
        .await?;
    let context = browser.context_builder().build().await?;
    let page = context.new_page().await?;

    let perfume_links = get_links_of_perfumes("C:/Users/dohai/Tuwaiq-DS-ML-bootcamp-V-8/CV_Projects/Perfume-Recommendation-System/Data/all_p_dict.json");
    //"\Data\all_p_dict - Copy.json"
    //"\Data\all_p_dic.json"
    //"C:\Users\dohai\Tuwaiq-DS-ML-bootcamp-V-8\CV_Projects\Perfume-Recommendation-System\Data\all_p_dict - Copy.json"
    let mut perfume_details = Vec::new();

    for (i, url) in perfume_links.iter().enumerate() {
        println!("Scraping {} of {}: {}", i + 1, perfume_links.len(), url);
        let product_info = scrape_perfume_info(url, &context).await;
        perfume_details.push(product_info);
    }

    let json_file_path = "golden_scent_perfumes.json";
    fs::write(json_file_path, serde_json::to_string_pretty(&perfume_details)?)?;

    browser.close().await?;

    let elapsed = start_time.elapsed();
    println!(
        "Time spent: {} hours, {} minutes, and {} seconds",
        elapsed.as_secs() / 3600,
        (elapsed.as_secs() % 3600) / 60,
        elapsed.as_secs() % 60
    );

    Ok(())
}
