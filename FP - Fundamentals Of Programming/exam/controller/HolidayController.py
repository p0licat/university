'''
	HolidayController module. This module defines the HolidayController class, which manages a repository of Holiday elements and acts as
	an interface between the UI and the repository.
'''

from domain.Holiday import Holiday

class HolidayController:
	def __init__(self, repo):
		'''
			Constructor for the HolidayController class. It assigns a Repository object to the controller.
			Input:
				repo (Repository)
		'''
		self._repo = repo

	def loadFromFile(self, filename):
		'''
			Loads the file with the given filename and adds all valid entries to the repository, or returns False
			if there are syntax errors.
			Input:
				(str) sfilename, the name of the file from which to load
			Return:
				True/False 
		'''
		dFile = open(filename, 'r')
		for i in dFile:
			line = i.split(';')
			try: # attempt to create a new Holiday object
				newId 	= int(line[0])
				newLoc 	= 	  line[1]
				newType = 	  line[2]
				for k in line[3]:
					if k == '\n':
						line[3] = line[3][:-1]
				newCost = int(line[3])
				newHoliday = Holiday(newId, newLoc, newType, newCost)
				self._repo.addElement(newHoliday)
			except Exception as e:
				print (e)
				return False
		return True

	def getHolidays(self):
		'''
			Returns a list of all holidays inside the repository, or False if this repository is empty.
			Returns:
				list of Holidays
				False: if repo is empty
		'''
		elementList = self._repo.getElements()
		if elementList == []:
			return False
		return elementList

	def getAllResorts(self):
		'''
			Returns a list of all resorts that exist in the repository.
			Return:
				list of strings
				False for no results
		'''
		result = []
		elementList = self.getHolidays()
		for i in elementList:
			if not i.getLocation() in result:
				result.append(i.getLocation())
		if result != []:
			return result
		return False

	def getAllTypes(self):
		'''
			Returns a list of all types that exist in the repository.
			Return:
				list of strings
				False for no results
		'''
		result = []
		elementList = self.getHolidays()
		for i in elementList:
			if not i.getType() in result:
				result.append(i.getType())
		if result != []:
			return result
		return False

	def searchByResort(self, parameter):
		'''
			Searches the repository for all Holidays of the resort equal to parameter and generates a list containing these entries
			sorted by price.
			Input:
				parameter (int)
			Returns:
				list of Holidays
				False if nothing is found 
		'''
		allElements = self.getHolidays()
		if allElements == False:
			return False

		typeList = []
		for i in allElements:
			if parameter in i.getLocation():
				typeList.append(i)

		for i in range(len(typeList)-1):
			for k in range(i+1, len(typeList)):
				if typeList[k].getPrice() > typeList[i].getPrice():
					typeList[k], typeList[i] = typeList[i], typeList[k] # swap
		if typeList == []:
			return False
		else:
			return typeList


	def searchByType(self, parameter):
		'''
			Searches the repository for all Holidays of the type equal to parameter and generates a list containing these entries
			sorted by price.
			Input:
				parameter (int)
			Returns:
				list of Holidays
				False if nothing is found 
		'''
		allElements = self.getHolidays()
		if allElements == False:
			return False

		typeList = []
		for i in allElements:
			if i.getType() == parameter:
				typeList.append(i)

		for i in range(len(typeList)-1):
			for k in range(i+1, len(typeList)):
				if typeList[k].getPrice() > typeList[i].getPrice():
					typeList[k], typeList[i] = typeList[i], typeList[k] # swap
		if typeList == []:
			return False
		else:
			return typeList
			