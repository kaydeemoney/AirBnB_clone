#!/usr/bin/python3
"""
__init__ file to make
the folder a package for easy importing
also a method for models directory"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
