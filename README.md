# Smart Complaint Management System — AI Module

Smart Complaint Management System is an AI-powered civic complaint management module that helps classify citizen complaints into different categories such as **Garbage, Water Supply, Drainage, Street Light, Road Damage, and Electricity**. The AI module preprocesses complaint text and prepares it for machine learning so that complaints can be automatically categorized and prioritized.

---

## Problem Statement

Citizens submit complaints in different formats, making manual categorization difficult and time-consuming. This project automates complaint preprocessing and prepares data for AI-based complaint classification and priority prediction.

---

## AI Module Objective

To automatically classify complaint text into the correct department category and predict complaint priority using Natural Language Processing (NLP) and Machine Learning.

---

## Dataset Description

Synthetic civic complaint dataset generated using Python.

**Raw Dataset:**
- 660 complaints
- 6 categories

**Categories:**
- Garbage
- Water Supply
- Drainage
- Street Light
- Road Damage
- Electricity

**After preprocessing:**
- `complaints_clean.csv` generated
- Text cleaned
- Lowercase conversion
- Punctuation removal
- Stopword removal
- Tokenization

---

## Folder Structure

```
ai-service/
│
├── data/
│   ├── complaints.csv
│   └── complaints_clean.csv
│
├── docs/
│   └── day5_backend_integration.md
│
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── notebooks/
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   ├── verify_dataset.py
│   └── verify_cleaning.py
│
├── generate_dataset.py
├── preprocess.py
├── train_model.py
├── requirements.txt
├── .gitignore
└── README.md

---

## Technologies Used

```
Python
VS Code
Git
GitHub
```

---

## Python Libraries

```
pandas
numpy
nltk
scikit-learn
matplotlib
joblib
```

---

## Installation

```
git clone <repository>

cd ai-service

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## Run

```
python generate_dataset.py

python preprocess.py
```

---

## Future Scope

```
Train NLP model

Deploy Flask API

Integrate with Backend

Predict complaint priority

Admin Dashboard

Complaint Analytics
```