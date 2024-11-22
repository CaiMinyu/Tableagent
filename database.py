from matplotlib.table import table
from sqlalchemy import create_engine,text,MetaData, Table
from sqlalchemy import  inspect
from sqlalchemy.orm import sessionmaker
import pandas as pd
import mysql.connector
from langchain_community.utilities.sql_database import SQLDatabase
#数据库信息
user = 'root'
password = '!QAZ2wsx'
host = '127.0.0.1'
database = 'agent'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

def save_to_db_csv(data_path,table_name):
    data = pd.read_csv(data_path)
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)

def get_onedata(table_name,coloumn_name,index_name,index):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(text(f"SELECT `{coloumn_name}` FROM `{table_name}` WHERE `{index_name}`  = {index} "))
    row = result.fetchone()
    session.close()
    return row

def db():
    user = 'root'
    password = '!QAZ2wsx'
    host = '127.0.0.1'
    database = 'agent'
    db = SQLDatabase.from_uri(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
    return db

def get_table_names():
    user = 'root'
    password = '!QAZ2wsx'
    host = '127.0.0.1'
    database = 'agent'
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    return table_names

def get_RowsNum(engine):
    table_name="execution_sequence"
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(text(f"SELECT COUNT(*) FROM `{table_name}`"))
    row_count = result.scalar()
    session.close()
    return row_count

def get_labels(engine,table_name):
    metadata = MetaData()
    table_name = table_name
    table = Table(table_name, metadata, autoload_with=engine)
    columns = [column.name for column in table.columns]
    return columns

def get_one_row(engine,line):
    index=line-1
    sql_query = f"SELECT * FROM `table1` LIMIT 1 OFFSET {index}"
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(text(sql_query))
    row = result.fetchone()
    columns = result.keys()
    columns=list(columns)
    session.close()
    row_dict=dict(zip(columns, row))
    return row_dict
get_labels(engine,'table1')