from flask import Blueprint, render_template, Flask, request, redirect,url_for, flash
from flask_login import login_required, current_user
from .models import Nursery,Product,Orders,ServiceRequest,ServiceAvailable,Customer,Services, Plant,Seed,Soil,Tools,Product_Reviews,Product_Request
from . import db
from random import randint
from datetime import date
current_prod=""
main = Blueprint('main', __name__)
import random
import math
import collections
import time
from sqlalchemy import ForeignKey
from sklearn.linear_model import LinearRegression

def str_time_prop(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.Username)

@main.route('/gardenerprofile')
@login_required
def gardenerprofile():
    return render_template('gardener_profile.html',name=current_user.Username)


@main.route('/shop')
@login_required
def shop():
    products=Product.query.order_by(Product.ProductID).all()
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


    return render_template('shop.html',ids=ids,plen=len(available),name=current_user.Username,available=available,description=description,price=price,rating=rating,types=types,typeID=type_id)


@main.route('/prod/<prodid>')
@login_required
def prod(prodid):
    global current_prod
    current_prod=prodid
    product = Product.query.filter_by(ProductID=prodid).first()
    products=[product]
    available=[]
    description=[]
    price=[]
    rating=[]
    types=[]
    type_id=[]
    ids=[]
    info=[]
    reviews=[]
    reviewrat=[]
    for i in products:
        ids.append(str(i.ProductID))
        available.append(str(i.Available))
        description.append(str(i.Description))
        price.append(str(i.Price))
        rating.append(str(i.Rating))
        types.append(str(i.Type))
        type_id.append(str(i.TypeID))
        if('P' in i.TypeID):
            plant = Plant.query.filter_by(PlantID=i.TypeID).first()
            info.append(plant.Name+" "+plant.Irrigation_Requirements)
        elif('E' in i.TypeID):
            seed = Seed.query.filter_by(SeedID=i.TypeID).first()
            info.append("Expected Selling price: "+str(seed.Expected_Selling_Price))
        elif('T' in i.TypeID):
            tool = Tools.query.filter_by(ToolID=i.TypeID).first()
            info.append(tool.Name)
        elif('S' in i.TypeID):
            soil = Soil.query.filter_by(SoilID=i.TypeID).first()
            info.append("Mineral Details : "+soil.Mineral_Details)
    product_reviews = Product_Reviews.query.filter_by(ProductID=prodid).all()
    
    for i in product_reviews:
        reviews.append([i.Review,i.Rating])
        # reviewrat.append(str(i.Rating))
    while(len(reviews)<3):
        reviews.append(["No review","None"])
    # if(len(reviews)<3):
        # reviews=[["No review","None"],["No review","None"],["No review","None"]]
    random.shuffle(reviews)
    
    

    

    print(reviews)




    return render_template('prod.html',ids=ids,plen=len(available),info=info,name=current_user.Username,available=available,description=description,price=price,rating=rating,types=types,typeID=type_id,reviews=reviews)

@main.route('/addServiceRequest')
@login_required
def addServiceRequest():
    return render_template('service_form.html')




@main.route('/addServiceRequest',methods=['POST'])
@login_required
def addServiceRequestpost():
    k=ServiceRequest.query.order_by(ServiceRequest.ServiceRequestID).all()
    next_cid=[0]
    for i in k:
        next_cid.append(int(str(i.ServiceRequestID).replace('R','')))
    next_cid.sort()
    my_id="R"+str(next_cid[-1]+1)
    print(current_user.UserID)
    price = str(request.form.get('Price'))
    description=str(request.form.get('Description'))
    location = str(request.form.get('Location'))
    if (len(location) == 0 or location.isdigit() or len(description)==0 or len(price) == 0 or price.isalpha()):
        flash('Please enter valid values')
        return render_template('service_form.html')
    order=ServiceRequest(ServiceRequestID=my_id,Price=str(request.form.get('Price')),Date=str(request.form.get('Date')),Job_type=str(request.form.get('Job_type')),Description=str(request.form.get('Description')),CustomerID=current_user.UserID)
    print(order)
    db.session.add(order)
    db.session.commit()
    return render_template('service_form.html')



