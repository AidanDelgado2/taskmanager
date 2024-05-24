from random import randrange
from datetime import date
import os, base64
import json

from flask_login import UserMixin

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
    
class Task(db.Model, UserMixin):
    __tablename__ = 'tasks'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, unique=False, nullable=False)
    duedate= db.Column(db.String, unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, task, duedate):
        self._task = task    # variables with self prefix become part of the object, 
        self._duedate = duedate

    # UserMixin/Flask-Login require a get_id method to return the id as a string
    def get_id(self):
        '''Used by Flask-Login to store user id in session cookie as unicode string'''
        return str(self.id)
    
    # UserMixin/Flask-Login requires is_authenticated to be defined
    @property
    def is_authenticated(self):
        return True

    # UserMixin/Flask-Login requires is_active to be defined
    @property
    def is_active(self):
        return True

    # UserMixin/Flask-Login requires is_anonymous to be defined
    @property
    def is_anonymous(self):
        return False

    # a name getter method, extracts name from object
    
    # a setter function, allows name to be updated after initial object creation
    @task.setter
    def task(self, task):
        self.task = task
    
    # a getter method, extracts email from object
    @property
    def task(self):
        return self.task
    
    # a setter function, allows name to be updated after initial object creation
    @duedate.setter
    def duedate(self, duedate):
        self.duedate = duedate
        
    # check if uid parameter matches user id in object, return boolean
    @property
    def duedate(self):
        return self.duedate

    # check password parameter versus stored/encrypted password
  

    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "task": self.task,
            "duedate": self.duedate,
        }

    # CRUD update: updates user name, password, phone
    # returns self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initTasks():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        t1 = Task(task='Get Groceries', duedate='05/23/2024')
        t2 = Task(task='Taxes', duedate='04/23/2025')
        tasks = [t1, t2]

        """Builds sample user/note(s) data"""
        for task in tasks:
            try:
                task.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()


