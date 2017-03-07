#include "UI.h"

UI * createUI(CountryRepoController * controller)
{
	UI* ui = malloc(sizeof(UI));
	if (ui == NULL) // if could not be created
		return NULL;

	ui->countryController = controller;
	return ui;
}

void destroyUI(UI ** ui)
{
	if (*ui == NULL)
		return;
	free(*ui);
	*ui = NULL;
}

int readMenuOption(char* message)
{
	char s[READ_LENGTH];
	int returnValue = 0;

	while (TRUE)
	{
		printf(message);
		scanf_s("%s", s, READ_LENGTH-1);
		int result = sscanf_s(s, "%d", &returnValue); // stores converted string to int
		if (result == 0) // if unsuccessfull
			printf("Please try inserting a valid integer again!\n");
		else
			break;
	}
	return returnValue;
}

i_cont readContinent(char* message)
{
	char s[READ_LENGTH];
	i_cont returnValue = None;

	while (TRUE)
	{
		printf(message);
		scanf_s("%s", s, READ_LENGTH - 1);
		
		char aux[CONTINENT_NAME_LENGTH];
		char* cts;
		int i = 0;
		for (i = 0; i <= 5; ++i)
		{
			cts = continentToString(i, aux);
			if (strcmp(s, cts) == 0)
				return i;
		}
		printf("Invalid continent!");
	}
	return None;
}

Country readCountry()
{
	printf("Please insert a name: ");
	char read[READ_LENGTH];
	getc(stdin);
	fgets(read, READ_LENGTH - 1, stdin);

	i_cont cont = readContinent("Please insert continent: ");
	int pop_m = readMenuOption("Please insert population: ");

	Country newCountry = createCountry(read, cont, pop_m);
	return newCountry;
}

void printMenu()
{
	printf("======================================================\n");
	printf("1 - Add a country.\n");
	printf("2 - Delete a country.\n");
	printf("3 - List countries.\n");
	printf("4 - Modify a country.\n");
	printf("5 - Undo last change.\n");
	printf("6 - Redo last change.\n");
	printf("0 - Exit.\n");
	printf("======================================================\n");
}

void selectShowCountriesOption()
{
	printf("1 - Show countries by name.\n");
	printf("2 - Show countries by continent.\n");
	printf("0 - Exit\n");
}

void printCountriesToScreen(CountryRepoController* controller)
{
	while (TRUE)
	{
		selectShowCountriesOption();
		int input = readMenuOption("Please choose an option.\n");
		switch (input)
		{
			case 0:
				return;
			case 1:
			{
				printf("Please insert a name ( leave empty to print all ): ");
				char read[READ_LENGTH];
				getc(stdin);
				fgets(read, READ_LENGTH - 1, stdin);
				char* pp = printCountriesBySubstring(controller, read);
				if (pp == NULL)
					printf("Nothing was found!\n");
				else
					printf(pp);
				break;
			}
			case 2:
			{
				i_cont cont = readContinent("Please insert continent ( None to exit ): ");
				char* pp = printCountriesByContinent(controller, cont);
				if (pp == NULL)
					printf("No continents were found!\n");
				else
					printf(pp);
				break;
			}
			default:
				printf("Choose a valid option!\n");
		}
	}
}

void uiAddCountry(CountryRepoController* controller)
{
	Country newCountry = readCountry();
	int success = controllerAddCountry(controller, newCountry);
	if (success)
		printf("Added country!\n");
	else
		printf("Could not add!\n");
}

void uiDeleteCountry(CountryRepoController* controller)
{
	Country country = readCountry();
	int rval = controllerDeleteCountry(controller, country);
	if (rval == 0)
		printf("No matching country was found.\n");
	else
		printf("Country removed!\n");
}

void printModifyCountryOptions()
{
	printf("1 - Modify name.\n");
	printf("2 - Modify continent.\n");
	printf("3 - Modify population.\n");
	printf("4 - Migrate population.\n");
	printf("0 - Exit\n");
}

void uiModifyCountry(CountryRepoController* controller)
{
	printf("Please insert the country to modify.\n");
	Country country = readCountry();
	int existsValue = controllerFindCountry(controller, country);
	if (!existsValue)
	{
		printf("No such country exists in the repository!\n");
		return;
	}

	while (TRUE)
	{
		printModifyCountryOptions();
		int input = readMenuOption("Choose an option!\n");

		switch (input)
		{
			case 0:
				return;
			case 1:
			{
				printf("Please insert a new name: ");
				char read[READ_LENGTH];
				getc(stdin);
				fgets(read, READ_LENGTH - 1, stdin);
				Country newCountry = createCountry(read, getContinent(&country), getPopulation(&country));
				controllerModifyCountry(controller, country, newCountry);
				break;
			}
			case 2:
			{
				i_cont continent = readContinent("Please insert new continent: \n");
				Country newCountry = createCountry(getName(&country), continent, getPopulation(&country));
				controllerModifyCountry(controller, country, newCountry);
				break;
			}
			case 3:
			{
				int pop_m = readMenuOption("Insert a new population: \n");
				Country newCountry = createCountry(getName(&country), getContinent(&country), pop_m);
				controllerModifyCountry(controller, country, newCountry);
				break;
			}
			case 4:
			{
				int pop_m = readMenuOption("Please insert the population to migrate: \n");
				printf("Please insert the country to migrate to: \n");
				Country migrateDest = readCountry();
				if (!controllerMigratePopulation(controller, country, migrateDest, pop_m))
					printf("Could not modify! Not enough population!\n");
				else
					printf("Success!\n");
				
				break;
			}
			default:
				printf("Please insert a valid option or 0 to quit!\n");
		}
	}
}

void uiPerformUndo(CountryRepoController* controller)
{
	if (controller->canUndo)
	{
		controllerPerformUndo(controller);
		printf("Successful!\n");
	}
	else
	{
		printf("Can not undo!\n");
	}
}

void uiPerformRedo(CountryRepoController* controller)
{
	if (controller->canRedo)
	{
		controllerPerformRedo(controller);
		printf("Successful!\n");
	}
	else
	{
		printf("Nothing to redo!\n");
	}
}

void startUI(UI * ui)
{
	while (TRUE) // main loop
	{
		printMenu(); // show options
		int input = readMenuOption("Choose an option!\n"); // read an option
		
		switch (input) // main switch
		{
			case 0:
				return;
			case 1:
				uiAddCountry(ui->countryController);
				break;
			case 2:
				uiDeleteCountry(ui->countryController);
				break;
			case 3:
				printCountriesToScreen(ui->countryController);
				break;
			case 4:
				uiModifyCountry(ui->countryController);
				break;
			case 5:
				uiPerformUndo(ui->countryController);
				break;
			case 6:
				uiPerformRedo(ui->countryController);
				break;
			default:
				printf("Invalid option!\n");
		}

	}
}

