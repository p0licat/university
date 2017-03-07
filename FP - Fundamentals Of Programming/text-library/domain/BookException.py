'''
    This module defines the BookException class, which handles all exception of the type BookException.
    it does not depend on any other module.
'''

class BookException(Exception):
    '''
        BookException class handles all thrown exceptions of the type BookException. It inherits the Exception 
        class.
    '''
    def __init__(self, message):
        self._message = message
        
    def __repr__(self, *args, **kwargs):
        return "Error! " + self._message