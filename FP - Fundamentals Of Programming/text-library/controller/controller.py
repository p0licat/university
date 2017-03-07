'''
	controller.py module. This module defines the Controller super class which is inheritted by all controller classes. 
'''

class Controller:
	'''
		Controller super class. This class is the model for every specialized controller, such as BookController and ClientController.
	'''
	def __init__(self, repository):
		'''
			Constructor for controller classes, which must all have a _repo property.
		'''
		self._repo = repository

	def __str__(self):
		'''
			Manual override of the str function.
		'''
		return str(self._repo)

	def getRepository(self):
		'''
			Getter for the self._repo property. Returns the repository property.
			Output:
				Repository type object
		'''
		return self._repo

	def getList(self):
		'''
			Getter for the list of elements inside the repository.
			Output:
				list of elements 
		'''
		return self._repo.getElementList()