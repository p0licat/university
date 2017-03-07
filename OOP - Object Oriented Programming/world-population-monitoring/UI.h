#pragma once

#define READ_LENGTH 16 // standard input should be 16 bytes, modify define to change
#define TRUE 1

#include <stdio.h>
#include <string.h>
#include "Controller.h"

/*
	This header contains the definition of the UI behaviour. The UI is console based, so this will handle
	output and input to the console with stdio.h. Each UI object should have a controller attached, and communicate
	with the internal data using the controller.

	In order to start the User Interface, create a UI object and call the method startUI().
*/

typedef struct {
	CountryRepoController* countryController;
} UI;

/*
	Constructor for the UI class. It assigns the pointer of type ( CountryRepoController* ) named 
	countryController to a repository that was already constructed. 

	Input:
		CountryRepoController* countryController - pointer to controller
	Output:
		UI* - pointer to object of type UI
*/
UI* createUI(CountryRepoController* controller);

/*
	Deallocate all memory in the UI object.
	Input:
		UI** ui - address of pointer to UI object
	Output:
		none ( void ) 
*/
void destroyUI(UI ** ui);

/*
	This method launches the main loop for the UI. The rest of the reading and writing methods have no
	prototypes in this header, but are dirrectly defined in the UI.c file.
	Input:
		UI* ui
	Output:
		none ( void ) 
*/
void startUI(UI* ui);
