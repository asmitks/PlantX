from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from .models import Customer,Gardener

from . import db
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(Username=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.Password, password):
        # flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signupCustomer',methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    userName = request.form.get('userName')
    phonenumber = request.form.get('phonenumber')
    locality = request.form.get('locality')
    address = request.form.get('address')
    age = request.form.get('age')
    password = request.form.get('password')

    new_customer=Customer(CustomerID="c1",First_Name=firstName,Last_Name=lastName,Phone_Number=phonenumber,EmailID=email,Locality=locality,Address=address,Age=age)
    new_user = Users(UserID="c1",Username=userName, Password=generate_password_hash(password, method='sha256'))


    user = Users.query.filter_by(Username=userName).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
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
    
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    userName = request.form.get('userName')
    phonenumber = request.form.get('phonenumber')
    locality = request.form.get('locality')
    priceRange = request.form.get('priceRange')
    identification = request.form.get('identification')
    date = request.form.get('date')
    speciality = request.form.get('speciality')
    experience = request.form.get('experience')

    address = request.form.get('address')
    age = request.form.get('age')
    password = request.form.get('password')

    new_gardener=Gardener(GardenerID="g1",First_Name=firstName,Last_Name=lastName,Phone_Number=phonenumber,Locality=locality,Address=address,Age=age,Speciality=speciality,Date_of_joining=date,Experience=experience,Price_Range=priceRange,Identification=identification)
    new_user = Users(UserID="g1",Username=userName, Password=generate_password_hash(password, method='sha256'))


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


# @auth.route('/signupGardener',methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     firstName = request.form.get('firstName')
#     lastName = request.form.get('lastName')
#     userName = request.form.get('userName')
#     phonenumber = request.form.get('phonenumber')
#     locality = request.form.get('locality')
#     address = request.form.get('address')
#     age = request.form.get('age')
#     password = request.form.get('password')

#     new_customer=Customer(CustomerID="c1",First_Name=firstName,Last_Name=lastName,Phone_Number=phonenumber,EmailID=email,Locality=locality,Address=address,Age=age)
#     new_user = Users(UserID="c1",Username=userName, Password=generate_password_hash(password, method='sha256'))


#     user = Users.query.filter_by(Username=userName).first() # if this returns a user, then the email already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again
#         return redirect(url_for('auth.signup'))

#     # create new user with the form data. Hash the password so plaintext version isn't saved.

#     # add the new user to the database
#     # print(new_user)
#     db.session.add(new_user)
#     db.session.commit()
#     db.session.add(new_customer)
#     db.session.commit()


#     return redirect(url_for('auth.login'))


@auth.route('/signupCustomer')
def signupCustomer():
    return render_template('customer_signup.html')

@auth.route('/signupGardener')
def signupGardener():
    return render_template('gardener_signup.html')


@auth.route('/logout')
def logout():
    return 'Logout'