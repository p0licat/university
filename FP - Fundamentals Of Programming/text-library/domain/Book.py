'''
    This module defines the class Book, which is one of the main items inside a library that we need to manage.
'''

from domain.BookException import BookException

class Book:
    '''
        Book class. Books are a type of item that the library manager needs to manage. Since this application only
        keeps track of the stock of books of the library, all attributes that we need are:
            ID, Title, Description, Author
            0    1       2            3
            
        0 - ID is a positive integer that serves as an unique identifier for each book. 
        1 - Title is a string of characters that can contain basically anything, since we don't want to limit the artist.
        2 - Description is a string characters, again with no restriction as with Title.
        3 - Author is a string of characters, again with no restriction as with Title.
    '''
    
    def __init__(self, _id, title, description, author):
        '''
            This is the constructor of the Book object. It first validates that the ID is a valid one, and then 
            constructs an object with the given values after a type validation.
            
            Except for ID there are no limits imposed on what the Title, Description and Author have to be as long
            as they are strings.
            
            Input:
                _id:         positive integer
                title:       string
                description: string
                author:      string
                
            No output.
        '''
        if type(_id) != type(0) or ( type(_id) == type(0) and _id < 0 ):
            raise BookException("Initialized with bad ID.")
        
        if type(title) != type(""):
            raise BookException("Initialized with bad Title.")
        
        
        if type(description) != type(""):
            raise BookException("Initialized with bad Description.")
        
        
        if type(author) != type(""):
            raise BookException("Initialized with bad Author.")
        
        self._id = _id
        self._title = title
        self._description = description
        self._author = author

    def __eq__(self, other):
        '''
           Manual override for comparison operation.
        '''
        if type(self) != type(other):
            return False
        if self._id != other.getId():
            return False
        if self._title != other.getTitle():
            return False
        if self._description != other.getDescription():
            return False
        if self._author != other.getAuthor():
            return False        
        return True
    
    # <GETTERS AND SETTERS>
    def getId(self):
        '''
            Getter for the ID property of the Book object. Returns a positive integer.
            Input:
                self: object defined by this class
            Output: 
                self._id: positive integer
        '''
        return self._id
    
    def getTitle(self):
        '''
            Getter for the Title property of the Book object. Returns a string.
            Input:
                self: object defined by this class
            Output: 
                self._title: string
        '''
        return self._title
    
    def getDescription(self):
        '''
            Getter for the Description property of the Book object. Returns a string.
            Input:
                self: object defined by this class
            Output: 
                self._description: string
        '''
        return self._description
    
    def getAuthor(self):
        '''
            Getter for the Author property of the Book object. Returns a string.
            Input:
                self: object defined by this class
            Output: 
                self._author: string
        '''
        return self._author
    
    def setTitle(self, title):
        '''
            Setter for the Title property of the Book object. Modifies the value of self._title.
            Input:
                self: object defined by this class
            
            No output.
        '''
        if type(title) == type(""):
            self._title = title
        else:
            raise BookException("Title is not of type string.")
    
    def setDescription(self, description):
        '''
            Setter for the Description property of the Book object. Modifies the value of self._description.
            Input:
                self: object defined by this class
            
            No output.
        '''
        if type(description) == type(""):
            self._description = description
        else:
            raise BookException("Description is not of type string.")
    
    def setAuthor(self, author):
        '''
            Setter for the Author property of the Book object. Modifies the value of self._author.
            Input:
                self: object defined by this class
            
            No output.
        '''
        if type(author) == type(""):
            self._author = author
        else:
            raise BookException("Author is not of type string.")
        
    # </GETTERS AND SETTERS>
        
    def __repr__(self):
        return ("ID: " + str(self._id) + " , Title: " + self._title + "\tAuthor: " + 
                self._author + "\tDescription: " + self._description)
        