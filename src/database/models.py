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
            ...

class User(Base, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=True)