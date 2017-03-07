'''
	This file contains the definition of every function that manipulates the list of transactions. It is imported by tests.py, which 
	is imported by the main file ( application.py )
'''

def add_entry(instruction_type, groups, list_of_transactions):
	''' 
		Adds an entry to the list_of_transactions either by using the add keyword or the insert keyword. Add only adds to the current day while
		when using insert you can specify the day.
		Input: 
			instruction_type 		( string containing the corresponding word to this instruction )
			groups 					( tuple containing three or four strings, first being the day, second the value, third the type and fourth the description )
			list_of_transactions	( list of all transactions )
		Output: 
			"True" or "False" depending on the success of the operation.
			( modifies parameter list_of_transactions )
	'''

	# there are two possible instructions: add or insert, so they are treated individually
	if instruction_type == "add": # add instruction: syntax is add [value], [in/out], "description"
		try:
			value = int(groups[0])  # integer, first parameter of instruction ([value])
			trans_type = groups[1]  # string , second parameter of instruction, should be either "in" or "out" 
			description = groups[2] # string , third parameter containing the description
			if (trans_type == "in" or trans_type == "out"):
				list_of_transactions.append([0, value, trans_type, description])
				return True
			else: # return false if second parameter ( which should contain "in"/"out" ) is neither of these values
				return False
		except: # return false if anything throws an exception
			return False
	if instruction_type == "insert": # inseret instruction: syntax is insert [day], [value], [in/out], "description"
		try:
			day = int(groups[0])     # integer, contains the first parameter, is 0 if the days is the current day
			value = int(groups[1])	 # integer, contains the second parameter
			trans_type = groups[2]	 # string , second parameter of instruction, should be either "in" or "out"  
			description = groups[3]  # string , third parameter containing the description

			# expression checks if the day is a correct value (0 is today, 1-31 is any other day)
			# and checks if the transaction type is correct (in/out) and the description is non empty
			if (day >= 0 and day <= 31) and ( trans_type == "in" or trans_type == "out" ) and ( description != '' ):
				list_of_transactions.append([day, value, trans_type, description])
				return True
			else: 
				return False
		except: # returns false if anything throws an exception
			return False

def transaction_filter(instruction_type, groups, list_of_transactions):
	'''
		Finds all entries in the list_of_transactions list and removes the ones that do not contain the criteria. If the parameter 
		"groups" contains onlt one string (v1) then it filters all transactions of that type, if it contains two (v1, v2) it also takes into account
		the value of the second string ( integer ) and filters every entry lower than or equal to v2. 
		Input:
			instruction_type		( string containing the word corresponding to this instruction )
			groups 				    ( tuple containing either a string or two, depending on the type of operation )
			list_of_transactions	( list of all transactions )
		Output: 
			"True" or "False" depending on the success of the operation.
			( modifies the parameter list_of_transactions )
	'''
	# filter instruction has 2 correct syntaxes: one without a second parameter and one with a second parameter
	if len(groups) > 0:
		# case when there are two parameters ( filter in/out, [value] )
		if groups[1] != '':
			try:
				trans_type = groups[0] 			# first parameter ("in"/"out")
				filter_value = int(groups[1]) 	# second parameter (integer value)
				list_of_transactions[:] = [i for i in list_of_transactions if i[2] == trans_type and int(i[1]) > filter_value]
				return True
			except: 
				return False
		# case when there is only one parameter ( filter in/out )
		else:
			try:
				trans_type = groups[0] # first parameter ( "in"/"out" )
				list_of_transactions[:] = [i for i in list_of_transactions if i[2] == trans_type]
				return True
			except:
				return False

def greater_than(instruction_type, groups, list_of_transactions):
	'''
		Scans list_of_transactions for all entries that have a greater value than a given v1. It then returns
		a list containing all the requested entries.
		Input: 
			instruction_type		( string containing the word corresponding to this instruction )
			groups 				    ( tuple containing a string with the value v1 )
			list_of_transactions	( list of all transactions )
		Output:
			result ( list containing all entries from list_of_transactions that respect the requirement )
			None ( string ) if result is empty
			"False" if there are no entries of the requested type or for some reason a list cannot be returned.
	'''
	result = [] # return value should be a list of lists
	try:
		value = int(groups[0]) # first parameter of the instruction
		
		# iterate the list of transactions and add to the result list each element with a value greater than 'value'
		for i in list_of_transactions:
			if int(i[1]) > value:
				result.append(i)
		if len(result) > 0: # only return the result list of lists if it is non empty
			return result
		else:
			return None
	except:
		return False

