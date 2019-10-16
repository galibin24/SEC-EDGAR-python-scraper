import pandas as pd 
import os
import datetime 
from functools import reduce
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
import re

# I can take substring of every string a check for it in every other string of df.index

# CODE
# TODO When joining all files together a lot of similar rows are not merged properly because of naming diffrences 
# TODO Delete rows with more than 10-20 Nans 
# TODO rename function(from CIK to Symbol)
# TODO Make optional to chose time period for parsing 

# MANAGMENT 
# TODO make pypi package 

# OVERALL
# TODO more testings
# TODO imporove decision method of document type
    # get one financial document for 100 companies and see which terms used in every statment 


# read all files in folder with scraped documents 
def raw_files():
    files = []
    for file in os.listdir("./files"):
        if file.endswith(".csv"):
            pat = os.path.join("./files", file)
            files.append(pat)
    return files


# Decide on the document type(eg. Balance Sheet, Income Statment, Cash Flow)
def doc_type(doc):
    df = pd.read_csv(doc, index_col= 1)
    df = df.dropna()

    names = list(df.index.values)
    names = [i.lower() for i in names]
        
    income_statement = ['net sales', 'cost of sales', 'operating income', 
                        'gross profit', 'net revenue', 'cost of goods sold',
                        'total operating expenses', 'operating expenses', 'interest', 'net revenue:', 'revenue', 'operating expenses:'
                        'total cost of revenue', 'general and administrative', 'marketing and sales', 'research and development']
    balance_sheet = ['current assets:', 'current liabilities:', "stockholders’ equity:", 'total liabilities', 'shareholders’ equity:',
                    'retained earnings', 'assets:', 'total liabilities', 'retained earnings', 'liabilities:', 'cash and cash equivalents', 
                    'short-term investments', 'inventories']
    cash_flow = ['cash', 'accounts payable', 'deferred income taxes', 
                'account receivables', 'investing activities:', 'operating activities:', 'financing activities:']

    points_for_is = 0
    points_for_bs = 0
    points_for_cs = 0

    for x in names:
        if x in income_statement:
            points_for_is += 1
        if x in balance_sheet:
            points_for_bs += 1
        if x in cash_flow:
            points_for_cs += 1

    name = 'none'
    company = doc.split(' ')[0]
    company = company[8:]

    if points_for_is >= 4:
        name = 'Income_Statment'
    elif points_for_cs >= 3:
        name = 'Cash_Flow'
    elif points_for_bs >= 3:
        name = 'Balance_sheet'
    date = doc.split(' ')[1]
    date = date[:-6]
    if name is not 'none':
        save_name = './parsed/' + company + ' '+ name + ' '+ date + '.csv'
        df.to_csv(save_name)
    return company


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
            df = df.rename(columns={"1": date})
            df = df[~df.index.duplicated()]
            df.index = df.index.map(str.lower)
            Is.append(df)
        if 'Balance_sheet' in i:
            date = i[-14:-4]
            df = pd.read_csv(i, index_col= 0, usecols = [0, 2] )
            df = df.rename(columns={"1": date})
            df = df[~df.index.duplicated()]
            df.index = df.index.map(str.lower)
            bs.append(df)    
        if 'Cash_Flow' in i:  
            date = i[-14:-4]
            df = pd.read_csv(i, index_col= 0, usecols = [0, 2] )
            df = df.rename(columns={"1": date})
            df = df[~df.index.duplicated()]
            df.index = df.index.map(str.lower)
            cs.append(df)
    try:
        Is_df = pd.concat(Is, axis = 1, sort = False)
        Is_df.to_csv('./ALL/' + company + '_Income_Statment.csv')
    except ValueError:
        pass

    try:
        Bs_df = pd.concat(bs, axis = 1, sort = False)
        Bs_df.to_csv('./ALL/' + company + '_Balance_sheet.csv')
    except ValueError:
        pass
    
    try:
        Cs_df = pd.concat(cs, axis = 1, sort = False)
        Cs_df.to_csv('./ALL/' + company + '_Cash_Flow.csv')
    except ValueError:
        pass

# use all
def main():

    # parse the companies' files 
    companies = [] 
    for i in raw_files():
        company = doc_type(doc = i)
        companies.append(company)
    companies = (list(set(companies))) 
    
    # Combine the files of the same type in one single document 
    for i in companies:
        join_all(i)


main()





