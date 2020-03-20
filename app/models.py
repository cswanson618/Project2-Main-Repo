from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .database import Base
import datetime


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }



class Covid(Base, DictMixIn):
    __tablename__ = "daily_cases"

    id = Column(Integer, primary_key=True)
    iso3 = Column(String)
    country_region = Column(String)
    province_state = Column(String)
    lat = Column(Float)
    long = Column(Float)
    date = Column(Date)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)

