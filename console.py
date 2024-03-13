#!/usr/bin/python3
"""Necessary things that need to be imported for the HBnB console to work."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State


def parse(arg):
    """we first search if args contain brackets or curly ones"""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            """strip everything by comma"""
            return [i.strip(",") for i in split(arg)]
        else:
            """This extracts a substring from the string arg.
            It starts from the beginning of arg and
             goes up to (but not including) the character
            at the position specified by the first element
              of the tuple returned by brackets.span()"""
            lexer = split(arg[:brackets.span()[0]])
            return_val_1 = [i.strip(",") for i in lexer]
            return_val_1.append(brackets.group())
            return return_val_1
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        return_val_1 = [i.strip(",") for i in lexer]
        return_val_1.append(curly_braces.group())
        return return_val_1


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The prompt will be changed from cmd to hbnb.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing if u input an empty line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        our_input = parse(arg)
        if len(our_input) == 0:
            print("** class name missing **")
        elif our_input[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(our_input[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        our_input = parse(arg)
        kdobjdict = storage.all()
        if len(our_input) == 0:
            print("** class name missing **")
        elif our_input[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(our_input) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(our_input[0], our_input[1]) not in kdobjdict:
            print("** no instance found **")
        else:
            print(kdobjdict["{}.{}".format(our_input[0], our_input[1])])

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        our_input = parse(arg)
        if len(our_input) > 0 and our_input[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(our_input) > 0 and our_input[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(our_input) == 0:
                    objl.append(obj.__str__())
            print(objl)
    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        our_input = parse(arg)
        kdobjdict = storage.all()
        if len(our_input) == 0:
            print("** class name missing **")
        elif our_input[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(our_input) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(our_input[0], our_input[1]) not in kdobjdict.keys():
            print("** no instance found **")
        else:
            del kdobjdict["{}.{}".format(our_input[0], our_input[1])]
            storage.save()

    def default(self, arg):
        """ when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            our_input = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", our_input[1])
            if match is not None:
                command = [our_input[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(our_input[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        our_input = parse(arg)
        count = 0
        for obj in storage.all().values():
            if our_input[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        our_input = parse(arg)
        kdobjdict = storage.all()

        if len(our_input) == 0:
            print("** class name missing **")
            return False
        if our_input[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(our_input) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(our_input[0], our_input[1]) not in kdobjdict.keys():
            print("** no instance found **")
            return False
        if len(our_input) == 2:
            print("** attribute name missing **")
            return False
        if len(our_input) == 3:
            try:
                type(eval(our_input[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(our_input) == 4:
            obj = kdobjdict["{}.{}".format(our_input[0], our_input[1])]
            if our_input[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[our_input[2]])
                obj.__dict__[our_input[2]] = valtype(our_input[3])
            else:
                obj.__dict__[our_input[2]] = our_input[3]
        elif type(eval(our_input[2])) == dict:
            obj = kdobjdict["{}.{}".format(our_input[0], our_input[1])]
            for k, v in eval(our_input[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
