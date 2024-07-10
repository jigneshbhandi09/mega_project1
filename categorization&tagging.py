import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')
def func(title):
    if pd.isna(title):
        title = ''
    doc = nlp(title)
    print(f"Processing title: '{title}'")
    categorization = []
    if any(keyword in title.lower() for keyword in ['politics', 'election', 'government', 'president']):
        categorization.append('Politics')
    if any(keyword in title.lower() for keyword in ['sports', 'football', 'soccer','cricket']):
        categorization.append('Sports')
    if any(keyword in title.lower() for keyword in ['technology', 'mobile', 'phones', 'smartphones', 'computer','tech']):
        categorization.append('Technology')    
    if any(keyword in title.lower() for keyword in ['$', 'economy']):
        categorization.append('Economics/Money Related')
    if any(keyword in title.lower()for keyword in ['kill','death','deaths','died']):
        categorization.append('Violence')
        
    ambiguous = False

    if '?' in title:
        ambiguous = True

    return categorization, ambiguous
combined_df = pd.read_csv("combined_file(in).csv")
if 'Unnamed: 0' in combined_df.columns:
    combined_df.drop(columns=['Unnamed: 0'], inplace=True)
combined_df['Categories'], combined_df['Ambiguous'] = zip(*combined_df['Title'].apply(func))
combined_df.to_csv("categorized and tagged news.csv", index = False)
