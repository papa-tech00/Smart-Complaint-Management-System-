import pandas as pd
import string
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Download required NLTK resources only when missing
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

try:
    word_tokenize("test")
except LookupError:
    nltk.download("punkt")
    nltk.download("punkt_tab")


# Load English stopwords once
stop_words = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Preprocess one complaint for API prediction.
    This matches the preprocessing used during training.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove English stopwords
    text = " ".join(
        word
        for word in text.split()
        if word not in stop_words
    )

    return text


def preprocess_dataset():
    """
    Preprocess the complete complaints dataset.
    This is your existing Day 2 preprocessing work.
    """

    df = pd.read_csv("data/complaints.csv")

    print("Original Shape:")
    print(df.shape)

    print("\nMissing Values:")
    print(df.isnull().sum())

    # Remove duplicate complaint texts
    df = df.drop_duplicates(
        subset=["complaint_text"]
    )

    print("\nAfter Removing Duplicates:")
    print(df.shape)

    # Apply the same reusable preprocessing function
    df["clean_text"] = df["complaint_text"].apply(
        preprocess_text
    )

    # Create token column
    df["tokens"] = df["clean_text"].apply(
        word_tokenize
    )

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

    # Save the cleaned dataset
    df.to_csv(
        "data/complaints_clean.csv",
        index=False
    )

    print("\nPreprocessing Completed Successfully!")
    print("Saved -> data/complaints_clean.csv")


if __name__ == "__main__":
    preprocess_dataset()