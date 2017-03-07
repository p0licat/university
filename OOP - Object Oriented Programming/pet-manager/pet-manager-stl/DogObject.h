#pragma once

#include <string>
#include <fstream>
#include <iostream>

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
		Used to output CSV compatible string from a DogObject.
	*/
	std::string toFileString()
	{
		std::string rval = "";
		rval += this->breed; rval += ";";
		rval += this->name; rval += ";";
		rval += this->photoUrl; rval += ";";
		rval += std::to_string(this->age); rval += "\n";

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

	/*
		Static member, returns a DogObject from a CSV string.
	*/
	static DogObject fromString(std::string input)
	{
		int counter = 0; // start at 0 commas, read until 3 ( 4 fields, 3 commas, 0,     1 ,      2   ,    3)
						//														 breed 	 name	  url     age

		std::string breed = "";
		std::string name = "";
		std::string url = "";
		int age = 0;

		for (auto i : input)
		{
			if (i == ';') // separator
			{
				counter++;  // move to next field
				continue;
			}

			if (counter == 0)
				breed += i;
			if (counter == 1)
				name += i;
			if (counter == 2)
				url += i;
			if (counter == 3)
			{
				age *= 10;
				age += i - '0';
			}

		}

		DogObject rval(name, breed, url, age);
		return rval;
	}

	/*
		Used for reading form the console, overloaded operator>>
	*/
	friend std::istream& operator>>(std::istream &input, DogObject& dog)
	{
		std::string breed;
		std::string name;
		std::string url;
		std::string ageString;
		int age;
			
		std::cout << "Please insert breed: ";
		input >> breed;
		std::cout << "Please insert name: ";
		input >> name;
		std::cout << "Please insert URL: ";
		input >> url;
		std::cout << "Please insert age: ";
		input >> ageString;

		age = atoi(ageString.c_str());
		
		DogObject newDog(breed, name, url, age);
		dog = newDog;

		return input;
	}

	/*
		Used for outputting to both console and files.
	*/
	friend std::ostream& operator<<(std::ostream &output, DogObject dog)
	{
		output << dog.toFileString();
		return output;
	}
};