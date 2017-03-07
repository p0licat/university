'''
    repository.py module. This module defines the class Repository which contains a list of elements and manages this list.
'''

from domain.Client import Client
from domain.Book import Book
from domain.Rental import Rental

class Repository:
    '''
        Repository class. This class defines an object that stores a list of elements in _list and manages this list.
        It contains methods that help manipulate this list of elements.
    '''
    
    def __init__(self, repoType = None):
        '''
            Constructor for Repository class. 
                initializes private parameter _list
            Input:
                self:       object defined by this class
        '''
        self._list = []
        self._numberOf = {}
        self._type = repoType

    def __len__(self):
        '''
            Manual override of the len() function. Returns the length of the _list property of this class.
            len(Repository) == len(_list)
            Input:
                self - object defined by this class
            Output:
                len(_list) - integer value 
        '''
        return len(self._list)

    def loadFile(self, filePath, fileValidator):
        '''
            Loads file if valid into repository.
        '''
        openFile = open(filePath, 'r+')
        for i in openFile:
            line = i.split(',')
            validObject = fileValidator.ValidateFileInput(self._type, line)
            if validObject != None:
                self.addElement(validObject)

        return True

    def _find(self, _id):
        '''
            Searches _list for element with matching id.
            Input:
                id - integer representing searched id
            Output:
                i - integer representing the position of the element inside _list if found.
                None - if corresponding element was not found.
        '''
        for i in range(len(self._list)):
            if self._list[i].getId() == _id:
                return self._list[i]
        return None
    
    def removeElement(self, element):
        '''
            The function's purpose is to remove the matching element from the _list inside this repository.
            To do this, it iterates through the list of elements and pops the one that has a matching id with the element parameter.
            
            Input:
                self - object defined by this class
                elementElement - a element type object
        '''
        for i in range(len(self._list)):
            if self._list[i] == element:
                self._list.pop(i)
                return
 
    def findId(self, _id):
        '''
            Checks if the repo already has that _id.
            Searches _list for an element with matching id. returns False if not found and True if found.
        ''' 
        if self._find(_id) == None:
            return False
        else:
            return True

    def elementFromId(self, _id):
        '''
            Returns a element object with the given id.
            Input:
                self - object defined by this class
                _id  - integer specifying the id of the desired element object
            Output:
                None if no element has matching ID.
                element type object if a element is found.
        '''
        for i in self._list:
            if i.getId() == _id:
                return i
        return False

    def addElement(self, element):
        '''
            public add(self, element): - public method that adds a element() object to the _list 
            The method first verifies that a element with the same id does not already exist, and then 
            adds the element, if possible, to the _list
            Input:
                self - object defined by this class
                element - element object defined by the element() method in domain.element
            Output:
                (raises elementException if trying to add element with an already existing id)
        '''
        if self._find(element.getId()) != None:
            return False
        self._list.append(element)
        try:
            val = self._numberOf[element.getId()]
            if type(val) == type(0):
                return True
        except:
            # case when there is no number in the dictionary associated to the current item that is
            # being added
            self._numberOf[element.getId()] = 1

    def setNumberOf(self, _id, num):
        '''
            Sets the number of elements with the id == _id to the value represented inside num.
            Input:
                self - object defined by this class
                _id  - integer
                num  - integer
        '''
        self._numberOf[_id] = num

    def getElementList(self):
        '''
            Getter for the _list, returns a list of element() objects, as defined in the domain.element
            module.
            Input:
                self - object defined by this class
            Output:
                list containing all objects in the repository

        '''
        return self._list

    def getNumberList(self):
        '''
            Getter for the _numberOf list, which holds the number of each entry. Used mainly for Book object repositories.
            Input:
                self - object defined by this class
            Output:
                list of integers
        '''
        return self._numberOf