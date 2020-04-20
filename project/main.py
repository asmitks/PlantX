from flask import Blueprint, render_template, Flask, request
from flask_login import login_required, current_user
from .models import Product
from . import db 

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.Username)


@main.route('/shop')
@login_required
def shop():
    products=Product.query.order_by(Product.ProductID).all()
    available=[]
    description=[]
    price=[]
    rating=[]
    types=[]

    for i in products:
        available.append(str(i.Available))
        description.append(str(i.Description))
        price.append(str(i.Price))
        rating.append(str(i.Rating))
        types.append(str(i.Type))


    return render_template('shop.html',plen=len(available),name=current_user.Username,available=available,description=description,price=price,rating=rating,types=types)

@main.route('/shop',methods=['POST'])
@login_required
def shop_buy():
    return render_template('shop.html',name=current_user.Username)



@main.route('/add_product',methods=['POST'])
@login_required
def post_product_post():
    types = request.form.get('type')
    description = request.form.get('description')
    available = request.form.get('available')
    price = request.form.get('price')
    new_product=Product(ProductID="p2",Description=description,Available=available,Type=types,Price=price,Rating=1,UserID=current_user.UserID,TypeID=1)

    db.session.add(new_product)
    db.session.commit()
    return render_template('post_product.html',name=current_user.Username)



@main.route('/add_product')
@login_required
def post_product():
    return render_template('post_product.html',name=current_user.Username)
