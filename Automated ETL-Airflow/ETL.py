#pip install sqlachemy
#pip install mysql-connector-python

import pandas as pd
import numpy as np
import sqlalchemy as db

def main():
    url='https://github.com/yinaS1234/EverydayPyCharms/blob/main/Automated%20ETL-Airflow/P1-AmazingMartEU2.xlsx?raw=true'
    df=pd.read_excel(url,sheet_name='ListOfOrders')
    dedup=df[~df.duplicated(['Customer Name','Order Date','City','Order ID'])]
    dedup.replace('',np.nan, inplace=True)
    print(df.isnull().sum())
    df=dedup[['Order ID', 'Order Date', 'Customer Name', 'City', 'State','Country','Region']]
    df['Customer Name']=df['Customer Name'].str.title()
    df['Order Date']=df['Order Date'].dt.strftime('%Y/%m/%d')
    df.sort_values(by='Order Date', ascending=False, inplace=True)
    df.shape

    db_connection_url = 'mysql+mysqlconnector://root:*@localhost/ETLload'
    engine = db.create_engine(db_connection_url)
    df.to_sql('orders', engine, if_exists='replace', index=False)
    print("Data loaded into MySQL successfully!")

if __name__ == "__main__":
    main()
