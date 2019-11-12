import pandas as pd 
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from joblib import dump, load
import time

# Times for each model based on small sample 
# Kmean time 0.4447798728942871
# SVC time 0.4916868209838867
# Combined models time 0.5555140972137451

# TODO increase the training sample for supervised model

count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()

# Load Classifiers

# Load Kmeans
Kmeans = load(r'C:\Users\Nikita\Desktop\ml_selector\model\Kmeans.joblib')
X_SVC_train_counts = load(r'C:\Users\Nikita\Desktop\ml_selector\model\X_vecto_SVC.joblib')
X_SVC_train_tfidf = load(r'C:\Users\Nikita\Desktop\ml_selector\model\X_transform_SVC.joblib')

# Load SVC
SVC = load(r'C:\Users\Nikita\Desktop\ml_selector\model\SVC.joblib')
X_Kmean_train_counts = load(r'C:\Users\Nikita\Desktop\ml_selector\model\X_vecto_cluster.joblib')
X_Kmean_train_tfidf = load(r'C:\Users\Nikita\Desktop\ml_selector\model\X_transform_cluster.joblib' )

# read all files in folder with raw documents 
def raw_files():
    files = []
    for file in os.listdir("./files"):
        if file.endswith(".csv"):
            pat = os.path.join("./files", file)
            files.append(pat)
    return files

# Function for SVC model
def SVC_predict(names, model = SVC, vectorizer = X_SVC_train_counts, transformer = X_SVC_train_tfidf):
    X_new_counts = vectorizer.transform(names)
    X_new_tfidf = transformer.transform(X_new_counts)
    
    predicted = model.predict(X_new_tfidf)
    probabilities = model.predict_proba(X_new_tfidf)

    return predicted, probabilities

# Funcion for Kmean model
def Kmean_predict(names, model = Kmeans, vectorizer = X_Kmean_train_counts, transformer = X_Kmean_train_tfidf):
    X_new_counts = vectorizer.transform(names)
    X_new_tfidf = transformer.transform(X_new_counts)
    
    predicted = model.predict(X_new_tfidf)

    return predicted

# Rename files from CIKs to Tickers
def rename(company):
    df = pd.read_excel('Sorted.xlsx', index_col = 0)
    
    df2 = df.loc[df['CIK'] == int(company)]
    print(df2)
    TICKER = str(df2['Ticker'].values[0])
    print(TICKER)
    return TICKER    

# Decide on the document type(eg. Balance Sheet, Income Statment, Cash Flow)
def doc_type(doc, model = 'Combined_model'):
    # Read document 
    df = pd.read_csv(doc, index_col= 1)
    # print(df)
    df.index = df.index.astype(str)

    # Convert index to a string 
    names = list(df.index.values)
    names = [i.lower() for i in names]
    names = [', '.join(names)]

    # Get results of model prediction
    doc_type = 'none'

    # Kmean Alone 
    if model == 'Kmean':
        result2 = Kmean_predict(names = names)
        if result2[0] == 1:
            doc_type = 'Balance_Sheet'
        if result2[0] == 6:
            doc_type = 'Income_Statment'
        if result2[0] == 0:
            doc_type = 'Cash_Flow'

    # SVC Alone
    if model == 'SVC':
        result, probability = SVC_predict(names = names)
        if result[0] == 3 and max(probability[0]) > 0.93:
            doc_type = 'Balance_Sheet'
        if result[0] == 2 and max(probability[0]) > 0.93:
            doc_type = 'Income_Statment'
        if result[0] == 1 and max(probability[0]) > 0.93:
            doc_type = 'Cash_Flow'

    # Combined model 
    if model == 'Combined_model':
        result, probability = SVC_predict(names = names)
        result2 = Kmean_predict(names = names)
        if result[0] == 3 and max(probability[0]) > 0.93 and result2[0] == 1:
            doc_type = 'Balance_Sheet'
        if result[0] == 2 and max(probability[0]) > 0.93 and result2[0] == 6:
            doc_type = 'Income_Statment'
        if result[0] == 1 and max(probability[0]) > 0.93 and result2[0] == 0:
            doc_type = 'Cash_Flow'

    # Company name(CIK)
    company = doc.split(' ')[0]
    company = company[8:]
    company = rename(company)
    # Date of publish 
    date = doc.split(' ')[1]
    date = date[:-6]

    if doc_type is not 'none':
        # print(df)
        df.drop('Unnamed: 0', axis = 'columns', inplace = True)
        # print(df)
        save_name = './parsed/' + company + ' '+ doc_type + ' '+ date + '.csv'
        df.to_csv(save_name)

# Labels all the documets and times the procecss
def sort():
    t = time.time()
    for i in raw_files():
        doc_type(i)
    t1 = time.time() - t
    print("The labeling took: " + str(t1)  + " seconds")

sort()