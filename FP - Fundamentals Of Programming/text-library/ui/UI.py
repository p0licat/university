'''
    This module contains the UI class, which manages the user input and displays the menu options.
'''

from sorting.shellsort import * 
from undo.Undo import Undo
from os import listdir
from domain.Client import Client
from domain.Book import Book
from domain.Rental import Rental
from domain.ClientException import ClientException
from domain.BookException import BookException
from domain.RentalException import RentalException
from repository.repository import Repository
from domain.FileValidator import FileValidator

class UserInterface:
    '''
        This class defines every method related to the user interface. An UI object will have the get_input() method, which waits
        for user input and returns it inside the 'user_input' parameter, and everything that needs to be done with the input is 
        done inside the object.
    '''    
    user_input = None            # user_input contains the last input that was read
    user_input_type = None        # user_input_type contains a string describing the type of user_input_type

    def __init__(self, clientController, bookController, rentalController, filePath = None):
        '''
            Constructor for the UI object. Has a clientController and a bookController as input.
            Input:
                clientController
                bookController
        '''
        self._undoController = Undo()
        self._clientController = clientController
        self._bookController = bookController
        self._rentalController = rentalController
        self._filePath = filePath

    def _addRental(self, userId, bookElement):
        try:
            result = self._rentalController._addRental(userId, bookElement)
            if result == True:
                print ("Added! There are now " + str(self._bookController.getNumberOf(bookElement.getId())) + " books left in repository.")
        except RentalException as e:
            print(e)
   
    def _showRentals(self):
        '''
            Returns all rentals.
        '''
        try:
            result = self._rentalController._showRentals()
            checkedList = []
            for i in result:
                if not self._clientController.searchById(i.getRenterId()) in checkedList:    
                    renterUser = self._clientController.searchById(i.getRenterId())
                    checkedList.append(renterUser)
                    bookList = []
                    for k in result:
                        if k.getRenterId() == renterUser.getId():
                            bookList.append(k.getRentedBook())
                    print ("User ", renterUser, " rented: \n")
                    for k in bookList:
                        print(k)
            return self._rentalController.getAllRentals()
        except RentalException as e:
            print (e)
        
        
        
    def _get_input(self, expected_type):
        '''
            This method tries to obtain a valid input from the user and store it in the user_input property of 
            this class. It relies on the standard input() function.
            
            Input:
                self: object defined by this class
                expected_type: object returned by the type() function specifying the desired type of input ( int / string )
            Output:
                'True' if user_input was modified.
                'False' if user_input was not modified.
        '''
        u_input = input("Enter command: ")

        if expected_type == type(0): # if expected type is <class 'int'>
            try:
                u_input = int(u_input)   # convert the string containing the integer to an actual int
            except:
                print ("Error! Please insert a natural number! \n")
                return False
        else:
            return False
        
        # structure below modifies the use_input and user_input_type parameters based on user input
        # prints error to console if invalid input
        if expected_type == type(0) and u_input >= 0 and u_input <= 12:
            self.user_input = u_input # int
            self.user_input_type = 'int'
            return True
        elif expected_type == type(''):
            self.user_input = u_input # string
            self.user_input_type = 'string'
            return True
        else:
            print ("Error! Insert a valid option! \n")
            return False
        
    def _loadFile(self):
        '''
            the _loadFile method takes a file, once the path has been validated and the file created, and
            loads it into the program's memory via the controllers and the fileValidator, which checks
            for mistakes in the file.
        '''
        fileValidator = FileValidator()
        
        self._clientController.loadFile(self._filePath, fileValidator)
        self._bookController.loadFile(self._filePath, fileValidator)
        self._rentalController.loadFile(self._filePath, fileValidator)
        print ("Loaded file!")

    def _saveFile(self):
        '''
            The _saveFile method saves the current repositories from memory to a file which has its path specified
            in self._filePath.
        '''
        if self._filePath != None:
            clientList = self._clientController.getAllClients()
            bookList   = self._bookController.getAllBooks()
            rentalList = self._rentalController.getAllRentals()

            openFile = open(self._filePath, 'r+')
            for i in clientList:
                openFile.write("Client, " + str(i.getId()) + ", " + str(i.getName()) + ", " + str(i.getCnp()) + '\n')
            for i in bookList:
                openFile.write("Book, " + str(i.getId()) + ", " + str(i.getTitle()) + ", " + str(i.getDescription()) + ", " + str(i.getAuthor()) + '\n') 
            for i in rentalList:
                openFile.write("Rental, " + str(i.getRenterId()) + ", " + str(i.getRentedBook().getId()) + ", " + str(i.getId()) + '\n' )

        
    def launchMainMenu(self, newFilePath = None):
        '''
            launchMenu() is the main function a UI object. When launchMenu() ends the program stops execution.
            The main loop works in 3 phases. First it prints the menu, it then asks for user input and then launches 
            the method corresponding to that input.
        '''
        # check if using file
        usingFile = False
        if newFilePath != None:
            usingFile = True
        if self._filePath != None:
            usingFile = True
            self._loadFile()
        elif self._filePath == None and usingFile == True:
            self._filePath = newFilePath
            newFile = open(self._filePath, 'w')
            self._loadFile()

        # adds undo controller to controllers
        self._clientController.addUndoController(self._undoController)
        self._bookController.addUndoController(self._undoController)
        self._rentalController.addUndoController(self._undoController)

        # builds the menu, to add or remove options just append or delete them
        # from this string and modify the conditions inside the main loop
        menu = "Actions: \n"
        menu += "\t1 - Operations on Clients. \n"
        menu += "\t2 - Operations on Books. \n"
        menu += "\t3 - Operations on Rentals\n"
        menu += "\t4 - Statistics\n"
        menu += "\t5 - Undo\n"
        menu += "\t6 - Redo\n"
        menu += "\t0 - Exit \n"
        
        keepAlive = True
        while keepAlive: # while exit was not called
            print (menu)
            u_input = self._get_input(type(0)) # get an integer ( type(0) == <class 'int'> ) 
            if u_input == True: # check for valid input
                if self.user_input == 0: # check first if input was exit
                    print ("Exiting...")
                    keepAlive = False   # elifs make sure this method is good
                    if usingFile == False:
                        while ( True ):
                            userInput = input("Save to file? (y/n): ")
                            if userInput == 'y':
                                print ("Current files are:")
                                files = listdir('resources')
                                fileNames = []
                                for i in files:
                                    print (i)
                                    if ".txt" in i:
                                        fileNames.append(i[:-4])
                                    else:
                                        fileNames.append(i)

                                newFileName = input("Enter new file name: ")
                                if '.txt' in newFileName:
                                    if newFileName[-4:] == '.txt':
                                        newFileName = newFileName[:-4]
                                if newFileName in fileNames:
                                    print ("File already exists!")
                                    continue
                                else:
                                    self._filePath = 'resources/' + newFileName + '.txt'
                                    newFile = open(self._filePath, 'w')
                                    self._saveFile()
                                    print ("Saved! Exitting...")
                                    return
                            if userInput == 'n':
                                return
                    elif usingFile == True:
                        self._saveFile()
                        print("Saved! Exitting...")

                elif self.user_input == 1:  # menu option 1
                    self._launchClientMenu()
                elif self.user_input == 2:  # menu option 2
                    self._launchBookMenu()
                elif self.user_input == 3:
                    self._rentBookMenu()
                elif self.user_input == 4:
                    self._launchStatisticsMenu()
                elif self.user_input == 5:
                    if self._undoController._undo() == True:
                        print ("Last operation was undone!")
                    else:
                        print ("Nothing to undo!")
                elif self.user_input == 6:
                    if self._undoController._redo() == True:
                        print ("Last undone operation was redone!")
                    else:
                        print ("Nothing to redo!")


    def _launchStatisticsMenu(self):
        '''
            Method prints options regarding the different statistics that can be displayed for the user, and calculates the required 
            statistic. Also handles printing that statistic to the screen.
        '''
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Print most rented book. \n"
        menuOptions += "\t2 - Print clients by activity.\n"
        menuOptions += "\t0 - Back\n"

        keepAlive = True
        while keepAlive:
            print(menuOptions)
            u_input = self._get_input(type(0))
            if u_input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    rlist = self._rentalController.getAllRentals()
                    if rlist != []:
                        listOfBooks = rlist
                        mostRentedMax = 0
                        mostRentedBook = None
                        for i in range(len(listOfBooks)):
                            numberOfRentals = 0
                            for k in range(i, len(listOfBooks)):
                                if listOfBooks[k].getRentedBook() == listOfBooks[i].getRentedBook():
                                    numberOfRentals += 1
                            if numberOfRentals > mostRentedMax:
                                mostRentedMax = numberOfRentals
                                mostRentedBook = listOfBooks[k].getRentedBook()
                        print ("Most rented: \n\t", self._bookController.searchById(mostRentedBook.getId()), "\n with ", mostRentedMax, " rentals.") 
                    else:
                        print ("No rentals!")
                elif self.user_input == 2:
                    rlist = self._rentalController.getAllRentals()
                    if rlist == []:
                        print ("No rentals!")
                        return
                    # generating [id, numberOfBooks] list 
                    renterIdList = []
                    for i in rlist:
                        found = False 
                        for k in renterIdList:
                            if i.getRenterId() == k[0]:
                                found = True
                        if not found:        
                            renterIdList.append([i.getRenterId(), 1])
                        else:
                            for k in renterIdList:
                                if k[0] == i.getRenterId():
                                    k[1] += 1
                    # sorting the list
                    done = False # first decide the order
                    while not done:
                        sortingOrder = self._get_alpha_str_input("Insert 'a' for ascending or 'd' for descending order: ")
                        if sortingOrder == None:
                            return
                        elif sortingOrder == 'a' or sortingOrder == 'd':
                            done = True
                        else:
                            print ("Plsease insert 'a' or 'd'")

                    if sortingOrder == 'a':
                        shellsort(renterIdList)
                    elif sortingOrder == 'd':
                        shellsort(renterIdList, True)

                    # printing the list
                    first = True
                    for i in renterIdList:
                        if first:
                            first = False
                            print(str(self._clientController.searchById(i[0])) + " with " + str(i[1]) + " rentals. *")
                        else:
                            print(str(self._clientController.searchById(i[0])) + " with " + str(i[1]) + " rentals.")

    def _launchClientMenu(self):
        '''
            Displays menu options for all operations involving Client type objects. The structure is similar to the
            one from the main menu, it first generates a string with the options and then picks a valid one from input.
            Back simply exits this loop and returns to the MainMenu.
        '''    
        
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Add Client\n"
        menuOptions += "\t2 - Show Clients\n"
        menuOptions += "\t3 - Search for Client\n"
        menuOptions += "\t4 - Remove a Client\n"
        menuOptions += "\t5 - Modify a Client\n"
        menuOptions += "\t0 - Back\n"
        
        keepAlive = True
        while keepAlive:
            print (menuOptions)
            u_input = self._get_input(type(0))
            try:
                if u_input == True:
                    if self.user_input == 0:
                        keepAlive = False
                    elif self.user_input == 1:
                        self._addClientMenu()
                    elif self.user_input == 2:
                        self._printClientMenu() 
                    elif self.user_input == 3:
                        self._searchClientMenu()
                    elif self.user_input == 4:
                        self._removeClientMenu()
                    elif self.user_input == 5:
                        self._modifyClientMenu()
            except ClientException as e:
                print (e)
               
    def _launchBookMenu(self):
        '''
            Displays menu options for all operations involving Book type objects. The structure is similar to the
            one from the main menu, it first generates a string with the options and then picks a valid one from input.
            Back simply exits this loop and returns to the MainMenu.
        '''
        
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Add Book \n"
        menuOptions += "\t2 - Show Books \n"
        menuOptions += "\t3 - Search for a Book\n"
        menuOptions += "\t4 - Remove a Book\n"
        menuOptions += "\t5 - Modify a Book\n"
        menuOptions += "\t6 - Rent or Return a Book\n"
        menuOptions += "\t0 - Back \n"
        
        keepAlive = True
        while keepAlive:
            print (menuOptions)
            u_input = self._get_input(type(0))
            if u_input == True:
                if self.user_input == 0: # check first if input was exit
                    keepAlive = False
                elif self.user_input == 1:
                    self._addBookMenu()
                elif self.user_input == 2:
                    self._printBooksMenu()
                elif self.user_input == 3:
                    self._searchBookMenu()
                elif self.user_input == 4:
                    self._removeBookMenu()
                elif self.user_input == 5:
                    self._modifyBookMenu()
                elif self.user_input == 6:
                    self._rentBookMenu()

    def _rentBookMenu(self):
        '''
            Displays the menus and options involving book renting to the user.
        '''
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Rent a Book\n"
        menuOptions += "\t2 - Return a Book\n"
        menuOptions += "\t3 - Show Rentals\n"
        menuOptions += "\t0 - Back\n"

        keepAlive = True
        while keepAlive:
            print (menuOptions)
            _input = self._get_input(type(0))
            if _input != None:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:

                    print ("Books: ")
                    bookList = self._bookController.getAllBooks()
                    for i in bookList:
                        print(str(self._bookController.getNumberOf(i.getId())) + " copies of: " + str(i))
                    
                    foundBook = self._searchBookById()

                    # first check if there are copies left in the repository
                    if foundBook != False:
                        if self._bookController.getNumberOf(foundBook.getId()) < 1:
                            print ("No more copies of that book to give!")
                            return

                    if foundBook != False:
                        print ("Users: ")
                        clientList = self._clientController.getAllClients()
                        for i in clientList:
                            print(i)
                        usrRent = self._get_int_input("Select user to rent to: ")
                        correctValue = False
                        for i in clientList:
                            if i.getId() == usrRent:
                                correctValue = True
                        if correctValue:
                            self._addRental(usrRent, foundBook)
                        else:
                            print ("Error! Not a valid ID!")
                            return

                elif self.user_input == 2:
                    print ("Users: ")
                    clientList = self._clientController.getAllClients()
                    validClientList = [] # save all clients that have rented a book
                    bookList = self._bookController.getAllBooks()
                    rentList = self._rentalController.getAllRentals()
                    
                    for i in clientList:
                        for k in rentList:
                            if k.getRenterId() == i.getId(): # only print clients that have rented a book
                                print(i)
                                validClientList.append(i) # add to list of clients that have rented a book

                    usrReturn = self._get_int_input("Select user ID: ")
                    if usrReturn == None:
                        return

                    print ("Books: ")
                    
                    for k in rentList:
                        if k.getRenterId() == usrReturn:
                            print(k.getRentedBook())

                    bookReturn = self._get_int_input("Select book ID to return: ")
                    if bookReturn == None:
                        return
                    result = self._rentalController._removeRental(usrReturn, bookReturn)
                    if result == False:
                        print ("Nothing to remove!")
                    elif result == True:
                        print ("Successfully removed rental!")

                elif self.user_input == 3:
                    self._showRentals()

    def _modifyBookMenu(self):
        '''
            Prints a menu which enables the user to first find and select one book based on different parameters 
            and then modify that book's properties. It uses the searchBook functions in order to obtain a Book
            type object. After a client has been 'selected', confirmModifyBook is called with that object as a 
            parameter.
        '''
        menuOptions = "Find the book to modify: \n"
        menuOptions += "\t1 - Find by ID\n"
        menuOptions += "\t2 - Find by Title\n"
        menuOptions += "\t0 - Back\n"
        
        keepAlive = True
        while keepAlive:
            print (menuOptions)
            _input = self._get_input(type(0))
            if _input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    result = self._searchBookById()
                    if result != False:
                        self._confirmModifyBookMenu(result)
                elif self.user_input == 2:
                    result = self._searchBookByTitle()
                    if result != False:
                        self._confirmModifyBookMenu(result)
        
    def _confirmModifyBookMenu(self, bookElement):
        '''
            This function gets a bookElement as a parameter. This can be either a single Book object or a list of
            Book objects, which is then reduced to a single object by asking the user to pick only one item.
            After a single Book object is 'selected', this function helps the user pick what field he wants to 
            modify.
        '''
        while type(bookElement) == type([1, 2]):
            print ("Warning! Multiple results!\n")
            _select_input = self._get_int_input("Please insert the ID of the correct item:")
            if _select_input == None:
                return False
            for i in bookElement:
                if i.getId() == _select_input:
                    bookElement = i
                    break
        
        print ("Choose what to modify: \n" + "\t1 - Title \n\t2 - Author \n\t3 - Number of Books \n\t0 - Back\n")
        _input = self._get_input(type(0))
        if _input != None:
            if self.user_input == 0:
                return 
            elif self.user_input == 1:
                self._modifyBookTitleMenu(bookElement)
            elif self.user_input == 2:
                self._modifyBookAuthorMenu(bookElement)
            elif self.user_input == 3:
                self._modifyNumberOfBooks(bookElement)

    def _modifyNumberOfBooks(self, bookElement):
        '''
            Helps user modify the number of books for bookElement.
        '''
        print ("Current number: " + str(self._bookController.getNumberOf(bookElement.getId())))
        newNumber = self._get_int_input("Insert new number: ")
        if newNumber != None:
            self._bookController.modifyNumberOf(bookElement.getId(), newNumber)
        else:
            return False

    
    def _modifyBookTitleMenu(self, bookElement):
        '''
        This function asks for a new book title in order to replace the old one that is found in bookElement.
            After a new title is specified by the user, the parameters are passed further into _bookController.
        '''
        newName = self._get_book_str_input("Insert new book title: ")
        if newName == None:
            return False
        else:
            self._bookController.modifyBookTitle(bookElement, newName)

    def _modifyBookAuthorMenu(self, bookElement):
        '''
            This function asks for a new book author in order to replace the old one that is found in bookElement.
            After a new author is specified by the user, the parameters are passed further into _bookController.
        '''
        newName = self._get_book_str_input("Insert new book author: ")
        if newName == None:
            return False
        else:
            self._bookController.modifyBookAuthor(bookElement, newName)
                    
    def _removeBookMenu(self):
        '''
            Prints menu that helps user select a book to remove.
        '''
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Remove by ID\n"
        menuOptions += "\t0 - Back"
        
        keepAlive = True
        while keepAlive:
            print (menuOptions)
            _input = self._get_input(type(0))
            if _input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    result = self._searchBookById()
                    if result != False:
                        self._confirmRemoveBookMenu(result)
    
    def _confirmRemoveBookMenu(self, bookElement):
        '''
            Allows user to filter results and remove correct entry.
        '''     
        # this structure reduces the number of search results to one
        while type(bookElement) == type([1, 2]):
            print ("Warning! Multiple results!\n")
            _select_input = self._get_int_input("Please insert the ID of the correct item:")
            if _select_input == None:
                return False
            for i in bookElement:
                if i.getId() == _select_input:
                    bookElement = i
                    break 
                
        # asks user if he is sure, if yes the Book object is passed to the _bookController    
        print ("Remove? \n" + "\t1 - Yes \n\t2 - No")
        _input = self._get_input(type(0))
        if _input != None:
            if self.user_input == 2:
                return 
            elif self.user_input == 1:
                val = self._bookController.removeElement(bookElement)
                rlist = self._rentalController.getAllRentals()
                if val == True:
                    done = False
                    while not done:
                        done = True
                        for i in rlist:
                            if i.getRentedBook() == bookElement:
                                self._rentalController.removeRental(i.getRenterId(), i.getRentedBook())
                                done = False
                                break
    
    def _searchBookMenu(self):
        '''
            Handles searching the repository for Book objects that correspond to the input and printing them to
            the screen. It works with multiple results, for example if some books have identical titles.
        '''
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Search by ID\n"
        menuOptions += "\t2 - Search by Title\n"
        menuOptions += "\t0 - Back\n"
        
        keepAlive = True
        while keepAlive:
            print (menuOptions)
            _input = self._get_input(type(0))
            if _input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    self._searchBookById()
                elif self.user_input == 2:
                    self._searchBookByTitle()
    
    def _searchBookByTitle(self):
        '''
            Gets a valid Title from the user and then passes it to the _bookController for lookup. The user
            can change his mind by inserting 'x', for which the _get_book_str_input function returns 'None'
        '''
        titleToSearch = self._get_book_str_input("Please insert title: ")
        if titleToSearch == None:
            return False
        else:
            result = self._bookController.searchByTitle(titleToSearch)
            if result != False:
                print (result)
                return result
            else:
                print ("No book with that title was found.")
                return False
            
                            
    def _searchBookById(self):
        '''
            Gets a valid ID from the user and then passes it to the _bookController for lookup. The user 
            can change his mind as usual by inserting 'x', for which the _get_int_input function returns 'None'
        '''        
        idToSearch = self._get_int_input("Insert ID to search for: ")
        if idToSearch == None:
            return False
        result = self._bookController.searchById(idToSearch)
        if result != False:
            print (result)
            return result
        else:
            print ("Book with that ID was not found!")
            return False
        
    
    def _modifyClientMenu(self):
        '''
            Prints a menu which enables the user to first find and select one client based on different parameters 
            and then modify that client's properties. It uses the searchClient functions in order to obtain a Client
            type object. After a client has been 'selected', confirmModifyClient is called with that object as a 
            parameter.
        '''
        menuOptions = "Find the client to modify: \n"
        menuOptions += "\t1 - Find by ID\n"
        menuOptions += "\t2 - Find by Name\n"
        menuOptions += "\t3 - Find by CNP\n"
        menuOptions += "\t0 - Back\n"
        
        keepAlive = True
        while keepAlive:
            print (menuOptions)
            _input = self._get_input(type(0))
            if _input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    result = self.searchClientByIdMenu()
                    if result != False:
                        self._confirmModifyClientMenu(result)
                elif self.user_input == 2:
                    result = self.searchClientByNameMenu()
                    if result != False:
                        self._confirmModifyClientMenu(result)
                elif self.user_input == 3:
                    result = self.searchClientByCnpMenu()
                    if result != False:
                        self._confirmModifyClientMenu(result)
      
    def _confirmModifyClientMenu(self, clientElement):
        '''
            This function gets a clientElement as a parameter. This can be either a single Client object or a list of
            Client objects, which is then reduced to a single object by asking the user to pick only one item.
            After a single Client object is 'selected', this function helps the user pick what field he wants to 
            modify.
        '''
        while type(clientElement) == type([1, 2]):
            print ("Warning! Multiple results!\n")
            _select_input = self._get_int_input("Please insert the ID of the correct item:")
            if _select_input == None:
                return False
            for i in clientElement:
                if i.getId() == _select_input:
                    clientElement = i
                    break
        
        print ("Choose what to modify: \n" + "\t1 - Name \n\t2 - CNP \n\t0 - Back\n")
        _input = self._get_input(type(0))
        if _input != None:
            if self.user_input == 0:
                return 
            elif self.user_input == 1:
                self._modifyClientNameMenu(clientElement)
            elif self.user_input == 2:
                self._modifyClientCnpMenu(clientElement)
    
    def _modifyClientNameMenu(self, clientElement):
        '''
            This function asks for a new client name in order to replace the old one that is found in clientElement.
            After a new name is specified by the user, the parameters are passed further into _clientController.
        '''
        newName = self._get_alpha_str_input("Insert new client name: ")
        if newName == None:
            return False
        else:
            self._clientController.modifyClientName(clientElement, newName)
        
    
    def _modifyClientCnpMenu(self, clientElement):
        '''
            This function asks for a new client CNP in order to replace the old one that is found in clientElement.
            After a new CNP is specified by the user, the parameters are passed further into _clientController.
        '''
        newCnp = self._get_client_cnp_input("Insert new client CNP: ")
        if newCnp == None:
            return False
        else:
            self._clientController.modifyClientCnp(clientElement, newCnp)
                
    def _printClientMenu(self):
        '''
            Prints all clients to the console. The function uses the ClientController class to interface with the 
            repository and gather the list from the repository that retains all clients using the getAll() method. 
            ClientController.getAll() returns a list of Client() objects. This list is printed.
        '''
        _list = self._clientController.getAllClients()
        for i in _list:
            print ( i )
            
    def _removeClientMenu(self):
        '''
            Menu enabling user to pick a single Client to remove. First a valid input is gathered, and then after using
            the searchClient functions to localize a single Client, the user is asked to confirm the deletion.
        '''
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Remove by ID\n"
        menuOptions += "\t2 - Remove by Name\n"
        menuOptions += "\t3 - Remove by CNP\n"
        menuOptions += "\t0 - Back\n"
        
        # structure below uses calls of the search functions in order to find an object to remove
        keepAlive = True
        while keepAlive:
            print(menuOptions)
            _input = self._get_input(type(0))
            if _input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    result = self.searchClientByIdMenu() 
                    if result != False:
                        self._confirmRemoveClientMenu(result)    
                elif self.user_input == 2:
                    result = self.searchClientByNameMenu()
                    if result != False:
                        self._confirmRemoveClientMenu(result)
                elif self.user_input == 3:
                    result = self.searchClientByCnpMenu()
                    if result != False:
                        self._confirmRemoveClientMenu(result)  
    
    def _confirmRemoveClientMenu(self, clientElement):
        '''
            In case multiple results have been returned by the search function, this Menu reduces the number of Clients
            to one, and asks for confirmation to remove that Client from the repository.
        '''
        
        # this structure reduces the number of search results to one
        while type(clientElement) == type([1, 2]):
            print ("Warning! Multiple results!\n")
            _select_input = self._get_int_input("Please insert the ID of the correct item:")
            if _select_input == None:
                return False
            for i in clientElement:
                if i.getId() == _select_input:
                    clientElement = i
                    break 
                
        # asks user if he is sure, if yes the Client object is passed to the _clientController    
        print ("Remove? \n" + "\t1 - Yes \n\t2 - No")
        _input = self._get_input(type(0))
        if _input != None:
            if self.user_input == 2:
                return 
            elif self.user_input == 1:
                val = self._clientController.removeElement(clientElement)
                rlist = self._rentalController.getAllRentals()
                if val == True:
                    done = False
                    while not done:
                        done = True
                        for i in rlist:
                            if i.getRenterId() == clientElement.getId():
                                self._rentalController.removeRental(i.getRenterId(), i.getRentedBook())
                                done = False
                                break
    
    def _searchClientMenu(self):
        '''
            Handles searching the repository for Client objects that correspond to the input and printing them to
            the screen. It works with multiple results, for example if some clients have identical names.
        '''
        menuOptions = "Actions: \n"
        menuOptions += "\t1 - Search by ID \n"
        menuOptions += "\t2 - Search by Name\n"
        menuOptions += "\t3 - Search by CNP\n"
        menuOptions += "\t0 - Back"
        
        keepAlive = True
        while keepAlive:
            print(menuOptions)
            _input = self._get_input(type(0))
            if _input == True:
                if self.user_input == 0:
                    keepAlive = False
                elif self.user_input == 1:
                    self.searchClientByIdMenu()
                elif self.user_input == 2:
                    self.searchClientByNameMenu()
                elif self.user_input == 3: 
                    self.searchClientByCnpMenu()
                
    def searchClientByIdMenu(self):
        '''
            Gets a valid ID from the user and then passes it to the _clientController for lookup. The user 
            can change his mind as usual by inserting 'x', for which the _get_int_input function returns 'None'
        '''
        idToSearch = self._get_int_input("Insert the ID to look for: ")
        if idToSearch == None:
            return False
        else:
            result = self._clientController.searchById((idToSearch))
            if result != False:
                print (result)
                return result
            else:
                print ("Client with that ID was not found!")
                return False
                
    def searchClientByNameMenu(self):
        '''
            Gets a valid Name from the user and then passes it to the _clientController for lookup. The user 
            can change his mind as usual by inserting 'x', for which the _get_alpha_str_input function returns 'None'
        '''
        nameToSearch = self._get_alpha_str_input("Insert Name to search for: ")
        if nameToSearch == None:
            return False
        else:
            result = self._clientController.searchByName(nameToSearch)
            if result != False:
                if type(result) == type([1, 2]):
                    for i in result:
                        print (i)
                    return result
                else:
                    print (result)
                    return result
                
            else:
                print ("Client with that Name was not found.")
                return False
                
    def searchClientByCnpMenu(self):
        '''
            Gets a valid CNP from the user and then passes it to the _clientController for lookup. The user 
            can change his mind as usual by inserting 'x', for which the _get_int_input function returns 'None'
            It takes any integer as a parameter for the CNP search, since if the CNP is invalid it will simply
            show the user that no Client with that CNP was found.
        '''
        cnpToSearch = self._get_int_input("Insert CNP to search for: ")
        if cnpToSearch == None:
            return False
        else:
            result = self._clientController.searchByCnp(cnpToSearch)
            if result != False:
                if type(result) == type([1, 2]):
                    for i in result:
                        print(i)
                    return result
                else:
                    print(result)
                    return result
            else:
                print ("Client with that CNP was not found.")
                return result
                
    
    def _printBooksMenu(self):
        '''
            Prints all books to the console. The function uses the BookController class to interface with the 
            repository and gather the list from the repository that retains all books using the getAll() method. 
            BookController.getAll() returns a list of Client() objects. This list is printed.
        '''
        _list = self._bookController.getAllBooks()
        _numb = self._bookController.getAllNumbers()
        for i in _list:
            print ( str(_numb[i.getId()]) + " copies of: " + str(i) ) 
    
             
    def _addClientMenu(self):
        '''
            Gathers input from the console and uses it to  add a Client type object to the client repository 
            by interfacing with the Control object. The input consists of three phases: 
                - getting a valid id (integer),
                - getting a valid name (any string)
                - getting a valid CNP (13 digit integer)
            A Client object has 3 attributes: id, name, cnp
            ClientController uses the addClient(Client()) method.
            
            Output: values returned by the _clientController.addClient() method.
                True if was successfully added.
                ClientException if there was a problem.
        '''
        _id = self._get_client_id_input("Insert ID: ")
        if _id == None:
            return
        
        name = self._get_alpha_str_input("Insert name: ")
        if name == None:
            return
        
        cnp = self._get_client_cnp_input("Insert CNP: ")
        if cnp == None:
            return
        else:
            if self._clientController.checkCnpExists(cnp) != False:
                print ("Warning! Client with given CNP already exists!")
        
        newClient = Client(_id, name, cnp)
        return self._clientController.addClient(newClient)

    def _addBookMenu(self):
        '''
            Gathers input from the console and uses it to  add a Book type object to the book repository 
            by interfacing with the Controller object. The input consists of four phases: 
                - getting a valid id (integer),
                - getting a valid Title (any string)
                - getting a valid Description (any string)
                - getting a valid Author (any string)
            A Client object has 3 attributes: id, Title, Description, Author
            ClientController uses the addClient(Client()) method.
            
            Output: values returned by the _clientController.addClient() method.
                True if was successfully added.
                ClientException if there was a problem.
        '''
        _id = self._get_book_id_input("Insert ID:")
        if _id == None:
            return

        value = False
        if self._bookController.findExistingId(_id) == False:            
            title = self._get_book_str_input("Insert Title: ")
            if title == None:
                return
            
            author = self._get_book_str_input("Insert Author: ")
            if author == None:
                return
            
            description = self._get_book_str_input("Insert Description: ")
            if description == None:
                return
            
            bookObj = Book(_id, title, description, author)
            value = self._bookController.addBook(bookObj)
        
        # structure keeps asking user for number of books with that id untill he quits or inserts a valid number 
        while value == False:
            inp = self._get_alpha_str_input ("Book already exists. Modify number of books? (y/n)")
            if inp != None:
                if inp == 'n':
                    return False
                elif inp == 'y':
                    num = self._get_int_input("Insert number of books with ID = " + str(_id) + ": ")
                    if self._bookController.modifyNumberOf(_id, num) == True:
                        print ("Successfully modified number of Books!")
                        return
                    else:
                        value = True
                else:
                    print ("Please insert 'y' or 'n' \n")
                    value = False



    def _get_book_id_input(self, mesg):
        '''
            _get_book_id_input(self, mesg) is a method which obtains a valid id from the console by repeatedly 
            asking for correct input. It can be stopped by inputing x.
            
            The function also checks if there is an already existing ID in the repository.
            
            Input:
                self - object defined by this class
                mesg - string containing message to display when the user is prompted for input
            Output:
                "None" if user inserts 'x'. This is returned by the _get_int_input() if the input is 'x' and
                is forwarded to handle the case when the user wants to stop trying.
        '''        
        while True:
            _input = self._get_int_input(mesg)
            if _input == None:
                return None
            if self._bookController.findExistingId(_input) == True:
                print ("Id already exists!")
                return _input
            else:
                return _input
        
                       
    def _get_book_str_input(self, mesg):
        '''
            _get_book_str_input(self, mesg) is a function that repeatedly tries to obtain a valid string to return
            to the functions that handle books. If the user changes his midn, he can insert 'x' after which 
            the loop will stop.
            
            Input:
                self - object defined by this class
                mesg - string containing message to display when the user is prompted for input
            Output:
                "None" if user inserts 'x'. This is returned by the _get_int_input() if the input is 'x' and
                is forwarded to handle the case when the user wants to stop trying.
        '''
        while True:
            print ("Insert x to cancel. ")
            _input = input(mesg)
            if _input == 'x':
                return None
            if type(_input) == type(""):
                return _input
            
 
    def _get_client_id_input(self, mesg):    
        '''
            _get_id_input(self, mesg) is a method which obtains a valid id from the console by repeatedly 
            asking for correct input. It can be stopped by inputing x.
            
            The function also checks if there is an already existing ID in the repository.
            
            Input:
                self - object defined by this class
                mesg - string containing message to display when the user is prompted for input
            Output:
                "None" if user inserts 'x'. This is returned by the _get_int_input() if the input is 'x' and
                is forwarded to handle the case when the user wants to stop trying.
        '''
        while True:    
            _input = self._get_int_input(mesg)
            if _input == None:
                return None
            try:
                self._clientController.checkIdExists(_input)
            except ClientException as e:
                print (e)  
            else:
                return _input
            

    def _get_client_cnp_input(self, mesg):
        '''
            _get_client_cnp_input(self, mesg) is a method which obtains a valid CNP from the console by repeatedly
            calling _get_int_value()
            
            It is basically an interface for the _get_int_value which propagates the mesg as the calling parameter
            for the _get_int_value(self, mesg) and returns its result after it ends.
            
            The interface repeatedly calls the _get_int_value until an integer of 13 digits is returned, or the user
            gives up.
            
            The CNP is always a positive number.
            
            Input:
                self - object defined by this class
                mesg - string containing message to display when the user is prompted for input
            Output:
                _input - 13 digit long integer as returned by the _get_int_input method
                -1 if the user gives up by inserting the character 'x'
                ( these output values respect the _get_int_input(self, mesg) output model )
        '''
        _input = 0
        while _input != None:
            _input = self._get_int_input(mesg)
            if _input == None:
                return None
            if len(str(_input)) != 13 or _input < 0:
                print ("Error! Please insert 13 digit long positive number!")
            else:
                return _input
        return None

    def _get_int_input(self, mesg):
        '''
            _get_int_input first displays the message that is transmitted as a parameter, and then tries to 
            obtain a positive integer value from the user through the console. If the input is valid it is returned, 
            if not an error message is shown. 
                The user can give up if he inserts x 
            
            Input:
                self - object defined by this class
                mesg - message to display to the user when prompting for input
            Output:    
                _user_input - positive integer value that was inputed by the user if it was valid
                False if user chooses to cancel.
                (prints "Error!...") - string containing error message, if input was invalid
                
        '''
        
        _user_input = None
        
        while ( _user_input != 'x' ):
            print ("Insert x to cancel.")
            _user_input = input(mesg)
            if _user_input == 'x':
                return None       
            try:
                _user_input = int(_user_input)
                if _user_input >= 0:
                    return _user_input
            except:
                print("Error! Please insert integer!")

    def _get_alpha_str_input(self, mesg):
        '''
            _get_alpha_str_input first first displays the message that is transmitted as a parameter, and then returns the
            string inputed by the user if it is valid. If string does not contain only alphanumeric characters
            an error message is printed.
            Input:
                self - object defined by this class.
                mesg - string containing message to display when user is asked for input
            Output:
                _input - string containing only alphanumeric characters
                "Error!..." - string containing error message, if _input is invalid
        '''
        _input = None
        while _input != 'x':
            print ("Insert x to cancel.")
            _input = input(mesg)
            if _input == 'x':
                return None
            valid = True
            for i in range(len(_input)):
                if _input[i] == ' ' or (_input[i] >= 'a' and _input[i] <= 'z') or (_input[i] >= 'A' and _input[i] <= 'Z'): # alphanumeric
                    continue
                else:
                    print ("Error! Please use only letters of the alphabet!")
                    valid = False
                    break
            if valid == True:
                return _input
            

