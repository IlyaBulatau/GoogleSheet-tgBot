from database.connect import Base, session
import sqlalchemy as db
from sqlalchemy.orm import relationship 

from logger.logger import logger

class BaseModel:

    def save(self):
        try:
            session.add(self)
            session.commit()
        except:
            session.rollback()

class User(Base, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=True)
    tablse = relationship('Table', backref='user')

    def save_email(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            logger.info(f'User with {self.tg_id} add email: {v}')
        session.commit()

    def save(self):
        super(User, self).save(self)
        logger.warning(f'ADD NEW USER WITH USERNAME: {self.username}, ID: {self.tg_id}')

    @classmethod
    def get_user_by_id(cls, tg_id):
        user = cls.query.filter(cls.tg_id == tg_id).first()
        return user
    
class Table(Base, BaseModel):
    __tablename__ = 'tablse'

    id = db.Column(db.BigInteger(), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    user_tg_id = db.Column(db.BigInteger(), db.ForeignKey('users.tg_id'))
    