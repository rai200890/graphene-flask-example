from sqlalchemy.sql import func

from .app import db


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.String(2), index=True, nullable=False)
    number = db.Column(db.String(9), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship("User", back_populates="phones")
    db.UniqueConstraint("ddd", "number", "user_id", name="ux_phones_ddd_number_user_id")


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
        session = db.session
        try:
            phones = params.pop("phones", [])
            user = User(**params)
            session.add(user)
            for phone in phones:
                phone["user"] = user
                session.add(Phone(**phone))
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