@main.route('/prod',methods=['POST'])
@login_required
def prods():
    prodid=current_prod
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
    ki=Product_Reviews.query.order_by(Product_Reviews.Product_ReviewID).all()
    next_cidi=[0]
    for i in ki:
        next_cidi.append(int(str(i.Product_ReviewID).replace('V','')))
    next_cid.sort()
    my_idi="V"+str(next_cid[-1]+10000000)
    print("********")
    print(my_idi)
    today=date.today()
    rr=request.form.get('rating')
    if(rr==""):
        rr="3"
    rat=Product_Reviews(Product_ReviewID=my_idi,ProductID=prodid,Rating=rr,CustomerID=current_user.UserID,Review="asdasdasda")
    db.session.add(rat)
    db.session.commit()
    print(my_id+"order")
    order=Orders(OrderID=my_id,Price=price[0],Quantity=1,Time=(date.today()),ProductID=prodid,CustomerID=current_user.UserID)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('main.shop'))


@main.route('/shop',methods=['POST'])
@login_required
def shop_buy():
    x=request.form.get('product')
    return redirect(url_for('main.prod',prodid=x))
    return render_template('shop.html',name=current_user.Username)


@main.route('/add_product',methods=['POST'])
@login_required
def post_product_post():
    count = 0
    types = request.form.get('type')
    description = request.form.get('description')
    available = request.form.get('available')
    price = request.form.get('price')
    print("**********"+types+"*************")

    if(types==''):
        count+=1
        types="abcdws"
        print("ADAD*******Asda")
    print(types[0])
    if (types[0]=='P'):
        count = 0
        a = 0
    main_type=""
    
    
    if (types[0]=='P'):
        main_type="Plant"
        # print('in types')
        k=Plant.query.order_by(Plant.PlantID).all()

        # subquery = db.session.execute('SELECT PlantID FROM Plant WHERE PlantID= :val', {'val':types})
        a = 0;
        for i in k:
            if (i.PlantID==types):
                a+= 1
                break

        if (a == 0):
            flash('Given Type ID does not exist')
            return render_template('post_product.html',name=current_user.Username)
    if (types[0]=='T'):
        main_type="Tool"

        k=Tools.query.order_by(Tools.ToolID).all()

        # subquery = db.session.execute('SELECT PlantID FROM Plant WHERE PlantID= :val', {'val':types})
        a = 0;
        for i in k:
            if (i.ToolID==types):
                a+= 1
                break

        if (a == 0):
            flash('Given Type ID does not exist')
            return render_template('post_product.html',name=current_user.Username)

    if (types[0]=='E'):
        main_type="Seed"

        k=Seed.query.order_by(Seed.ToolsID).all()

        # subquery = db.session.execute('SELECT PlantID FROM Plant WHERE PlantID= :val', {'val':types})
        a = 0;
        for i in k:
            if (i.Seed==types):
                a+= 1
                break

        if (a == 0):
            flash('Given Type ID does not exist')
            return render_template('post_product.html',name=current_user.Username)
    if (types[0]=='S'):
        main_type="Soil"

        k=Soil.query.order_by(Soil.ToolsID).all()

        # subquery = db.session.execute('SELECT PlantID FROM Plant WHERE PlantID= :val', {'val':types})
        a = 0;
        for i in k:
            if (i.Soil==types):
                a+= 1
                break

        if (a == 0):
            flash('Given Type ID does not exist')
            return render_template('post_product.html',name=current_user.Username)

    if (types.isdigit() or description.isdigit() or len(types)==0):
        count += 1

    if ((len(available) > 0 and available[0]=='-') or (len(price)>0 and price[0]=='-')):
        count+=1

    if (count > 0):
        flash('Please enter valid values')
        return render_template('post_product.html',name=current_user.Username)
    k=Product.query.order_by(Product.ProductID).all()
    next_cid=[0]
    for i in k:
        next_cid.append(int(str(i.ProductID).replace('I','')))
    next_cid.sort()
    my_id="I"+str(next_cid[-1]+90000)
    new_product=Product(ProductID=my_id,Description=description,Available=available,Type=main_type,Price=price,Rating=3,UserID=current_user.UserID,TypeID=types)

    if (a == 0):
        return render_template('post_product.html',name=current_user.Username)
    db.session.add(new_product)
    db.session.commit()
    return render_template('post_product.html',name=current_user.Username)

