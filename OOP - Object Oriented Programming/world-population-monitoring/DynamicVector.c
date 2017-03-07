#include "DynamicVector.h"
#include "DynamicVector.h"

DynamicVector * createDynamicVector(int capacity)
{
	if (capacity < 0) // capacity less than 0 makes no sense
		return NULL;
	// cast return value to pointer of type DynamicVector*
	DynamicVector* vect = (DynamicVector*)malloc(sizeof(DynamicVector));
	
	if (vect == NULL) // verify if object was created
		return NULL;

	// initialize members
	vect->capacity = capacity;
	vect->length = 0;

	// allocate space for members
	vect->elements = (VElement*)malloc(capacity * sizeof(VElement));
	if (vect->elements == NULL) // verify if memory was allocated
		return NULL;

	return vect;
}

void destroyDynamicVector(DynamicVector **vect)
{
	if (*vect == NULL) // verify if stuff can be destroyed
		return;

	// free memory where elements are allocated
	DynamicVector* delements = (*vect)->elements;
	free(delements);  // remove allocated elements
	(*vect)->elements = NULL; // carefully remove dangerous pointer

	free(*vect);  // destroy the object
	*vect = NULL; // carefully store the pointer in a safe place
}

void pushElementToVector(DynamicVector * vect, VElement elem)
{
	if (vect == NULL || vect->elements == NULL) // verify if vector is valid and has elements
		return;

	// adapt to new size requirements if necessary
	if (vect->length == vect->capacity)
		resizeVector(vect);

	// append to end of vector
	vect->elements[vect->length++] = elem;
}

void resizeVector(DynamicVector * vect)
{
	if (vect == NULL) // check if vector is valid
		return;

	// case when capacity is initially 0
	if (vect->capacity == 0)
	{
		vect->capacity = 1;
		vect->elements = (VElement*)realloc(vect->elements, vect->capacity * sizeof(VElement));
		return;
	}

	vect->capacity *= 2;
	vect->elements = (VElement*)realloc(vect->elements, vect->capacity * sizeof(VElement));
}

int getLength(DynamicVector * vect)
{
	if (vect == NULL)
		return -1;
	return vect->length;
}

int getCapacity(DynamicVector * vect)
{
	if (vect == NULL)
		return -1;
	return vect->capacity;
}

VElement getElementAtIndex(DynamicVector * vect, int index)
{
	// modify this if you use a different type
	createVElement createNewElement = createCountry;
	if (index > vect->length)
	{
		VElement newElement = createNewElement("", None, -1);
		return newElement;
	}

	return vect->elements[index];
}

void swapElementsInVector(DynamicVector * vect, int source, int dest)
{
	if (vect == NULL || vect->elements == NULL)
		return;
	int length = getLength(vect);
	if (source > length || dest > length)
		return;

	VElement s_aux = vect->elements[source];
	vect->elements[source] = vect->elements[dest];
	vect->elements[dest] = s_aux;
}

void sortElements(DynamicVector * vect, compareVElement compFunc, int order)
{
	if (vect == NULL)
		return;

	int i, j, length = getLength(vect);
	int done = 0;
	while (!done)
	{
		done = 1;
		for (i = 0; i < length - 1; ++i)
		{
			for (j = i + 1; j < length; ++j)
			{
				VElement e1 = getElementAtIndex(vect, i);
				VElement e2 = getElementAtIndex(vect, j);
				if (compFunc(&e1, &e2) == order)
				{
					swapElementsInVector(vect, i, j);
					done = 0;
				}
			}
		}
	}
}
