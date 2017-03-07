#include "UI.h"

void UI::startUI()
{
	if (this->controller == NULL)
	{
		std::cout << "Error initializing UI!\n";
		return;
	}
	else
	{
		while (true)
		{
			std::cout << "1 - Administrator mode. \n";
			std::cout << "2 - User mode. \n";
			std::cout << "0 - Exit.\n";
			int userInput = readInteger();
			if (userInput == 0)
				return;
			else if (userInput == 1)
			{
				runAdminMode();
			}
			else if (userInput == 2)
			{
				runUserMode();
			}
			else
			{
				std::cout << "Please insert a valid option.\n";
				continue;
			}
		}
	}
}

void UI::printMenuOptions(bool admin)
{
	std::vector<std::string> menuOptions;
	if (admin)
		menuOptions = this->adminMenuOptions;
	else
		menuOptions = this->userMenuOptions;
	std::vector<std::string>::iterator it;
	for (it = menuOptions.begin(); it != menuOptions.end(); ++it)
		std::cout << *it << '\n';
}

int UI::readInteger()
{
	int rval = -1;
	std::cout << "Please insert integer: ";
	std::string readInput;
	std::cin >> readInput;


	if (readInput.size() == 1) // one integer, valid
		rval = readInput[0] - '0';

	return ((rval < 0 || rval > 9) ? -1 : rval);
}


int UI::readNumber()
{
	int rval = -1;
	std::cout << "Please insert a number: ";
	std::string readInput;
	std::cin >> readInput;

	// check if all characters of the string are digits ( '0', '1', ... , '9' )
	for (unsigned int i = 0; i < readInput.size(); ++i)
		if (!isdigit(readInput[i]))
			return rval; // return -1 if not

	rval = 0;
	for (unsigned int i = 0; i < readInput.size(); ++i)
	{
		rval *= 10;
		rval += readInput[i] - '0';
	}

	return rval;
}

void UI::printDogs()
{
	DynamicVector<DogObject> allDogs = this->controller->getAllDogs();
	for (int i = 0; i < allDogs.getSize(); ++i)
	{
		DogObject currentDog = allDogs[i];
		std::cout << currentDog.toString();
	}
}

std::string UI::readString(std::string message)
{
	std::cout << message;
	std::string rval; std::cin >> rval;

	return rval;
}

void UI::addDogMenu()
{
	DogObject newDog(readDog());
	if ( !newDog.isValid() )
	{
		std::cout << "Invalid dog! \n";
		return;
	}

	this->controller->addDogToRepo(newDog);
}

void UI::removeDogMenu()
{
	DogObject dogInput(readDog());
	if (!dogInput.isValid())
	{
		std::cout << "Invalid dog! \n";
		return;
	}

	if ( !this->controller->dogExists(dogInput) )
	{
		std::cout << "Dog does not exist. \n";
		return;
	}

	this->controller->removeDogFromRepo(dogInput);
	std::cout << "Removed dog from repo! \n";
}

DogObject UI::readDog()
{
	std::string dogName = readString("Please insert the dog's name: ");
	std::string dogBreed = readString("Please insert a dog breed: ");
	std::string imageUrl = readString("Please insert a picture url: ");
	std::cout << "Please insert the dog's age. \n";
	int dogAge = readNumber(); // readInteger is only used for menu options

	return DogObject(dogBreed, dogName, imageUrl, dogAge);
}

void UI::updateDogMenu()
{
	DogObject foundDog(readDog());
	if (!foundDog.isValid())
	{
		std::cout << "Invalid dog!\n";
		return;
	}

	if (!this->controller->dogExists(foundDog))
	{
		std::cout << "Dog does not exist! \n";
		return;
	}

	std::cout << "Dog was found!\n";
	while (true)
	{
		std::cout << "Please enter new dog. \n";
		DogObject newDog(readDog());
		if (!newDog.isValid())
			continue;

		this->controller->removeDogFromRepo(foundDog);
		this->controller->addDogToRepo(newDog);

		break;
	}
}

void UI::runAdminMode()
{
	// main loop for admin mode
	while (true)
	{
		printMenuOptions(true);
		int readValue = readInteger();
		
		switch (readValue)
		{
			case 1: // print dogs
				printDogs();
				break;
			case 2: // add dog
				addDogMenu();
				break;
			case 3: // remove dog
				removeDogMenu();
				break;
			case 4: // update dog
				updateDogMenu();
				break;
			case 0:
				return;
			default:
				std::cout << "Please insert a vaild option! \n";
				break;
		}
	}
}

void UI::rollDogs()
{
	if (this->controller->repoIsEmpty())
	{
		std::cout << "No dogs in the database! \n";
		return;
	}

	
	DynamicVector<DogObject> allDogs = this->controller->getAllDogs();
	int index = 0;
	int numberOfDogs = allDogs.getSize();


	while (true)
	{
		DogObject currentDog = allDogs[index];

		if (this->adoptedDogs.dogExists(currentDog))
		{
			if (adoptedDogs.getNumberOfDogs() == this->controller->getNumberOfDogs())
			{
				std::cout << "You've adopted all dogs! \n";
				return;
			}

			std::cout << "Dog exists! Skipping...\n";
			if (index == numberOfDogs - 1)
				index = 0;
			else
				index++;
			continue;
		}


		std::cout << currentDog.toString();

		std::cout << "Adopt? (y/n/x)\n";
		std::string readValue;
		std::cin >> readValue;
		if (readValue == "y") // adopt
		{
			this->adoptedDogs.addDog(currentDog);
			std::cout << "Adopted dog! Congratulations! \n";
		}
		else if (readValue == "n" ) // don't adopt
		{
			std::cout << "Skipping dog. \n";
		}
		else // exit
		{
			std::cout << "Exitting...\n";
			return;
		}


		if (index == numberOfDogs-1)
			index = 0;
		else
			index++;
	}

}

void UI::printAdoptions()
{
	DynamicVector<DogObject> dogs = this->adoptedDogs.getAllDogs();
	if (dogs.getSize() == 0)
	{
		std::cout << "You didn't adopt any dogs! \n";
		return;
	}

	int length = dogs.getSize();
	for (int i = 0; i < length; ++i)
		std::cout << dogs[i].toString();
}

void UI::breedPrintMenu()
{
	std::cout << "Please insert a breed: ";
	std::string breed;
	std::cin >> breed;
	
	DynamicVector<DogObject> allDogs = this->controller->getAllDogs();
	DynamicVector<DogObject> printDogs;

	for (int i = 0; i < allDogs.getSize(); ++i)
	{
		DogObject currentDog = allDogs[i];
		if (currentDog.getBreed() == breed)
			printDogs.addElement(currentDog);
	}
	if (printDogs.getSize() == 0)
	{
		std::cout << "Nothing was found! \n";
		return;
	}
	for (int i = 0; i < printDogs.getSize(); ++i)
		std::cout << printDogs[i].toString();
}

void UI::runUserMode()
{
	// main loop for user mode
	while (true)
	{
		printMenuOptions();
		int readValue = readInteger();

		switch (readValue)
		{
		case 1:
			rollDogs();
			break;
		case 2:
			printAdoptions();
			break;
		case 3:
			breedPrintMenu();
			break;
		case 0:
			return;
		default:
			std::cout << "Please insert a vaild option! \n";
			break;
		}
	}
}