#pragma once

/*
	This header defines a repository of Country elements. This relies on the DynamicVector header.
	It is no more than an interface to the DynamicVector.
*/

#include "country.h"
#include "DynamicVector.h"

// Class acts as a layer of indirection to a DynamicVector. Will be useful for deletions and filtering data.
typedef struct {
	DynamicVector* countryVector;
} CountryRepo;

/*
	Constructor of the repository. Calls the constructor of the DynamicVector.
	Input: -
	Output:
		CountryRepo* - address of the repository allocated by malloc()
*/
CountryRepo* createCountryRepo();

/*
	Frees memory. Uses two levels of indirection, same as the destructor of the DynamicVector.
	Input:
		CountryRepo** repo - address of pointer to repo
	Output:
		none ( void ) 
*/
void destroyCountryRepo(CountryRepo** repo);

/*
	Adds an element to the repository. Uses methods from the DynamicVector class. The difference is that
	this method filters countries that already exists, so duplicates are avoided.
	There are three possible output values: -1, 0, 1. 
	{ -1 } means that the address of the repo was null.
	{ 0  } means that there is already a country with that name
	{ 1  } means that the country was added
	
	Input:
		CountryRepo* repo - pointer to repository
		Country c - element to be added
	Output:
		(int) { -1 or 0 or 1 }
		
*/
int addCountryToRepo(CountryRepo* repo, Country c);

/*
	Getter for the repo length. Calls the getLength of the DynamicVector.
	Input:
		CountryRepo* repo - pointer to repo
	Ouptut: 
		int - length of repo ( number of countries in repo ) 
*/
int getLengthOfRepo(CountryRepo* repo);

/*
	Finds the position of the country with the same name as the one in char name[] or returns -1 if not found.
	Input:
		CountryRepo* repo - pointer to repo
		char name[] - name of country to look for
	Output:
		int - position of country with the given name
		* -1 if not found
*/
int getRepoPosCountryByName(CountryRepo* repo, char name[]);

/*
	Returns a copy of the country found at position ( int index ) in the repository.
	If position is outside of the range of the repository, an empty country will be returned.
	An empty country is defined as the value returned by: createCountry("", None, 0) 
	Input:
		CountryRepo* repo - pointer to repo
		int index - position 
	Output:
		Country - copy of country at position of empty country if not found
*/
Country getCountryAtRepoIndex(CountryRepo* repo, int index);

/*
	This method removes the country with the same name as the one in ( char name[] ) from the repository.
	This is done rather inefficiently, by reconstructing the elements DVector and appending every country except
	the one that has to be removed. However, the vector is constructed only once so the most important contributor
	to the inefficiency is not the resize() function, but the complexity of the appendToDVector() function.
	
	Input:
		CountryRepo* repo - pointer to repository
		char name[]		  - array of characters containing name of the country that has to be removed
	Output:
		-1 if repo address is invalid
		 0 if there is no country with given name
		 1 if country has been removed
*/
int removeRepoCountryWithName(CountryRepo* repo, char name[]);

/*
	This method replaces the country inside the repository on position ("int index") with Country ("c").
	This is done by reconstructing the vector, similarly to the removeRepoCountryWithName method.
	The vector is reconstructed, but instead of omitting the element at position "index", it is replaced
	with the new element ( of type Country ).
	
	Input:
		CountryRepo* repo - pointer to repository
		int index - position of country to be modified
		Country c - country to replace the previous one
	Output:
		-1 if repository is invalid
		 0 if the index is out of the range of the repo
		 1 if country was replaced
*/
int updateRepoCountryAtIndex(CountryRepo* repo, int index, Country c);

/*
	This method creates and returns a vector containing all of the Countries from the given repository
	that contain the substring "subs" in their name. This is done using the method strstr() from the 
	string.h standard library. This search is performed on the result of every call of the getName(Country*)
	method. The DynamicVector is constructed by calling its constructor, so malloc() handles the memory 
	assignment, making it possible to return a pointer to it. If no countries can be found, NULL is returned.
	If the string "subs" is the empty string, all countries will be returned.

	Input:
		CountryRepo* repo - pointer to repository
		char* subs - substring, null terminated array of characters
	Output:
		DynamicVector* - pointer to a DynamicVector constructed in the function
*/
DynamicVector* getCountriesContainingSubstring(CountryRepo* repo, char* subs);

/*
	This function returns a pointer to a DynamicVector ( DynamicVector* ) which contains all of 
	the countries of the continent matching "cont" from the repository, in a similar way to the 
	getCountriesContainingSubstring(). 

	Input:
		CountryRepo* repo - pointer to the repository
		i_cont cont - Continent (enum) type 
	Output:
		DynamicVector* - pointer to a DynamicVector constructed in the function.
		NULL if there is nothing that matches
*/
DynamicVector* getCountriesByContinent(CountryRepo* repo, i_cont cont);


/*
	This function returns an integer representing the capacity of the DynamicVector contained inside the
	CountryRepo.
	Input:
		CountryRepo* repo ( pointer to repo ) 
	Output:
		int ( capacity of the DynamicVector )
*/
int getRepoCapacity(CountryRepo* repo);

/*
	This function deletes the country if it exists and returns 1 or returns 0 for non existing country in
	the repo.
	Input:
		CountryRepo* repo
		Country c
	Output:
		int - error value
*/
int deleteCountryFromRepo(CountryRepo* repo, Country c);

/*
	This function modifies the country c from the repository to country newCountry. This is done by
	removing the old country and adding the new one.
	If successfull it returns 1, otherwise 0.
	Input:
		CountryRepo* repo
		Country c
	Output:
		int - error value ( 0 for fail or 1 for success ) 
*/
int modifyCountryFromRepo(CountryRepo* repo, Country c, Country newCountry);

/*
	This function clears the contents of the repository, keeping the capacity intact. This is done by performing
	delete operations.
	Input:
		CountryRepo* repo
	Output:
		none
*/
void clearCountryRepo(CountryRepo* repo);