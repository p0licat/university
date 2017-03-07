#include "test.h"

void testAll()
{
	int country_t = testCountry();
	int dvector_t = testDynamicVector();
	int ctrrepo_t = testCountryRepo();

	// perform a logical AND ( && ) over all return values of the test functions
	// in order to verify all tests
	if (country_t && dvector_t && testCountryRepo)
		printf_s("All tests passed!\n");
	else
		printf_s("Some tests failed!\n");

	//check for memory leaks
	_CrtDumpMemoryLeaks();
}

int testCountry()
{
	// create country
	Country country_t = createCountry("Romania", Europe, 21);

	// check for valid creation of object
	// and verify that getters work correctly
	if (strcmp(getName(&country_t), "Romania") != 0 ||
		getContinent(&country_t) != Europe ||
		getPopulation(&country_t) != 21) {
		return 0;
	}

	// check continentToString() function 
	char cont_aux[CONTINENT_NAME_LENGTH];
	if ( strcmp(continentToString(getContinent(&country_t), cont_aux), "Europe") != 0 ) // if str1 != str2
		return 0;

	// test toString function 
	char stringOfCountry[MAXIMUM_PRINT_LENGTH];
	toString(&country_t, stringOfCountry);
	if ( strcmp(stringOfCountry, "Name: Romania | Continent: Europe | Population: 21\n") != 0 ) // if str1 != str2
		return 0;

	return 1;
}

int testDynamicVector()
{
	DynamicVector *vector_z = createDynamicVector(0);  // zero
	DynamicVector *vector_o = createDynamicVector(1);  // one
	DynamicVector *vector_m = createDynamicVector(30); // many

	// check if vectors were created
	if (vector_z == NULL || vector_o == NULL || vector_m == NULL)
		return 0;

	// test if all lengths are 0 at the moment of creation
	if (getLength(vector_z) != 0 || getLength(vector_o) != 0 || getLength(vector_m) != 0 )
		return 0;

	// test if all capacities are valid
	if (getCapacity(vector_z) != 0 || getCapacity(vector_o) != 1 || getCapacity(vector_m) != 30)
		return 0;


	/*
		<test insert>
		// TODO: replace with pointer to velement constructing function
	*/
	// for test generalization we use function pointers
	createVElement createElement = &createCountry; // modify this line if you use other elements for the
												   // dynamic vector, give a pointer to your constructor

	VElement element_o = createElement("Romania", Europe, 21); // create element 
	pushElementToVector(vector_z, element_o); // append element to vector

	// check if length has changed
	if (getLength(vector_z) != 1)
		return 0;

	VElement in_elem = getElementAtIndex(vector_z, 0); // get element from vector
	// we will compare the elements by the results of the toString() function
	char out[MAXIMUM_PRINT_LENGTH];
	toString(&in_elem, out); // result is stored in 'out'

	char comp[MAXIMUM_PRINT_LENGTH];
	toString(&element_o, comp);

	if (strcmp(out, comp) != 0) // if strings are not equal then elements are not inserted correctly
		return 0;

	if (getCapacity(vector_z) != getLength(vector_z)) // capacity and length should be equal now ( 1/1 ) 
		return 0;

	pushElementToVector(vector_z, in_elem); // pushing second element, capacity should be 2 and length 2
	if (getCapacity(vector_z) != getLength(vector_z)) // capacity and length should still be equal ( 2/2 )
		return 0;

	in_elem.continent = Asia; // prepare for swap test
	pushElementToVector(vector_z, in_elem); // pushing third element, capacity should be 4 and length 3
	if (getCapacity(vector_z) != 4 || getLength(vector_z) != 3) // capacity and length should be (4, 3)
		return 0;

	swapElementsInVector(vector_z, 2, 0); // swap elements 0 and 2
	memset(out, 0, strlen(out));   // clear contents of strings
	memset(comp, 0, strlen(comp)); // clear contents of strings
	VElement swap_a = getElementAtIndex(vector_z, 0); // store element 0 in swap_a
	VElement swap_b = getElementAtIndex(vector_z, 2); // store element 2 in swap_b
	toString(&swap_a, out); // store string of element 0 in out
	toString(&swap_b, comp);// store string of element 1 in comp

	// TODO: problem
	if (strcmp(out, comp) == 0) // they must be different
		return 0;

	if (swap_a.continent == Europe) // it must be asia
		return 0;
	/*
		</test insert>
	*/
	// test sort
	DynamicVector* testSort = createDynamicVector(10);
	pushElementToVector(testSort, createCountry("Pal", Europe, 31));
	pushElementToVector(testSort, createCountry("Pale", Europe, 32));
	pushElementToVector(testSort, createCountry("Palest", Europe, 34));
	pushElementToVector(testSort, createCountry("Palestina", Europe, 99));
	sortElements(testSort, compareCountries, 1);
	assert(getElementAtIndex(testSort, 0).pop_m == 99);
	sortElements(testSort, compareCountries, -1);
	assert(getElementAtIndex(testSort, 0).pop_m == 31);
	
	destroyDynamicVector(&testSort);

	// test destructor
	destroyDynamicVector(&vector_z); 
	destroyDynamicVector(&vector_o); 
	destroyDynamicVector(&vector_m); 

	if (vector_z != NULL || vector_o != NULL || vector_m != NULL)
		return 0;

	// test resize
	DynamicVector* vector_resizer = createDynamicVector(0);
	pushElementToVector(vector_resizer, createCountry("a", Asia, 13));
	pushElementToVector(vector_resizer, createCountry("b", Asia, 13));
	pushElementToVector(vector_resizer, createCountry("c", Asia, 13));
	pushElementToVector(vector_resizer, createCountry("d", Asia, 13));
	pushElementToVector(vector_resizer, createCountry("e", Asia, 13));
	assert(vector_resizer->length == 5);
	return 1;
}

