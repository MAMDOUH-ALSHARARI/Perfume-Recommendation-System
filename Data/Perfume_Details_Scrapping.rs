use playwright::Playwright;
use playwright::api::{Browser, BrowserContext, Page};
use std::{collections::HashMap, fs::File, io::Write, path::Path};
use tokio;

// Function to load perfume links from a JSON file
fn get_links_of_perfumes(file_path: &str) -> Vec<String> {
    let file = std::fs::read_to_string(file_path).expect("Failed to read JSON file");
    let data: HashMap<String, Vec<String>> =
        serde_json::from_str(&file).expect("Failed to parse JSON file");
    let base_url = "https://www.goldenscent.com";

    data.values()
        .flat_map(|perfume_list| {
            perfume_list.iter().map(|perfume| format!("{}{}", base_url, perfume))
        })
        .collect()
}

// Function to scrape perfume information
async fn scrape_perfume_info(url: &str, context: &BrowserContext) -> HashMap<String, String> {
    let mut product_info = HashMap::new();
    match context.new_page().await {
        Ok(page) => {
            if let Err(err) = page.goto(url, None).await {
                eprintln!("Failed to load page: {}", err);
                return product_info;
            }

            // Close message and stay on the web
            close_message(&page).await;
            click_stay_on_web_button(&page).await;

            // Extract name
            product_info.insert(
                "name".to_string(),
                page.eval("document.querySelector('h1')?.innerText", None)
                    .await
                    .unwrap_or_else(|_| "N/A".to_string()),
            );

            // Extract rating
            product_info.insert(
                "rating".to_string(),
                page.eval("document.querySelector('div.rc-midcontent h4')?.innerText", None)
                    .await
                    .unwrap_or_else(|_| "N/A".to_string()),
            );

            // Extract total ratings
            product_info.insert(
                "total_ratings".to_string(),
                page.eval("document.querySelector('div.rc-midcontent span')?.innerText", None)
                    .await
                    .unwrap_or_else(|_| "N/A".to_string()),
            );

            // Extract image
            product_info.insert(
                "img".to_string(),
                page.eval("document.querySelector('div.thumbnails__block.active img')?.src", None)
                    .await
                    .unwrap_or_else(|_| "N/A".to_string()),
            );

            // Extract final price
            product_info.insert(
                "final_price".to_string(),
                page.eval(
                    "document.querySelectorAll('div.savings')[0]?.innerText",
                    None,
                )
                .await
                .unwrap_or_else(|_| "N/A".to_string()),
            );

            // Extract additional attributes
            if let Ok(rows) = page.eval("Array.from(document.querySelectorAll('li.row'))", None).await {
                for row in rows.as_array().unwrap_or(&vec![]) {
                    let label = row["querySelector"]("div.col-md-2.p0")?.inner_text;
                    let value = row["querySelector"]("div.col-md-5.p0")?.inner_text;
                    if !label.is_empty() && !value.is_empty() {
                        product_info.insert(label, value);
                    }
                }
            }

            page.close().await.unwrap_or_else(|err| eprintln!("Failed to close page: {}", err));
        }
        Err(err) => {
            eprintln!("Failed to create a new page: {}", err);
        }
    }
    product_info
}

// Function to close any pop-up message
async fn close_message(page: &Page) {
    if let Ok(_) = page.eval(
        "document.querySelector('.ab-close-button[aria-label=\'Close Message\']')?.click()",
        None,
    )
    .await
    {
        println!("Closed message successfully.");
    }
}

// Function to click "Stay on the Web" button
async fn click_stay_on_web_button(page: &Page) {
    if let Ok(_) = page.eval("document.querySelector('button.c-t-w')?.click()", None).await {
        println!("Clicked 'Stay on the Web' button.");
    }
}

// Main function
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let start_time = std::time::Instant::now();

    // Initialize Playwright
    let playwright = Playwright::initialize().await?;
    let browser = playwright.chromium().launch(false).await?;
    let context = browser.new_context().await?;

    let perfume_links = get_links_of_perfumes("all_p_dict - Copy.json");
    let mut perfume_details = Vec::new();

    for (i, url) in perfume_links.iter().enumerate() {
        println!("Scraping {} of {}: {}", i + 1, perfume_links.len(), url);
        let product_info = scrape_perfume_info(url, &context).await;
        perfume_details.push(product_info);
    }

    // Save data to CSV
    let csv_file_path = "golden_scent_perfumes.csv";
    let mut wtr = csv::Writer::from_path(csv_file_path)?;
    for details in perfume_details {
        wtr.serialize(details)?;
    }
    wtr.flush()?;

    // Close browser
    context.close().await?;
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