@main.route('/add_product')
@login_required
def post_product():
    return render_template('post_product.html',name=current_user.Username)


@main.route('/ServiceRequest')
@login_required
def serviceRequest():
    print("IN app")
    data = []
    requests=ServiceRequest.query.order_by(ServiceRequest.ServiceRequestID).all()
    subquery = db.session.execute('SELECT ServiceRequestID FROM ServiceAvailable WHERE GardenerID= :val', {'val':current_user.UserID})
    current_user_applications = set()
    for j in subquery:
        current_user_applications.add(str(j['ServiceRequestID']))
    for i in requests:
        if (str(i.ServiceRequestID) not in current_user_applications):
            temp = []
            temp.append(str(i.ServiceRequestID))
            temp.append(str(i.Price))
            temp.append(str(i.Job_type))
            temp.append(str(i.Date))
            temp.append(str(i.Description))
            data.append(temp)

    if (len(data) == 0):
        return render_template('NoResult.html', message='No active ServiceRequest available at this time')
    else:
        return render_template('ServiceRequest.html', rlen=len(data), clen=len(data[0]), data=data)
@main.route('/ServiceRequest',methods=['POST'])
@login_required
def post_servicerequest():
    sr_id = request.form.get('apply')
    jobtype_selected = request.form.get('JobType')
    print(sr_id, jobtype_selected)
    if (sr_id == None and jobtype_selected != None):
        result = db.session.execute('SELECT * FROM Service_Select WHERE Job_type = :val', {'val': jobtype_selected})
        data = []
        for r in result:
            temp = []
            temp.append(str(r['ServiceRequestID']))
            temp.append(str(r['Price']))
            temp.append(str(r['Job_type']))
            temp.append(str(r['Date']))
            temp.append(str(r['Rating']))
            temp.append(str(r['Locality']))
            data.append(temp)

        if (len(data) == 0):
            return render_template('NoResult.html', message='No active ServiceRequest of ' + jobtype_selected +' is available at this time')
        else:
            return render_template('ServiceRequest.html', rlen=len(data), clen=len(data[0]), data=data)
    else:
        response=ServiceAvailable(ServiceRequestID=sr_id, GardenerID=current_user.UserID)
        db.session.add(response)
        db.session.commit()
        return redirect(url_for('main.serviceRequest'))

@main.route('/ServiceHistory')
@login_required
def servicehistory():
    requests = db.session.execute('SELECT * FROM Services WHERE GardenerID = :val', {'val': current_user.UserID})
    data = []
    for r in requests:
        temp = []
        temp.append(str(r['Price']))
        temp.append(str(r['Job_type']))
        temp.append(str(r['Date']))
        temp.append(str(r['CustomerID']))
        data.append(temp)
    if (len(data) == 0):
        return render_template('NoResult.html', message='No Service History found')
    else:
        return render_template('Servicehistory.html', rlen=len(data), clen=len(data[0]), data=data)








@main.route('/ServiceAssign')
@login_required
def ServiceAssign():
    data = []

    requests=ServiceRequest.query.order_by(ServiceRequest.ServiceRequestID).all()
    valid=[]
    for c, i in db.session.query(ServiceRequest, ServiceAvailable).filter(ServiceRequest.ServiceRequestID == ServiceAvailable.ServiceRequestID).all():
        if(c.CustomerID==current_user.UserID):
            valid.append([c,i])
    current_user_applications = set()
    for i in valid:
            temp = []
            temp.append(str(i[0].ServiceRequestID))
            temp.append(str(i[0].Price))
            temp.append(str(i[1].GardenerID))
            temp.append(str(i[0].Date))
            temp.append(str(i[0].Description))
            data.append(temp)

    if (len(data) == 0):
        return render_template('NoResult.html', message='Ooops No services to assign')
    else:
        return render_template('ServiceAvailable.html', rlen=len(data), clen=len(data[0]), data=data)




