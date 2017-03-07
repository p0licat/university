'''
    This is the main module of the application. It imports all other modules and launches the application from
    the main function defined below. Its main responsibility is the User Interface.
'''

from os import listdir
from os.path import isfile, join
from repository.repository import Repository
from controller.ClientController import ClientController
from controller.BookController import BookController
from controller.RentalController import RentalController
from domain.Book import Book
from domain.Client import Client
from ui.UI import UserInterface

def main():
    '''
        This is the main() function and is the first thing that is ran by the program. It contains all the objects 
        necessary for execution and everything related to the UI.
    '''

    # repositories must be initialized with a string containing the type of the repository in order to use files
    clientRepository = Repository("Client")
    bookRepository = Repository("Book")
    rentalRepository = Repository("Rental")

    clientController = ClientController(clientRepository)
    bookController = BookController(bookRepository)
    rentalController = RentalController(rentalRepository, clientController, bookController)

    keepAlive = True
    while keepAlive:    
        userInput = input("Please choose the mode (memory/file). Insert 'x' to quit: ")
        if userInput == 'x':
            return
        elif userInput == 'memory':
            clientRepository.addElement(Client(0, 'Mircea', 1962353535353))
            clientRepository.addElement(Client(1, 'Dorin', 1962353535354))
            clientRepository.addElement(Client(3, 'Marius', 1962353335353))
            clientRepository.addElement(Client(6, 'Dacia', 1962353444353))
            bookRepository.addElement(Book(0, "Dorin Mateiu", "Viata pe un Stalp", "Mihaila"))
            bookRepository.addElement(Book(1, "Salutare", "Lume", "Viata"))
            bookRepository.addElement(Book(2, "Inca", "O Carte", "Buna"))

            ui_object = UserInterface(clientController, bookController, rentalController)
            ui_object.launchMainMenu()

            keepAlive = False
        elif userInput == 'file':
            print ("Available files: ")

            files = listdir('resources')
            for i in files:
                if i[-4:] == '.txt':
                    print (i)
            print()

            print ("Please choose the file you want to load.", "If that file does not exist it will be created.")
            print ("Insert 'x' at any time to quit.")
            chosenFile = input("Please insert file name: ")

            if chosenFile == 'x':
                continue

            alreadyExists = False
            existingFile = None
            for i in files:
                if i[:-4] == chosenFile:
                    alreadyExists = True
                    existingFile = i

            if alreadyExists == True:
                print ("File found! Type again to load: ")
                confirmInput = input()
                if confirmInput == 'x':
                    continue
                if confirmInput == chosenFile:
                    # file was found and will be loaded
                    if '.txt' in chosenFile:
                        chosenFile = chosenFile[:-4]
                    filePath = 'resources/' + chosenFile + '.txt'
                    
                    ui_object = UserInterface(clientController, bookController, rentalController, filePath)
                    ui_object.launchMainMenu()
                else:
                    print ("Returning...")
                    continue
            else:
                print ("Create file? Type again to confirm: ")
                confirmInput = input()
                if confirmInput == 'x':
                    continue
                if confirmInput == chosenFile:
                    filePath = 'resources/' + chosenFile + '.txt'
                    
                    ui_object = UserInterface(clientController, bookController, rentalController, None)
                    ui_object.launchMainMenu(filePath)
                else:
                    print ("Returning...")
                    continue
                
            keepAlive = False
        else:
            print ("Error! Please insert 'file' or 'memory' ")

main()