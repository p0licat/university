#include "Controller.h"

CountryRepoController createCountryRepoController(CountryRepo * countryRepo)
{
	CountryRepoController controller;
	controller.countryRepo = countryRepo;
	controller.previousState = createCountryRepo();
	controller.canUndo = 0;
	controller.canRedo = 0;
	return controller;
}

char * printCountriesBySubstring(CountryRepoController * controller, char subs[])
{
	int lengthOfString = 0;
	DynamicVector* result = getCountriesContainingSubstring(controller->countryRepo, subs);
	if (result == NULL) // if nothing was found
		return NULL;
	lengthOfString = getLength(result);

	// don't ask
	char* format = (char*)malloc(2 * lengthOfString + lengthOfString * MAXIMUM_PRINT_LENGTH * (sizeof(char)));
	int sob = 2 * lengthOfString + lengthOfString * MAXIMUM_PRINT_LENGTH * (sizeof(char));

	memset(format, 1, sob);
	format[sob - 1] = 0; // terminate with null
	strcpy_s(format, strlen(format),"Countries are: \n");
	int i;
	for (i = 0; i < lengthOfString; ++i)
	{
		Country c = getElementAtIndex(result, i);
		char re[MAXIMUM_PRINT_LENGTH];
		toString(&c, re);
		strcat_s(re, MAXIMUM_PRINT_LENGTH, "\n");
		strcat_s(format, sob, re);
	}

	return format;
}

char * printCountriesByContinent(CountryRepoController * controller, i_cont cont)
{
	int lengthOfString = 0;
	DynamicVector* result = getCountriesByContinent(controller->countryRepo, cont);
	if (result == NULL) // if nothing was found
		return NULL;
	lengthOfString = getLength(result);

	char* format = (char*)malloc(2 * lengthOfString + lengthOfString * MAXIMUM_PRINT_LENGTH * (sizeof(char)));
	int sob = 2 * lengthOfString + lengthOfString * MAXIMUM_PRINT_LENGTH * (sizeof(char));


	memset(format, 1, sob);
	format[sob - 1] = 0; // terminate with null
	strcpy_s(format, strlen(format), "Countries are: \n");

	int i;
	for (i = 0; i < lengthOfString; ++i)
	{
		Country c = getElementAtIndex(result, i);
		char re[MAXIMUM_PRINT_LENGTH];
		toString(&c, re);
		strcat_s(re, MAXIMUM_PRINT_LENGTH, "\n");
		strcat_s(format, sob, re);
	}

	return format;
}

int controllerAddCountry(CountryRepoController * controller, Country c)
{
	controllerUndoSetPreviousState(controller);
	
	int val = addCountryToRepo(controller->countryRepo, c);
	if (!val)
	{
		controller->canUndo = 0;
		controller->canRedo = 0;
	}
	else
	{
		controller->canUndo = 1;
		controller->canRedo = 0;
	}
	return val;
}

int controllerDeleteCountry(CountryRepoController * controller, Country c)
{
	controllerUndoSetPreviousState(controller);
	int val = deleteCountryFromRepo(controller->countryRepo, c);
	if (!val)
	{
		controller->canUndo = 0;
		controller->canRedo = 0;
	}
	else
	{
		controller->canUndo = 1;
		controller->canRedo = 0;
	}
	return val;
}

int controllerModifyCountry(CountryRepoController * controller, Country c, Country newCountry)
{
	controllerUndoSetPreviousState(controller);
	int val = modifyCountryFromRepo(controller->countryRepo, c, newCountry);
	if (!val)
	{
		controller->canUndo = 0;
		controller->canRedo = 0;
	}
	else
	{
		controller->canRedo = 0;
		controller->canUndo = 1;
	}
	return val;
}

int controllerFindCountry(CountryRepoController * controller, Country c)
{
	int i, length = getLengthOfRepo(controller->countryRepo);
	for (i = 0; i < length; ++i)
	{
		Country current = getCountryAtRepoIndex(controller->countryRepo, i);
		if (compareCountries(&current, &c) == 0)
			return 1;
	}
	return 0;
}

