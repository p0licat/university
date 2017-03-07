'''
	This is the main file of the application. It imports tests.py, which imports methods.py
	This file only contains the User Interface and UI related functions.
'''

from tests import *
from undo import *
import sys
import os
import re

def exit_application():
	print ("Exiting application.")
	sys.exit()

def show_help():
	# whenever a new instruction is implemented the list_of_instructions and list_of_commands needs to be updated
	# list_of_commands contains all the instructions
	# list_of_instructions is a dictionary with the string containing instruction as key and text to be printed as the value for that key

	os.system("cls")
	list_of_commands =  [[1, "add"], [2, "insert"], [3, "greater than"], [4, "less than"], 
						 [5, "all", "all in", "all out"], [6, "balance"], [7, "help"], [8, "filter"], [9, "sum"], [10, "max"], [11, "sort"], 
						 [12, "remove"], [13, "remove from"], [14, "replace"], [15, "undo"], [16, "redo"], [0, "exit"]]


	list_of_instructions =  { "add": "adds an entry in the transaction history for the current day. \nadd [value], [in/out], \"description\" \n",
						      "insert": "inserts an entry in the history for a specific day. \ninsert [day], [value], [in/out], \"description\" \n",
					          "greater than": "prints all entries of a value greater than a given value. \ngreater than [value]\n",
						  	  "less than": "prints all entries of a value less than a given value. \nless than [value]\n",
						  	  "all": "prints all transaction entries of a certain type (in/out). If unspecified prints all entries. \nall \nall [in/out]\n",
						      "balance": "prints the balance of the account for a specific day." + 
						  	 			 " If day is unspecified the total balance will be shown. \nbalance \nbalance [day]\n",
						  	   "filter": "filters entries based on criteria. \nfilter [in/out] (value)\n",
						  	   "help": "provides help information for program commands.\n",
						  	   "sum": "displays the sum of all transactions of a given type (in/out). \nsum [in/out]\n",
						  	   "max": "displays the day containing the largest transaction of a given type (in/out)." +
						  	   		  "\nmax [in/out] [day]\n",
						  	   "sort": "sorts all transaction either from current day or by type, as needed.\n[asc/desc] sort [day/(in/out)]\n",
						  	   "remove": "removes a certain transaction. \nremove [day]\nremove [in/out]\n", 
						  	   "remove from": "removes all transactions from a given interval, where the first parameter is greater than the second." +
						  	   				  "\nremove from [day] to [day]\n",
						  	   "replace": "replaces the value of an existing transaction.\nreplace [day], [type], [description], [new_value]\n",
						  	   "undo": "undoes the last performed operation.\n",
						  	   "redo":"undoes the last undo.",
						  	   "exit": "exits the application.\n"
							}	

	# print the text associated with each instruction
	for i in list_of_commands:
		print (i[1] + ": " + list_of_instructions[i[1]])

