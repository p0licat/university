// entry point for the program

#include "UI.h"
#include "DogRepoController.h"
#include "DogRepo.h"
#include "DogObject.h"
#include "Tests.h"

#include <crtdbg.h>

int main()
{
	if (!runTests())
		std::cout << "Warning!!! Some tests failed! \n";


	// this is the repo that stores all of the DogObjects in the shelter
	DogRepo dogRepo("database.csv");

	// dogRepo is passed to the controller
	DogRepoController controller(dogRepo);
	UI ui(controller); // controller is passed to the UI

	
	ui.startUI();

	_CrtDumpMemoryLeaks();

	return 0;
}
