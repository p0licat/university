'''
	Holiday module, defines the holiday class. Since the objects are not required to be modified by the application after reading, 
	no setters are implemented in this class.
'''

class Holiday:
	'''
		Holiday is the main object used by the program. It holds information about:
		the ID, location, type and price.
		    0 	   1		2 		3
		(int) 0: ID of the holiday, unique for each holiday in order to distinguish them with certainty.
		(str) 1: Location, somewhere in the world.
		(str) 2: Type, such as city-break or seaside, depending on the point of interest.
		(int) 3: Price, in euro. 
	'''
	def __init__(self, _id, _location, _type, _price):
		'''
			Constructor for the holiday object.
			Input:
				(int) _id   	0: ID of the holiday, unique for each holiday in order to distinguish them with certainty.
				(str) _location 1: Location, somewhere in the world.
				(str) _type 	2: Type, such as city-break or seaside, depending on the point of interest.
				(int) _price	3: Price, in euro.
		'''
		self._id = _id
		self._type = _type
		self._location = _location
		self._price = _price

	def getId(self):
		'''
			Getter for the ID of the object.
			Returns:
				(int) ID
		'''
		return self._id


	def getType(self):
		'''
			Getter for the type of the object.
			Returns:
				(str) type
		'''
		return self._type

	def getLocation(self):
		'''
			Getter for the location of the object.
			Returns:
				(str) Location
		'''
		return self._location


	def getPrice(self):
		'''
			Getter for the price of the object.
			Returns:
				(int) Price
		'''
		return self._price

	def __repr__(self):
		'''
			Override for the representation of the Holiday object.
		'''
		return str(self._id) + ": " + self._location + ", " + self._type + " at " + str(self._price) + "$ "

		

