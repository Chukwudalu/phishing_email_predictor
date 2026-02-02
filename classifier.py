import pandas as pd
import numpy as np
import re
import string
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix


vectorizer = TfidfVectorizer()
model = LogisticRegression()

def load_dataset_from_excel(file_path):
    df = pd.read_csv(file_path)
    return df

data_file = "Phishing_validation_emails.csv"
df = load_dataset_from_excel(data_file)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(f"[{string.punctuation}]", "", text) 
    return text

def convert_to_dimensions():
    df['Email'] = df['Email'].apply(clean_text)
    
    x = vectorizer.fit_transform(df['Email'])
    y = df['Label']
    return (x, y)


def train_data():
    x, y = convert_to_dimensions()[0], convert_to_dimensions()[1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model.fit(x_train, y_train)
    
train_data()


def predict_phishing(emails:list):
    try:
        if not len(emails):
            raise ValueError('There is no email in the address')
        emails_cleaned = [clean_text(email) for email in emails]
        emails_vectorized = vectorizer.transform(emails_cleaned)
        emails_predictions = model.predict(emails_vectorized)
    
        labels = []
        for email, pred in zip(emails, emails_predictions):
            
            label = "Phishing email" if pred == 1 else "Safe email"
            labels.append(label)
        
        return labels
    except ValueError as e:
        print(e)
        return

    


