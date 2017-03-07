'''
    RentalController.py module. This module defines the RentalController class, which connects the UI to the repository.
'''

from undo.Operation import *
from undo.Undo import Undo
from controller.controller import Controller
from domain.Book import Book
from domain.Client import Client
from domain.Rental import Rental
from domain.RentalException import RentalException

class RentalController(Controller):
    '''
        RentalController class. A RentalController object is used by any class that interacts directly with the user
        and acts as an interface between the user input and the back-end. 
        
        Every RentalController object has a _repo property, meaning that for each object a repository is associated.
        It is initialized with a Repository object as a parameter, and performs actions upon this repository.
    
        The values of the IDs of the Rentals are automatically controlled.

    '''
    def __init__(self, repo, clientController, bookController):
        '''
            Creates the _repo property and associates the _repo parameter which is a Repository object with
            this property.
            Input:
                self - object defined by this class
                repo - Repository   
                _undoController - None until an Undo object is associated via addUndoController()
        '''
        self._lastId = 0
        self._repo = repo
        self._undoController = None
        self._bookController = bookController
        self._clientController = clientController

    def loadFile(self, filePath, fileValidator):
        '''
            Loads file into the repository contained by this class.
        '''
        if self._repo.loadFile(filePath, fileValidator) == False:
            return False
        return True


    def addUndoController(self, undoController):
        '''
            Adds undo controller.
        '''
        self._undoController = undoController
        return True

    def _addRental(self, userId, bookElement):
        '''
            Adds rental to _repo.
        '''
        if self._repo.findId(userId) == False:
            if  self._bookController.getNumberOf(bookElement.getId()) > 0:
                newElement = Rental(userId, bookElement, self._lastId)
                self._repo.addElement(newElement)
                addOperation = AddOperation(self._repo, newElement)
                self._undoController._addOperation(addOperation)
                self._bookController.modifyNumberOf(bookElement.getId(), self._bookController.getNumberOf(bookElement.getId())-1)
                self._lastId += 1
                return True
            else:
                raise RentalException("No more books in repository!")
                return False
        elif self._repo.findId(userId) == True:
            element = self._repo.getElementList()
            for i in element:
                if i.getId() == userId and i.getRentedBook() == bookElement:
                    raise RentalException ("That client already rented " + bookElement.getTitle())
                    return False
            if self._bookController.getNumberOf(bookElement.getId()) > 0:
                newElement = Rental(userId, bookElement, self._lastId)
                self._repo.addElement(newElement)
                addOperation = AddOperation(self._repo, addOperation)
                self._undoController._addOperation(addOperation)
                self._lastId += 1
                self._bookController.modifyNumberOf(bookElement.getId(), self._bookController.getNumberOf(bookElement.getId())-1)
                return True
        else:
            raise RentalException ("Client already has that book!") 

    def _removeRental(self, usrReturn, bookReturn):
        listOfElements = self._repo.getElementList()
        for i in listOfElements:
            if i.getRenterId() == usrReturn:
                if i.getRentedBook().getId() == bookReturn:
                    icopy = i.getRentedBook()
                    self._repo.removeElement(i)
                    self._bookController.modifyNumberOf(i.getRentedBook().getId(), self._bookController.getNumberOf(i.getRentedBook().getId()+1))
                    removeOperation = RemoveOperation(self._repo, i)
                    self._undoController._addOperation(removeOperation)
                    return True
        return False

    def _showRentals(self):
        '''
            Returns all rentals.
        '''
        rentalList = self._repo.getElementList()
        if rentalList != []:
            return rentalList
        else:
            raise RentalException("No rentals!")

    def getAllRentals(self):
        return self._repo.getElementList()


