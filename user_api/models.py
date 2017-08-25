from sqlalchemy.sql import func
from user_api.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, index=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_on = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
    last_login_at = db.Column(db.TIMESTAMP, server_default=func.now())
    phones = db.relationship("Phone", back_populates="user")


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.String(2), index=True, unique=True, nullable=False)
    number = db.Column(db.String(9), index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="phones")
