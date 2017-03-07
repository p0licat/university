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
from sorting.shellsort import *
from sorting.filter import *

class TestApp(unittest.TestCase):

    def testSorts(self):
        testList = [1, 3, 2, 56, 5, 3, 2]
        sortedList = shellsort(testList)
        self.assertEqual(type(sortedList), type([1, 2, 3]))
        for i in range(len(sortedList) - 1):
            self.assertLessEqual(sortedList[i], sortedList[i+1])

        sortedList = shellsort(testList, True)
        for i in range(len(sortedList) - 1):
            self.assertGreaterEqual(sortedList[i], sortedList[i+1])

    def testFilter(self):
        testList = [1, 3, 2, 532, 432, 1, 4]
        filteredList = filterList(testList, lambda x: x < 500)
        for i in filteredList:
            self.assertNotEqual(i, 500)
            self.assertLessEqual(i, 500)

    def testBook(self):
        try:
            book1 = Book(1, "a", "b", "c")
            self.assertEqual(book1.getId(), 1)
            self.assertEqual(book1.getTitle(), "a")
            self.assertEqual( book1.getDescription() , "b")
            self.assertEqual( book1.getAuthor() ,  "c")
        except:
            self.assertEqual( False )
            
        try:
            book1 = Book("D", "d", "d", "d")
            self.assertEqual( False )
        except BookException:
            pass
        
        try:
            book1 = Book(1, "a", "b", "c")
            book1.setTitle(3)
            self.assertEqual( False )
        except:
            pass
        

    def testBookController(self):
        repo = Repository()
        controller = BookController(repo)
        undoController = Undo()
        controller.addUndoController(undoController)
        
        self.assertEqual( controller.addBook(Book(1, "ala", "mala", "dala")) ,  True )
        self.assertNotEqual( controller.searchById(1) , False )

        found = controller.searchById(1)
        self.assertEqual( found ,  Book(1, "ala", "mala", "dala") )
        self.assertEqual( controller.searchByTitle("ala") ,  Book(1, "ala", "mala", "dala") )

        self.assertNotEqual( controller.modifyBookAuthor(Book(1, "ala", "mala", "dala"), 
                "Mercan") , False )

        self.assertEqual( controller.modifyBookTitle(Book(1, "ala", "mala", "Mercan"), "Newt") ,  True )
        self.assertEqual( controller.findExistingId(1) ,  True )

        self.assertEqual( controller.removeElement(Book(1, "Newt", "mala", "Mercan")) ,  True )
        self.assertEqual( controller.searchById(1) ,  False )
        self.assertEqual( controller.checkIdExists(1) ,  False )
        
    def testBookRepository(self):
        repo = Repository()
        book1 = Book(1, "ala", "mala", "dala")
        
        repo.addElement(book1)
        self.assertEqual( len(repo) ,  1 )
        
        try:
            if repo.addElement(book1) != False:
                self.assertEqual( False )
        except BookException:
            pass
        
        book2 = Book(2, "ala", "mala", "dala")
        repo.addElement(book2)
        
        self.assertEqual( len(repo) ,  2 )
        
    def testClient(self):
        
        try:
            cli = Client(1, "Matthew", 1695454879852) # object to test    
            self.assertEqual( cli.getId() ,  1 )
            self.assertEqual( cli.getName() ,  "Matthew" )
            self.assertEqual( cli.getCnp() ,  1695454879852 )
            
            cli.setName("Mastodon")
            cli.setCnp(1952354451235)
            
            self.assertEqual( cli.getId() ,  1 )
            self.assertEqual( cli.getName() ,  "Mastodon" )
            self.assertEqual( cli.getCnp() ,  1952354451235 )
        except:
            self.assertEqual( False )
        
        try:
            cli1 = Client("N", "na", 1955555555555)
            self.assertEqual( False )
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

        
    def testClientRepository(self):
        
        repo = Repository()
        c1 = Client(1, "Alice", 6548987854215)
        c2 = Client(2, "Vlad", 1944444444444)

        self.assertEqual( len(repo) ,  0 )

        repo.addElement(c1)
        self.assertEqual( len(repo) ,  1 )
        repo.addElement(c2)
        self.assertEqual( len(repo) ,  2 )

    def testClientController(self):
        repo = Repository()
        contr = ClientController(repo)
        undoController = Undo()
        contr.addUndoController(undoController)

        self.assertEqual( contr.addClient(Client(1, "alice", 1111111111111)) ,  True )

    def testRental(self):
        repo = Repository()
        book1 = Book(1, "ala", "mala", "dala")
        
        rentList = Repository()
        rentList.addElement(Rental(2, book1, 0))

        lis1 = rentList.getElementList()
        self.assertEqual( len(lis1) ,  1 )

        rentList.addElement(Rental(2, book1, 1))
        lis1 = rentList.getElementList()
        self.assertEqual( len(lis1) ,  2 )
        self.assertEqual( lis1[0].getRenterId() ,  2 )
        self.assertEqual( lis1[0].getRentedBook() ,  book1 )
        self.assertEqual( lis1[0].getId() ,  0 )

    def testRentalRepository(self):
        rentalRepo = Repository()
        book1 = Book(0, "The Q", "Albert", "Heinrich")
        book2 = Book(1, "The D", "Elbert", "Reinsich")
        client1 = Client(0, "Mihai", 1854987548795)
        client2 = Client(1, "Alex", 1987548759658)

        rentalRepo.addElement(Rental(1, book1, 0))
        rentalRepo.addElement(Rental(0, book2, 1))

        # _find(_id) returns the Rental from the repository
        # that has the client Id equal to _id

        self.assertEqual( rentalRepo._find(0).getRentedBook() ,  book1 ) 
        self.assertEqual( rentalRepo._find(1).getId() ,  1 )

        self.assertEqual( rentalRepo._find(1).getRentedBook() ,  book2 )
        self.assertEqual( rentalRepo._find(0).getId() ,  0 )

        # findId() function for Repository class
        self.assertEqual( rentalRepo.findId(12) ,  False )
        self.assertEqual( rentalRepo.findId(0) ,  True )

        # elementFromId()
        self.assertEqual( rentalRepo.elementFromId(0).getRentedBook() ,  book1 )

        rentalRepo.addElement(Rental(1, book2, 2)) 

if __name__ == '__main__':
    unittest.main()