def less_than(instruction_type, groups, list_of_transactions):
	'''
		Scans list_of_transactions for all entries that have a value less than a given v1. It then returns
		a list containing all the requested entries.
		Input: 
			instruction_type		( string containing the word corresponding to this instruction )
			groups 				    ( tuple containing a string with the value v1 )
			list_of_transactions	( list of all transactions )
		Output:
			result ( list containing all entries from list_of_transactions that respect the requirement )
			None ( string ) if result is empty
			"False" if there are no entries of the requested type or for some reason a list cannot be returned.
	'''
	result = [] # return value should be a list of lists 
	try:
		value = int(groups[0]) # first parameter of the instruction

		# iterate the list of transactions and add to the result list each element with a value greater than 'value'
		for i in list_of_transactions:
			if int(i[1]) < value:
				result.append(i)
		if len(result) > 0: # only return the result list of lists if it is non empty
			return result
		else:
			return None
	except:
		return False

def get_all(instruction_type, groups, list_of_transactions):
	'''
		Generates and returns a list of all the transactions in list_of_transactions that meet the requirement in the
		parameter "groups". If there is no parameter it returns the list_of_transactions.
		Input:
			instruction_type		( string containing the word corresponding to this instruction )
			groups 					( tuple containing an optional parameter that is either the string "in" or "out" )
			list_of_transactions	( list of all transactions )
		Output:
			result 	( list containing entries from list_of_transactions )
			None ( string ) if result is empty
			"False" if for some reason there can be nothing returned.	
	'''
	try:
		# the 'all' instruction has three different cases: all (without parameters), and two for all in/out
		if groups[0] != '': # case when the optional parameter is included
			result = [i for i in list_of_transactions if groups[0] in i[:-1] ] # avoid looking in description by using i[:-1]
			if result != []: # return result only if non empty
				return result
			else:
				return None
		elif list_of_transactions != []: # case when there are no parameters: return list if not empty
			return list_of_transactions
		else:
			return None
	except: # if any exception is thrown function returns false
		return False

def get_balance(instruction_type, groups, list_of_transactions):
	'''
		Returns the balance of the account from a certain day or the corresponding error message depending on the situation.
		Input:
			instruction_type		( string containing the word corresponding to this instruction )
			groups 					( tuple containing a string which specifies the day for which to calculate the balance )
									( if groups is empty then the function will return the balance for every entry in the transaction list )
			list_of_transactions	( list of all transactions )
		Output:
			balance ( string containing the requested value ). Note that a string must be used in order to avoid problems with printing to cosole.
	'''
	if groups[0] == '': # two correct syntaxes for balance: without parameters and with the optional in/out parameter
		return str(calculate_balance(None, list_of_transactions)) # case of no parameters: call returns total balance
	else: # case with parameter
		return str(calculate_balance(int(groups[0]), list_of_transactions)) # call returns total balance of a certain day 



def calculate_balance(day, list_of_transactions):
	'''
		Iterates through list_of_transactions, calculates and returns the balance of the account. There are no special cases since if 
		the list_of_transactions is empty it will just return the initial value of 0.
		This function should only be ran by the get_balance function!
		Input: 
			list_of_transactions ( list of all transactions )
		Output:
			balance ( integer containing the balance of the account )
	'''
	balance = 0 # initialize with 0 in case there are no transactions
	
	# nothing to calculate if list is empty
	if list_of_transactions == []:
		return balance

	if day == None: # case when day is unspecified
		sign = 1 # in transactions are positive, out transactions are negative
		for i in list_of_transactions:
			if i[2] == 'in':
				sign = 1
			elif i[2] == 'out':
				sign = -1
			balance += int(i[1])*sign
		return balance
	else: # case when day is specified
		sign = 1 # in transactions are positive, out transactions are negative
		for i in list_of_transactions:
			if int(i[0]) == day: # check if day corresponds with day parameter
				if i[2] == 'in':
					sign = 1
				elif i[2] == 'out':
					sign = -1
				balance += int(i[1])*sign
		return balance
		
def get_sum(instruction_type, groups, list_of_transactions):
	'''
		Iterates through list_of_transactions and calculates the sum of the values of the transactions where the type 
		corresponds to the type found in the "groups" parameter ('in'/'out').
		Input:
			instruction_type		( string containing the word corresponding to this instruction )
			groups 					( tuple containing a string which specifies the type for which to calculate the sum ). 
									( this can be 'in' or 'out' )
			list_of_transactions	( list of all transactions )
		Output:
			sum_result ( string containing the requested value )
	'''
	sum_result = 0 # initialize with 0 if there is nothing to calculate

	# case when list is empty
	if list_of_transactions == []:
		return str(sum_result)	# return string '0' if list is empty
							  	# should be string because value 0 is interpreted as False by the UI function (main)

	if groups[1] == '': # if there is no second parameter
		for i in list_of_transactions:
			if i[2] == groups[0]: # calculate sum across all days corresponding to the type in the groups parameter
				sum_result += int(i[1])
	else: # if the day is specified by the second parameter
		for i in list_of_transactions:
			if (i[2] == groups[0]) and (int(i[0]) == int(groups[1])):
				sum_result += int(i[1]) # calculate sum only for the requested day
	return str(sum_result)

