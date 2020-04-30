# from . import db 
from datetime import date
from models import Product,Orders,ServiceRequest,ServiceAvailable

# cust=['C1','C10','C100','C101','C102']
from random import randint
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import urllib.parse 
from flask import Flask
import pyodbc
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

server = 'tcp:plantx.database.windows.net'
database = 'PlantX'
username = 'Atishay'
password = 'DBMSproject123'
driver= '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

for i in range(1):
    x=randint(2,140)
    p=randint(2,140)
    prodid='I'+str(p)
    cid='C'+str(x)
    product = Product.query.filter_by(ProductID=prodid).first()
    val=product.Available
    if(int(val)==1):
        Product.query.filter_by(ProductID=prodid).delete()
        db.session.commit()

    else:
        product.Available=int(val)-1
        db.session.commit()

    products=[product]
    available=[]
    description=[]
    price=[]
    rating=[]
    types=[]
    type_id=[]
    ids=[]
    for i in products:
        ids.append(str(i.ProductID))
        available.append(str(i.Available))
        description.append(str(i.Description))
        price.append(str(i.Price))
        rating.append(str(i.Rating))
        types.append(str(i.Type))
        type_id.append(str(i.TypeID))
    k=Orders.query.order_by(Orders.OrderID).all()
    next_cid=[0]
    for i in k:
        next_cid.append(int(str(i.OrderID).replace('O','')))
    next_cid.sort()
    my_id="O"+str(next_cid[-1]+1)
    today=date.today()
    order=Orders(OrderID=my_id,Price=price[0],Quantity=1,Time=(date.today()),ProductID=prodid,CustomerID=cid)
    db.session.add(order)
    db.session.commit()