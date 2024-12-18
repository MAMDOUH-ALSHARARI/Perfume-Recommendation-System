# Usecase-8-Project-5



# Perfume Recommendation System

## Our stramlit app link: https://perfume-recommendation.streamlit.app/

---
## Team Members
- Mamdouh Alsharari
- Abdullah alhokbanl
- Abdulkrem Al Shammari
- Taif Alanazi
- Adel Albagmi

---
## Problem Statement

The perfume industry offers a wide variety of products that differ in brand, fragrance family, target audience, and price. This diversity presents challenges for both consumers, who may struggle to find products aligned with their preferences, and retailers, who need to provide tailored recommendations to enhance customer satisfaction and drive sales.

This project aims to analyze a comprehensive perfume dataset to uncover market trends and categorize products based on their attributes, including:
1. **Fragrance Family**: Identifying preferences for specific fragrance types (e.g., floral, woody).
3. **Product Characteristics**: Assessing notes, concentration levels.
4. **Target Audience**: Understanding gender-based preferences and their influence on sales.

By achieving these goals, the project seeks to deliver insights that improve consumer recommendations and retailer strategies.

---

## Data Collection

The dataset used for this project contains detailed information about perfumes, including attributes such as:
- Product name
- Price
- Fragrance family
- Concentration level (e.g., Eau de Parfum)
- Target audience (e.g., gender-specific or unisex)
- Fragrance Character

**Data Source**:
- The data was collected from [Golden Scent](https://www.goldenscent.com/) via web scraping techniques. This involved extracting relevant information from product pages, such as descriptions, pricing, and classifications.

**Collection Methodology**:
1. **Platform Selection**:
   - Golden Scent was chosen for its extensive catalog of perfumes and detailed product descriptions.
2. **Scraping Tools**:
   - Tools such as `BeautifulSoup` and `Selenium` were used to scrape data from the website.
3. **Data Fields Extracted**:
   - Key fields like product name, price, brand, fragrance notes, and different fragrance Characteristics were extracted.
4. **Data Cleaning**:
   - Raw data was processed to handle inconsistencies and prepare it for machine learning.

---

## EDA Process

The exploratory data analysis (EDA) phase focused on understanding the dataset and identifying patterns. Key activities included:
- **Data Cleaning**: Addressed missing values, corrected inconsistencies, and handled outliers.
- **Univariate Analysis**: Analyzed the distribution of variables such as price and fragrance family.
- **Bivariate/Multivariate Analysis**: Explored relationships between variables (e.g., fragrance family vs. target gender).
- **Visualizations**: Created meaningful charts and graphs (e.g., histograms, scatter plots, and heatmaps) to uncover trends and insights.

---

## Modeling Process

The modeling process included the following steps:
1. **Model Selection**:
   - Two unsupervised learning models were chosen: K-Means and DBSCAN.
2. **Preprocessing**:
   - Encoded categorical variables and standardized numerical features.
3. **Feature Engineering**:
   - Created new features and refined existing ones to improve clustering performance.
4. **Model Training and Evaluation**:
   - Trained models using the processed dataset.
   - Evaluated models using silhouette score.
5. **Model Comparison**:
   - Compared models based on clustering quality and interpretability.

---

## Deploy the Model

The deployment phase involved creating an interactive application to demonstrate the model’s functionality:
1. **API Endpoint**:
   - Developed a FastAPI endpoint to serve the clustering model.
2. **User Interface**:
   - Built a Streamlit application featuring:
     - Visualizations of clustering results.
     - An interface for users to input new data points and view recommendations.
3. **Integration**:
   - Connected the Streamlit app with the FastAPI endpoint for real-time recommendations.

---