def get_max(instruction_type, groups, list_of_transactions):
	'''
		Iterates through list_of_transactions and finds the day with the largest transaction of the given type (in/out). It then
		returns the day of the entry from list_of_transactions.
		Input:
			instruction_type		( string containing the word corresponding to this instruction )
			groups 					( tuple containing a string which specifies the type of the transaction ). 
									( this can be 'in' or 'out' )
			list_of_transactions	( list of all transactions )
		Output:
			list_of_transactions[i,0] where i is the index of the entry containing the requested result.
			None if list_of_transactions is empty.
			"False" if entry parameters do not respect syntax.
	'''

	# filter bad input
	if groups[0] != 'in' and groups[0] != 'out':
		return False
	# list is empty case
	if list_of_transactions == []:
		return None
	
	# check if there are transactions of the requested type
	found_type = False
	for i in list_of_transactions:
		found_type = found_type or groups[0] in i[:-1] # use i[:-1] to avoid looking into description
	if not found_type:
		return None

	# we can now begin calculating since there is something to calculate
	max_element = ['0', '-1'] 	# value to be returned, initialize with lowest possible value
								# since we are looking for maximum
	for i in list_of_transactions:
		if i[2] == groups[0]: # groups[0] contains the desired type
			if int(i[1]) > int(max_element[1]):
				max_element = i
	return str(max_element[0]) # return a string since 0 is interpreted as False by the UI

def sort_transactions(instruction_type, groups, list_of_transactions):
	'''
		Sorts the list_of_transactions in either ascending or descending order, either from the current day or per type.
		Input:
			instruction_type		( string containing the word corresponding to this instruction )
			groups 					( tuple containing two strings, specifying the order of the sort and type of sort ). 
									( the first string can be "asc" or "desc" and the second one "day" or "type" )
			list_of_transactions	( list of all transactions, sorted after end of execution )
		Output:
			"True" if the list_of_transactions was sorted.
			None if there is nothing to sort.
			"False" if input is incorrect.
	'''

	# syntax for the sort instruction is [order("asc"/"desc")] sort [type("day"/"type")]

	sort_order = groups[0] 	# first parameter of the sort instruction, contains the desired order (asc/desc) 
	sort_type = groups[1]	# second parameter of the sort instruction, contains the type of the sort
							# if type is "day" it sorts first by day and then by values inside the partitions
							# if type is "type" it sorts first by type (in/out) and then by values inside the partitions

	# filter bad input
	if sort_order != 'asc' and sort_order != 'desc':
		return False
	if sort_type != 'day' and sort_type != 'type':
		return False

	# don't attempt sorting an empty list
	if list_of_transactions == []:
		return None

	# call sorting function: returns the sorted list
	list_of_transactions[:] = sort_list_of_transactions(list_of_transactions, sort_order, sort_type)

	return True

def sort_list_of_transactions(list_of_transactions, sort_order, sort_type):
	'''
		Function called by sort_transactions, it returns a sorted list_of_transactions.
		Input:
			list_of_transactions
			sort_order ( 'asc' / 'desc' )
			sort_type ( 'day' / 'in' / 'out' )
		Output:
			sorted list_of_transactions
	'''
	if sort_type == 'day': # sort normally, by value
	# function uses manual implementation of bubblesort
	# we require two sorts, one for each criteria ( in this case one to sort by days and one by value inside the sorted partitions )
		# begin day bubblesort
		done = False
		while not done:
			done = True
			for i in range(0, len(list_of_transactions)-1):
				current_element = list_of_transactions[i]
				next_element = list_of_transactions[i+1]
				if ((( int(current_element[0]) > int(next_element[0])) and ( sort_order == 'asc' )) or ( 
					 ( int(current_element[0]) < int(next_element[0])) and ( sort_order == 'desc'))):
					done = False
					aux = list_of_transactions[i+1]
					list_of_transactions[i+1] = list_of_transactions[i]
					list_of_transactions[i] = aux
		# end day bubblesort

		# begin value bubblesort
		done = False
		while not done:
			done = True
			for i in range(0, len(list_of_transactions)-1):
				current_element = list_of_transactions[i]
				next_element = list_of_transactions[i+1]
				if (( int(current_element[1]) >  int(next_element[1]) and sort_order == 'asc' ) or ( 
					  int(current_element[1]) <  int(next_element[1]) and sort_order == 'desc') ) and ( 
					  int(current_element[0]) == int(next_element[0]) ):
					done = False
					aux = list_of_transactions[i+1]
					list_of_transactions[i+1] = list_of_transactions[i]
					list_of_transactions[i] = aux
		# end value bubblesort
	elif sort_type == 'type':
		# here we require two sorts: one for dividing the list into an 'in' and an 'out' half
		# and another to sort inside these halves by value
		
		#begin 'in'/'out' bubblesort
		done = False
		while not done:
			done = True
			for i in range(0, len(list_of_transactions)-1):
				if list_of_transactions[i][2] == 'out' and list_of_transactions[i+1][2] == 'in':
					done = False
					aux = list_of_transactions[i+1]
					list_of_transactions[i+1] = list_of_transactions[i]
					list_of_transactions[i] = aux
		#end 'in'/'out' bubblesort

		#begin halves bubblesort
		done = False
		while not done:
			done = True
			for i in range(0, len(list_of_transactions)-1):
				if list_of_transactions[i][2] == list_of_transactions[i+1][2] and (
				  (list_of_transactions[i][1] >  list_of_transactions[i+1][1] and sort_order == 'asc' ) or (
				   list_of_transactions[i][1] <  list_of_transactions[i+1][1] and sort_order == 'desc') ):
					done = False
					aux = list_of_transactions[i+1]
					list_of_transactions[i+1] = list_of_transactions[i]
					list_of_transactions[i] = aux
		#end halves bubblesort
	return list_of_transactions

