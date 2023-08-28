import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tea_collection_association_table = db.Table(
    'tea_collection_association',
    db.Model.metadata,
    db.Column('tea_id', db.Integer, db.ForeignKey('teas.tea_id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.collection_id'))
)

class Tea(db.Model):
    __tablename__ = 'teas'
    
    tea_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blend_name = db.Column(db.String(128), unique=True, nullable=False)
    tasting_notes = db.Column(db.String(1000))
    date_of_purchase = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float)
    origin = db.Column(db.String(128))
    caffeine = db.Column(db.Boolean, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'))
    variety_type = db.Column(db.String(128), db.ForeignKey('variety.variety_type'), nullable=False, )
    brewing_temp_F = db.Column(db.Integer)
    brewing_temp_C = db.Column(db.Integer)
    brewing_time_min = db.Column(db.Integer)
    tsp_per_cup = db.Column(db.Integer)
    
    collections = db.relationship(
        'Collection', secondary=tea_collection_association_table, backref='teas')
    varieties = db.relationship("Variety", backref="tea")
    ratings = db.relationship("Rating", backref="tea", cascade= "all, delete")
    suppliers = db.relationship("Supplier", backref="tea")

class Variety(db.Model):
    __tablename__ = 'varieties'
    
    teatype = db.Column(db.String(128), primary_key=True, unique = True, nullable = False)
    standard_brewing_temp_F = db.Column(db.Integer)
    standard_brewing_temp_C = db.Column(db.Integer)
    standard_brewing_time = db.Column(db.Integer)
    standard_tsp_per_cup = db.Column(db.Integer)
        
class Rating(db.Model):
    __tablename__ = 'ratings'
    
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False)
    review_comments = db.Column(db.String(1000))
    ranking = db.Column(db.Integer, nullable=False)
    tea_id = db.Column(db.Integer, db.ForeignKey('teas.tea_id'))
    author_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), unique = True, nullable = False)
    password = db.Column(db.String(128), unique = True, nullable = False)
    
    collections = db.relationship('Collection', backref='users')
    ratings = db.relationship('Rating', backref='users', cascade = 'all, delete')
    
class Collection(db.Model):
    __tablename__ = 'collections'
    
    collection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    collection_name = db.Column(db.String(128), nullable = False)
    
    teas = db.relationship('Tea', secondary=tea_collection_association_table, back_populates='collections')
    
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable = False)
    location = db.Column(db.String(128))
    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))
    
    teas = db.relationship('Tea', backref='suppliers', cascade= "all, delete")
    


