#include "CountryRepo.h"

CountryRepo * createCountryRepo()
{
	CountryRepo* repo = malloc(sizeof(CountryRepo));
	if (repo == NULL) // check if repo was created correctly
		return NULL;

	repo->countryVector = createDynamicVector(1); // default size is empty
	return repo;
}

void destroyCountryRepo(CountryRepo ** repo)
{
	if (repo == NULL) // if repo does not exist
		return; // exit

	DynamicVector* repoVector = (*repo)->countryVector;
	destroyDynamicVector(&repoVector); // free dynamic vector
	free(*repo);  // free memory allocated to repository object
	*repo = NULL; // safely put pointer in cupboard
}

int addCountryToRepo(CountryRepo * repo, Country c)
{
	if (repo == NULL) // if repo is invalid
		return -1; // -1 is the code for invalid repo

	// two countries with the same name will not be added, so we check first if
	// such a country does not already exist
	if (getRepoPosCountryByName(repo, getName(&c)) == 0)
		return 0; // 0 is the code for a country that already exists

	DynamicVector* repoVector = repo->countryVector;
	pushElementToVector(repoVector, c);
	return 1; // 1 is the code for correct insertion
}

int getLengthOfRepo(CountryRepo * repo)
{
	if (repo == NULL) // check if repo is valid
		return -1;

	DynamicVector* repoVector = repo->countryVector;
	return getLength(repoVector); // length of repo is length of dynamic vector
}

int getRepoPosCountryByName(CountryRepo * repo, char name[])
{
	if (repo == NULL)
		return -1;

	int i;
	for (i = 0; i < getLengthOfRepo(repo); ++i)
	{
		Country current = getCountryAtRepoIndex(repo, i);
		if (strcmp(getName(&current), name) == 0)
			return i;
	}
	return -1; // nothing found
}

Country getCountryAtRepoIndex(CountryRepo * repo, int index)
{
	if ((repo == NULL) || index < 0 || index > getLength(repo->countryVector))
		return createCountry("", None, 0);
	return getElementAtIndex(repo->countryVector, index);
}

int removeRepoCountryWithName(CountryRepo * repo, char name[])
{
	if (repo == NULL) // if repo address is invalid
		return -1;

	int position = getRepoPosCountryByName(repo, name);
	if (position == -1) // if no country was found 
		return 0; // return the code of nothing found, which is 0

	// from this point, a country has been found
	int newCapacity = getCapacity(repo->countryVector);
	int oldLength = getLength(repo->countryVector);
	if ( (oldLength < newCapacity - 1) && newCapacity > 0 ) // if capacity permits
		newCapacity--; // decrement because one element will be removed

	DynamicVector* newElements = createDynamicVector(newCapacity);
	int i;
	for (i = 0; i < oldLength; ++i) // add all but exclude index ("position")
		if ( i != position )
			pushElementToVector(newElements, getCountryAtRepoIndex(repo, i));

	DynamicVector* oldElements = repo->countryVector; // save pointer to current repo's vector
	repo->countryVector = newElements;

	destroyDynamicVector(&oldElements); // this is vital to avoid memory leaks

	return 1;
}

int updateRepoCountryAtIndex(CountryRepo * repo, int index, Country c)
{
	if (repo == NULL) // check if repo has an invalid address
		return -1;

	if (index < 0 || index > getLengthOfRepo(repo) - 1)
		return 0;

	// from this point, replacing is possible
	DynamicVector* newVector = createDynamicVector(getCapacity(repo->countryVector));
	int i, length = getLength(repo->countryVector);
	for (i = 0; i < length; ++i) // reconstruct identically, except for position index
		if (i == index) // on given position
			pushElementToVector(newVector, c); // add modified country
		else
			pushElementToVector(newVector, getCountryAtRepoIndex(repo, i)); // else add same country

	DynamicVector* oldElements = repo->countryVector; // save pointer to current repo's vector
	repo->countryVector = newVector;

	destroyDynamicVector(&oldElements); // this is vital to avoid memory leaks

	return 1;
}

