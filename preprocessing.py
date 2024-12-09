#preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# Step 1: Load your data (Assuming you already have it in a DataFrame 'data')
# Example:
data = pd.read_csv('engineered_features.csv')

# Step 2: Handle Missing Data
# Check for any missing values
print(f"Missing Data:\n{data.isnull().sum()}")

# Fill missing values for numeric columns with the median
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())

# For non-numeric columns (like Conversation_ID), we can leave them as-is or fill them with a placeholder value
data['Conversation_ID'] = data['Conversation_ID'].fillna('Unknown_Conversation')

# Step 3: Feature Scaling
# If your data has features with different scales, it's essential to scale them.
# We will scale the numerical features using StandardScaler

scaler = StandardScaler()

# Select only numerical columns for scaling
numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns

# Apply scaling to numerical columns
data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

# Step 4: Encode Categorical Variables
# If there are any categorical variables, we will encode them. 
# Let's assume 'Protocol_Encoded' is a categorical column in your dataset.
# For categorical columns, we will use Label Encoding.

encoder = LabelEncoder()

# Apply label encoding on categorical columns (if any)
# Example: data['Protocol_Encoded'] = encoder.fit_transform(data['Protocol_Encoded'])

# If there are multiple categorical columns, apply encoding for each:
categorical_cols = ['Protocol_Encoded']  # Add any other categorical columns here
for col in categorical_cols:
    data[col] = encoder.fit_transform(data[col])

# Step 5: Split the Data into Features (X) and Target (y)
# Assuming your target variable (label) is called 'Target'
# Modify the target column name as per your dataset

X = data.drop('Target', axis=1)  # Drop the target column from features
y = data['Target']  # The target column

# Step 6: Split into Training and Test Sets
# This is necessary before training the model to evaluate its performance

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"Data Preprocessing Complete!\n")
print(f"Shape of training data: {X_train.shape}")
print(f"Shape of testing data: {X_test.shape}")

# Now your data is ready for machine learning models
