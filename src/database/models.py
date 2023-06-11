from database.connect import Base, session
import sqlalchemy as db

from logger.logger import logger

class BaseModel:

    def save(self):
        try:
            session.add(self)
            session.commit()
            logger.warning(f'ADD NEW USER WITH USERNAME: {self.username}, ID: {self.tg_id}')
        except:
            session.rollback()

class User(Base, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=True)

    def save_email(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        session.commit()

    @classmethod
    def get_user_by_id(cls, tg_id):
        user = cls.query.filter(cls.tg_id == tg_id).first()
        return user
    