DynamicVector * getCountriesContainingSubstring(CountryRepo * repo, char * subs)
{
	// the following three lines of code removes the trailing newline character if it exists
	char *pos;
	if ((pos = strchr(subs, '\n')) != NULL)
		*pos = '\0';

	// if substring is the empty string ""
	if (strcmp(subs, "") == 0)
	{
		DynamicVector* allCountries = createDynamicVector(getCapacity(repo->countryVector));
		int i, length = getLengthOfRepo(repo);
		if (length == 0)
		{
			destroyDynamicVector(&allCountries);
			return NULL;
		}
		for (i = 0; i < length; ++i)
			pushElementToVector(allCountries, getCountryAtRepoIndex(repo, i));
		return allCountries;
	}

	// first count occurences
	int occurences = 0;
	int i, length = getLengthOfRepo(repo);
	for (i = 0; i < length; ++i)
	{
		Country c = getCountryAtRepoIndex(repo, i);
		if (strstr(getName(&c), subs) != NULL)
			occurences++;
	}

	if (occurences == 0) // if nothing is found return NULL
		return NULL;

	DynamicVector* returnVector = createDynamicVector(occurences); // create vector with cap = occ
	for (i = 0; i < length; ++i)
	{
		Country c = getCountryAtRepoIndex(repo, i);
		if (strstr(getName(&c), subs) != NULL)
			pushElementToVector(returnVector, c); // add all valid countries
	}

	return returnVector; // return the address of the vector
}

DynamicVector * getCountriesByContinent(CountryRepo * repo, i_cont cont)
{
	if (cont == None)
		return NULL;

	int occurences = 0;
	int i, length = getLengthOfRepo(repo);
	for (i = 0; i < length; ++i)
	{
		Country c = getCountryAtRepoIndex(repo, i);
		if (getContinent(&c) == cont)
			occurences++;
	}

	if (occurences == 0)
		return NULL;

	DynamicVector* returnVector = createDynamicVector(occurences);
	for (i = 0; i < length; ++i)
	{
		Country c = getCountryAtRepoIndex(repo, i);
		if (getContinent(&c) == cont)
			pushElementToVector(returnVector, c);
	}

	return returnVector;
}

int getRepoCapacity(CountryRepo * repo)
{
	return repo->countryVector->capacity;
}

int deleteCountryFromRepo(CountryRepo * repo, Country c)
{
	int i, length = getLengthOfRepo(repo);
	int removeIndex = -1;

	// sweep DynamicVector for match
	for (i = 0; i < length; ++i)
	{
		Country current = getCountryAtRepoIndex(repo, i);

		// when found, stop and remember
		if (compareCountries(&current, &c) == 0)
		{
			removeIndex = i;
			break;
		}
	}

	// if match was found, reconstruct vector
	if (removeIndex == -1)
		return 0; // 0 is the error code for no match ( see specification ) 
	
	// no match will be found for a vector of length 0 so no need to check
	DynamicVector* newVector = createDynamicVector(getRepoCapacity(repo));
	
	for (i = 0; i < length; ++i)
	{
		if (i == removeIndex)
			continue;
		else
		{
			pushElementToVector(newVector, getElementAtIndex(repo->countryVector, i));
		}
	}
	
	free(repo->countryVector->elements);
	repo->countryVector->elements = malloc(sizeof(VElement) * repo->countryVector->capacity);
	memcpy(repo->countryVector->elements, newVector->elements, sizeof(VElement) * (length - 1));
	repo->countryVector->length--;

	destroyDynamicVector(&newVector);

	return 1;
}

int modifyCountryFromRepo(CountryRepo * repo, Country c, Country newCountry)
{
	int i, length = getLengthOfRepo(repo), countryIndex = -1;
	for (i = 0; i < length; ++i)
	{
		Country current = getCountryAtRepoIndex(repo, i);
		if (compareCountries(&c, &current) == 0)
		{
			countryIndex = i;
			break;
		}
	}

	if (countryIndex == -1)
		return 0;

	deleteCountryFromRepo(repo, c);
	addCountryToRepo(repo, newCountry);

	return 1;
}

void clearCountryRepo(CountryRepo * repo)
{
	int oldCapacity = getRepoCapacity(repo);
	destroyDynamicVector(&repo->countryVector);
	repo->countryVector = createDynamicVector(oldCapacity);
}

