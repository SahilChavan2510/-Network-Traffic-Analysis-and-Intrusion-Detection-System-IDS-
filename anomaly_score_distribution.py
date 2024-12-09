#anamoly_score_distribution.py
import matplotlib.pyplot as plt
import pandas as pd

# Load the labeled data (replace with your actual file path)
data = pd.read_csv('labeled_network_traffic.csv')  # Update this to the file you saved

# Plot histogram of the Anomaly Score
plt.hist(data['Anomaly_Score'], bins=20)
plt.title('Anomaly Score Distribution')
plt.xlabel('Anomaly Score')
plt.ylabel('Frequency')
plt.show()
