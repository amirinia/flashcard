import pandas
import sqlalchemy
 
# Create the engine to connect to the PostgreSQL database
engine = sqlalchemy.create_engine('sqlite:///exdata.db')
 
# Read data from CSV and load into a dataframe object
data = pandas.read_csv('dfexport.csv')
 
# Write data into the table in  database
data.to_sql('superstore',engine)