@main.route('/ServiceAssign',methods=['POST'])
@login_required
def post_serviceAssign():
    sr_id = request.form.get('apply')
    valid=[]
    k=Services.query.order_by(Services.ServiceID).all()
    
    next_cid=[0]
    for i in k:
        next_cid.append(int(str(i.ServiceID).replace('R','')))
    next_cid.sort()
    my_id="R"+str(next_cid[-1]+1)


    c =db.session.query(ServiceRequest).filter(ServiceRequest.ServiceRequestID == sr_id).all()[0]
    for k, i in db.session.query(ServiceRequest, ServiceAvailable).filter(ServiceRequest.ServiceRequestID == ServiceAvailable.ServiceRequestID).all():
        if(c.CustomerID==current_user.UserID):
            valid.append([c,i])
    gid=""
    for i in valid:
        if i[1].ServiceRequestID==sr_id:
            gid=i[1].GardenerID
            break
    response=Services(ServiceID=my_id, GardenerID= gid,Price=c.Price,Date=c.Date,Job_type=c.Job_type,CustomerID=current_user.UserID)
    
    # for i in valid:
        # if i[1].ServiceRequestID==sr_id:
            # db.session.delete(i[1])
            # db.session.commit()
    db.session.delete(c)
    db.session.commit()
    db.session.add(response)
    db.session.commit()
    
    return redirect(url_for('main.ServiceAssign'))



def sim_pearson(prefs,p1,p2):
    similar={}
    for prods in prefs[p1]:
        for prods2 in prefs[p2]:
            if prods==prods2:
                similar[prods]='common'
            
    n=len(similar)
    if n==0:
        return 0
    sum1=0
    sum2=0
    sumsq1=0
    sumsq2=0
    for mov in similar:
        sum1+=prefs[p1][mov]
        sum2+=prefs[p2][mov]
        sumsq1+=pow(prefs[p1][mov],2)
        sumsq2+=pow(prefs[p2][mov],2)
    
    prod_sum=0
    for mov in similar:
        prod_sum+=prefs[p1][mov]*prefs[p2][mov]

    num=prod_sum-(sum1*sum2/n)
    den=math.sqrt((sumsq1-pow(sum1,2)/n)*(sumsq2-pow(sum2,2)/n))
    if den==0:
        return 0

    sim=num/den

    return sim
    
@main.route('/recommendations')
@login_required
def recommendations():
    requests = db.session.execute('SELECT * FROM Product_Reviews')
    prefs={}
    for i in requests:
        try:
            prefs[str(i['CustomerID'])][i['ProductID']]=float(i['Rating'])
        except:
            prefs[str(i['CustomerID'])]={}
            prefs[str(i['CustomerID'])][i['ProductID']]=float(i['Rating'])
    # print(prefs[str(current_user.UserID)])
    try:
        x=prefs[str(current_user.UserID)]
    except:
        return render_template('NoResult.html', message='Ooops No recommendations for you')

    try:
        totals={}
        simSums={}
        for other in prefs:
            if(other==str(current_user.UserID)):
                continue
            simp=sim_pearson(prefs,str(current_user.UserID),other)
            # print(simp)
            if(simp<=0):
                continue
            for item in prefs[other]:
                if(item not in prefs[str(current_user.UserID)] or prefs[str(current_user.UserID)][item]==0):
                    # print("***********")
                    totals.setdefault(item,0)
                    totals[item]+=prefs[other][item]*simp
                    simSums.setdefault(item,0)
                    simSums[item]+=simp
        print(totals,simSums)
        ranks=[(total/simSums[item],item) for item,total in totals.items()]
        ranks.sort(reverse=True)
        products=Product.query.order_by(Product.ProductID).all()
        available=[]
        description=[]
        price=[]
        rating=[]
        types=[]
        type_id=[]
        ids=[]
        for j in ranks[:5]:
            for i in products:
                if(i.ProductID==j[1]):
                    ids.append(str(i.ProductID))
                    available.append(str(i.Available))
                    description.append(str(i.Description))
                    price.append(str(i.Price))
                    rating.append(str(i.Rating))
                    types.append(str(i.Type))
                    type_id.append(str(i.TypeID))
        if(len(available)<5):
            assert(1<0)
        return render_template('recommend.html',ids=ids,plen=len(available),name=current_user.Username,available=available,description=description,price=price,rating=rating,types=types,typeID=type_id)
    except:
        return render_template('NoResult.html', message='Ooops No recommendations for you, not enough Data')



