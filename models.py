from sqlalchemy import Column, Integer, String, Numeric,Float
from database import Base

# Define AddressBook class inheriting from Base
class AddressEntry(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    city = Column(String(256))
    state = Column(String(256))
    latitude = Column(Float)
    longitude = Column(Float)
