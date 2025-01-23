from sqlalchemy import Float, Column, Integer, String, ForeignKey
from database import Base


class Continent(Base):
    __tablename__ = 'continent'
    continent_id = Column(Integer, primary_key=True)
    continent_name = Column(String, nullable = False)

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String, nullable=False)
    capital = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    population = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    continent = Column(Integer, ForeignKey('continent.continent_id'))


