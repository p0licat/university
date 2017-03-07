'''
	AppCoordinator module, binds all the elements of the application together.
'''

from ui.UserInterface import UserInterface
from controller.HolidayController import HolidayController
from repository.Repository import Repository

def main():
	holidayRepository = Repository()
	holidayController = HolidayController(holidayRepository)
	ui = UserInterface(holidayController, "database.txt")

	ui.mainMenu()

main()