import pandas as pd
import json

# Path to the JSON file
file_path = "C:/Users/dohai/Tuwaiq-DS-ML-bootcamp-V-8/CV_Projects/Perfume-Recommendation-System/Data/golden_scent_perfumes.json"
# "C:\Users\dohai\Tuwaiq-DS-ML-bootcamp-V-8\CV_Projects\Perfume-Recommendation-System\Data\golden_scent_perfumes.json"
# Load the JSON data
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)
non_unique_columns=[]
unique_columns=[]
# Iterate over each dictionary and its keys
for idx, perfume in enumerate(data):
    print(f"Perfume {idx + 1}: done")
    for key, value in perfume.items():
        non_unique_columns.append(key)
        #print(f"  {key}: {value}")
        
    #print("-" * 50)  # Separator for readability
unique_columns=list(set(non_unique_columns))
print("Non_uniques")
print(len(non_unique_columns))
print("-" * 50) 
print("Uniques")
print(len(unique_columns))
print("-" * 50) 


# Combine 'Size' and 'size' into a single column
#df['combined_size'] = df['Size'].combine_first(df['size'])
# Display the DataFrame
print(len(df.columns))
#print(df['size'])
#print(df['combined_size'])
# Drop the old columns if needed
#df = df.drop(columns=['Size', 'size'])


# Optional: Save the DataFrame to a CSV file if needed
df.to_csv('golden_scent_perfumes6.csv', index=False, encoding='utf-8')
