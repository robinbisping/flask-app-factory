from secrets import token_urlsafe
from sqlalchemy.ext.hybrid import hybrid_property

from neon.extensions import bcrypt, db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    __password = db.Column("password", db.String(254), nullable=False)
    last_login = db.Column(db.DateTime())
    tokens = db.relationship("Token")

    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = bcrypt.generate_password_hash(password)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User(id={0}, email={1}, password={2}, last_login={3})>"\
            .format(self.id, self.email, self.password, self.last_login)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(id=user_id).first()


class Token(db.Model):
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(254), unique=True, nullable=False)
    last_login = db.Column(db.DateTime)

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = token_urlsafe(32)

    def __repr__(self):
        return "<Token(id={0}, user={1}, token={2}, last_login={3})>"\
            .format(self.id, self.user_id, self.token, self.last_login)
