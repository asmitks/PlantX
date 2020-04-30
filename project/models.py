from . import db
from flask_login import UserMixin
# from sqlalchemy import relationship
from sqlalchemy.orm import sessionmaker, relationship

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
    # Address = db.Column(db.String(200))
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
   
class Orders(UserMixin, db.Model):
    OrderID = db.Column(db.String(200), primary_key=True)
    Price = db.Column(db.String(200))
    Quantity = db.Column(db.String(200))
    Time = db.Column(db.String(200))
    ProductID = db.Column(db.String(200))
    CustomerID = db.Column(db.String(200))
    # UserID = db.Column(db.String(200))
    # TypeID = db.Column(db.String(200))


class ServiceRequest(UserMixin, db.Model):
    __tablename__ = 'ServiceRequest'
    ServiceRequestID = db.Column(db.String(200), primary_key=True)
    # Location = db.Column(db.String(200))
    CustomerID = db.Column(db.String(200))
    Job_type = db.Column(db.String(200))
    Price = db.Column(db.String(200))
    Date = db.Column(db.String(200))
    Description = db.Column(db.String(200))
    # Customer = relationship(lambda: Customer, remote_side=CustomerID, backref='ServiceRequest')

class ServiceAvailable(UserMixin, db.Model):
    __tablename__ = 'ServiceAvailable'
    ServiceRequestID = db.Column(db.String(200), primary_key=True)
    GardenerID = db.Column(db.String(200), primary_key=True)

class Services(UserMixin, db.Model):
    __tablename__ = 'Services'
    ServiceID = db.Column(db.String(200), primary_key=True)
    GardenerID = db.Column(db.String(200))
    Price = db.Column(db.String(200))
    Date = db.Column(db.String(200))
    Job_type = db.Column(db.String(200))
    CustomerID = db.Column(db.String(200))


class Plant(UserMixin, db.Model):
    __tablename__ = 'Plant'
    PlantID = db.Column(db.String(200), primary_key=True)
    Name = db.Column(db.String(200))
    SoilID = db.Column(db.String(200))
    Irrigation_Requirements = db.Column(db.String(200))
    Environment = db.Column(db.String(200))
    Comments = db.Column(db.String(200))

class Seed(UserMixin, db.Model):
    __tablename__ = 'Seed'
    SeedID = db.Column(db.String(200), primary_key=True)
    Name = db.Column(db.String(200))
    # SoilID = db.Column(db.String(200))
    Irrigation_Requirements = db.Column(db.String(200))
    Expected_Selling_Price = db.Column(db.String(200))
    Comments = db.Column(db.String(200))


class Soil(UserMixin, db.Model):
    __tablename__ = 'Soil'
    SoilID = db.Column(db.String(200), primary_key=True)
    Mineral_Details = db.Column(db.String(200))
    Type = db.Column(db.String(200))
    Fertiliser = db.Column(db.String(200))

class Tools(UserMixin, db.Model):
    __tablename__ = 'Tools'
    ToolID = db.Column(db.String(200), primary_key=True)
    Name = db.Column(db.String(200))
    Description = db.Column(db.String(200))

class Product_Reviews(UserMixin, db.Model):
    __tablename__ = 'Product_Reviews'
    Product_ReviewID = db.Column(db.String(200), primary_key=True)
    Review = db.Column(db.String(200))
    ProductID = db.Column(db.String(200))
    CustomerID = db.Column(db.String(200))
    Rating = db.Column(db.String(200))


class Product_Request(UserMixin, db.Model):
    __tablename__ = 'Product_Request'
    RequestID = db.Column(db.String(200), primary_key=True)
    ProductID = db.Column(db.String(200))
    Quantity = db.Column(db.String(200))
    CustomerID = db.Column(db.String(200))


class Service_Select(UserMixin, db.Model):
    __tablename__='Service_Select'
    ServiceRequestID = db.Column(db.String(200), primary_key=True)
    First_name = db.Column(db.String(200))
    Last_name = db.Column(db.String(200))
    Locality = db.Column(db.String(200))
    Address = db.Column(db.String(200))
    Rating = db.Column(db.String(200))
    Price = db.Column(db.String(200))
    Date = db.Column(db.String(200))
    Job_type = db.Column(db.String(200))

class Nursery(UserMixin, db.Model):
    __tablename__ = 'Nursery'
    NurseryID = db.Column(db.String(200), primary_key=True)
    Name = db.Column(db.String(200))
    Phone_Number = db.Column(db.String(200))
    Location = db.Column(db.String(200))
    Email = db.Column(db.String(200))
    Price_Range = db.Column(db.String(200))
    GST_number = db.Column(db.String(200))
    Rating = db.Column(db.String(200))
    Number_of_Rating = db.Column(db.String(200))
