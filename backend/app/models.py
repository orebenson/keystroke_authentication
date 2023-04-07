from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import BaseModel


class User(BaseModel):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	password = Column(String)

	samples = relationship('Sample', back_populates='user')


class Sample(BaseModel) :
	__tablename__ = 'sample'

	id = Column(Integer, primary_key=True, index=True)
	user_id =  Column(Integer, ForeignKey('user.id'))
	timestamp = Column(DateTime)
	keytimes = Column(JSON)

	user = relationship('User', back_populates='samples')



