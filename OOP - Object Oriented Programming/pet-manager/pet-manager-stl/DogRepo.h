#pragma once

#include "DogObject.h"
#include "DynamicVector.h" // this version uses STL vector
#include <fstream>
#include <vector>
#include <string>

/*
	DogRepo is a repository that manages a list of DogObjects with an already existing implementation of a DynamicVector ( view DynamicVector.h )
*/
class DogRepo {
private:
	std::vector<DogObject> dogs;
	std::string filename;
public:
	DogRepo();
	DogRepo(std::string filename);
	DogRepo(std::vector<DogObject>& v);
	~DogRepo();

	void addDog(DogObject d);
	void removeDog(const DogObject& dog); // removes identical match with parameter from repository
	DogObject& operator[](int index);
	std::vector<DogObject>& getAllDogs();
	bool dogExists(const DogObject& dog);
	int getNumberOfDogs();
	void writeToFile();
	bool hasFileName();
	void addFile(std::string filename);
	std::string getTextFile();
	void readFromFile(std::string filename);
};

/*
	Dumps all repo entries in a text file, CSV format.
*/
inline void DogRepo::writeToFile()
{
	if (!this->hasFileName())
		return;

	std::ofstream fout(this->filename.c_str());

	for (auto dog : this->dogs)
	{
		fout << dog.toFileString();
	}

	fout.close();
}

/*
	Checks if a file is associated with the repo, to check if any output and input can be performed from that file.
*/
inline bool DogRepo::hasFileName()
{
	if (this->filename == "")
		return false;
	return true;
}


/*
	If the constructor receives a filename it also populates the repository with the entries from that file, if it is valid.
	Input: std::string filename 
	Output: none
*/
inline DogRepo::DogRepo(std::string filename)
{
	this->filename = filename;

	std::string line;
	std::ifstream fin(filename.c_str());

	while (std::getline(fin, line))
	{
		this->addDog(DogObject::fromString(line));
	}


	fin.close();
}

/*
	Associates a file with the repo, in case it was not initialized with a filename. This makes the repo read everything automatically.
*/
inline void DogRepo::addFile(std::string filename)
{
	this->filename = filename;

	std::string line;
	std::ifstream fin(filename.c_str());

	while (std::getline(fin, line))
	{
		this->addDog(DogObject::fromString(line));
	}


	fin.close();
}

/*
	Returns a string containing the filename associated with the repo.
*/
inline std::string DogRepo::getTextFile()
{
	return this->filename;
}


/*
	Clears all repo contents and reads file again.
*/
inline void DogRepo::readFromFile(std::string filename = "")
{
	if (filename == "")
		filename = this->filename;

	this->dogs.clear();
	std::string line;
	std::ifstream fin(filename.c_str());

	while (std::getline(fin, line))
	{
		this->addDog(DogObject::fromString(line));
	}


	fin.close();
}
/*
	Getter for the number of DogObjects stored in the DynamicVector represented internally.
	Input:
		none
	Output:
		(int) numberOfDogs
*/
inline int DogRepo::getNumberOfDogs()
{
	return this->dogs.size();
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
	for (auto i : dogs)
		if (i == dog)
			return true;
	return false;
}

/*
	Constructor, declaration necessary because of overloaded constructor.
*/
inline DogRepo::DogRepo()
{
	this->filename = "";
}

/*
	This constructor takes a DynamicVector of DogObjects and copies it into the newly created repository.
*/
inline DogRepo::DogRepo(std::vector<DogObject>& v)
{
	this->dogs = v;
}

/*
	Destructor necessary only when using files, as a trigger to write to file before destructing.
*/
inline DogRepo::~DogRepo()
{
	if (this->filename != "")
		this->writeToFile();
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
	this->dogs.push_back(d);
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
	int length = this->dogs.size();
	int foundPosition = -1;
	for (auto i : dogs)
	{
		if (i == dog)
		{
			auto it = std::find(std::begin(dogs), std::end(dogs), i);
			foundPosition = std::distance(it, dogs.begin());
			break;
		}
	}

	if (foundPosition == -1)
		return;

	std::vector<DogObject>::iterator it = this->dogs.begin() + foundPosition;

	this->dogs.erase(it);
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
inline std::vector<DogObject>& DogRepo::getAllDogs()
{
	return this->dogs;
}
