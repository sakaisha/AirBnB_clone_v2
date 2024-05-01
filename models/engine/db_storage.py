#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import os
import json
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


class DBStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __engine:
        __session:
    """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.environ['HBNB_MYSQL_USER'],
                                             os.environ['HBNB_MYSQL_PWD'],
                                             os.environ['HBNB_MYSQL_HOST'],
                                             os.environ['HBNB_MYSQL_DB'],
                                             pool_pre_ping=True))

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
            if cls is None, return all objects, else return class's
        """
        all_objects = {}
        class_names = ['State', 'City', 'User', 'Place', 'Review', 'Amenity']
        if cls is None:
            for class_name in class_names:
                for obj in self.__session.query(eval(class_name)).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    all_objects[key] = obj
        else:
            for obj in self.__session.query(eval(cls)).all():
                key = str(obj.name) + "." + str(obj.id)
                all_objects[key] = obj
        return all_objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """serialize the file path to JSON file path
        """
        self.__session.commit()

    def reload(self):
        """serialize the file path to JSON file path
        """
        Base.metadata.create_all(self.__engine)
        session_fac = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_fac)
        self.__session = scoped_session(session_fac)

    def delete(self, obj=None):
        """1 - delete obj from __objects and write to JSON filename
        """
        my_dict = {}
        self.__session.delete(obj)

    def close(self):
        """close the session"""
        self.__session.remove()
