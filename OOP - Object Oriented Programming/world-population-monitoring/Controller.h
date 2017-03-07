#pragma once

#include "CountryRepo.h"

/*
	This module defines the class Controller. A controller is an interface between the UI and the repository.
*/

typedef struct {
	CountryRepo* countryRepo;
	CountryRepo* previousState;
	int canUndo, canRedo;
} CountryRepoController;

/*
	Constructor of countryRepoController. Returns a newly created object, with the repo pointing to the given
	repo's address. 
	Input: -
	Output:
		CountryRepoController - return created controller
*/
CountryRepoController createCountryRepoController(CountryRepo* countryRepo);

/*	
	This method creates a printable formatted string by calling the repo's substring search method.
	Input:
		CountryRepoController* - pointer to controller
	Output:
		char* - formatted null terminated string
*/
char* printCountriesBySubstring(CountryRepoController* controller, char subs[]);

/*
	This method creates a printable formatted string by calling the repo's search by continent method.
	Very similar to printCountriesBySubstring().
	Input:
		CountryRepoController* controller - pointer to controller
		i_cont cont - continent to match
	Output:
		char* - pointer to dynamically allocated formatted string
*/
char* printCountriesByContinent(CountryRepoController* controller, i_cont cont);

/*
	Tries to add a country to the repo inside the controller. Returns 0 if another country with the 
	same name exists, or 1 if successfull.
	Input:
		CountryRepoController* controller - pointer to controller
		Country c - country to add
	Output:
		int - error value
*/
int controllerAddCountry(CountryRepoController* controller, Country c);

/*
	This function deletes the given country from the repo associated with the controller by calling 
	a function belonging to the repo.
	Input:
		CountryRepoController* controller - pointer to controller
		Country c - country to remove
	Output:
		int - error value ( 1 for successfull, 0 for non existing country )
*/
int controllerDeleteCountry(CountryRepoController* controller, Country c);


/*
	This function modifies the country from the controller that matches the one passed to the function.
	It does this by first checking if it exists, then changing its fields.

	Input:
		CountryRepoController * controller - pointer to controller 
		Country c - country to modify
	Output:
		int - error value ( 1 for successfull, 0 for non existing country )

*/
int controllerModifyCountry(CountryRepoController* controller, Country c, Country newCountry);

/*
	This function returns a 1 if the given country is found, or 0 otherwise.
	Input:
		CountryRepoController* controller - pointer to the controller
		Country c - country to find
	Output:
		0 or 1 ( 0 for not found, 1 for found )
*/
int controllerFindCountry(CountryRepoController* controller, Country c);

/*
	This function migrates population from Country c1 to Country c2, if possible. If not possible returns 0.
	Input:
		CountryRepoController* controller - pointer to controller
		Country c1 - source country
		Country c2 - destination country
		int pop_m  - population to migrate
	Output:
		int - 0 for impossible, 1 for success
*/
int controllerMigratePopulation(CountryRepoController* controller, Country c1, Country c2, int pop_m);

/*
	Sets the canUndo property to one and copies the current state of the repo into the previous state.
	Input:
		CountryRepoController* controller - pointer to the controller
	Output:
		none
*/
void controllerUndoSetPreviousState(CountryRepoController* controller);

/*
	Performs an undo by restoring the current state to the previous state.
	Input:
		CountryRepoController* controller
	Output:
		1 for success or 0 if unable to undo
*/
int controllerPerformUndo(CountryRepoController* controller);