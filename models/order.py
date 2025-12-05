from . import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_image = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    status = db.Column(db.String(20), default="To Pay")  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



