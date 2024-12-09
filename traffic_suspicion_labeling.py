#traffic_suspicion_labeling.py
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load your data (replace with your actual CSV file path)
data = pd.read_csv('engineered_features.csv')

# Select the features to use for anomaly detection (drop non-numeric columns like 'Conversation_ID' and 'Protocol_Encoded')
X = data.drop(['Conversation_ID', 'Protocol_Encoded'], axis=1)

# Step 1: Scale the data (important for anomaly detection)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 2: Apply Isolation Forest for anomaly detection
# The 'contamination' parameter defines the expected proportion of outliers (suspicious data)
model = IsolationForest(contamination=0.1, random_state=42)  # Set contamination to a reasonable value
data['Anomaly_Score'] = model.fit_predict(X_scaled)

# Step 3: Label anomalies (1 = normal, -1 = anomalous)
data['Target'] = data['Anomaly_Score'].apply(lambda x: 'Normal' if x == 1 else 'Suspicious')

# Step 4: Review the labeled data
print(data.head())

# Step 5: Save the labeled data to a new file
data.to_csv('labeled_network_traffic.csv', index=False)
