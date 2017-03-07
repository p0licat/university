'''
	This module handles everything related to the undo() and redo() operations. It is imported by application.py
'''

class UndoList:
	'''
		This class defines an object that contains the history of all modifications inside list_of_transactions and manipulates 
		this history in order to restore an earlier state of the list_of_transactions.
		It can also restore the state before the last undo.  
	'''
	action_list = [] # a list of all instances of list_of_transactions
	last_undo = []   # a list containing the state of list_of_transactions before the last undo
	def __init__(self, list_of_transactions): # constructor
		self.action_list[:] = list(list_of_transactions)

	def AddAction(self, list_of_transactions): # adds a new state of list_of_transactions
		'''
			Function appends a new state of list_of_transactions to the action_list.
			Input:
				self: 				  object defined by this class
				list_of_transactions: item to append
			Output:
				'True'
		'''
		self.action_list.append(list(list_of_transactions))
		return True

	def GetLastAction(self):
		'''
			GetLastAction tries to return the last state of list_of_transactions. If there is nothing to undo, the function returns False.
			This function deletes the last entry in action_list before returning it, but saves it inside last_undo before doing so. This makes a redo possible.
			Input:
				self: object defined by this class
			Output:
				last_action: a list containing the previous state of the list_of_transactions
				'False' if there is nothing to undo.
		'''
		last_action = [] # list containing previous state of list_of_transactions
		if len(self.action_list): 
			self.last_undo[:] = list(self.action_list[-1:]) # save current state to allow a redo()
			self.action_list.pop(len(self.action_list)-1)   # remove from action_list to allow the next undo()
			last_action[:] = list(self.action_list[-1:])	# cast to list to avoid returning reference
			return list(last_action)
		else:
			return False
	def GetLastUndo(self):
		'''
			This function returns the last element of action_list before the last undo() was called. This element was saved in last_undo.
			Input:
				self: object defined by this class
			Output:
				list containing the state of list_of_transactions before the last undo()
				'False' if nothing was undone.
		'''
		if self.last_undo == []:
			return False
		return self.last_undo

def Undo(undo_list, list_of_transactions):
	'''
		This function is called inside application.py, which is the main module. It restores list_of_transactions to a previous state.
		Input:
			undo_list:				 object defined by UndoList class
			list_of_transactions	 list containing all of the transactions
		Output:
			"True" if state was restored, "False" if there is nothing to restore.
			modifies list_of_transactions
	'''
	last_action = undo_list.GetLastAction()
	if last_action != False:
		if len(last_action) == 1:
			last_action = last_action[0]
		list_of_transactions[:] = list(last_action)
		return True
	return False

def Redo(undo_list, list_of_transactions):
	'''
		This function is called inside application.py, which is the main module. It restores list_of_transactions to the state before undo() was called.
		Input: 
			undo_list:  object defined by UndoList class
			list_of_transactions	 list containing all of the transactions
		Output:
			"True" if state was restored, "False" if there is nothing to restore.
			modifies list_of_transactions
	'''
	last_undo = undo_list.GetLastUndo()
	if last_undo != False:
		if len(last_undo) == 1:
			last_undo = last_undo[0]
		list_of_transactions[:] = last_undo
		undo_list.AddAction(list_of_transactions)
		return True
	return False

