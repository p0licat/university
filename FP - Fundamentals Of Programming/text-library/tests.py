'''
    This file contains everything related to testing the application.
'''

import unittest
from domain.Client import Client
from domain.ClientException import ClientException
from domain.BookException import BookException
from controller.ClientController import ClientController
from controller.BookController import BookController
from undo.Undo import Undo
from domain.Book import Book
from repository.repository import Repository
from domain.Rental import Rental

def testBook():
    try:
        book1 = Book(1, "a", "b", "c")
        assert book1.getId() == 1
        assert book1.getTitle() == "a"
        assert book1.getDescription() == "b"
        assert book1.getAuthor() == "c"
    except:
        assert False
        
    try:
        book1 = Book("D", "d", "d", "d")
        print(book1)
        assert False
    except BookException:
        pass
    
    try:
        book1 = Book(1, "a", "b", "c")
        book1.setTitle(3)
        assert False
    except:
        pass
    
    print ("Book tests ran successfully!")
    
def testBookController():
    repo = Repository()
    controller = BookController(repo)
    undoController = Undo()
    controller.addUndoController(undoController)
    
    assert controller.addBook(Book(1, "ala", "mala", "dala")) == True
    assert controller.searchById(1) != False

    found = controller.searchById(1)
    assert found == Book(1, "ala", "mala", "dala")
    assert controller.searchByTitle("ala") == Book(1, "ala", "mala", "dala")

    assert controller.modifyBookAuthor(Book(1, "ala", "mala", "dala"), 
            "Mercan") != False

    assert controller.modifyBookTitle(Book(1, "ala", "mala", "Mercan"), "Newt") == True
    assert controller.findExistingId(1) == True

    assert controller.removeElement(Book(1, "Newt", "mala", "Mercan")) == True
    assert controller.searchById(1) == False
    assert controller.checkIdExists(1) == False
    
    print ("BookController tests ran successfully!")

def testBookRepository():
    repo = Repository()
    book1 = Book(1, "ala", "mala", "dala")
    
    repo.addElement(book1)
    assert len(repo) == 1
    
    try:
        if repo.addElement(book1) != False:
            assert False
    except BookException:
        pass
    
    book2 = Book(2, "ala", "mala", "dala")
    repo.addElement(book2)
    
    assert len(repo) == 2
    
    print ("BookRepository tests ran successfully!")

def testClient():
    
    try:
        cli = Client(1, "Matthew", 1695454879852) # object to test    
        assert cli.getId() == 1
        assert cli.getName() == "Matthew"
        assert cli.getCnp() == 1695454879852
        
        cli.setName("Mastodon")
        cli.setCnp(1952354451235)
        
        assert cli.getId() == 1
        assert cli.getName() == "Mastodon"
        assert cli.getCnp() == 1952354451235
    except:
        assert False
    
    try:
        cli1 = Client("N", "na", 1955555555555)
        print(cli1)
        assert False
    except ClientException:
        pass
    
    try:
        cli1 = Client(1, "ok", 1952354451235)
        cli1.setName("(")
    except:
        pass
    
    try:
        cli1 = Client(1, "ok", 1952354451235)
        cli1.setCnp(-1)
    except:
        pass


    # at this point, constructor and getters should work.

    print ("Client tests ran successfully!")

def testClientRepository():
    
    repo = Repository()
    c1 = Client(1, "Alice", 6548987854215)
    c2 = Client(2, "Vlad", 1944444444444)

    assert len(repo) == 0

    repo.addElement(c1)
    assert len(repo) == 1
    repo.addElement(c2)
    assert len(repo) == 2


    print ("ClientRepository tests ran successfully!")


def testClientController():
    repo = Repository()
    contr = ClientController(repo)
    undoController = Undo()
    contr.addUndoController(undoController)

    assert contr.addClient(Client(1, "alice", 1111111111111)) == True


    print ("ClientController tests ran successfully!")

def testRental():
    repo = Repository()
    book1 = Book(1, "ala", "mala", "dala")
    
    rentList = Repository()
    rentList.addElement(Rental(2, book1, 0))

    lis1 = rentList.getElementList()
    assert len(lis1) == 1

    rentList.addElement(Rental(2, book1, 1))
    lis1 = rentList.getElementList()
    assert len(lis1) == 2
    assert lis1[0].getRenterId() == 2
    assert lis1[0].getRentedBook() == book1
    assert lis1[0].getId() == 0

    print ("Rental tests ran successfully!")

def testRentalRepository():
    rentalRepo = Repository()
    book1 = Book(0, "The Q", "Albert", "Heinrich")
    book2 = Book(1, "The D", "Elbert", "Reinsich")
    client1 = Client(0, "Mihai", 1854987548795)
    client2 = Client(1, "Alex", 1987548759658)

    rentalRepo.addElement(Rental(1, book1, 0))
    rentalRepo.addElement(Rental(0, book2, 1))

    # _find(_id) returns the Rental from the repository
    # that has the client Id equal to _id

    assert rentalRepo._find(0).getRentedBook() == book1 
    assert rentalRepo._find(1).getId() == 1

    assert rentalRepo._find(1).getRentedBook() == book2
    assert rentalRepo._find(0).getId() == 0

    # findId() function for Repository class
    assert rentalRepo.findId(12) == False
    assert rentalRepo.findId(0) == True

    # elementFromId()
    assert rentalRepo.elementFromId(0).getRentedBook() == book1

    rentalRepo.addElement(Rental(1, book2, 2)) 

    print ("Rental repository tests ran successfully!")


testClient()
testClientController()
testClientRepository()

testBook()
testBookController()
testBookRepository()

testRental()
testRentalRepository()