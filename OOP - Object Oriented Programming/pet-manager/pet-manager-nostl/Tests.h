#pragma once

/*
	This contains the tests for the vital methods inside this application.
*/

#include "DogObject.h"
#include "DogRepo.h"
#include "DogRepoController.h"

bool runTests(); // this function runs all of the tests for each individual header file.
bool testDogObject(); // test for DogObject.h
bool testDogRepo(); // test for DogRepo.h
bool testDogRepoController(); // test for DogRepoController.h