def remove_item(instruction_type, groups, list_of_transactions):
	'''
		This function removes an item from the transaction list based on a given parameter. If it is an integer it removes all elements from that day.
		If the parameter is a string, it will remove all the in transactions in case the paramter is 'in', and all the transactions in case the
		parameter is 'out'.

		Input:
			instruction_type: 		a string containing the word associated with this instruction_type
			groups: 		   		a tuple containing one of all possible parameter configurations ( either contains an integer(day) or a string(in/out) )
			list_of_transactions:	a list containing all the transactions on which the function will make changes
		Output:
			'True' if the function successfully ran.
			'False' if there was a problem, such as wrong syntax.
	'''

	to_remove = groups[0] # first parameter from input: either "in" or "out" or an integer
	remove_type = None
	if to_remove == "in" or to_remove == "out":
		remove_type = 'type'
	elif int(to_remove) >= 0 or int(to_remove) <= 31:
		remove_type = 'day'
	else:
		return False

	temp_list = list_of_transactions

	done = False
	while not done: # while there are still items that need to be deleted
		done = True
		for i in range(0, len(temp_list)):
			if i < len(temp_list):
				if remove_type == 'type' and temp_list[i][2] == to_remove:
					done = False
					temp_list.pop(i)
				if remove_type == 'day' and int(temp_list[i][0]) == int(to_remove):
					done = False
					temp_list.pop(i)

	list_of_transactions[:] = temp_list
	return True

def remove_from(instruction_type, groups, list_of_transactions):
	'''
		Function removes all entries from a given day interval.
		Input:
			instruction_type: 		string containing the name of the instruction_type
			groups:					tuple containing the two parameters ( day1 / day2 )
			list_of_transactions 	list containing all the transactions
		Output:
			'True' if the function successfully ran.
			'False' if there was a problem, such as wrong syntax.
	'''

	# first a check is performed to construct the correct interval
	day1 = int(groups[0])
	day2 = int(groups[1])

	if day1 > day2:
		day1, day2 = day2, day1 # this swaps day1, day2

	temp_list = list_of_transactions
	done = False
	while not done:
		done = True
		for i in range(0, len(temp_list)):
			if i < len(temp_list):
				if int(temp_list[i][0]) >= day1 and int(temp_list[i][0]) <= day2:
					done = False
					temp_list.pop(i)

	list_of_transactions[:] = temp_list
	return True

def replace_entry(instruction_type, groups, list_of_transactions):
	'''
		This function searches for an entry that matches the given parameters
		and modifies its value with a given one.
		Input:
			instruction_type: 		string containing the name of the instruction_type
			groups: 				tuple containing all of the four necessary parameters
									(day, type, description, new_value)
			list_of_transactions: 	list containing all of the transactions
		Output:
			'True' if the function successfully ran.
			'False' if there was a problem.
	'''
	# all 4 parameters from groups: day, type, description and new_value
	search_day = int(groups[0])
	search_type = groups[1]
	search_desc = groups[2]
	replace_value = int(groups[3])

	temp_list = list_of_transactions
	for i in temp_list:
		if int(i[0]) == search_day and i[2] == search_type and i[3] == search_desc:
			i[1] = replace_value
	list_of_transactions[:] = temp_list

	return True


