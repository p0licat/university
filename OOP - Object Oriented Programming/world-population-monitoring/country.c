#include "country.h"

Country createCountry(char name[], i_cont continent, int pop_m)
{
	Country country;

	// without adding 1 the \0 is omitted and everything fails massively
	strcpy_s(country.name, sizeof(char) * strlen(name) + 1, name); 
	country.continent = continent;
	country.pop_m = pop_m;
		
	return country;
}

char * getName(Country * c)
{
	return c->name;
}

char * continentToString(i_cont continent, char aux[])
{
	char c_Africa[]    = { "Africa"  };
	char c_America[]   = { "America" };
	char c_Australia[] = { "Australia" };
	char c_Europe[]    = { "Europe" };
	char c_Asia[]      = { "Asia" };
	char c_None[]	   = { "None" };

	switch (continent)
	{
		case Africa:
			strcpy_s(aux, sizeof(char) * strlen(c_Africa) + 1, c_Africa);
			return aux;
		case Asia:
			strcpy_s(aux, sizeof(char) * strlen(c_Asia) + 1, c_Asia);
			return aux;
		case America:
			strcpy_s(aux, sizeof(char) * strlen(c_America) + 1, c_America);
			return aux;
		case Europe:
			strcpy_s(aux, sizeof(char) * strlen(c_Europe) + 1, c_Europe);
			return aux;
		case Australia:
			strcpy_s(aux, sizeof(char) * strlen(c_Australia) + 1, c_Australia);
			return aux;
		default:
			strcpy_s(aux, sizeof(char) * strlen(c_None) + 1, c_None);
			return aux;
	}

	return NULL;
}

int getPopulation(Country * c)
{
	return c->pop_m;
}

i_cont getContinent(Country * c)
{
	return c->continent;
}

void toString(Country * c, char* out)
{
	char aux[COUNTRY_NAME_LENGTH];

	char* countryName = getName(c);
	i_cont countryContinent = getContinent(c);
	int countryPopulation = getPopulation(c);
	char* continentString = continentToString(countryContinent, aux);

	sprintf_s(out, sizeof(char) * MAXIMUM_PRINT_LENGTH, "Name: %s | Continent: %s | Population: %d\n", countryName, continentString, countryPopulation);
}

int compareCountries(Country * c1, Country * c2)
{
	if (c1 == NULL || c2 == NULL)
		return -2;

	int popC1 = getPopulation(c1);
	int popC2 = getPopulation(c2);

	if (popC1 > popC2)
		return -1;

	if ( popC1 == popC2 )
		return 0;

	if (popC1 < popC2)
		return 1;
	return -2;
}
