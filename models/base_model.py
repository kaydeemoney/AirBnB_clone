#!/usr/bin/python3
"""we are importing models since we already
 made it a package using our __init__.py
    file, then uuid4 creates a very unique
     id that is not time dependent
    Defines our BaseModel class that is
     common to everyone."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the HBnB project.
     classes can inherit from this"""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Probably Unused.
            **kwargs (dict): Key/value pairs of
             attributes that will enter this.
            id :this is gotten through uuid4
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        """if the new object argument/parameters
         is not empty
         explanation of the below code
         kwargs.items contains all parameters
             taken by a basemodel object,
             k represents the key, v is the value:
        if there is anything like created_at
                     or updated_at
                    as a key in the dictionary of parameters
                     meaning the new object 
                    is already not empty, then the said key
                     will be equal to
                    the datetime.today() value but will be in
                     the tform format which is
                    year-month-day hour:minute:seconds format
                     and the value and 
                    corresponding key will be saved back to the
                     object dictionary in that format
        if theres nothing like created_at or
                     updated_at as a key but other keys exists,
                    let the values of that other key remain the
                     same with the key and continue
                    as keyword parameters
         """
        if len(kwargs) != 0:
            
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)
            """if what we want to save has empty parameters
             ie contains no creation
            or update date then already from our __init__.py,
             we explained storage as an instance of 
            class FileStorage, so we will use the new() method"""

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        kddict = self.__dict__.copy()
        kddict["created_at"] = self.created_at.isoformat()
        kddict["updated_at"] = self.updated_at.isoformat()
        kddict["__class__"] = self.__class__.__name__
        return kddict

    def __str__(self):
        """Return the print/str representation
         of the BaseModel instance."""
        kdclass_name = self.__class__.__name__
        return "[{}] ({}) {}".format(kdclass_name, self.id, self.__dict__)
