#!/usr/bin/python3
'''
    Contains the FileStorage class
'''
import json
import models


class FileStorage:
    '''
        serializes instances to a JSON file & deserializes back to instances
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            returns the dictionary __objects
        '''
        new_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dict[k] = v
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        '''
            sets in __objects the obj with key <obj class name>.id
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            serializes __objects to the JSON file (path: __file_path)
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            deserializes the JSON file to __objects
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        delete obj from __objects if it’s inside
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
        call reload() method for deserializing the JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        '''
        Retrieves an instance based on the provided class and ID.
        Args:
            cls (type): Class of the instance to retrieve.
            id (str): ID of the instance to retrieve.
        Returns:
            object: The instance if found, otherwise returns None.
        '''
        obj_dict = self.all(cls)
        for i, j in obj_dict.items():
            matchstring = cls + '.' + id
            if i == matchstring:
                return j

        return None

    def count(self, cls=None):
        '''
        Counts the number of instances of a specified class or
        all classes if no class is provided.
        Args:
            cls (type): Optional. Class whose instances are to be counted.
        Returns:
            int: Total number of instances of the specified class or all classes.
        '''
        obj_dict = self.all(cls)
        return len(obj_dict)
