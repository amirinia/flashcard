import pandas
import sqlalchemy
 
# Create the engine to connect to the PostgreSQL database
engine = sqlalchemy.create_engine('sqlite:///exdata.dbo')
 
# Read data from CSV and load into a dataframe object
data = pandas.read_csv('superstore.csv')
 
# Write data into the table in PostgreSQL database
data.to_sql('superstore',engine)