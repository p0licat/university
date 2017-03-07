'''
	FileValidator module. This module helps the repository class to validate the input by exchanging brute file 
	data for usable objects.
'''

from domain.Client import Client
from domain.Book import Book
from domain.Rental import Rental

class FileValidator:
	'''
		FileValidator class, only static methods that help processing of files.
	'''
	def __init__(self):
		self._tempClientRepo = []
		self._tempBookRepo 	 = []
		self._tempRentalRepo = []

	def ValidateFileInput(self, repoType, fileInput):
		if repoType == "Client":
			if len(fileInput) != 4:
				return None
			try:
				clientId = int(fileInput[1])
				clientName = fileInput[2]
				clientCnp = int(fileInput[3])

				while ( clientName[0] == " " ):
					clientName = clientName[1:]

				validElement = Client(clientId, clientName, clientCnp)
				self._tempClientRepo.append(validElement) # necessary for complete validation
				return validElement
			except:
				return None

		if repoType == "Book":
			if len(fileInput) != 5:
				return None
			try:
				bookId = int(fileInput[1])
				bookTitle = fileInput[2]
				bookDescription = fileInput[3]
				bookAuthor = fileInput[4]

				while ( bookTitle[0] == " " ):
					bookTitle = bookTitle[1:]

				while ( bookDescription[0] == " " ):
					bookDescription = bookDescription[1:]

				while ( bookAuthor[0] == " " ):
					bookAuthor = bookAuthor[1:]

				bookAuthor = bookAuthor.replace("\n", "")

				validElement = Book(bookId, bookTitle, bookDescription, bookAuthor)
				self._tempBookRepo.append(validElement) # necessary for complete validation

				return validElement
			except:
				return None

		if repoType == "Rental":
			if len(fileInput) != 4:
				return None
			try:
				rentalId = int(fileInput[3])
				rbookId = int(fileInput[2])
				rclientId = int(fileInput[1])
				rbook = None

				valid = False
				for i in self._tempClientRepo:
					if i.getId() == rclientId:
						valid = True
						break

				if not valid:
					return None

				for i in self._tempBookRepo:
					if i.getId() == rbookId:
						rbook = i
						break

				if rbook == None:
					return None


				for i in self._tempRentalRepo:
					if i.getId() == rentalId:
						return None

				validElement = Rental(rclientId, rbook, rentalId)
				self._tempRentalRepo.append(validElement)

				return validElement

			except:
				return None

		return None
