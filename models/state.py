#!/usr/bin/python3
"""This is the state class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade='all, delete-orphan',
                              backref='state')
    else:
        name = ""

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def cities(self):
            """ returns City instances
            """
            all_cities = models.storage.all(City)
            select_cities = []
            for v in all_cities.values():
                if v.state_id == self.id:
                    select_cities.append(v)
            return select_cities
