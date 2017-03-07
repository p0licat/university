from methods import *

'''
	This file contains the test functions of every function defined in methods.py, which is imported.
	This file is imported by the main file ( application.py )
'''

def sort_transactions_test(list_of_transactions):
	list_of_transactions = [['7', '120', 'out', 'first'], ['7', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]

	assert sort_transactions('sort', (['asc', 'day']), list_of_transactions) == True
	for i in range(1, len(list_of_transactions)):
		assert ( int(list_of_transactions[i][0]) >= int(list_of_transactions[i-1][0]) ) == True
		if int(list_of_transactions[i][0]) == int(list_of_transactions[i-1][0]):
			assert ( int(list_of_transactions[i][1]) >= int(list_of_transactions[i-1][1]) ) == True
	
	assert sort_transactions('sort', (['desc', 'day']), list_of_transactions) == True
	for i in range(1, len(list_of_transactions)):
		assert (int(list_of_transactions[i][0]) <= int(list_of_transactions[i-1][0])) == True
		if int(list_of_transactions[i][0]) == int(list_of_transactions[i-1][0]):
			assert (int(list_of_transactions[i][1]) <= int(list_of_transactions[i-1][1])) == True

	assert sort_transactions('sort', (['asc', 'type']), list_of_transactions) == True

	list_of_transactions = [['0', '10', 'out', 'test']]

	assert sort_transactions('sort', (['asc', 'day']), list_of_transactions) == True
	assert sort_transactions('sort', (['asc', 'type']), list_of_transactions) == True

	list_of_transactions[:] = []

	assert sort_transactions('sort', (['asc', 'day']), list_of_transactions) == None
	assert sort_transactions('sort', (['asc', 'type']), list_of_transactions) == None

def get_max_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['0', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	assert get_max('max', (['in', 'day']), list_of_transactions) == '4'
	assert get_max('max', (['out', 'day']), list_of_transactions) == '1'
	list_of_transactions[:] = []
	assert get_max('max', (['out', 'day']), list_of_transactions) == None
	assert get_max('max', (['in', 'day']), list_of_transactions) == None

def get_sum_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['0', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	assert int(get_sum('sum', (['in', '']), list_of_transactions)) == 1000
	assert int(get_sum('sum', (['out', '']), list_of_transactions)) == 315
	assert int(get_sum('sum', (['out', '0']), list_of_transactions)) == 115
	list_of_transactions[:] = []
	assert int(get_sum('sum', (['in', '']), list_of_transactions)) == 0

def get_balance_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['0', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	# balance should be 685, for day 1 should be -200
	assert int(get_balance('balance', (['']), list_of_transactions)) == 685
	assert int(get_balance('balance', (['1']), list_of_transactions)) == -200
	assert int(get_balance('balance', (['']), [])) == 0
	assert int(get_balance('balance', (['']), [['0','440','out','ok']])) < 0 # negative
	list_of_transactions[:] = []

def get_all_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['0', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]

	assert get_all('all', (['']), list_of_transactions) == list_of_transactions
	assert get_all('all', (['in']), list_of_transactions) != False

	result = get_all('all', (['in']), list_of_transactions)
	for i in result:
		assert i[2] == 'in'

	result = get_all('all', (['out']), list_of_transactions)
	for i in result:
		assert i[2] == 'out'

	list_of_transactions[:] = []



def less_than_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['0', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	
	assert less_than('greater than', (['100']), list_of_transactions) != False
	result = less_than('greater than', (['100']), list_of_transactions)

	if result != False and result != None:
		for i in result:
			assert int(i[1]) < 100 

	list_of_transactions[:] = []



def greater_than_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['0', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	
	assert greater_than('greater than', (['100']), list_of_transactions) != False
	result = greater_than('greater than', (['100']), list_of_transactions)

	if result != False and result != None:
		for i in result:
			assert int(i[1]) > 100 

	list_of_transactions[:] = []


def transaction_filter_test(list_of_transactions):
	list_of_transactions = [['0', '100', 'in', 'first'], ['0', '100', 'out', 'second'], ['1', '100', 'in', 'third'], ['4', '100', 'in', 'fourth']]
	
	assert transaction_filter('filter', (['in', '']), list_of_transactions) == True
	for i in list_of_transactions:
		assert i[2] == 'in'

	list_of_transactions = [['0', '100', 'in', 'first'], ['0', '105', 'out', 'second'], ['1', '105', 'in', 'third'], ['4', '99', 'in', 'fourth']]
	
	assert transaction_filter('filter', (['out', '']), list_of_transactions) == True
	for i in list_of_transactions:
		assert i[2] == 'out'

	list_of_transactions = [['0', '100', 'in', 'first'], ['0', '105', 'out', 'second'], ['1', '105', 'in', 'third'], ['4', '99', 'in', 'fourth']]
	
	assert transaction_filter('filter', (['in', '100']), list_of_transactions) == True
	for i in list_of_transactions:
		assert i[2] == 'in'
		assert int(i[1]) > 100
	list_of_transactions = []

def add_entry_test(list_of_transactions):
	groups_commands = ['add', 'insert']
	insert_groups_tuple = [[('10', '100', 'out', 'description'), True],
						   [('0', '30', 'in', 'desc'), True],
						   [('x', '3j', '', 'desc'), False],
						   [('0', '30', 'in', ''), False],
						   [('M_', '30', 'in', 'desc'), False], 
						   [('-23', '32', '2222222', ''), False],
						   [(' 2313', '322', 'in2', 'desc'), False]]
	add_groups_tuple = [[('10', 'in', 'correct'), True],
						[('-1', '-1', '-1'), False],
						[('', 'x', 'x'), False],
						[('', ' ', ''), False],
						[('', '', ' '), False],
						[('', 'x@', ''), False],
						[('11', '11', '11'), False]]

	for i in insert_groups_tuple:
		assert add_entry(groups_commands[1], i[0], list_of_transactions) == i[1]
	
	for i in add_groups_tuple:
		assert add_entry(groups_commands[0], i[0], list_of_transactions) == i[1]
	list_of_transactions[:] = []

def remove_item_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['15', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	assert remove_item('remove', (['15']), list_of_transactions) == True
	for i in list_of_transactions:
		assert i[0] != 15

	print (list_of_transactions)
	assert remove_item('remove', (['in']), list_of_transactions) == True
	print (list_of_transactions)
	for i in list_of_transactions:
		assert i[2] != 'in'

	assert remove_item('remove', (['out']), list_of_transactions) == True
	for i in list_of_transactions:
		print (i)
		assert i[2] != 'out'

	list_of_transactions[:] = []

def remove_from_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['15', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]

	assert remove_from('remove from', (['1', '4']), list_of_transactions) == True
	for i in list_of_transactions:
		assert int(i[0]) < 1 or int(i[0]) > 4

	assert remove_from('remove from', (['1', '0']), list_of_transactions) == True

	list_of_transactions[:] = []

def replace_entry_test(list_of_transactions):
	list_of_transactions = [['0', '10', 'out', 'first'], ['15', '105', 'out', 'second'], ['1', '200', 'out', 'third'], ['4', '1000', 'in', 'fourth']]
	
	assert replace_entry('replace', (['15', 'out', 'second', '200']), list_of_transactions) == True
	for i in list_of_transactions:
		if i[0] == 15 and i[3] == 'second':
			assert i[1] == 200

	assert replace_entry('replace', (['11', 'out', 'second', '200']), list_of_transactions) == True

	list_of_transactions[:] = []	

# ========================================================= TEST FUNCTIONS  ===============================================================================