int controllerMigratePopulation(CountryRepoController * controller, Country c1, Country c2, int pop_m)
{
	// make sure they exist
	if (!(controllerFindCountry(controller, c1) && controllerFindCountry(controller, c2)))
		return 0;

	int pop_c1 = getPopulation(&c1); // population of Country c1
	int pop_c2 = getPopulation(&c2); // population of Country c2

	// can't migrate more than the whole population
	if (pop_m > pop_c1)
		return 0;

	controllerUndoSetPreviousState(controller);

	Country newCountry_c1 = createCountry(getName(&c1), getContinent(&c1), pop_c1 - pop_m);
	Country newCountry_c2 = createCountry(getName(&c2), getContinent(&c2), pop_c2 + pop_m);

	modifyCountryFromRepo(controller->countryRepo, c1, newCountry_c1);
	modifyCountryFromRepo(controller->countryRepo, c2, newCountry_c2);

	return 1;
}

void controllerUndoSetPreviousState(CountryRepoController * controller)
{
	controller->canUndo = 1;
	controller->canRedo = 0;
	
	free(controller->previousState);
	controller->previousState = createCountryRepo();

	int i, length = getLengthOfRepo(controller->countryRepo);
	for (i = 0; i < length; ++i)
	{
		Country current = getCountryAtRepoIndex(controller->countryRepo, i);
		addCountryToRepo(controller->previousState, current);
	}
}

int controllerPerformUndo(CountryRepoController * controller)
{
	if (!controller->canUndo || controller->previousState == NULL)
		return 0;

	CountryRepo* auxRepo = createCountryRepo();
	int i, lengthOfPrevious = getLengthOfRepo(controller->previousState),
		   lengthOfCurrent = getLengthOfRepo(controller->countryRepo);

	for (i = 0; i < lengthOfCurrent; ++i)
	{
		Country currentCountry = getCountryAtRepoIndex(controller->countryRepo, i);
		addCountryToRepo(auxRepo, currentCountry);
	}

	clearCountryRepo(controller->countryRepo);

	for (i = 0; i < lengthOfPrevious; ++i)
	{
		Country currentCountry = getCountryAtRepoIndex(controller->previousState, i);
		addCountryToRepo(controller->countryRepo, currentCountry);
	}

	clearCountryRepo(controller->previousState);

	for (i = 0; i < lengthOfCurrent; ++i)
	{
		Country currentCountry = getCountryAtRepoIndex(auxRepo, i);
		addCountryToRepo(controller->previousState, currentCountry);
	}
	free(auxRepo);
	controller->canUndo = 0;
	controller->canRedo = 1;

	return 1;
}

int controllerPerformRedo(CountryRepoController* controller)
{
	if (!controller->canRedo || controller->previousState == NULL)
		return 0;

	CountryRepo* auxRepo = createCountryRepo();
	int i, lengthOfPrevious = getLengthOfRepo(controller->previousState),
		lengthOfCurrent = getLengthOfRepo(controller->countryRepo);

	for (i = 0; i < lengthOfCurrent; ++i)
	{
		Country currentCountry = getCountryAtRepoIndex(controller->countryRepo, i);
		addCountryToRepo(auxRepo, currentCountry);
	}

	clearCountryRepo(controller->countryRepo);

	for (i = 0; i < lengthOfPrevious; ++i)
	{
		Country currentCountry = getCountryAtRepoIndex(controller->previousState, i);
		addCountryToRepo(controller->countryRepo, currentCountry);
	}

	clearCountryRepo(controller->previousState);

	for (i = 0; i < lengthOfCurrent; ++i)
	{
		Country currentCountry = getCountryAtRepoIndex(auxRepo, i);
		addCountryToRepo(controller->previousState, currentCountry);
	}

	free(auxRepo);
	controller->canUndo = 1;
	controller->canRedo = 0;

	return 1;
}

