'''
	This module defines everything related to the sorting algorithms used by the main application that uses 
	shellsort.

'''

def shellsort(data, reverse = False, key = lambda x: x):
	'''
		Default ascending shellsort with largest gap = 32. 32 was chosen only because of pretty divisions.
		The function performs modifications upon the data parameter and then retruns it with all of its elements
		in ascending order.

		Input:
			data: list type object, otherwise raises exception
		Output:
			data: same list in sorted order
	'''
	if type(data) != type([1, 2, 3]):
		raise TypeError("Input must be a list.")

	def comp(a, b):
		return key(a) < key(b)

	def rev_comp(a, b):
		return key(a) > key(b)

	if reverse == True:
		comp = rev_comp

	gaps = [32, 16, 8, 4, 2, 1]
	for gap in gaps:
		if gap < len(data):
			for i in range(len(data) - gap):
				for k in range(i + gap, len(data)):
					if comp( data[k], data[i] ):
						data[k], data[i] = data[i], data[k] # swap data[i], data[k]
	return data