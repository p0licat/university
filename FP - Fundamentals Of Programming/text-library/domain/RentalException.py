'''
    This module defines the RentalException class, which handles all exception of the type RentalException.
    it does not depend on any other module.
'''

class RentalException(Exception):
    '''
        RentalException class handles all thrown exceptions of the type RentalException. It inherits the Exception 
        class.
    '''
    def __init__(self, message):
        self._message = message
    
    def __repr__(self, *args, **kwargs):
        return "Error! " + self._message
    