'''
	Operation module. This module defines the Operation object, which is the object that is handled by the Undo class.
	An Operation object assigns a different meaning for every operation belonging to the main program in order to render it undoable.
'''

class Operation:
	'''
		Operation object. An operation should allow the program to restore its state to a previous one. This means that the information
		that it contains must be unique for each operation that is performed upon the repositories, which are the objects that handle all
		stored information inside the program.

		This is a superclass, meaning that all operations are derrived from this class.
	'''

	def __init__(self, repository, keyElement):
		self._repository = repository
		self._keyElement = keyElement

	def _getRepository(self):
		return self._repository

	def _getKeyElement(self):
		return self._keyElement


class AddOperation(Operation):
	'''
		Add operation class. Inherits the superclass "Operation", and stores information about the last add operation and how to reverse it.
	'''
	def __init__(self, repository, keyElement):
		super().__init__(repository, keyElement)
		self._operationType = "Add"

	def _redoOperation(self):
		self._repository.addElement(self._keyElement)

	def _reverseOperation(self):
		self._repository.removeElement(self._keyElement)

	def _getOperationType(self):
		return self._operationType

class RemoveOperation(Operation):
	'''
		Remove operation class. Inherits the superclass "Operation", and stores information about the last remove operation and how to
		reverse it.
	'''
	def __init__(self, repository, keyElement):
		super().__init__(repository, keyElement)
		self._operationType = "Remove"

	def _redoOperation(self):
		self._repository.removeElement(self._keyElement)

	def _reverseOperation(self):
		self._repository.addElement(self._keyElement)

	def _getOperationType(self):
		return self._operationType

class ModifyOperation:
	'''
		Modify operation class. Inherits the superclass "Operation", and stores information about the last modify operation and how to
		reverse it. These kinds of operations consist of a RemoveOperation and an AddOperation applied successively.
	'''
	def __init__(self, repository, elementBeforeModify, elementAfterModify):
		self._repository = repository
		self._elementBeforeModify = elementBeforeModify
		self._elementAfterModify = elementAfterModify
		self._operationType = "Modify"

	def _redoOperation(self):
		self._repository.removeElement(self._elementBeforeModify)
		self._repository.addElement(self._elementAfterModify)

	def _reverseOperation(self):
		self._repository.removeElement(self._elementAfterModify)
		self._repository.addElement(self._elementBeforeModify)

	def _getOperationType(self):
		return self._operationType
