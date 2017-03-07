'''
    ClientController.py module. This module defines the ClientController class, which connects the UI to the repository.
    Module imports ClientException in order to return some Exceptions back to the UI.
'''

from undo.Operation import *
from sorting.filter import *
from undo.Undo import Undo
from controller.controller import Controller
from domain.ClientException import ClientException
from domain.BookException import BookException
from domain.Client import Client
from copy import deepcopy

class ClientController(Controller):
    '''
        ClientController class. A ClientController object is used by any class that interacts directly with the user
        and acts as an interface between the user input and the back-end. 
        
        Every ClientController object has a _repo property, meaning that for each object a repository is associated.
        It is initialized with a Repository object as a parameter, and performs actions upon this repository.
    '''
    def __init__(self, repo):
        '''
            Creates the _repo property and associates the repo parameter which is a Repository object with
            this property.

            To allow undoes, this class also has an _undoController property, which can be initialized with an 
            Undo type object via the addUndoController() method.

            Input:
                self - object defined by this class
                repo - Repository object which stores all the Client objects inside a list.
                _undoController - None until an Undo object is associated via addUndoController()
        '''
        self._repo = repo
        self._undoController = None

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
        
    def checkCnpExists(self, cnp):
        '''
            Method searches the _repo list of clients for a Client with the same id as the given parameter.
            If it is found it returns True, otherwise returns False.
            Input:
                self - object defined by this class
                cnp - 13 digit long integer 
            Output:
                True if element was found.
                False otherwise.
        '''
        listOfElements = self._repo.getElementList()
        findValue = False
        for i in listOfElements:
            if i.getCnp() == cnp:
                findValue = i

        if findValue == False:
            return False
        else:
            return True
        
    def checkIdExists(self, _id):
        '''
            Method looks inside the repository for an element with a matching id.
            If such an element is found it returns True, otherwise False.
            
            Input:
                self - object defined by this class
                _id - integer value representing the id we are looking for
            Output:
                 True if an element with a matching id is found
                False otherwise, and raises ClientException
        '''
        if self._repo.findId(_id) == True:
            raise ClientException("Error! Client with specified id already exists.")
            return True
        else:
            return False
        
    def addClient(self, client):
        '''
            addClient method. This method takes as a parameter a Client object constructed by using user input, 
            and adds it to the repository by using the _repo.add(Client) method.
            If the add(Client) function throws an exception this exception is returned to the UI. Otherwise True 
            is returned.
            
            Input:
                self - object defined by this class
                client - a Client type object which the method tries to add to the repository
            Output:
                True if operation was successfully performed.
                (throws ClientException if there was a problem)
        '''
        try:
            self._repo.addElement(client)
            newOperation = AddOperation(self._repo, client)
            self._undoController._addOperation(newOperation)
            return True
        except ClientException as e:
            return e
        
    def searchById(self, _id):
        '''
            Returns the client with the matching id from the ClientRepository, if that client exists.
            Input:
                self - object defined by this class
                _id  - integer
            Output:
                False if not found.
                Client object if found.
        '''
        if self._repo.findId(_id) != False:
            return self._repo.elementFromId(_id)
        else:
            return False
            
    def searchByName(self, nameToSearch):
        '''
            Searches ClientRepository for all clients who have the given name and then returns a list of these Clients.
            If there is only one result, the return value is not a list, it is a Client object.
            
            Input:
                self - object defined by this class
                nameToSearch - string containing name
            Output:
                False if not found.
                Client object if found.
                list of Client objects if multiple results are found.
        '''
        rlist = []
        result = self._repo.getElementList()

        rlist = filterList(result, lambda x: x.getName() == nameToSearch)

        if rlist != []:
            if len(rlist) == 1:
                return rlist[0]
            else:
                return rlist
        else:
            return False
        
    def searchByCnp(self, cnpToSearch):
        '''
            Searches ClientRepository for all clients who have the given name and then returns a list of these Clients.
            If there is only one result, the return value is not a list, it is a Client object.
            
            Input:
                self - object defined by this class
                nameToSearch - string containing name
            Output:
                False if not found.
                Client object if found.
                list of Client objects if multiple results are found.
        '''
        rlist = []
        result = self._repo.getElementList()

        rlist = filterList(result, lambda x: x.getCnp() == cnpToSearch)

        if rlist != []:
            if len(rlist) == 1:
                return rlist[0]
            else:
                return rlist
        else:
            return False
        
    def removeElement(self, clientElement):
        '''
            Removes the element from the repository that matches the given Client object.
            Input:
                self - object defined by this class
                clientElement - Client type object
        '''
        self._repo.removeElement(clientElement)
        newOperation = RemoveOperation(self._repo, clientElement)
        self._undoController._addOperation(newOperation)
        return True
        
    def modifyClientName(self, clientElement, newName):
        '''
            ModifyClientName has the result of modifying the name of a client from the repository that matches 
            clientElement. The way this is handled is the following: 
                1. the matching client is removed from the repository
                2. a new Client is constructed with the same properties as clientElement except the name
                    which will now be newName
                3. this Client is added to the repository.
        '''
        self._repo.removeElement(clientElement)
        newClient = Client(clientElement.getId(), newName, clientElement.getCnp())
        newOperation = ModifyOperation(self._repo, clientElement, newClient)
        self._undoController._addOperation(newOperation)
        self._repo.addElement(newClient)
    
    def modifyClientCnp(self, clientElement, newCnp):
        '''
            ModifyClientCnp has the result of modifying the CNP of a client from the repository that matches 
            clientElement. The way this is handled is the following: 
                1. the matching client is removed from the repository
                2. a new Client is constructed with the same properties as clientElement except the CNP
                    which will now be newCnp
                3. this Client is added to the repository.
        '''
        self._repo.removeElement(clientElement)
        newClient = Client(clientElement.getId(), clientElement.getName(), newCnp)
        newOperation = ModifyOperation(self._repo, clientElement, newClient)
        self._undoController._addOperation(newOperation)
        self._repo.addElement(newClient)
    
    def getAllClients(self):
        '''
            getAll method returns the list of Client objects that is found in the _repo property.
        '''
        return self._repo.getElementList()
    
    