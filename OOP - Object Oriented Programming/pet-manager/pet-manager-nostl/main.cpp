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

	DogRepo dogRepo;

	// <repository> memory repository: adding 5 items
	//							Breed      Name     URL      Age
	dogRepo.addDog(DogObject("Schnauzer", "Schnazi", "www.com", 2));
	dogRepo.addDog(DogObject("Doberman", "Thor", "www.com", 3));
	dogRepo.addDog(DogObject("Golden_Retriever", "Cutu", "www.com", 2));
	dogRepo.addDog(DogObject("Akita_Inu", "Sasha", "www.com", 5));
	dogRepo.addDog(DogObject("Pointer_englez", "Smarty", "www.com", 1));
	// </repository>
	DogRepoController controller(dogRepo);
	UI ui(controller);

	ui.startUI();

	_CrtDumpMemoryLeaks();

    return 0;
}
