#!/usr/bin/python3
"""
importing all the classes and subclasses together with json
because we are going to need them
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects. if it is
        not initialised, the objects will be empty"""
        return FileStorage.__objects

    def new(self, obj):
        """where obj is the parameters of the class
        the kdobj_classname is the name of the class,
        eg lets say class Dog, and
        puppy=Dog(self), the kdobj_classname will be Dog"""
        kdobj_classname = obj.__class__.__name__
        """in the the __objects dictionary, a new key with
        the name of the class.the_id will be equal to
            all the parameters involved using our example
        in the last comment, we can save all our params as
            __objects[Dog.unique_obj_id]=all_parameters"""
        FileStorage.__objects["{}.{}".format(kdobj_classname, obj.id)] = obj

    def save(self):
        """with the dictionary and unique id created from new,
            we will be saving it into file using the json format
            since the dictionary name is __objects and there is a key named:
            classname.unique_id containing all the
            parameters such as created_at,
            updated_at etc """
        general_dict = FileStorage.__objects
        """for every key in general_dict,  """
        """kdobjdict an empty dictionary to store the result then we
        will Iterate over the keys of the general_dict"""
        kdobjdict = {}
        """the new but empty dictionary kdobjdict; its keys will contain
        a key value obj from the general_dict
        Convert the value corresponding to the current key to a
        dictionary and assign it to kdobjdict with the key obj
        in essence, kdobjdict[obj] value is a dictionary string
        containing things in k:v format """
        for obj in general_dict.keys():
            kdobjdict[obj] = general_dict[obj].to_dict()
            with open(FileStorage.__file_path, "w") as f:
                json.dump(kdobjdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                kdobjdict = json.load(f)
                for o in kdobjdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
