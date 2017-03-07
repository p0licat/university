'''
	This module contains the definition of the Rental class, which is used by the Repository class. A repository containing Rental objects
	is the way all rentals are stored.
'''

class Rental:
	'''
		Rental object, contains a user id that is linked to a Book object.
	'''
	def __init__(self, clientId, bookElement, rentalId):
		'''
			Constructor for the Rental object. Defines three properties:
			_rentalId, _bookElement, _clientId
				0 			1			2

			The idea behind any Rental object is the following: a client is associated with a book. The fact that a rental associating
			client x with book y exists means that client x rented book y.

			0 - _rentalId holds an automatically generated positive integer. This is has to be unique and generated upon construction.
			1 - _bookElement holds a Book type object, and is associated with a Client type object.
			2 - _clientId holds an integer that specifies the Id of the client associated with the book inside _bookElement.
		'''
		self._rentalId = rentalId
		self._bookElement = bookElement
		self._clientId = clientId

	def getRenterId(self):
		'''
			Getter for the Id of the renter, which is a client Id. Returns the ID of the Client who rented the book.
			Input: 
				self - object defined by this class
			Output:
				_clientId - integer
		'''
		return self._clientId

	def getRentedBook(self):
		'''
			Getter for the _bookElement property of this class. Returns the rented book as a Book object.
			Input: 
				self - object defined by this class
			Output:
				Book type object
		'''
		return self._bookElement

	def getId(self):
		'''
			Theoretically inherited by the LibraryObject class, has to have a getId function for handling by the repository.
			Getter for the Id of the rental. Each rental has an unique, automatically generated Id.
			Input:
				self - object defined by this class
			Output: 
				The return value of getRentalId() which is an integer
		'''
		return self.getRentalId()

	def getRentalId(self):
		'''
			Getter for the rentalId. Returns an integer representing the unique Id of a Rental object.
			Input:
				self - object defined by this class
			Output:
				_rentalId - integer representing the Id of a Rental object
		'''
		return self._rentalId

	def __repr__(self):
		return "Client with ID: " + str(self._clientId) + " rented: " + str(self._bookElement) 

