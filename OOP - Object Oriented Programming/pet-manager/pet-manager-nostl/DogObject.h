#pragma once

#include <string>

/*
	Main object used by the application. A dog must have: name, breed, photoUrl, age, and is initialized in that order.
*/
class DogObject {
private:
	std::string breed;
	std::string name;
	std::string photoUrl;
	int age;
public:
	// constructors
	DogObject() : breed(""), name(""), photoUrl(""), age(-1) {}
	DogObject(std::string breed, std::string name, std::string photoUrl, int age) :
				    breed(breed), name(name), photoUrl(photoUrl), age(age) {}
	
	// copy constructor
	DogObject(const DogObject& dog) 
	{
		this->breed = dog.breed;
		this->name = dog.name;
		this->photoUrl = dog.photoUrl;
		this->age = dog.age;
	}

	// destructor
	~DogObject() {}

	// getters 
	std::string getBreed() { return this->breed; }
	std::string getName() { return this->name; }
	std::string getPhotoUrl() {return this->photoUrl;}
	int getAge() {return this->age;}

	// utility functions
	bool isValid()
	{
		if (this->age == -1)
			return false;
		return true;
	}
	
	/*
		toString() returns a formatted std::string containing the information inside a DogObject, for easy printing.
		Input:
			none
		Output:
			std::string
	*/
	std::string toString()
	{
		std::string rval = "";
		rval += "Breed: "; rval += this->breed; rval += " | ";
		rval += "Name: ";  rval += this->name;  rval += " | ";
		rval += "Url: ";   rval += this->photoUrl; rval += " | ";
		rval += "Age: ";   rval += std::to_string(this->age); rval += '\n';
		return rval;
	}

	/*
		Overloaded comparison operator, two DogObjects are equal only if all fields are identical.
	*/
	bool operator==(const DogObject& dog)
	{
		if (this->age == dog.age && this->name == dog.name && this->breed == dog.breed && this->photoUrl == dog.photoUrl)
			return true;
		return false;
	}
};