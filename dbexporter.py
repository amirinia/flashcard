import sqlalchemy as db
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine
from sqlalchemy import *
import pandas as pd 


engine = db.create_engine('sqlite:///cardsdatabase.db')
df = pd.read_sql_query("SELECT * from card", engine)
meta = MetaData()
meta.reflect(bind=engine)
for t in meta.sorted_tables:
    print("t ",t.name)
print(meta.tables.keys())
print(df)
df.to_csv('dfexport.csv', index=False)