def main():
	# list_of_transactions is basically the database containing every transaction that the user adds or wants to manipulate
	# format is : [day], [value], [type], [description]
	#				0		1		2		3

	# 0 : [day] 	only contains positive integer values although the test functions called everything with strings containing integer values
	# 1 : [value] 	only contains positive integer values although the test functions called everything with strings containing integer values
	# 2 : [type] 	is always a string, and should be either "in" or "out"
	#				this means that input should always be filtered to ensure that everything works
	# 3 : [desc]	or the description contains only text as a string and exists to help the user
	# 				since the user can enter basically anything in the description you should be careful when searching inside the elements
	#				of list_of_transaction
	# 				
	#				also, the only correct syntax by entering a description is when the user puts it between two quotatino marks ( "" )

	list_of_transactions = [] # this is a list of lists that will contain all transactions with the format specified above
							  # example: [[0, 100, "out", "donation"], [1, 50, "in", "salary"]]

	# list_of_commands is a list of lists, each containing a number of order, a string with a certain command and a third element
	# that is a pointer to a function
	#
	# whenever a new instruction is added, it needs to be introduced here, since the main loop takes user input and searches this list for
	# corresponding instructions inside the input
	
	# format is: [order], [function], [command]
	#				0		   1 		  2

	# 0 : [order] 	contains an integer that is assigned to every instruction, in the order in which they were implemented
	# 1 : [func]	contains a pointer to the corresponding function of each instruction
	# 2 : [command]	contains a string with the key word of each instruction
	#				for example: for adding a new entry it is "add", for sorting the list it is "sort" although there needs to be a sorting
	#				order before it inside the input

	list_of_commands =  [[1, add_entry, "add"], [2, add_entry, "insert"], [3, greater_than, "greater than"], [4, less_than, "less than"], 
						 [5, get_all, "all", "all in", "all out"], [6, get_balance, "balance"], [7, show_help, "help"], [8, transaction_filter, "filter"], 
						 [9, get_sum, "sum"], [10, get_max, "max"], [11, sort_transactions, "sort"], [12, remove_item, "remove"], 
						 [13, remove_from, "remove from"], [14, replace_entry, "replace"], [15, "undo"], [16, "redo"], [0, exit_application, "exit"]]
	
	# this is a dictionary consisting of a string as a key, which contains the name of the instruction found in lis_of_commands
	# and its associated value is a regex formula that is used for parsing user input and easily filtering bad inputs
	list_of_syntaxes =  {
							"add": r"^\s*add\s*([0-9]+),\s*([a-zA-Z]+),\s*\"(.*)\"\s*$",
							"insert": r"^\s*insert ([0-9]+),\s*([0-9]+),\s*([a-zA-Z]+),\s*\"(.+)\"\s*$",
							"help": r"^\s*help\s*$",
							"greater than": r"^\s*greater\s*than\s*([0-9]+)\s*$",
							"less than": r"^\s*less\s*than\s*([0-9]+)\s*$",
							"all": r"^\s*all\s*([a-z]*)\s*",
							"balance": r"^\s*balance\s*([0-9]*)\s*",
							"filter": r"^\s*filter\s*([a-z]+)\s*([0-9]*)\s*",
							"sum": r"^\s*sum\s*([a-z]+)\s*([0-9]*)\s*",
							"max": r"^\s*max\s*([a-z]+)\s*day\s*",
							"sort": r"^\s*([a-z]+)\s*sort\s*([a-z]+)\s*",
							"remove": r"^\s*remove\s*([a-z0-9]+)\s*",
							"remove from": r"^\s*remove\s*from\s*([0-9]+)\s*to\s*([0-9]+)\s*",
							"replace": r"^\s*replace\s*([0-9]+),\s*([a-z]+),\s*\"(.+)\"\s*with\s*([0-9]+)\s*",
							"undo": r"^\s*undo\s*",
							"redo": r"^\s*redo\s*",
							"exit": r"^\s*exit\s*$"
						}

	# undo_list handles the undo() and redo() functions.
	# it is an object of type UndoList, as defined in the undo.py module
	#
	# it contains the history of all actions and allows an unlimited number
	# of undo() calls and one redo() call for the last undo() 
	undo_list = UndoList(list_of_transactions)

	# run tests 
	add_entry_test(list_of_transactions)
	transaction_filter_test(list_of_transactions)
	greater_than_test(list_of_transactions)
	less_than_test(list_of_transactions)
	get_all_test(list_of_transactions)
	get_balance_test(list_of_transactions)
	get_sum_test(list_of_transactions)
	get_max_test(list_of_transactions)
	sort_transactions_test(list_of_transactions)
	remove_item_test(list_of_transactions)
	remove_from_test(list_of_transactions)
	replace_entry_test(list_of_transactions)
	# end tests

	os.system("cls")
	print ("Type \'help\' for instructions.")
	
	# main loop
	# the idea behind the main loop is simple: it first waits for a command
	# some text is inputted by the user, it needs to verify whether the command exists, and verify the syntax if it does exist 
	# 
	# to verify if the instruction exists, a search is first performed in list_of_syntaxes
	# a for loop iterates through every regex formula and stops when it finds one that can apply
	# 
	# once an input passes the regex test, the key associated with the regex formula will be the name of the instruction
	# this means that we can use it to search inside the list_of_commands dictionary for a command that has that name, and call
	# its respective function with the parameters gathered by the re.match() function
	#
	# every instruction has an assigned function with a specific prototype, which should be the same whenever a new instruction is implemented
	# this means that every function assigned to every command is always called with the same 3 parameters:
	# func(name, match_obj.groups(), list_of_transactions), where: 
	#		name is the command name as a string
	#		match_obj.groups() is a tuple containing all of the elements from the syntax specific to that instruction found in the user input
	# 		list_of_transactions is the database containg all of the transaction entries
	# since everythin that the program does is basically a management of this database, every instruction can be performed by using this pattern

	while True:
		user_input = input("Please insert a command: ") # wait for input
		found = False
		for i, j in list_of_syntaxes.items(): # searches for valid user input
			match_obj = re.match(j, user_input) # i is the instruction name and j is the regex formula
												# the call returns inside match_obj a tuple containing each parameter of 
												# the expected syntax in the input as a string
			if match_obj: # if input is valid it means that re.matched returned a non-false value
				found = True
				for k in list_of_commands: # we search the list of commands for corresponding instruction
					if i in k: # if the input word is found in the list of commands we launch its corresponding function
					# k[0] is the number of the command, k[1] is the function associated to that command, k[2] is the name of the command
						if i == "undo": # special handling for undo() due to different call syntax
							result = Undo(undo_list, list_of_transactions)
							if result == False:
								print ("Nothing to undo.")
						elif i == "redo": # special handling for undo() due to different call syntax
							result = Redo(undo_list, list_of_transactions)
							if result == False:
								print ("Nothing to redo.")
						elif len(match_obj.groups()) >= 1: # some functions need parameters
							returned_obj = k[1](k[2], match_obj.groups(), list_of_transactions)
							# returned_obj stores the result of every function that performs an instruction
							# can be True, False, or something else
							if returned_obj == True:
								print ("Operation performed successfully!")
								undo_list.AddAction(list_of_transactions) # it makes sense to only undo correct operations
							elif returned_obj == False:
								print ("Please use the correct syntax! Enter \"help\" for details.")
							elif returned_obj != [None]: # if the result is an non empty list, we display it
								print (returned_obj)
						else:
							k[1]() # some instructions like "all", "help" and "exit" don't
		if found == False:
			print ("Error! Inexistent command! Type \"help\" for instructions.")


# ========================================================== USER INTERFACE ===============================================================================

main()