@main.route('/recommendations',methods=['POST'])
@login_required
def rec():
    x=request.form.get('product')
    return redirect(url_for('main.prod',prodid=x))
    return render_template('shop.html',name=current_user.Username)

@main.route('/orders')
@login_required
def orders():
    items=Orders.query.order_by(Orders.OrderID).all()
    ids=[]
    for i in items:
        if(i.CustomerID==current_user.UserID):
            ids.append(i.ProductID)
    data = []
    print(ids)
    requests=Product.query.order_by(Product.ProductID).all()
    valid=[]
    for c in requests:
        if(str(c.ProductID) in ids):
            print(c.ProductID)
            for i in range(ids.count(c.ProductID)):
                valid.append(c)
    print(valid)
    # current_user_applications = set()
    for i in valid:
            temp = []
            temp.append(str(i.ProductID))
            temp.append(str(i.Description))
            temp.append(str(i.Price))
            data.append(temp)
    # print(data)
    if (len(data) == 0):
        return render_template('NoResult.html', message='Ooops No orders yet')
    else:
        return render_template('orders.html', rlen=len(data), clen=len(data[0]), data=data)
    




@main.route('/requestproduct')
@login_required
def requestproduct():
    data = []

    requests=Product.query.order_by(Product.ProductID).all()
    valid=[]
    for c in db.session.query(Product).filter(Product.Available == 0).all():
        # if(c.CustomerID==current_user.UserID):
        valid.append(c)
    current_user_applications = set()
    for i in valid:
            temp = []
            temp.append(str(i.ProductID))
            temp.append(str(i.Description))
            temp.append(str(i.Price))
            data.append(temp)

    if (len(data) == 0):
        return render_template('NoResult.html', message='Ooops No products to request')
    else:
        return render_template('prodreq.html', rlen=len(data), clen=len(data[0]), data=data)




@main.route('/requestproduct',methods=['POST'])
@login_required
def requestproductpost():
    sr_id = request.form.get('apply')
    valid=[]
    k=Product_Request.query.order_by(Product_Request.RequestID).all()
    
    next_cid=[0]
    for i in k:
        next_cid.append(int(str(i.RequestID).replace('Q','')))
    next_cid.sort()
    my_id="Q"+str(next_cid[-1]+1)
    q=request.form.get('Quantity')
    if(q==""):
        q="1"
    add=Product_Request(RequestID=my_id,ProductID=sr_id,Quantity=q,CustomerID=current_user.UserID)
    db.session.add(add)
    db.session.commit()


    
    return redirect(url_for('main.requestproduct'))

