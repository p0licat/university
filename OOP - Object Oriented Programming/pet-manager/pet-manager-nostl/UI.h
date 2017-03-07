#pragma once

#include "DogRepoController.h"
#include <iostream>
#include <string>
#include <vector>

class UI {
private:
	std::vector<std::string> adminMenuOptions;
	std::vector<std::string> userMenuOptions;
	DogRepoController* controller;
	DogRepo adoptedDogs;
public:
	UI() { controller = NULL; }
	UI(DogRepoController& controller) : controller(&controller) 
	{
		// admin
		this->adminMenuOptions.push_back("1 - List dogs.");
		this->adminMenuOptions.push_back("2 - Add new dog.");
		this->adminMenuOptions.push_back("3 - Delete dog.");
		this->adminMenuOptions.push_back("4 - Update dog.");
		this->adminMenuOptions.push_back("0 - Exit.");
	
		// user
		this->userMenuOptions.push_back("1 - Adopt a dog!");
		this->userMenuOptions.push_back("2 - See your adoptions.");
		this->userMenuOptions.push_back("3 - See dogs by breed.");
		this->userMenuOptions.push_back("0 - Exit.");
	}

	~UI() {}

	void startUI();

private:
	void runAdminMode();
	void runUserMode();

	// admin mode
	void printMenuOptions(bool admin = false);
	void printDogs();
	void addDogMenu();
	void removeDogMenu();
	void updateDogMenu();

	// user mode
	void rollDogs();
	void printAdoptions();
	void breedPrintMenu();


	// utility
	DogObject readDog();
	std::string readString(std::string message);
	int readInteger(); // read only one digit
	int readNumber(); // read a number
};

