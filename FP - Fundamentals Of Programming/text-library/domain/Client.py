'''
    Client.py module. This module defines the Client class, which defines a Client type object.
    A client is an object that needs to be managed by the application. Each client has an unique id, 
    an alphanumeric string for a name, and a 13-digit long integer which is the CNP. (personal numeric code)
    
    It imports the ClientException module to throw any exceptions related to the Client class and its controller
    and repository.
'''

from domain.ClientException import ClientException

class Client:
    '''
        Client class. A client is one of the main objects that a library manager needs to manage. This class has the 
        private properties ID, Name, CNP.
                            0   1     2
                            
        0 - ID is a positive number unique for each client, used as an identifier.
        1 - Name is a string that can only contain alphanumeric characters and spaces.
        2 - CNP is a positive 13 digit number that the romanian government uses to identify citizens.
    '''
    def __init__(self, _id, name, cnp):
        '''
            Constructor for the Client class. Takes three parameters and initializes each property with their values.
            Validation is done using the ClientException class, any wrong constructor parameter type will throw a
            ClientException.
            
            Input: 
                self - object defined by this class
                _id  - an integer containing an unique value for each client
                name - alphanumeric string defining the client's name
                cnp  - 13 digit long integer
        '''
        if type(_id) != type(0) or ( type(_id) == type(0) and _id < 0 ):
            raise ClientException("Error! Initialized with bad id.")
        
        valid = True
        for i in range(len(name)):
            if not (name[i] == ' ' or (name[i] >= 'a' and name[i] <= 'z') or (name[i] >= 'A' and name[i] <= 'Z')):
                valid = False
                break
        if not valid:
            raise ClientException("Error! Initialized with bad name.")
        
        if len(str(cnp)) != 13:
            raise ClientException("Error! Initialized with bad CNP.")
        
        self._id = _id # used _id instead of id because name id is reserved
        self._name = name
        self._cnp = cnp
        
    # <GETTERS AND SETTERS>
        
    def getId(self):
        '''
            Getter for the id property of the Client class.
            There is no setter for id.
            Input:
                self - object defined by this class
            Output:
                _id - integer value
        '''
        return self._id
    
    def getName(self):
        '''
            Getter for the name property of the Client class.
            Input:
                self - object defined by this class
            Output:
                _name - string containing alphanumeric characters
        '''
        return self._name
    
    def setName(self, name):
        '''
            Setter for the name property. Modifies the _name property of this class.
            This method validates the name parameter and raises exception if it is not a string of alphanumeric
            characters.
            
            Input:
                self - object defined by this class
                name - string containing the new name
        '''
        for i in range(len(name)):
            if not (name[i] >= 'a' and name[i] <= 'z') and not(name[i] >= 'A' and name[i] <= 'Z') and not name[i] == ' ':
                raise ClientException("Error! Please only use letters of the alphabet!")
        self._name = name
    
    def getCnp(self):
        '''
            Getter for the CNP property of the Client class. 
            Input:
                self - object defined by this class
            Output: 
                _cnp - 13 digit long integer value
        '''
        return self._cnp
    
    def setCnp(self, cnp):
        '''
            Setter for the cnp property of the Client class. 
            A CNP - cod numeric personal ( PNC - Personal numeric code ) is a code used by the romainan government
            for identification of any citizen. Every romanian citizen has an unique personal numeric code.
            For this reason, in case the program will find a user with the same CNP as the one that we're trying to 
            insert, a warning will be displayed.
            
            Input:
            self - object defined by this class
                _cnp - integer of 13 digits
        '''
        if len(str(cnp)) != 13: # check that CNP has 13 digits
            raise ClientException("CNP must be 13 digits long!")
        self._cnp = cnp
        
    # </GETTERS AND SETTERS>    
    
    def __repr__(self): # representation 
        return str(self._id) + " , name = " + self._name + ", cnp = " + str(self._cnp)
