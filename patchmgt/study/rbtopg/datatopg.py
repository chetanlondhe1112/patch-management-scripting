from sqlalchemy import create_engine
import pandas as pd
import psycopg2
# Connection string format: dialect+driver://username:password@host:port/database
# Replace 'postgresql://username:password@host:port/database' with your actual connection string
db_url = 'postgresql://postgres:password@localhost:5432/postgres'
engine = create_engine(db_url)

print(engine)

data={'id':[3,4],'column1':['value1','value2'],'column2':['value1','value2']}

df=pd.DataFrame(data=data)
print(df.columns)
print(df)

df.to_sql(name='temp1',con=engine,if_exists='append',index=0)