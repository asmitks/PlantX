from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from .models import Customer,Gardener,Nursery
from flask_login import login_user, logout_user, login_required
from . import db 
import random
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(Username=email).first()

    if (len(email) == 0 or len(password) == 0):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    if not user or not check_password_hash(user.Password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    # if (str(user.UserID))[0] == 'G':
    #     return redirect(url_for('main.gardenerprofile'))
    return redirect(url_for('main.profile'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signupCustomer',methods=['POST'])
def signup_post():
    count = 0
    email = request.form.get('email')

    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    userName = request.form.get('userName')
    if (not firstName.isalpha()) or (not lastName.isalpha()) or len(userName)==0:
        print('name')
        count+=1

    if email.isdigit() or email.isspace() or len(email) == 0:
        print('Cond 1')
        count+=1

    phonenumber = request.form.get('phonenumber')
    locality = request.form.get('locality')
    address = request.form.get('address')

    if (not phonenumber.isdigit()) or phonenumber.isspace():
        count+=1
        print('no.')
    if (locality.isdigit()) or (address.isdigit()) or len(locality)==0 or len(address)==0:
        count+=1
        print('adress')

    age = request.form.get('age')
    if (len(age)<=0):
        count+=1
        print('age')
    password = request.form.get('password')
    if (len(str(password))==0):
        count+=1
        print('pass')

    if (count > 0):
        flash('Please enter valid credentials')
        return redirect(url_for('auth.signupCustomer'))

    cid="C"+str(random.randint(1,100))
    k=Customer.query.order_by(Customer.CustomerID).all()
    next_cid=[]
    for i in k:
        next_cid.append(int(str(i.CustomerID).replace('C','')))
    next_cid.sort()
    my_id="C"+str(next_cid[-1]+1)
    print(my_id)

    new_customer=Customer(CustomerID=my_id,First_Name=firstName,Last_Name=lastName,Phone_Number=phonenumber,EmailID=email,Locality=locality,Address=address,Age=age)
    new_user = Users(UserID=my_id,Username=userName, Password=generate_password_hash(password, method='sha256'))


    user = Users.query.filter_by(Username=userName).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Ooops Username already exists')
        return redirect(url_for('auth.signupCustomer'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.

    # add the new user to the database
    # print(new_user)
    db.session.add(new_user)
    db.session.commit()
    db.session.add(new_customer)
    db.session.commit()


    return redirect(url_for('auth.login'))



@auth.route('/signupGardener',methods=['POST'])
def signup_post_g():
    count = 0
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    userName = request.form.get('userName')

    if (not firstName.isalpha()) or (not lastName.isalpha()) or len(userName)==0:
        print('name')
        count+=1

    phonenumber = request.form.get('phonenumber')
    locality = request.form.get('locality')
    address = request.form.get('address')

    if (not phonenumber.isdigit()) or phonenumber.isspace():
        count+=1

    if (locality.isdigit()) or (address.isdigit()) or len(locality)==0 or len(address)==0:
        count+=1

    priceRange = request.form.get('priceRange')
    identification = request.form.get('identification')

    if (identification.isdigit() or len(identification) == 0):
        count += 1
    date = request.form.get('date')
    speciality = request.form.get('speciality')
    experience = request.form.get('experience')

    age = request.form.get('age')
    password = request.form.get('password')
    if (len(password) == 0 or int(str(age))<17 or int(str(age))>59 ):
        count += 1

    if (count > 0):
        flash('Please enter valid credentials')
        return redirect(url_for('auth.signupGardener'))

    k=Gardener.query.order_by(Gardener.GardenerID).all()
    next_cid=[]
    for i in k:
        next_cid.append(int(str(i.GardenerID).replace('G','')))
    next_cid.sort()
    my_id="G"+str(next_cid[-1]+1)
    print(my_id)
    new_gardener=Gardener(GardenerID=my_id,First_Name=firstName,Last_Name=lastName,Phone_Number=phonenumber,Locality=locality,Age=age,Speciality=speciality,Date_of_joining=date,Experience=experience,Price_Range=priceRange,Identification=identification)
    new_user = Users(UserID=my_id,Username=userName, Password=generate_password_hash(password, method='sha256'))


    user = Users.query.filter_by(Username=userName).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signupGardener'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.

    # add the new user to the database
    # print(new_user)
    db.session.add(new_user)
    db.session.commit()
    db.session.add(new_gardener)
    db.session.commit()


    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signupCustomer')
def signupCustomer():
    return render_template('customer_signup.html')

@auth.route('/signupGardener')
def signupGardener():
    return render_template('gardener_signup.html')




@auth.route('/signupNursery',methods=['POST'])
def signup_post_n():
    count = 0
    email = request.form.get('email')
    Name = request.form.get('Name')
    userName = request.form.get('userName')

    if (not Name.isalpha()) or len(userName)==0:
        print('name')
        count+=1

    if email.isdigit() or email.isspace() or len(email) == 0:
        print('Cond 1')
        count+=1

    phonenumber = request.form.get('phonenumber')
    locality = request.form.get('locality')

    if (not phonenumber.isdigit()) or phonenumber.isspace():
        count+=1
    if (locality.isdigit()) or len(locality)==0:
        count+=1

    price_range = request.form.get('Price-Range')
    gst_number = request.form.get('GST-number')
    password = request.form.get('password')

    if (len(gst_number) == 0 or len(password) == 0):
        count += 1

    if (count > 0):
        flash('Please enter valid credentials')
        return redirect(url_for('auth.signupNursery'))

    cid="N"+str(random.randint(1,100))
    k=Nursery.query.order_by(Nursery.NurseryID).all()
    next_cid=[]
    for i in k:
        next_cid.append(int(str(i.NurseryID).replace('N','')))
    next_cid.sort()
    my_id="N"+str(next_cid[-1]+1)
    print(my_id)

    new_nursery=Nursery(NurseryID=my_id,Name=Name,Phone_Number=phonenumber,Email=email,Location=locality,Price_Range=price_range, GST_number=gst_number, Rating=0.01, Number_of_Rating=0.0)
    new_user = Users(UserID=my_id,Username=userName, Password=generate_password_hash(password, method='sha256'))


    user = Users.query.filter_by(Username=userName).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Ooops Username already exists')
        return redirect(url_for('auth.signupNursery'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.

    # add the new user to the database
    # print(new_user)
    db.session.add(new_user)
    db.session.commit()
    db.session.add(new_nursery)
    db.session.commit()


    return redirect(url_for('auth.login'))

@auth.route('/signupNursery')
def signupNursery():
    return render_template('nursery_signup.html')
