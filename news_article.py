Date of news : 06-07-2024
Country : India
News Title : NEET UG Row: CBI takes 3 accused to Delhi, likely to produce trio before magistrate forr further remand
type of news : education

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('news_dataset.csv')  


label_encoder = LabelEncoder()
data['category'] = label_encoder.fit_transform(data['category'])


X_train, X_test, y_train, y_test = train_test_split(data['text'], data['category'], test_size=0.2, random_state=42)


vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

from flask import Flask, request, jsonify
import joblib

app = Flask(__news_dataset__)

model = joblib.load('news_classifier_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
label_encoder = joblib.load('label_encoder.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)
    category = label_encoder.inverse_transform(prediction)
    return jsonify({'category': category[0]})

if __news_dataset__ == '__main__':
    app.run(debug=True)

import joblib

joblib.dump(model, 'news_classifier_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

