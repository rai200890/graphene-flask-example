from sqlalchemy.sql import func
from .app import db


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.String(2), index=True, unique=True, nullable=False)
    number = db.Column(db.String(9), index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship("User", back_populates="phones")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    last_name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(200), unique=True, index=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now(), index=True)
    updated_on = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now(), index=True)
    phones = db.relationship("Phone", back_populates="user")

    @classmethod
    def create(cls, **params):
        connection = db.engine.connect()
        transaction = connection.begin()
        try:
            phones = []
            if params.get("phones"):
                phones = params.pop("phones")
            user = User(**params)
            db.session.add(user)
            for phone in phones:
                phone["user"] = user
                db.session.add(Phone(**phone))
            transaction.commit()
            return user
        except Exception as e:
            transaction.rollback()
            raise e
