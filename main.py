
# import library

import pandas as pd
import numpy as np
import logging
import os
import sqlalchemy as db


# extra function
def extract(store_data,extra_data):
    store_df=pd.read_csv(store_data)
    extra_df=pd.read_parquet(extra_data)
    merged_df=pd.merge(store_df,extra_df,on='index')
    return merged_df

merged_df = extract('/Users/linda/Desktop/elearning/Python/Build a Data Pipeline-Walmart Online/grocery_sales.csv',
                    '/Users/linda/Desktop/elearning/Python/Build a Data Pipeline-Walmart Online/extra_data.parquet')


# transform function
def transform(raw_data):
    raw_data.fillna({
        'CPI':raw_data['CPI'].mean(),
        'Weekly_Sales':raw_data['Weekly_Sales'].mean(),
        'Unemployment':raw_data['Unemployment'].mean()
    }, inplace=True
    )
    raw_data.Date=pd.to_datetime(raw_data.Date)
    raw_data['Month']=raw_data.Date.dt.month
    raw_data=raw_data[raw_data['Weekly_Sales']>10000]
    raw_data=raw_data.drop(["index", "Temperature", "Fuel_Price", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5", "Type", "Size", "Date"], axis = 1)
    return raw_data


cleaned_df=transform(merged_df)

# avg_monthly_sales()

def avg_monthly_sales(clean_data):
    
    return clean_data.groupby("Month")['Weekly_Sales'].mean().round(2).reset_index(name='Avg_Sales')

agg_data = avg_monthly_sales(cleaned_df)



# load into mysql
def load(df):
    db_connection_url = 'mysql+mysqlconnector://root:*12@localhost/ETLload'
    engine = db.create_engine(db_connection_url)
    df.to_sql('walmart_monthly_sales', engine, if_exists='replace', index=False)
    print("Data loaded into MySQL successfully!")

load_sql=load(agg_data)

