from flask import Flask, render_template, request, jsonify
import pickle
import json
import numpy as np

app = Flask(__name__)

# Load the trained model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Load the feature names
    with open('features.json', 'r') as f:
        features = json.load(f)
except FileNotFoundError:
    print("Error: model.pkl or features.json not found. Run train_model.py first.")
    exit(1)

@app.route('/')
def index():
    """
    Renders the homepage.
    Passes the feature list to the template to generate checkboxes dynamically.
    """
    return render_template('index.html', features=features)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives JSON data containing selected symptoms.
    Processes the data and returns the predicted disease.
    """
    try:
        data = request.get_json()
        selected_symptoms = data.get('symptoms', [])
        
        if not selected_symptoms:
            return jsonify({"error": "No symptoms selected"}), 400

        # Create a feature vector initialized with 0
        input_vector = [0] * len(features)
        
        # Set 1 for each selected symptom
        for symptom in selected_symptoms:
            if symptom in features:
                index = features.index(symptom)
                input_vector[index] = 1
        
        # Reshape input for model prediction
        final_features = [np.array(input_vector)]
        prediction = model.predict(final_features)
        
        return jsonify({
            "prediction": prediction[0]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5001)
