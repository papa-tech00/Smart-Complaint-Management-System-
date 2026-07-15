import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

import joblib
# Load the cleaned dataset
df = pd.read_csv("data/complaints_clean.csv")

# Display dataset information
print("Dataset Loaded Successfully!")
print("Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())
# Display all column names
print("\nDataset Columns:")
print(df.columns)
# Prepare features (X) and labels (y)
X = df["clean_text"]
y = df["category"]

print("\nFeatures and Labels Prepared Successfully!")
print("Total Complaints:", len(X))
print("Total Categories:", len(y))

print("\nSample Complaint:")
print(X.iloc[0])

print("\nSample Category:")
print(y.iloc[0])
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nDataset Split Successfully!")

print("Training Data:", len(X_train))
print("Testing Data :", len(X_test))
# Convert text into TF-IDF features
vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("\nTF-IDF Vectorization Completed!")

print("Training Matrix Shape:", X_train_tfidf.shape)
print("Testing Matrix Shape :", X_test_tfidf.shape)
# Train the Naive Bayes model
model = MultinomialNB()

model.fit(X_train_tfidf, y_train)

print("\nModel Training Completed Successfully!")
# Make predictions on the test data
y_pred = model.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Testing Completed!")
print("Model Accuracy:", round(accuracy * 100, 2), "%")
# Display classification report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
# Save the trained model
joblib.dump(model, "models/model.pkl")

# Save the TF-IDF vectorizer
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel and Vectorizer saved successfully!")