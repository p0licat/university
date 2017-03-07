'''
	Filter module, thid module contains the definitino for the function that handles filtering inside a list.
'''

def filterList(data, lambdaFunc):
	'''
		filterList iterates through a list and eliminates all values that do not respect the condition.
		
		Input:
			data: 		a list, otherwise raises exception
			lambdaFunc: a comparison function
		Output:
			filteredList
	'''
	if type(data) != type([1, 2, 3]):
		raise TypeError("First parameter must be a list.")
	filteredList = []
	for i in data:
		if lambdaFunc(i):
			filteredList.append(i)

	return filteredList