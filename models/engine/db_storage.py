#!/usr/bin/python3
'''
    Contains the class DBStorage
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    '''
        interaacts with the MySQL database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Instantiate a DBStorage object
        '''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Query current database session
        '''
        db_dict = {}

        if cls is not None and cls != '':
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dict[key] = obj
            return db_dict

    def new(self, obj):
        '''
            add the object to the current database session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            commit all changes of the current database session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            delete from the current database session obj if not None
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            reloads data from the database
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            call remove() method on the private session attribute
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
        Retrieves an instance based on the provided class and ID.
        Args:
            cls (type): Class of the instance to retrieve.
            id (str): ID of the instance to retrieve.
        Returns:
            object: The instance if found, otherwise returns None.
        '''
        o_dict = models.storage.all(cls)
        for i, j in o_dict.items():
            matchstring = cls + '.' + id
            if i == matchstring:
                return j

        return None

    def count(self, cls=None):
        '''
        Counts the number of instances of a specified class
        '''
        o_dict = models.storage.all(cls)
        return len(o_dict)
