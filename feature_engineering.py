#feature_engineering.py
import pandas as pd
import numpy as np

# Load the cleaned dataset
df = pd.read_csv("network_traffic4.csv")  # Replace with your filename

# Ensure Time is a datetime object
df['Time'] = pd.to_datetime(df['Time'])

# Derive Conversation ID (Source IP + Destination IP pair)
df['Conversation_ID'] = df['Source IP'] + '-' + df['Destination IP']

# Feature 1: Session Duration
df['Session_Start'] = df.groupby('Conversation_ID')['Time'].transform('min')
df['Session_End'] = df.groupby('Conversation_ID')['Time'].transform('max')
df['Session_Duration'] = (df['Session_End'] - df['Session_Start']).dt.total_seconds()

# Feature 2: Packet Count and Length Aggregation
df['Packet_Count'] = df.groupby('Conversation_ID')['Length'].transform('count')
df['Total_Length'] = df.groupby('Conversation_ID')['Length'].transform('sum')
df['Avg_Packet_Length'] = df['Total_Length'] / df['Packet_Count']

# Feature 3: Flag Summaries
flag_columns = ['SYN_Flag', 'ACK_Flag', 'FIN_Flag', 'RST_Flag', 'PSH_Flag', 'URG_Flag']
for flag in flag_columns:
    df[f'{flag}_Count'] = df.groupby('Conversation_ID')[flag].transform('sum')

# Feature 4: TTL Statistics
df['Avg_TTL'] = df.groupby('Conversation_ID')['TTL'].transform('mean')

# Feature 5: Protocol Encoding
protocol_mapping = {
    'TCP': 1,
    'UDP': 2,
    'TLS': 3,
    'DNS': 4
}
df['Protocol_Encoded'] = df['Protocol'].map(protocol_mapping)

# Feature 6: Payload Analysis
df['Payload_Length'] = df['Payload'].str.len().fillna(0)

# Final Aggregated Features per Conversation
agg_df = df.groupby('Conversation_ID').agg({
    'Session_Duration': 'mean',
    'Packet_Count': 'max',
    'Total_Length': 'mean',
    'Avg_Packet_Length': 'mean',
    'SYN_Flag_Count': 'sum',
    'ACK_Flag_Count': 'sum',
    'FIN_Flag_Count': 'sum',
    'RST_Flag_Count': 'sum',
    'PSH_Flag_Count': 'sum',
    'URG_Flag_Count': 'sum',
    'Avg_TTL': 'mean',
    'Protocol_Encoded': 'first',  # Keep one protocol per conversation
    'Payload_Length': 'mean',
}).reset_index()

# Save the engineered dataset
agg_df.to_csv("engineered_features4.csv", index=False)

print("Feature engineering completed and saved to 'engineered_features.csv'.")
