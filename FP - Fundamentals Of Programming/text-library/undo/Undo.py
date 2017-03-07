'''
	Undo module. This module defines the class that handles undo and redo operations.
'''

class Undo:
	'''
		This class handles all the Undo and Redo functionalities of the program. The idea is the following:
			* A list is defined that holds operations of type Operation, as defined in the Operation class inside the 
			  undo folder.
			* There is a pointer that points somewhere in this list, and restores the program to a previous state, or undoes
			  that restore by managing the pointer.
			* This strategy allows for implementing an unlimited number of undoes.
			* A redo will not be possible if an operation was performed after the last undo.
		self._operationList holds all Operation objects 
		self._operationIndex points to the current state
	'''
	def __init__(self):
		'''
			Constructor for the Undo class, defines the following:
				_operationList, operationIndex
					   0              1

			0: a list of Operation type objects that store information about previous states of the program, allowing for unlimited undoes.
			1: an index (integer) pointing to the element of the current state. 

			* Note that the index needs to point to the last element if another operation is performed after the last undo. This means that
			the operatoinList must be sliced whenever an operation is performed after an undo. 
		'''
		self._operationList = [] 	# list of all Operation objects, handled with the help of _operationIndex
		self._operationIndex = None # initialize with None to differentiate between possible undoes and no operations performed 

	def _addOperation(self, operation):
		'''
			After an add operation, the index must be pointing to the last element. This means that the list should be sliced.
		'''
		if self._operationIndex == None and self._operationList == []:
			self._operationList.append(operation)
			self._operationIndex = 0
		elif self._operationIndex == None:
			self._operationList = []
			self._operationList.append(operation)
			self._operationIndex = 0

		if self._operationIndex == len(self._operationList)-1:
			self._operationList.append(operation)
			self._operationIndex += 1

		if self._operationIndex < len(self._operationList)-1:
			self._operationList = self._operationList[:self._operationIndex]
			self._operationList.append(operation)
			self._operationIndex += 1

	def _undo(self):
		'''
			If the list is not empty, an undo is possible. If an undo was performed, then the index is not pointing to the last element
			of the _operationList and a redo is also possible.
		'''
		if self._operationIndex == None:
			return False
		elif self._operationIndex == 0:
			self._operationList[self._operationIndex]._reverseOperation()
			self._operationIndex = None
			return True
		elif self._operationIndex > 0:
			self._operationList[self._operationIndex]._reverseOperation()
			self._operationIndex -= 1
			if self._operationIndex == 0:
				self._operationIndex = None
			return True

	def _redo(self):
		'''
			Only possible if an undo was performed recently. This means that after an operation is performed, no redo is possible.
		'''
		if self._operationIndex == None and self._operationList == []:
			return False
		elif self._operationIndex == None and self._operationList != []:
			self._operationIndex = 0

		if self._operationIndex < len(self._operationList)-1:
			self._operationIndex += 1
			self._operationList[self._operationIndex]._redoOperation()
			return True
		return False