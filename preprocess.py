import pandas as pd
import string
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download("punkt")
nltk.download("stopwords")
df = pd.read_csv("data/complaints.csv")
print("Original Shape:")
print(df.shape)
print("\nMissing Values:")
print(df.isnull().sum())
df = df.drop_duplicates(subset=["complaint_text"])

print("\nAfter Removing Duplicates:")
print(df.shape)
df["clean_text"] = df["complaint_text"].str.lower()
df["clean_text"] = df["clean_text"].str.translate(
    str.maketrans("", "", string.punctuation)
)
df["clean_text"] = df["clean_text"].str.replace(
    r"\d+",
    "",
    regex=True
)
stop_words = set(stopwords.words("english"))

df["clean_text"] = df["clean_text"].apply(
    lambda x: " ".join(
        word for word in x.split()
        if word not in stop_words
    )
)
df["tokens"] = df["clean_text"].apply(word_tokenize)
print("\nSample Cleaned Data:\n")

print(
    df[
        [
            "complaint_text",
            "clean_text",
            "tokens"
        ]
    ].head()
)
df.to_csv(
    "data/complaints_clean.csv",
    index=False
)
print("\nPreprocessing Completed Successfully!")
print("Saved -> data/complaints_clean.csv")