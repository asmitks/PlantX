from flask import Blueprint, render_template, Flask
from flask_login import login_required, current_user

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
    return render_template('shop.html',name=current_user.Username)