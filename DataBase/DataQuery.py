"""This model used to upload the row data into database.
"""

import sqlite3 as sql
import pandas as pd 


## Database Config
Database='DataBase\SeedDataBase.db'
connection=sql.connect(Database)
cursor=connection.cursor()

def insert_data(clean_df):
    try:
        if clean_df:
            
            table='Seed_Data_'
            columns=', '.join(clean_df.columns)
            placeholders = ', '.join(['?'] * len(clean_df.columns))
            sql_insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            for row in clean_df.itertuples(index=False, name=None):
                cursor.execute(sql_insert_query, row)
                
            connection.commit()
            connection.close()
            return 'data inserted'
        else:
            return 'Data insertion failed'
    except Exception as e:
        return f'Error occure {e}'