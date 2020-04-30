import pyodbc
import urllib.parse
import datetime
from tqdm import tqdm

print("in")
server = 'tcp:plantx.database.windows.net'
database = 'PlantX'
username = 'Atishay'
password = 'DBMSproject123'
driver= '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

def trigger():
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    id_set = set()
    cursor.execute('SELECT CustomerID FROM Customer')
    row = cursor.fetchone()
    print("executing")
    while row:
        id_set.add(str(row[0]))
        row = cursor.fetchone()

    cursor.execute('SELECT GardenerID FROM Gardener')
    row = cursor.fetchone()
    while row:
        id_set.add(str(row[0]))
        row = cursor.fetchone()

    cursor.execute('SELECT NurseryID FROM Nursery')
    row = cursor.fetchone()
    while row:
        id_set.add(str(row[0]))
        row = cursor.fetchone()

    print(len(id_set))
    count = 0
    cursor.execute('SELECT UserID FROM Users')
    row = cursor.fetchone()
    delete = []
    while (row):
        if (str(row[0])[0]!='R' and str(row[0])[0]!='A' and str(row[0]) not in id_set):
            # cursor.execute('DELETE FROM USERS WHERE UserID=?',str(row[0]))
            print(str(row[0]))
            delete.append(str(row[0]))
            count+=1
        row = cursor.fetchone()
    print(count)

    #deleting the redundant users
    try:
        for s in delete:
            cursor.execute('DELETE FROM Users WHERE UserID=?', s)
    except:
        print('Updated')

    cnxn.commit()

    #removing redundant customer reviews and ratings
    customers = set()
    cursor.execute('SELECT CustomerID FROM Customer')
    row = cursor.fetchone()
    while (row):
        customers.add(str(row[0]))
        row = cursor.fetchone()

    delete = []
    cursor.execute('SELECT CustomerID from Complaint')
    row = cursor.fetchone()
    while (row):
        if (str(row[0]) not in customers):
            delete.append(str(row[0]))
        row = cursor.fetchone()

    try:
        for s in delete:
            cursor.execute('DELETE FROM Complaint WHERE CustomerID=?', s)
    except:
        print('Updated')

    cnxn.commit()

    delete = []
    cursor.execute('SELECT CustomerID from Product_Reviews')
    row = cursor.fetchone()
    while (row):
        if (str(row[0]) not in customers):
            delete.add(str(row[0]))
        row = cursor.fetchone()

    try:
        for s in delete:
            cursor.execute('DELETE FROM Product_Reviews WHERE CustomerID=?', s)
    except:
        print('Updated')

    cnxn.commit()

    delete = []
    cursor.execute('SELECT CustomerID from Gardener_Reviews')
    row = cursor.fetchone()
    while (row):
        if (str(row[0]) not in customers):
            delete.add(str(row[0]))
        row = cursor.fetchone()

    try:
        for s in delete:
            cursor.execute('DELETE FROM Gardener_Reviews WHERE CustomerID=?', s)
    except:
        print('Updated')

    cnxn.commit()


    delete = []
    cursor.execute('SELECT CustomerID from ServiceRequest')
    row = cursor.fetchone()
    while (row):
        if (str(row[0]) not in customers):
            delete.add(str(row[0]))
        row = cursor.fetchone()

    try:
        for s in delete:
            cursor.execute('DELETE FROM ServiceRequest WHERE CustomerID=?', s)
    except:
        print('Updated')

    cnxn.commit()

    Type ={}

    print('Plant')

    cursor.execute('SELECT PlantID FROM Plant')
    row = cursor.fetchone()
    while (row):
    	Type[row[0]] = 1
    	row = cursor.fetchone()

    print('Seed')

    cursor.execute('SELECT SeedID FROM Seed')
    row = cursor.fetchone()
    while (row):
    	Type[row[0]] = 1
    	row = cursor.fetchone()

    print('Soil')

    cursor.execute('SELECT SoilID FROM Soil')
    row = cursor.fetchone()
    while (row):
    	Type[row[0]] = 1
    	row = cursor.fetchone()

    print('Tools')

    cursor.execute('SELECT ToolID FROM Tools')
    row = cursor.fetchone()
    while (row):
    	Type[row[0]] = 1
    	row = cursor.fetchone()

    print('Product')

    cursor.execute('SELECT ProductID, TypeID FROM Product')
    row = cursor.fetchone()
    data = []
    while (row):
    	data.append(row)
    	row = cursor.fetchone()

    for i in tqdm(range(len(data))):
    	try:
    		k = Type[data[i][1]]
    		continue
    	except:
    		print("deleting "+data[i][0])
    		cursor.execute('DELETE FROM Product WHERE ProductID=?',data[i][0])

    cnxn.commit()
    print('Product Check complete')

    cursor.execute('SELECT ProductID ,Time , Quantity from Orders')

    today = str(datetime.datetime.now().day)
    dict = {}
    row = cursor.fetchone()
    while (row):
        # print((int(str(row[1][:2]))))
        d = str(row[1])[0:2]
        count  = int(today) - int(d)
        if (count <= 7):
            if (str(row[0]) in dict):
                dict[str(row[0])] += int(str(row[2]))
            else:
                dict[str(row[0])] = int(str(row[2]))
        row = cursor.fetchone()

    print("sorting")
    lst = []
    for key in dict:
        lst.append((key, dict[key]))

    lst = sorted(lst, key = lambda x: x[1], reverse=True)
    print(lst)
    cursor.execute('DELETE FROM TRENDING WHERE Quantity>0')
    cnxn.commit()
    for i in range(10):
        if (i < len(lst) and lst[i][1] > 0):
            a = lst[i][0]
            b = lst[i][1]
            cursor.execute('INSERT INTO TRENDING (ProductID, Quantity) VALUES (?,?)', (a, b))
            cnxn.commit()
    cursor.close()
import time
while(True):
	trigger()
	print('in sleep')
	time.sleep(600)
	print('working')
# print("out")
# cursor.execute("SELECT TOP (1000) * FROM [dbo].[Users]")
# row = cursor.fetchone()
# while row:
#     print (str(row[0]) + " " + str(row[1]))
#     row = cursor.fetchone()
# mport pyodbc
# from sqlalchemy import create_engine
#
# params = urllib.parse.quote_plus \
# (r)
# conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
# engine_azure = create_engine(conn_str,echo=True)
#
# print('connection is ok')
# print(engine_azure.table_names())
