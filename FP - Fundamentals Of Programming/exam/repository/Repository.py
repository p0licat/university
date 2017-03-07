'''
	Repository module. This module defines a Repository class, which stores a list of Holiday objects and manipulates this list using calls
	of functions that come from the HolidayController class.
'''

class Repository:
	def __init__(self):
		'''
			Constructor for the Repository object. Creates a list called _elements which will store Holiday objects.
		'''
		self._elements = []

	def addElement(self, element):
		'''
			Add element method. Will return true if element was added or false if it already exists.
		'''
		for i in self._elements:
			if i.getId() == element.getId():
				return False

		self._elements.append(element)
		return True


	def getElements(self):
		'''
			Getter for the Elements list. Will return every element in this repository.
		'''
		return self._elements

