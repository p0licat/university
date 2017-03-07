#include "Tests.h"
#include <cassert>

bool runTests()
{
	if (testDogObject() == false)
		return false;

	if (testDogRepo() == false)
		return false;

	if (testDogRepoController() == false)
		return false;

	return true;
}

bool testDogRepoController()
{
	DogRepo repo;
	DogObject dogC("Twitch", "Fai0thx", "twitch.tv", 3);
	DogObject dogD("Twitch", "Xxjordthebroxx", "twitch.tv", 3);

	repo.addDog(dogC);
	repo.addDog(dogD);
	repo.addDog(dogC);

	DogRepoController controller(repo);
	assert(!(controller.repoIsEmpty()));


	return true;
}

bool testDogRepo()
{
	DogRepo repo;
	DogObject dogC("Twitch", "Fai0thx", "twitch.tv", 3);
	DogObject dogD("Twitch", "Xxjordthebroxx", "twitch.tv", 3);

	repo.addDog(dogC);
	repo.addDog(dogD);
	repo.addDog(dogC);

	assert(repo.getNumberOfDogs() == 2);
	repo.removeDog(dogC);
	assert(repo.getNumberOfDogs() == 1);
	assert(repo[0] == dogD);
	assert(repo.dogExists(dogD));

	return true;
}

bool testDogObject()
{
	DogObject dogA("Twitch", "Twitchy", "twitch.tv", 3);
	DogObject dogA2("Twitch", "Twitchy", "twitch.tv", 3);
	DogObject dogB("Twitch", "Cypryss", "twitch.tv", 3);
	DogObject dogC("Twitch", "Fai0thx", "twitch.tv", 3);
	DogObject dogD("Twitch", "Xxjordthebroxx", "twitch.tv", -1);

	if (!(dogA == dogA2))
		return false;

	if (dogD.isValid()) // invalid dog, validity means positive age
		return false;

	std::string test = dogA.toString();
	assert(test == dogA.toString()); // check if returns string in a 
									// very strange and complicated
								   // and unnecessary way

	DogObject empty("", "", "", -1);
	assert(empty == DogObject()); // check default constructor

	return true;
}
