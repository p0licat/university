#pragma once

#include "DogObject.h"
#include "DynamicVector.h"

/*
	DogRepo is a repository that manages a list of DogObjects with an already existing implementation of a DynamicVector ( view DynamicVector.h )
*/
class DogRepo {
private:
	DynamicVector<DogObject> dogs;
public:
	DogRepo();
	DogRepo(DynamicVector<DogObject>& v);
	~DogRepo();

	void addDog(DogObject d);
	void removeDog(const DogObject& dog); // removes identical match with parameter from repository
	DogObject& operator[](int index);
	DynamicVector<DogObject>& getAllDogs();
	bool dogExists(const DogObject& dog);
	int getNumberOfDogs();
};

/*
	Getter for the number of DogObjects stored in the DynamicVector represented internally.
	Input:
		none
	Output:
		(int) numberOfDogs
*/
inline int DogRepo::getNumberOfDogs()
{
	return this->dogs.getSize();
}

/*
	For a given DogObject parameter, this method checks if that DogObject already exists in the DynamicVector.
	Input:
		DogObject - dog to look for
	Output:
		true - it already exists
		false - it does not already exist
*/
inline bool DogRepo::dogExists(const DogObject& dog)
{
	int length = this->dogs.getSize();
	for (int i = 0; i < length; ++i)
	{
		if (this->dogs[i] == dog)
			return true;
	}
	return false;
}

/*
	Constructor, declaration necessary because of overloaded constructor.
*/
inline DogRepo::DogRepo()
{

}

/*
	This constructor takes a DynamicVector of DogObjects and copies it into the newly created repository.
*/
inline DogRepo::DogRepo(DynamicVector<DogObject>& v)
{
	this->dogs = v;
}

/*
	Destructor not necessary.
*/
inline DogRepo::~DogRepo()
{
}

/*
	The addition of elements is managed by the DynamicVector template class. This method simply calls the addElement method of the 
	DynamicVector.
	Input:
		DogObject - object to add
	Output:
		none
*/
inline void DogRepo::addDog(DogObject d)
{
	if (this->dogExists(d))
		return;
	this->dogs.addElement(d);
}

/*
	This method attempts to remove the matching DogObject received as a parameter from the repository.
	Since this application does not require it, no return value has been specified, so to check if a DogObject
	has indeed been removed you must veify it before using this method.
	Input:
		DogObject
	Ouptut:
		none ( for both success and failure ) 
*/
inline void DogRepo::removeDog(const DogObject & dog)
{
	int length = this->dogs.getSize();
	int foundPosition = -1;
	for (int i = 0; i < length; ++i)
	{
		if (this->dogs[i] == dog)
		{
			foundPosition = i;
			break;
		}
	}

	if (foundPosition == -1)
		return;

	this->dogs.removeElement(foundPosition);
}

/*
	Indexing operator overload.
*/
inline DogObject& DogRepo::operator[](int index)
{
	return this->dogs[index];
}

/*
	Getter for the list of DogObjects. 
	Input:
		none
	Output:
		DynamicVector<DogObject>
*/
inline DynamicVector<DogObject>& DogRepo::getAllDogs()
{
	return this->dogs;
}
