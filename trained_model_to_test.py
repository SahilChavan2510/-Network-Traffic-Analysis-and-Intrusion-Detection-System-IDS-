import pandas as pd
import joblib

# Step 1: Load the saved model and scaler
model = joblib.load('traffic_classifier_model.pkl')  # Load the trained model
scaler = joblib.load('scaler.pkl')  # Load the scaler used during training

# Step 2: Load the new data
new_data = pd.read_csv('engineered_features4.csv')  # Load the feature-engineered new data

# Step 3: Add placeholder for missing column
new_data['Anomaly_Score'] = 0  # Add a dummy Anomaly_Score column

# Step 4: Ensure column order matches training data
X_new = new_data.drop(['Conversation_ID'], axis=1)

# Step 5: Scale the new data
X_new_scaled = scaler.transform(X_new)

# Step 6: Make predictions
predictions = model.predict(X_new_scaled)

# Step 7: Add predictions to the new data
new_data['Prediction'] = ['Normal' if label == 1 else 'Suspicious' for label in predictions]

# Step 8: Save and display the results
print(new_data[['Conversation_ID', 'Prediction']])  # Display predictions
new_data.to_csv('predicted_traffic.csv', index=False)  # Save the predictions
