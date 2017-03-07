#include <stdio.h>
#include "test.h"
#include "country.h"
#include "DynamicVector.h"
#include "CountryRepo.h"
#include "UI.h"

int main()
{
	printf("Compilation successful!\n");
	testAll();
	
	CountryRepo* countryRepo = createCountryRepo();
	CountryRepoController controller = createCountryRepoController(countryRepo);
	UI* ui = createUI(&controller);

	startUI(ui);


	destroyUI(&ui);
	destroyCountryRepo(&countryRepo);
	_CrtDumpMemoryLeaks();
    return 0;
}
