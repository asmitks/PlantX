import pyodbc
import time
import urllib.parse
server = 'tcp:plantx.database.windows.net'
database = 'PlantX'
username = 'Atishay'
password = 'DBMSproject123'
driver= '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
from sqlalchemy import create_engine
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str,echo=True)

print('connection is ok')
print(engine_azure.table_names())

import csv
import tqdm

def fill(result, name, test):
    for i in result:
        temp = []
        for j in i:
            temp.append(j)
        test.append(temp)
    with open(name+'.csv', 'wt') as out_file:
        csv_writer = csv.writer(out_file)
        for i in test:
            csv_writer.writerow(i)

def Product():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Product];");
        test = [["ProductID", "Type", "Description", "Price", "Available", "Rating", "UserID", "TypeID"]]
        fill(result, "Product", test)

def Admin():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Admin];");
        test = [["AdminID", "Name", "Designation"]]
        fill(result, "Admin", test)

def Complaint():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Complaint];");
        test = [["ComplaintID", "ProductID", "Description", "CustomerID"]]
        fill(result, "Complaint", test)

def Customer():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Customer];");
        test = [["CustomerID", "First_Name", "Last_Name", "EmailID", "Locality", "Address", "Age", "Rating", "Phone_number"]]
        fill(result, "Customer", test)

def Gardener():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Gardener];");
        test = [["GardenerID", "First_Name", "Last_Name", "Locality", "Price_Range", "Identification", "Date_of_joining", "Age", "Rating", "Speciality", "Experience", "Phone_number"]]
        fill(result, "Gardener", test)

def Gardener_Request():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Gardener_Request];");
        test = [["GRequestID", "First_Name", "Last_Name", "Locality", "Price_Range", "Identification", "Date_of_application", "Age", "Speciality", "Experience", "Phone_number"]]
        fill(result, "Gardener_Request", test)

def Gardener_Review():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Gardener_Reviews];");
        test = [["Gardener_ReviewID", "GardenerID", "Review", "CustomerID", "Rating"]]
        fill(result, "Gardener_Review", test)

def Nursery():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Nursery];");
        test = [["NurseryID", "Name", "Phone_number", "Location", "Email", "Price_Range", "GST_number", "Rating", "Number_of_Rating"]]
        fill(result, "Nursery", test)

def Orders():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Orders];");
        test = [["OrderID", "Price", "Quantity", "ProductID", "CustomerID"]]
        fill(result, "Orders", test)

def Plant():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Plant];");
        test = [["PlantID", "Name", "SoilID", "Irrigation_Requirements", "Environment", "Comments"]]
        fill(result, "Plant", test)

def Product_Request():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Product_Request];");
        test = [["RequestID", "ProductID", "Quantity", "CustomerID"]]
        fill(result, "Product_Request", test)

def Product_Review():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Product_Reviews];");
        test = [["Product_ReviewID", "ProductID", "Review", "CustomerID", "Rating"]]
        fill(result, "Product_Review", test)

def Seed():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Seed];");
        test = [["SeedID", "Name", "Irrigation_Requirements", "Expected_Selling_Price", "Comments"]]
        fill(result, "Seed", test)

def ServiceAvailable():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[ServiceAvailable];");
        test = [["ServiceRequestID", "GardenerID"]]
        fill(result, "ServiceAvailablew", test)

def ServiceRequest():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[ServiceRequest];");
        test = [["ServiceRequestID", "Price", "Date", "Job_Type", "Description",  "CustomerID"]]
        fill(result, "ServiceRequest", test)

def Services():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Services];");
        test = [["ServiceRequestID", "GardenerID", "Price", "Date", "Job_Type", "CustomerID"]]
        fill(result, "Services", test)

def Soil():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Soil];");
        test = [["SoilID", "Mineral_Details", "Type", "Fertiliser"]]
        fill(result, "Soil", test)

def Tools():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Tools];");
        test = [["ToolID", "Description", "Name"]]
        fill(result, "Tools", test)

def Users():
    with engine_azure.connect() as connection:
        result = connection.execute("Select * from [dbo].[Users];");
        test = [["UserID", "Username", "Password"]]
        fill(result, "Users", test)

if __name__ == "__main__": 
    while(True):
        try:
            Admin()
            Complaint()
            Customer()
            Gardener()
            Gardener_Request()
            Gardener_Review()
            Nursery()
            Orders()
            Plant()
            Product()
            Product_Request()
            Product_Review()
            Seed()
            ServiceAvailable()
            ServiceRequest()
            Services()
            Soil()
            Tools()
            Users()
            time.sleep(43200)
        except:
            time.sleep(60)
            engine_azure = create_engine(conn_str,echo=True)
