from database.connect import Base, session
import sqlalchemy as db

class BaseModel:

    def save(self):
        try:
            session.add(self)
            session.commit()
        except:
            ...

class User(Base, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True, nullable=False)
    username = db.Column(db.String(), nullable=False)
