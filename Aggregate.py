import pandas as pd 
import os
import datetime 
from functools import reduce
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
import re
from difflib import SequenceMatcher


# TODO come up with proper merging cel process
    # surpivised learning model
    # look for proccesing language model 
# TODO Try implementing processing language model to see similirities between words
#   so the synunoms will be merged together 

# TODO Delete rows with more than 10-20 Nans(replace other nans using 
#   https://www.kaggle.com/juejuewang/handle-missing-values-in-time-series-for-beginners)
# TODO rename function(from CIK to Symbol)

# TODO make pypi package 

# company = all uniqie
def companies():
    files = []
    for file in os.listdir("./files"):
        if file.endswith(".csv"):
            pat = os.path.join("./files", file)
            files.append(pat)
    companies = []
    for i in files:
        company = i.split(' ')[0]
        company = company[8:]
        companies.append(company)
    companies = list(set(companies))
    return companies

# print(companies())

# read files in folder with parsed documents
def get_company_parsed(company):
    parsed_files = []
    for file in os.listdir("./parsed"):
        if file.endswith(".csv"):
            pat = os.path.join("./parsed", file)
            if company in pat:
                parsed_files.append(pat)
    return parsed_files

# Combines the files of the same type in one single spreadsheet
def join_all(company):
    count = 0
    Is_count = []
    parsed_files = get_company_parsed(company)
    Is = []
    bs = []
    cs = []
    for i in parsed_files:
        if 'Income_Statment' in i:  
            date = i[-14:-4]
            df = pd.read_csv(i, index_col= 0, usecols = [0, 2] )
            df.index = df.index.astype(str)
            df = df.rename(columns={"2": date})
            df = df[~df.index.duplicated()]
            df.index = df.index.map(str.lower)
            Is.append(df)
        if 'Balance_Sheet' in i:
            date = i[-14:-4]
            df = pd.read_csv(i, index_col= 0, usecols = [0, 2] )
            df.index = df.index.astype(str)
            df = df.rename(columns={"2": date})
            df = df[~df.index.duplicated()]
            df.index = df.index.map(str.lower)
            bs.append(df)    
        if 'Cash_Flow' in i: 
            date = i[-14:-4]
            df = pd.read_csv(i, index_col= 0, usecols = [0, 2] )
            df.index = df.index.astype(str)
            df = df.rename(columns={"2": date})
            df = df[~df.index.duplicated()]
            # print(df.index)
            df.index = df.index.map(str.lower)
            cs.append(df)
    # try:
    Is_df = pd.concat(Is, axis = 1, sort = False)
    for i in Is_df.index:
        for b in Is_df.index:
            rat = SequenceMatcher(None, i, b).ratio()
            if rat > 0.7:
                Is_df.rename(index = {i: b}, inplace = True)
    Is_df = Is_df.groupby(level=0, axis = 0, sort = False).sum()

    for column in Is_df:
        columnSeriesObj = Is_df[column]
        # print(Is_df)
        check = columnSeriesObj.str.contains('us-gaap', regex=False)
        if check.any() == True:
            for val in columnSeriesObj.values:
                val = str(val)
                val2 = val.split('us-gaap')[0]
                Is_df.replace({val: val2}, inplace = True)
    Is_df.to_csv('./ALL/' + company + '_Income_Statment.csv')

    # except ValueError:
    #     pass

    try:
        Bs_df = pd.concat(bs, axis = 1, sort = False)
        for i in Bs_df.index:
            for b in Bs_df.index:
                rat = SequenceMatcher(None, i, b).ratio()
                # print(rat)
                if rat > 0.7:
                    Bs_df.rename(index = {i: b}, inplace = True)
        Bs_df = Bs_df.groupby(level=0, axis = 0, sort = False).sum()

        # rename us-gaap in year 2015 
        for column in Bs_df:
            columnSeriesObj = Bs_df[column]
            check = columnSeriesObj.str.contains('us-gaap', regex=False)
            if check.any() == True:
                for val in columnSeriesObj.values:
                    val = str(val)
                    val2 = val.split('us-gaap')[0]
                    Bs_df.replace({val: val2}, inplace = True)
                
        Bs_df.to_csv('./ALL/' + company + '_Balance_sheet.csv')
    except ValueError:
        pass
    
    try:
        Cs_df = pd.concat(cs, axis = 1, sort = False)
        for i in Cs_df.index:
            for b in Cs_df.index:
                rat = SequenceMatcher(None, i, b).ratio()
                # print(rat)
                if rat > 0.7:
                    Cs_df.rename(index = {i: b}, inplace = True)
        Cs_df = Cs_df.groupby(level=0, axis = 0, sort = False).sum()

        # rename us-gaap in year 2015 
        for column in Cs_df:
            columnSeriesObj = Cs_df[column]
            check = columnSeriesObj.str.contains('us-gaap', regex=False)
            if check.any() == True:
                for val in columnSeriesObj.values:
                    val = str(val)
                    val2 = val.split('us-gaap')[0]
                    Cs_df.replace({val: val2}, inplace = True)
        Cs_df.to_csv('./ALL/' + company + '_Cash_Flow.csv')
    except ValueError:
        pass

# use all
def main(companies = companies() ):
    
    # Combine the files of the same type in one single document 
    for i in companies:
        join_all(i)







