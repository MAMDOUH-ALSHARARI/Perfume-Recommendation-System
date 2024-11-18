from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import joblib
import pandas as pd

# Load pre-trained KMeans model and scaler
kmeans_model = joblib.load('kmeans.joblib')  # Replace with your model file path
scaler = joblib.load('scaler.joblib')  # Replace with your scaler file path
data = pd.read_csv('final.csv')  # Preload dataset

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}
# get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

from pydantic import BaseModel
# Pydantic model for user input validation
class InputFeatures(BaseModel):
    Gender: str
    Character: str
    Fragrance_Family: str
    # Concentration: str

# Preprocessing function
def preprocess_input(input_features: InputFeatures):
    # Encode the input features
    encoded_input = {
        'Gender': {
            # 'Kids': 0,
            'Men': 0,
            'Unisex': 1,
            'Women': 2
        }.get(input_features.Gender, -1),
        'Character': {
            'Charismatic': 0,
            'Classical': 1,
            'Dynamic': 2,
            'Extravagant': 3,
            'Feminine': 4,
            'Glamorous': 5,
            'Masculine': 6,
            'Modern': 7,
            'Natural': 8,
            'Romantic': 9,
            'Sensual': 10,
            'Sophisticated': 11
        }.get(input_features.Character, -1),
        'Fragrance_Family': {
            'Aquatic': 0,
            'Arabian': 1,
            'Aromatic': 2,
            'Aromatic,Citrus': 3,
            'Aromatic,Woody': 4,
            'Chypre': 5,
            'Citrus': 6,
            'Dry Woods': 7,
            'Floral': 8,
            'Floral Oriental': 9,
            'Floral Woody': 10,
            'Floral,Aromatic': 11,
            'Floral,Citrus': 12,
            'Floral,Fruity': 13,
            'Floral,Fruity,Chypre': 14,
            'Floral,Leather': 15,
            'Floral,Oriental': 16,
            'Floral,Woody': 17,
            'Fruity': 18,
            'Fruity,Chypre': 19,
            'Fruity,Floral Oriental': 20,
            'Fruity,Oud': 21,
            'Fruity,Woody': 22,
            'Fruity,Woody,Leather': 23,
            'Green': 24,
            'Leather': 25,
            'Mossy Woods': 26,
            'Musky': 27,
            'Oriental': 28,
            'Oud': 29,
            'Soft Floral': 30,
            'Soft Oriental': 31,
            'Sweet': 32,
            'Woody': 33,
            'Woody Oriental': 34,
            'Woody,Leather': 35,
            'Woody,Oud': 36,
            'Woody,Woody': 37
        }.get(input_features.Fragrance_Family, -1),
        # 'Concentration': {
        #     'Eau Fraiche': 0,
        #     'Eau de Cologne': 1,
        #     'Eau de Parfum': 2,
        #     'Eau de Parfum Intense': 3,
        #     'Eau de Senteur': 4,
        #     'Eau de Toilette': 5,
        #     'Extrait de Parfum': 6,
        #     'Parfum': 7,
        #     'Perfume Oil': 8
        # }.get(input_features.Concentration, -1)
    }

    # Convert dictionary values to a list in the correct order
    features_list = [encoded_input[key] for key in sorted(encoded_input)]


    scaled_features = scaler.transform([list(encoded_input.values())])
    return scaled_features

@app.get("/predict")
def predict(input_features: InputFeatures):
    return preprocess_input(input_features)

@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocess_input(input_features)
    y_pred = kmeans_model.predict(data)
    return {"pred": y_pred.tolist()[0]}

# Recommendation endpoint
@app.post("/recommend")
async def recommend(input_features: InputFeatures):
    try:
        # Preprocess user input
        scaled_input = preprocess_input(input_features)
        
        # Predict the cluster
        cluster_label = kmeans_model.predict(scaled_input)[0]
        
        # Filter perfumes in the predicted cluster
        cluster_data = data[data['Cluster'] == cluster_label]
        
        # Sort and fetch the top 5 recommendations
        recommendations = cluster_data.sort_values(
            by=['rating', 'total_ratings'], ascending=False
        ).head(5)
        
        # Return recommendations as a list of dictionaries
        return recommendations[['الاسم', 'rating', 'total_ratings', 'السعر النهائي', 'img']].to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
