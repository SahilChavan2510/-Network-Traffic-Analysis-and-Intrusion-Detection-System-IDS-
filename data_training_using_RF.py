#data_training_using_RF.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler
import joblib

# Step 1: Load the labeled data (ensure your file path is correct)
data = pd.read_csv('labeled_network_traffic.csv')  # Replace with the actual path to your labeled data

# Step 2: Split the data into features (X) and target (y)
# Drop non-numeric columns that are not needed for training (e.g., 'Conversation_ID', 'Protocol_Encoded')
X = data.drop(['Target', 'Conversation_ID'], axis=1)
y = data['Target']  # The 'Target' column contains labels (Normal or Suspicious)

# Step 3: Preprocessing - Scaling the data (important for some algorithms)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Split the data into training and testing sets
# 70% training, 30% testing (you can adjust the test_size if needed)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Step 5: Train the Random Forest Classifier model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 6: Make predictions on the test data
y_pred = model.predict(X_test)

# Step 7: Evaluate the model's performance
# Print classification report for precision, recall, f1-score, and accuracy
print("Classification Report:\n", classification_report(y_test, y_pred))

# Display the confusion matrix to see how well the model performed
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot()

# Step 8: Save the trained model for future use
joblib.dump(model, 'traffic_classifier_model.pkl')  # Save the model
joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for future transformations

# Step 9: Save the preprocessed test data for further analysis if needed
data.to_csv('processed_labeled_traffic.csv', index=False)
