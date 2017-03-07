'''
	Tests module, this is where tests for all classes are defined.
	All methods from Domain, Controller and Repository are tested.
'''

from domain.Holiday import Holiday
from repository.Repository import Repository
from controller.HolidayController import HolidayController

def testHoliday():
	holiday1 = Holiday(0, "Madrid", "seaside", 342)
	holiday2 = Holiday(1, "Quebec", "city-break", 342)

	assert holiday1.getId() == 0
	assert holiday2.getId() == 1

	assert holiday1.getType()	  == "seaside"
	assert holiday1.getLocation() == "Madrid"
	assert holiday1.getPrice()	  == 342

	return True

def testDomain():
	if testHoliday() == True:
		return True
	else:
		return False


def testRepository():
	repository = Repository()
	holiday1 = Holiday(0, "Madrid", "seaside", 342)
	holiday2 = Holiday(1, "Quebec", "city-break", 342)	

	assert repository.addElement(holiday1) == True
	assert repository.addElement(holiday1) == False
	assert repository.addElement(holiday2) == True

	assert len(repository.getElements()) > 0
	assert len(repository.getElements()) == 2

	return True

def testController():
	repository = Repository()	
	holiday1 = Holiday(0, "Madrid", "seaside", 342)
	holiday2 = Holiday(1, "Quebec", "city-break", 342)
	holiday3 = Holiday(2, "Quebec", "seaside", 333)	
	controller = HolidayController(repository)

	assert repository.addElement(holiday1) == True
	assert repository.addElement(holiday2) == True
	assert repository.addElement(holiday3) == True

	assert len(controller.getHolidays())	== 3
	assert len(controller.getAllResorts()) 	== 2
	assert len(controller.getAllTypes())	== 2

	assert len(controller.searchByResort("Quebec")) == 2
	assert len(controller.searchByResort("Madrid")) == 1

	assert len(controller.searchByType("seaside"))	   == 2
	assert len(controller.searchByType("city-break"))  == 1

	assert controller.loadFromFile("database.txt") == True

	return True

def testAll():
	if testDomain() == True:
		print ("Tests from Domain passed!")
	else:
		print ("Tests from Domain failed!")
	

	if testController() == True:
		print ("Tests from Controller passed!")
	else:
		print ("Tests from Controller failed!")


	if testRepository() == True:
		print ("Tests from Repository passed!")
	else:
		print ("Tests from Repository failed!")

testAll()