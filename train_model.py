import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import json
import os

# 1. Load the dataset
dataset_path = "disease_dataset_1080.csv"
df = pd.read_csv(dataset_path)

# 2. Separate features and target
# 'disease' is the target column, others are binary symptoms
X = df.drop('disease', axis=1)
y = df['disease']

# Save feature column names for the frontend
features = X.columns.tolist()
with open('features.json', 'w') as f:
    json.dump(features, f)
print(f"Features saved to features.json: {len(features)} symptoms found.")

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and train the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Training Complete!")
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 6. Save the trained model using pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved as model.pkl")
