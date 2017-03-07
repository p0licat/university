'''
	UserInterface module. Defines the UserInterface class, which handles all interactions with the client through a console.
'''

class UserInterface:
	'''
		UserInterface class, handles all printing and reading via the console. It validates user input and uses the Controllers 
		to perform actions.
	'''
	def __init__(self, controller, filename):
		'''
			Initializer for the UI class, binds a controller to the UserInterface object.
		'''
		self._controller = controller
		self._filename = filename

	def mainMenu(self):
		'''
			MainMenu method for the UserInterface class. This method starts the main loop of the program, which is a menu.
		'''
		menuOptions = "Actions: \n"
		menuOptions += "\t1 - Search by Type\n"
		menuOptions += "\t2 - Search by Resort\n"
		menuOptions += "\t0 - Exit\n"

		if self._controller.loadFromFile(self._filename) != False: # load from file
			print ("Loaded from file!")
		else:
			print ("ERROR! CORRUPTED FILE!")

		keepAlive = True
		while keepAlive:
			print(menuOptions)
			userInput = input("Please choose an option: ")
			try:
				userInput = int(userInput)
				if userInput == 0:
					keepAlive = False
				elif userInput == 1:
					self.__searchTypeMenu()
				elif userInput == 2:
					self.__searchResortMenu()
				else:
					print ("Please choose a valid option!")
			except Exception as e:
				print ("Please insert an integer.")

	def __searchResortMenu(self):
		while True:
			print ("Possible resorts are: ")
			print (self._controller.getAllResorts())
			uInput = input("Please insert the resort or 'x' to return: ")
			if uInput == 'x':
				return

			result = self._controller.searchByResort(uInput)
			if result != False:
				for i in result:
					print (i)
			else:
				print ("No results!")

	def __searchTypeMenu(self):
		while True:
			print ("The possible types are: ")
			print (self._controller.getAllTypes())
			uInput = input("Please insert the type or 'x' to return: ")
			if uInput == 'x':
				return

			result = self._controller.searchByType(uInput)
			if result != False:
				for i in result:
					print (i)
			else:
				print ("No results!")


