#pragma once

/*
	Made by: Bodica Septimiu

	This header contains the definition of the DynamicVector class. A DynamicVector is a generalized vector
	which can store any type of data. The tests found in test.h and test.c are also generalized, and this
	class can be made to work with any object by simply modifying a few typedefs below.

	For sorting, a typedef of the comparison function must be defined. The comparison function must return
	comp(a, b) must return -1 if a > b, 0 if a == b and 1 if a < b.

	Step 1: Include the header of the object that you want to store. Make sure there is a Constructor and
	a Destructor if necessary.

	Step 2:	view the typedefs in the first comment below this one. The first typedef specifies the object X
	that will be stored. The second typedef specifies the of this object X. If necessary, the third one
	specifies the destructor.

	Step 3: Modify the tests. The single line that should be modified at the moment is the one where
	a function pointer to the constructor is assigned.
*/

#include <stdlib.h>
#include "country.h"

/*
typedef X VElement;
typedef VElement (*createVElement)(params);
typedef void (*destroyVElement)(VElement);
typedef 
*/

typedef Country VElement; // this specifies the object which will be stored in a vector
						  // modify this line in order to create a vector for a custom type

typedef VElement (*createVElement)(char name[], Continent continent, int pop_m); // constructor of element

typedef int (*compareVElement)(VElement* v1, VElement* v2); // comparison function

/*
	Stores data dynamically. Read the definition of the constructor for more information.
	
	VElement* elements: is a dynamically allocated array of VElements, which are decided at the top of this header.
	int length: is the current number of elements that the vector stores. Initially it is 0.
	int capacity: maximum length of the vector, determined by the ammount of memory allocated to VElement* elements
*/
typedef struct {
	VElement* elements; // array of VElements
	int length;   // current length of the array
	int capacity; // maximum length of the array
} DynamicVector;

/*
	Constructor for a DynamicVector. Allocates memory for elements and initializes members.
	Capacity has to be at least 0. If it is 0, on the addition of the first element it is resized to 1.
	After each time the length reaches the capacity and a new element has to be added, its size doubles.
	For resizing, the function realloc() from stdlib is used. For building memory, malloc() is used.
	So the sizes should go: 0 -> 1 -> 2 -> 4 -> 8 ...

	Input: 
		int capacity   - the initial size of the vector, so that resizes can be avoided if possible
					     for optimization purposes. 
	Output:
		DynamicVector* - pointer to the constructed vector. This is ok, as the memory is allocated on heap
						 using malloc(). The pointer is actually to the return value of malloc()
*/
DynamicVector* createDynamicVector(int capacity);

/*
	Destructor for a DynamicVector. This function uses free() from stdlib in order to free memory from heap
	that was used during construction of object. USE THIS TO AVOID MEMORY LEAKS!
	In order to free memory correctly, TWO LEVELS OF INDIRECTION ARE USED! Please pass the ADDRESS OF A POINTER
	TO THE VECTOR, NOT the address of the vector.

	Input:
		DynamicVector** vect - address of a pointer to the vector
	Output:
		none ( void ) 
		*vect will point to NULL
*/
void destroyDynamicVector(DynamicVector **vect);

/*
	Operation which adds a DynamicElement ( VElement ) to the vector. This calls resize if necessary.
	Please read the documentation for resize().
	The length increases by one if the addition is successfull.

	Input: 
		DynamicVector* vect - pointer to the vector to which an element will be added
		VElement elem       - copy of the element to be added. 
	Output:
		none ( void ) 
*/
void pushElementToVector(DynamicVector* vect, VElement elem);

/*
	Doubles the size of the vector. This should be called when the length equals the capacity when trying
	to add an element.
	After each time the length reaches the capacity and a new element has to be added, its size doubles.
	For resizing, the function realloc() from stdlib is used. For building memory, malloc() is used.
	So the sizes should go: 0 -> 1 -> 2 -> 4 -> 8 ...

	Input: 
		DynamicVector* vect - pointer to the vector
	Output:
		none ( void ) 
		* capacity of the vector is twice as large ( capacity *= 2 )
*/
void resizeVector(DynamicVector* vect);

/*
	Getter for the length of the vector. Length is current ammount of VElements stored in memory.
	Input:
		DynamicVector* vect - pointer to DynamicVector
	Output:
		int - length of vector, which means number of elements stored
*/
int getLength(DynamicVector* vect);

/*
	Getter for the capacity of the vector, that is the number of elements that can be stored on currently
	allocated space in memory.

	Input:
		DynamicVector* vect - pointer to DynamicVector
	Output:
		int - capacity member of the vector
*/
int getCapacity(DynamicVector* vect);

/*
	Returns the element on position ( int index ). If the position is outside the vector, then
	it returns an "empty" VElement. This needs modifications whenever a different VElement is used,
	as there is no way to predict what an empty VElement is. MODIFY IF VElement IS NEW!

	A typedef to a constructEmpty() method could be defined.

	Input:
		DynamicVector* vect - pointer to DynamicVector
		int index - position of element to be returned
	Output:
		VElement ( copy of element found on position ) 
*/
VElement getElementAtIndex(DynamicVector* vect, int index);

/*
	Swaps two elements from the vector, if indexes are valid.

	Input: 
		DynamicVector* vect - pointer to DynamicVector
		int source - index one
		int dest   - index two
	Output:
		none ( void ) 
*/
void swapElementsInVector(DynamicVector* vect, int source, int dest);
/*
	This method sorts the elements of the DynamicVector using calls to the swap method and an implementation of
	bubble sort.
	The method requires a pointer to a comparison function, and an order. The order has to be -1 for descending
	and 1 for ascending.

	Input:
		DynamicVector* vect - pointer to vector
		compareVElement compFunc - pointer to comparison function
		int order - should be either -1 or 1 for ascending, or descending. Other values will keep it unsorted.
	Output:
		none ( void ) 
*/
void sortElements(DynamicVector* vect, compareVElement compFunc, int order);