int testCountryRepo()
{
	CountryRepo* repo = createCountryRepo(); // create repo
	Country c = createCountry("Romania", Europe, 21); // create two different countries
	Country d = createCountry("Hungary", Europe, 69); // create two different countries
	addCountryToRepo(repo, c); // add one country: length = 1 and capacity = 1

	assert(getLengthOfRepo(repo) == 1); // check if country was added
	assert(addCountryToRepo(repo, d) == 1); // check if you can add a different country
	assert(getLengthOfRepo(repo) == 2); // check if length was incremented
	assert(addCountryToRepo(repo, c) == 0); // check if it is NOT possible to add the same country ( 0 )
	assert(removeRepoCountryWithName(NULL, "") == -1); // cannot remove from nothing
	assert(removeRepoCountryWithName(repo, "") == 0);  // cannot remove something that does not exist
	assert(removeRepoCountryWithName(repo, "Hungary") == 1); // can remove something
	assert(getLengthOfRepo(repo) == 1); // length decremented

	Country indexZero = getCountryAtRepoIndex(repo, 0);
	assert(strcmp(getName(&indexZero), "Romania") == 0); // check if index 0 is romania

	assert(updateRepoCountryAtIndex(repo, 0, d) == 1); // modified "Romania" to "Hungary" and pop_m from 21 to 69
	assert(getLengthOfRepo(repo) == 1); // length remains the same

	Country checkName = getCountryAtRepoIndex(repo, 0); // get country at position 0 ( d ) 
	assert(strcmp(getName(&checkName), "Hungary") == 0);// see if "Romania" is now "Hungary"

	// test continent filter
	DynamicVector* contSearch = getCountriesByContinent(repo, Europe); // test getByContinent
	assert(getLength(contSearch) == 1);

	// test string filter
	contSearch = getCountriesContainingSubstring(repo, "gary"); // test getBySubstring
	assert(getLength(contSearch) == 1);
	contSearch = getCountriesContainingSubstring(repo, "gari");
	assert(contSearch == NULL); // test fail conditions
	contSearch = getCountriesByContinent(repo, None); 
	assert(contSearch == NULL); // test fail conditions

	destroyCountryRepo(&repo);
	destroyDynamicVector(&contSearch);

	return 1;
}
