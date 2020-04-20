from . import db
from flask_login import UserMixin
class Users(UserMixin, db.Model):
    def get_id(self):
           return (self.UserID)
    UserID = db.Column(db.String(100), primary_key=True) # primary keys are required by SQLAlchemy
    # email = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))
    Username = db.Column(db.String(1000))

class Customer(UserMixin, db.Model):
    CustomerID = db.Column(db.String(200), primary_key=True)
    First_Name = db.Column(db.String(200))
    Last_Name = db.Column(db.String(200))
    Phone_Number = db.Column(db.String(200))
    EmailID = db.Column(db.String(200))
    Locality = db.Column(db.String(200))
    Address = db.Column(db.String(200))
    Age = db.Column(db.String(200))
    Rating = db.Column(db.String(200))

class Gardener(UserMixin, db.Model):
    GardenerID = db.Column(db.String(200), primary_key=True)
    First_Name = db.Column(db.String(200))
    Last_Name = db.Column(db.String(200))
    Phone_Number = db.Column(db.String(200))
    Locality = db.Column(db.String(200))
    Address = db.Column(db.String(200))
    Age = db.Column(db.String(200))
    Rating = db.Column(db.String(200))
    Speciality = db.Column(db.String(200))
    Experience = db.Column(db.String(200))
    Price_Range = db.Column(db.String(200)) 
    Date_of_joining = db.Column(db.String(200))
    Identification = db.Column(db.String(200))


class Product(UserMixin, db.Model):
    ProductID = db.Column(db.String(200), primary_key=True)
    Type = db.Column(db.String(200))
    Description = db.Column(db.String(200))
    Price = db.Column(db.String(200))
    Available = db.Column(db.String(200))
    Rating = db.Column(db.String(200))
    UserID = db.Column(db.String(200))
    TypeID = db.Column(db.String(200))
   