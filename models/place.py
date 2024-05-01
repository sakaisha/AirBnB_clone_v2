#!/usr/bin/python3
"""This is the place class"""
import models
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey
                     ('cities.id', ondelete="CASCADE"),
                     nullable=False)
    user_id = Column(String(60), ForeignKey
                     ('users.id', ondelete="CASCADE"),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", cascade='all, delete-orphan',
                           backref='place')
    amenity_ids = []

    # @property
    # def reviews(self):
    #     """ returns Review instances
    #     """
    #     all_reviews = models.file_storage.all(models.Review)
    #     select_reviews = []
    #     for v in all_reviews.values():
    #         if v.place_id == self.id:
    #             select_reviews.append(v)
    #     return select_reviews

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'), nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), nullable=False))
    amenities = relationship("Amenity", secondary='place_amenity',
                             viewonly=False)

    if 'HBNB_TYPE_STORAGE' in os.environ.keys() and \
       os.environ['HBNB_TYPE_STORAGE'] == 'db':
            pass
    else:
        @property
        def reviews(self):
            """ returns Review instances
            """
            all_reviews = models.file_storage.all(models.Review)
            select_reviews = []
            for v in all_reviews.values():
                if v.place_id == self.id:
                    select_reviews.append(v)
            return select_reviews

        @property
        def amenities(self):
            """ returns Amenity instances
            """
            aminity_list = []
            all_amenities = models.file_storage.all(models.Amenity)
            for v in all_amenities.values():
                if v.id in amenity_ids:
                    amenity_list.append(v)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            if obj.__class__ is Amenity:
                amenity_ids.append(obj.id)
