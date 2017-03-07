#pragma once

#include <string.h>
#include <stdio.h>

/*
This header contains the definition of the class Country, which is the main object used by the application.

Requirement: 
	Each Country has a unique name, the continent it belongs 
	to (may be Europe, America, Africa, Australia and Asia) and a population (stored  in  millions).

The unicity of the name will be handled by the repository.
*/

#define COUNTRY_NAME_LENGTH 20   // maximum name length is not specified
#define CONTINENT_NAME_LENGTH 10 //  the continent with the longest name is Australia, with 9 characters
#define MAXIMUM_PRINT_LENGTH 90  // length of toString should never exceed 82 but it is set as 90
#define i_cont Continent

// all continent types, and the type None for empty initializations
typedef enum {
	Europe, America, Africa, Australia, Asia, None
} Continent;

// actual class Country
typedef struct {
	char name[COUNTRY_NAME_LENGTH]; // string containing the name of the Country object
	i_cont continent;	// continent to which the country belongs
	int pop_m;			// population, stored in millions
} Country;

/*
	Constructor function for any Country object. Allocates memory and initializes members.
	Input:
		char name[] - c_string containing the name of the country
		i_cont cont - i_cont ( Continent ) with one of the available continents
		int pop_m   - integer specifying the number of residents, in millions ( _m ) 
	Output:
		Country		- object that will be constructed inside the function
*/
Country createCountry(char name[], i_cont continent, int pop_m);

/*
	Getter for the name property of a Country object. ( returns c->name )
	Input:
		Country* c - pointer to country object
	Output:
		char*	   - address of the array of characters found in the name member of the object
*/
char* getName(Country* c);

/*
	Returns a string of character that corresponds to each continent, for formatting and printing.
	Requires an auxiliary array of characters in order to work. This should have at least length
	(CONTINENT_NAME_LENGTH).
	Input:
		i_cont cont  - continent type ( enum )
		char aux[L]  - empty array needed by the function in order to work
					   L should be at least CONTINENT_NAME_LENGTH
	Output:
		char*		 - pointer to aux, which will contain the result

*/
char* continentToString(i_cont continent, char aux[]);

/*
	Getter for the population member of the country c.
	Input:
		Country* c - pointer to a country object
	Output:
		int	- value found inside the member "population" from the object c
*/
int getPopulation(Country* c);

/*
	Getter for the continent member of the country c.
	Input:
		Country* c - pointer to a country object
	Output:
		i_cont ( Continent enum ) - the continent of the object
*/
i_cont getContinent(Country* c);

/*
	This function formats the information inside object in a user friendly and human readable way, 
	and stores it in the array "char out[]".
	The formatting is the following: "Name: * | Continent: * | Population: *\n"
	
	Input:
		Country * c - pointer to country object
		char out[]  - array of characters, of at least size MAXIMUM_PRINT_LENGTH
	Output:
		none ( void )
		* result is stored in char out[] 
*/
void toString(Country * c, char out[]);

/*
	This method compares two countries, based on their populations. If c1 is larger, -1 is returned.
	If they are equal, 0 is returned. If c2 is larger, 1 is returned.

	Input:
		Country* c1 - pointer to first country
		Country* c2 - pointer to second country
	Output:
		{ -1 or 0 or 1 } depending on comparison
		* -2 is considered error
*/
int compareCountries(Country* c1, Country* c2);