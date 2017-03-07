#pragma once

#include "DogObject.h"
#include "DogRepo.h"

/*
	This is a controller for the DogRepo repository, since the UI must not call methods of the repository dirrectly this serves as 
	an interface between the UI and the DogRepo.
*/
class DogRepoController {
private:
	DogRepo& repo; // reference to an already existing DogRepo
public:

	// constructor & destructor
	DogRepoController(DogRepo& repo) : repo(repo) {} 
	~DogRepoController();
	
	// utility methods
	std::vector<DogObject> &getAllDogs();
	void addDogToRepo(DogObject dog);
	void removeDogFromRepo(const DogObject& dog);
	bool dogExists(const DogObject& dog);
	bool repoIsEmpty();
	bool repoHasTextFile();
	int getNumberOfDogs() { return this->repo.getNumberOfDogs(); }
	std::string getTextFile();
};

/*
	Evaluate if the Repo has no dogs.
	Input:
		none
	Output:
		true - there are some dogs in the repository
		false - repository is empty
*/
inline bool DogRepoController::repoIsEmpty()
{
	if (this->repo.getNumberOfDogs() == 0)
		return true;
	return false;
}

/*
	Checks if repository has a text file associated.
*/
inline bool DogRepoController::repoHasTextFile()
{
	if (this->repo.hasFileName())
		return true;
	return false;
}

/*
	Obtain the text file name as a string from the repository.
*/
inline std::string DogRepoController::getTextFile()
{
	return this->repo.getTextFile();
}

/*
	No need for destructor! Do not attempt to destruct the DogRepo reference!
*/
inline DogRepoController::~DogRepoController()
{
}

/*
	Getter for the DogObjects inside the repo. Returned as a DynamicVector.
	Input:
		none
	Output:
		DynamicVector<DogObject>
*/
inline std::vector<DogObject>& DogRepoController::getAllDogs()
{
	return this->repo.getAllDogs();
}

/*
	Adds a dog to the repository.
	Input:
		DogObject dog - dog to add
	Output:
		none ( both for success and failure )
*/
inline void DogRepoController::addDogToRepo(DogObject dog)
{
	this->repo.addDog(dog);
	return;
}

/*
	Remove DogObject that matches parameter, if it exists in the repository.
	Input:
		DogObject - dog to remove
	Output:
		none
*/
inline void DogRepoController::removeDogFromRepo(const DogObject & dog)
{
	if (!this->repo.dogExists(dog))
		return;
	this->repo.removeDog(dog);
}

/*
	Check if DogObject dog exists within the repository.
*/
inline bool DogRepoController::dogExists(const DogObject & dog)
{
	if (this->repo.dogExists(dog))
		return true;
	return false;
}
