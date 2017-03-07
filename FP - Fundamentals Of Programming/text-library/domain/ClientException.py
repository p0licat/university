'''
    This module defines the ClientException class, which handles all exception of the type ClientException.
    it does not depend on any other module.
'''

class ClientException(Exception):
    '''
        ClientException class handles all thrown exceptions of the type ClientException. It inherits the Exception 
        class.
    '''
    def __init__(self, message):
        self._message = message
    
    def __repr__(self, *args, **kwargs):
        return "Error! " + self._message
    