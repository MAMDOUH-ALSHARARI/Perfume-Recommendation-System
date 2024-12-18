import streamlit as st
import requests



# API URL
API_URL = "https://perfume-recommendation-system.onrender.com"  # Update with your FastAPI server URL if deployed remotely

# Streamlit app title and header
st.title("Perfume Recommender System ⚱️✨")

st.markdown("""
**With a wide range of perfumes to choose from, it can be challenging to find your perfect scent.** 🌿

**We're here to help!** Based on your **character** and **preferred fragrance family**, we'll provide you with top recommendations that match your unique style. ✨

**Discover the perfumes that resonate with you and make every moment unforgettable.** 
""")

# , and **desired concentration**
st.write("## Let's begin exploring your perfect fragrance!")

# Dropdown options for the features
gender_options = [
    # 'Kids',
      'Men', 'Unisex', 'Women']
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
# concentration_options = [
#     'Eau Fraiche', 'Eau de Cologne', 'Eau de Parfum', 'Eau de Parfum Intense',
#     'Eau de Senteur', 'Eau de Toilette', 'Extrait de Parfum', 'Parfum', 'Perfume Oil'
# ]

# Dropdown inputs for the user
gender = st.selectbox("Select the fragrance group that represents you", gender_options)
character = st.selectbox("How would you like your fragrance to express your character? 🎭", character_options)
fragrance_family = st.selectbox("What fragrance family best captures your essence?", fragrance_family_options)
# concentration = st.selectbox("What concentration suits your style?", concentration_options)

# Submit button
if st.button("Get Recommendations"):
    # Create payload for the API request
    payload = {
        "Gender": gender,
        "Character": character,
        "Fragrance_Family": fragrance_family
        # ,
        # "Concentration": concentration
    }

    # Make POST request to the `/recommend` endpoint
    response = requests.post(f"{API_URL}/recommend", json=payload)

    # Handle response
    if response.status_code == 200:
        recommendations = response.json()
        
        if recommendations:
            
            st.write("### Here are your top perfume picks!")
            for rec in recommendations:
                st.write(f"**Name:** {rec['الاسم']}")
                st.write(f"**Rating:** {rec['rating']} ⭐")
                st.write(f"**Total Ratings:** {rec['total_ratings']}")
                st.write(f"**Price:** {rec['السعر النهائي']} SAR")
                st.markdown(f"""
                           <div style="width: 300px; height: 300px; overflow: hidden; border-radius: 8px;">
                           <img src="{rec['img']}" alt="Perfume Image" style="width: 100%; height: 100%; object-fit: cover;"></div>
                           """, unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.write("No recommendations found!")
    else:
        st.error("Failed to fetch recommendations. Please check the API connection.")