import pandas as pd
import datetime as dt
@main.route('/prediction',methods=['POST'])
@login_required
def prediction_post():
    # seed_id='E3'
    seed_id = request.form.get('apply')

    PID = [['I125', 'I163'], ['I181', 'I33'], ['I172', 'I38', 'I86'], ['I19'], ['I106', 'I51'], ['I133'], ['I31'], ['I113'], ['I1'],['I120','I81'], ['I11', 'I14', 'I36'], ['I148', 'I37', 'I61'], ['I121', 'I122', 'I149'], ['I103', 'I158', 'I2'], ['I182', 'I74'], ['I140', 'I171', 'I48'], ['I131'], ['I137'], ['I143'], ['I112', 'I192', 'I87'], ['I134', 'I151'],['I101', 'I109'], ['I139', 'I147', 'I7'], ['I95'], ['I129', 'I18', 'I4'], ['I189', 'I53', 'I91'], ['I20', 'I24'], ['I165', 'I185', 'I41', 'I78'], ['I123', 'I176']]
    regressor = LinearRegression()
    print(PID[int(seed_id.replace('E',''))-1])
    orders=db.session.query(Orders).filter(1==1).all()
    valid=[]
    for i in orders:
        if(str(i.ProductID)in PID[int(seed_id.replace('E',''))-1]):
            valid.append(i)
    data=[]
    train_x=[]
    datess=[]
    train_y=[]
    print(valid)
    for i in valid:
        dto=dt.datetime.strptime(i.Time,"%d-%m-%Y")
        data.append([dto,i.Price])
        train_x.append([dt.datetime.toordinal(dto)])
        datess.append(i.Time)
        

        train_y.append(i.Price)

    print(data)
    df=pd.DataFrame(data,columns=['Time','Price'])
    df['Time']=df['Time'].map(dt.datetime.toordinal)
    # print(df['Time'])
    print(df)
    test=[]
    testx=[]
    tt=[]
    tod=dt.datetime.now()
    for i in range(7):
        test.append(tod+dt.timedelta(days=i))
        tt.append(test[i].strftime("%d-%m-%Y"))
        testx.append([dt.datetime.toordinal(test[i])])
    print(test,testx)
    # return "ok"
    # timestampStr = dateTimeObj
    # print('Current Timestamp : ', timestampStr)
    import numpy as np;
    regressor.fit(np.array(train_x),np.array(train_y))
    y_pred=regressor.predict(testx)
    print(y_pred)
    import matplotlib.pyplot as plt;
    X=train_x[len(train_x)-5:-1]
    Y=train_y[len(train_x)-5:-1]
    plt.scatter(X, Y,color='g')
    print(test,testx)
    plt.plot(datess[len(train_x)-5:-1], regressor.predict(X),color='k')
    import os
    myp=os.path.abspath(__file__)
    plt.savefig(myp.replace('main.py','')+'static/foo.png')

    return render_template('prediction.html',rlen=7, date=tt,price=y_pred)

@main.route('/prediction')
@login_required
def prediction():
    data = []

    requests=Seed.query.order_by(Seed.SeedID).all()
    valid=[]
    for c in db.session.query(Seed).filter(1==1).all():
        # if(c.CustomerID==current_user.UserID):
        valid.append(c)
    for i in valid:
            temp = []
            temp.append(str(i.SeedID))
            temp.append(str(i.Name))
            temp.append(str(i.Irrigation_Requirements))
            data.append(temp)

    if (len(data) == 0):
        return render_template('NoResult.html', message='Ooops No services to assign')
    else:
        return render_template('seeds.html', rlen=len(data), clen=len(data[0]), data=data)

@main.route('/information')
@login_required
def information():
    valid1=[]
    valid2=[]
    valid3=[]
    valid4=[]
    data1=[]
    data2=[]
    data3=[]
    data4=[]


    for c in db.session.query(Seed).filter(1==1).all():
        valid1.append(c)
    for c in db.session.query(Plant).filter(1==1).all():
        valid2.append(c)
    for c in db.session.query(Tools).filter(1==1).all():
        valid3.append(c)
    for c in db.session.query(Soil).filter(1==1).all():
        valid4.append(c)

    for i in valid1:
            temp = []
            temp.append(str(i.SeedID))
            temp.append(str(i.Name))
            temp.append(str(i.Irrigation_Requirements))
            data1.append(temp)

    
    for i in valid2:
            temp = []
            temp.append(str(i.PlantID))
            temp.append(str(i.Name))
            temp.append(str(i.Irrigation_Requirements))
            data2.append(temp)
    
    for i in valid3:
            temp = []
            temp.append(str(i.ToolID))
            temp.append(str(i.Name))
            temp.append(str(i.Description))
            data3.append(temp)
    
    for i in valid4:
            temp = []
            temp.append(str(i.SoilID))
            temp.append(str(i.Mineral_Details))
            temp.append(str(i.Type))
            data4.append(temp)
    return render_template('info.html', rlen1=len(data1), data1=data1,rlen2=len(data2), data2=data2,rlen3=len(data3),  data3=data3,rlen4=len(data4),  data4=data4)





@main.route('/trending')
@login_required
def trending():
    requests=db.session.execute('EXEC GETTRENDING')
    data = []
    for i in requests:
        temp = []
        temp.append(i['ProductID'])
        temp.append(i['Type'])
        temp.append(i['Description'])
        temp.append(i['Price'])
        data.append(temp)
    if (len(data) == 0):
        return render_template('NoResult.html', message='Trending Products')
    else:
        return render_template('trending.html', rlen=len(data), clen=len(data[0]), data=data)

