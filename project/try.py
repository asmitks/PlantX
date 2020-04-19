import pyodbc
import urllib.parse

print("in")
server = 'tcp:plantx.database.windows.net'
database = 'PlantX'
username = 'Atishay'
password = 'DBMSproject123'
driver= '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

# cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()
# print("out")
# cursor.execute("SELECT TOP (1000) * FROM [dbo].[Users]")
# row = cursor.fetchone()
# while row:
#     print (str(row[0]) + " " + str(row[1]))
#     row = cursor.fetchone()
# mport pyodbc
from sqlalchemy import create_engine

# params = urllib.parse.quote_plus \ 
# (r)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str,echo=True)

print('connection is ok')
print(engine_azure.table_names())