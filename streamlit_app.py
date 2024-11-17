import streamlit as st
import requests

# API URL
API_URL = "http://127.0.0.1:8000"  # Update with your FastAPI server URL if deployed remotely

# Streamlit app title and header
st.title("Perfume Recommender System")

st.write("Select the features to get perfume recommendations.")

# Dropdown options for the features
gender_options = ['Kids', 'Men', 'Unisex', 'Women']
character_options = [
    'Charismatic', 'Classical', 'Dynamic', 'Extravagant', 'Feminine', 'Glamorous',
    'Masculine', 'Modern', 'Natural', 'Romantic', 'Sensual', 'Sophisticated'
]
fragrance_family_options = [
    'Aquatic', 'Arabian', 'Aromatic', 'Aromatic,Citrus', 'Aromatic,Woody', 'Chypre', 'Citrus',
    'Dry Woods', 'Floral', 'Floral Oriental', 'Floral Woody', 'Floral,Aromatic',
    'Floral,Citrus', 'Floral,Fruity', 'Floral,Fruity,Chypre', 'Floral,Leather',
    'Floral,Oriental', 'Floral,Woody', 'Fruity', 'Fruity,Chypre', 'Fruity,Floral Oriental',
    'Fruity,Oud', 'Fruity,Woody', 'Fruity,Woody,Leather', 'Green', 'Leather', 'Mossy Woods',
    'Musky', 'Oriental', 'Oud', 'Soft Floral', 'Soft Oriental', 'Sweet', 'Woody',
    'Woody Oriental', 'Woody,Leather', 'Woody,Oud', 'Woody,Woody'
]
concentration_options = [
    'Eau Fraiche', 'Eau de Cologne', 'Eau de Parfum', 'Eau de Parfum Intense',
    'Eau de Senteur', 'Eau de Toilette', 'Extrait de Parfum', 'Parfum', 'Perfume Oil'
]

# Dropdown inputs for the user
gender = st.selectbox("Gender", gender_options)
character = st.selectbox("Character", character_options)
fragrance_family = st.selectbox("Fragrance Family", fragrance_family_options)
concentration = st.selectbox("Concentration", concentration_options)

# Submit button
if st.button("Get Recommendations"):
    # Create payload for the API request
    payload = {
        "Gender": gender,
        "Character": character,
        "Fragrance_Family": fragrance_family,
        "Concentration": concentration
    }

    # Make POST request to the `/recommend` endpoint
    response = requests.post(f"{API_URL}/recommend", json=payload)

    # Handle response
    if response.status_code == 200:
        recommendations = response.json()
        
        if recommendations:
            st.write("### Top Recommendations:")
            for rec in recommendations:
                st.write(f"**Name:** {rec['الاسم']}")
                st.write(f"**Rating:** {rec['rating']} ⭐")
                st.write(f"**Total Ratings:** {rec['total_ratings']}")
                st.write(f"**Price:** {rec['السعر النهائي']} SAR")
                st.markdown(f"![Alt Text]({rec['img']})")
                st.markdown("---")
        else:
            st.write("No recommendations found!")
    else:
        st.error("Failed to fetch recommendations. Please check the API connection.")
