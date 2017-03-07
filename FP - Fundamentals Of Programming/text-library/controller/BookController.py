'''
    BookController module is a module that defines the BookController class. The BookController interfaces with
    BookRepository and the UI, as we use a MVC structure in this program.
'''

from undo.Operation import *
from sorting.filter import *
from undo.Undo import Undo
from controller.controller import Controller
from domain.BookException import BookException
from domain.Book import Book
from copy import deepcopy

class BookController(Controller):
    '''
        Class BookController interfaces with the UI and performs actions on the BookRepository using methods that
        safely validate all input.
        
        Every BookController object has a _repo property in which it holds a BookRepository type object. This object
        contains a list of all Book items and performs operations on this list of books through the BookController.
    '''
    
    def __init__(self, repo):
        '''
            Constructor for the BookController object. This constructor defines the _repo property. The idea behind the 
            controller is the following:

                There are methods that perform operations on the _repo property of a controller object, in order to avoid
                direct manipulation of the rpeository from the UI class. 
            
                _repo: a Repository type object that is handled by the methods defined in this class.
        '''
        self._repo = repo
        self._undoController = None

    def getRepo(self):
        return self._repo

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
        
    def searchById(self, _id):
        '''
            This method looks inside the repository for a book that exists with the same id as _id and passes it back
            to the user interface.
            Input:
                self - object defined by this class
                _id  - integer 
            Output:
                Book - Book type object
                False - if no book is found
        '''
        if self._repo.findId(_id) != False:
            return self._repo.elementFromId(_id)
        return False
    
    def searchByTitle(self, titleToSearch):
        '''
            Method passes titleToSearch to the repository's searchByTitle() method which returns either false for
            no results or a list of Books for multiple results, or a single Book object for one result.
            Input:
                self - object defined by this class
                titleToSearch - string 
            Output: 
                Book or list of Books for matching results
                False for no results
        '''
        rlist = []
        result = self._repo.getElementList()

        rlist = filterList(result, lambda x: x.getTitle() == titleToSearch)

        if rlist != []:
            if len(rlist) == 1:
                return rlist[0]
            else:
                return rlist
        else:
            return False
        
    def modifyBookAuthor(self, bookElement, newAuthor):
        '''
            Searches repository for corresponding bookElement and replaces its author. This is done by first removing the entry
            from the repository, constructing a new one and adding it.
            Input:
                self - object defined by this class
                bookElement - Book type object
                newAuthor - string
            Output:
                True/False
        '''
        if self._repo.findId(bookElement.getId()) == False:
            return False
        newBook = Book(bookElement.getId(), bookElement.getTitle(), bookElement.getDescription(), newAuthor)
        self._repo.removeElement(bookElement)
        self._repo.addElement(newBook)
        newOperation = ModifyOperation(self._repo, bookElement, newBook)
        self._undoController._addOperation(newOperation)
        return True
        
    def modifyBookTitle(self, bookElement, newTitle):
        '''
            Searches repository for corresponding bookElement and replaces its title. This is done by first removing the entry
            from the repository, constructing a new one and adding it.
            Input:
                self - object defined by this class
                bookElement - Book type object
                newTitle - string
            Output:
                True/False
        '''
        if self._repo.findId(bookElement.getId()) == False:
            return False
        newBook = Book(bookElement.getId(), newTitle, bookElement.getDescription(), bookElement.getAuthor())
        self._repo.removeElement(bookElement)
        self._repo.addElement(newBook)
        newOperation = ModifyOperation(self._repo, bookElement, newBook)
        self._undoController._addOperation(newOperation)
        return True

    def modifyNumberOf(self, _id, num):
        '''
            Modifies number of books with ID == _id
            Input:
                self - object defined by this class
                _id  - integer
                num  - value of books with id == _id
            Output:
                True if book with id == _id was found and modified.
                False if book with id == _id was not found.
        '''
        books = self._repo.getElementList()
        for i in books:
            if i.getId() == _id:
                self._repo.setNumberOf(_id, num)
                return True
        return False
    
    def removeElement(self, bookElement):
        '''
            Method passes bookElement to the repository and asks for removal.
            Input:
                self - object defined by this class
                bookElement - Book type object
        '''
        self._repo.removeElement(bookElement)
        newOperation = RemoveOperation(self._repo, bookElement)
        self._undoController._addOperation(newOperation)
        return True
    
    def addBook(self, book):
        '''
            Adds a book to repository.
            Input:
                book - book type object
            Output:
                True/False
        '''
        if not self.checkIdExists(book.getId()):
            try:
                self._repo.addElement(book)
                newOperation = AddOperation(self._repo, book)
                self._undoController._addOperation(newOperation)
                return True
            except BookException as e:
                return e
        else:
            return False
            
    def checkIdExists(self, _id):
        '''
            Returns true if book with id == _id is found in repository.
            Input:
                self - object defined by this class
                _id  - integer
            Output:
                True/False
        '''
        if self.findExistingId(_id) != False:
            raise BookException("Id already exists!")
            return True
        return False    

    def findExistingId(self, _id):
        '''
            Returns true if a book in repository has book.id() == _id.
            Input:
                self - object defined by this class
                _id  - integer
            Output:
                True / False
        '''
        if self.searchById(_id) != False:
            return True
        return False
        
    def getAllBooks(self):
        '''
            Getter for bookElements in repository.
            Output:
                list of Book type objects
        '''
        return self._repo.getElementList()

    def getAllNumbers(self):
        '''
            Getter for number of books, used for rental managing.
            Output:
                dictionary of _id -> number
        '''

        return self._repo.getNumberList()

    def getNumberOf(self, _id):
        '''
            Returns the number of copies of book with id == _id inside the repository.
            Input:
                self - object defined by this class
                _id  - integer
            Output:
                nlist[_id] - integer found in dictionary _id -> number of copies
        '''
        nlist = self._repo.getNumberList()
        return nlist[_id]
