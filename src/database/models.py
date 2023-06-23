from database.connect import Base, session
import sqlalchemy as db
from sqlalchemy.orm import relationship 

from logger.logger import logger

class BaseModel:

    def save(self):
        session.add(self)
        session.commit()
        

class User(Base, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True, nullable=False)
    username = db.Column(db.String(), nullable=False, default='Not have username')
    email = db.Column(db.String(), nullable=True)
    vip = db.Column(db.Boolean(), default=False)
    tablse = relationship('Table', backref='user')

    def save_email(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            logger.info(f'User with {self.tg_id} add email: {v}')
        session.commit()

    def save(self):
        try:
            super(User, self).save()
            logger.warning(f'ADD NEW USER WITH USERNAME: {self.username}, ID: {self.tg_id}')
        except Exception as e:
            logger.critical(f'Error {e} DONT SAVE USER')
            session.rollback()

    @classmethod
    def get_all_users(cls):
        users = cls.query.all()
        return users

    @classmethod
    def get_user_by_id(cls, tg_id):
        user = cls.query.filter(cls.tg_id == tg_id).first()
        return user
    
class Table(Base, BaseModel):
    __tablename__ = 'tablse'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(), nullable=False, default='New Table')
    url = db.Column(db.String(), nullable=False)
    user_tg_id = db.Column(db.BigInteger(), db.ForeignKey('users.tg_id'))

    def save(self):
        if self.is_unique_table(self.url):
            try:
                super(Table, self).save()
                logger.warning(f'USER BY ID {self.user_tg_id} CREATE NEW TABLE WITH URL {self.url}')
            except Exception as e:
                logger.critical(f'ERROR CREATE TABLE WITH USER ID {self.user_tg_id}')
                session.rollback()

    @classmethod
    def is_unique_table(cls, url):
        table = cls.query.filter(cls.url == url).first()
        return table == None
    
    @classmethod
    def rename(cls, **kwargs):
        url = kwargs.pop('table_url', None)
        table = cls.query.filter(cls.url == url).first()
        try:
            for k, v  in kwargs.items():
                setattr(table, k, v)
            session.commit()
        except:
            session.rollback()
    