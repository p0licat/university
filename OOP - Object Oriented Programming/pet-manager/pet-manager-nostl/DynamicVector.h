#pragma once

/*
	DynamicVector template class. This is a Vector data structure implemented in C++ with templates. All elements are dynamically allocated.
	It has a size property, and a capacity property.
		size - the current number of elements
		capacity - the maximum number of elements until resize

	It is very similar to the STL std::vector class. 
	This implementation begins with the capacity of 10, and doubles that capacity every time the vector's size reaches its capacity.
	The resize factor ( 2 by default ) can be changed.

	Elements can be indexed, since the [] indexing operator is overloaded, however no iterators are implemented.
*/

template <typename T>
class DynamicVector {
private:	
	T* elements;
	int size;
	int capacity;
public:
	// constructor 
	DynamicVector(int capacity = 10);
	// copy constructor
	DynamicVector(const DynamicVector& v); 
	// destructor
	~DynamicVector();

	void addElement(T element);
	void removeElement(int position);
	int getSize() { return this->size; }

	//operators
	T& operator[](int pos);
	DynamicVector& operator=(const DynamicVector<T>& v);
	bool operator==(const DynamicVector<T>& v);
private:
	void resize(double factor = 2);
};

template<typename T>
inline void DynamicVector<T>::removeElement(int position)
{
	for (int i = position; i < size - 1; ++i)
		elements[i] = elements[i + 1];
	this->size--;
}

template<typename T>
inline DynamicVector<T>::DynamicVector(int capacity = 10)
{
	this->capacity = capacity;
	this->size = 0;
	this->elements = new T[capacity];
}

template<typename T>
inline DynamicVector<T>::DynamicVector(const DynamicVector & v)
{
	this->size = v.size;
	this->capacity = v.capacity;
	this->elements = new T[this->capacity];
	for (int i = 0; i < this->size; ++i)
		this->elements[i] = v.elements[i];
}

template<typename T>
inline DynamicVector<T>::~DynamicVector()
{
	delete[] this->elements;
}

/*
	Adds an element of type T to the vector. The initial capacity is 10, if the size reaches its capacity then it will have to perform 
	a call to the resize() method first.
	Input:
		T element - template
	Output:
		none
*/
template<typename T>
inline void DynamicVector<T>::addElement(T element)
{
	if (this->size == this->capacity)
		this->resize();
	this->elements[this->size++] = element;
}

/*
	Resize method for the DynamicVector, automatically called when size is equal to capacity, hence it is a private method.
	Input:
		(double ) resize_factor - the number by which the vector's capacity will increase.
	Output:
		none
*/
template <typename T>
inline void DynamicVector<T>::resize(double factor)
{
	this->capacity *= (int)factor; // increase capacity
	T* elems = new T[this->capacity]; // create a new array of elements of type T, called [elems], [elems] != this->elements
	
	// copy everything already allocated into the new array of elements
	for (int i = 0; i < this->size; ++i)
		elems[i] = this->elements[i];

	// delete the current array of elements of size this->capacity/factor
	delete[] this->elements;

	// assign newly allocated array to the elements pointer
	this->elements = elems;
}

/*
	Assignment operator overload. 
*/
template<typename T>
DynamicVector<T>& DynamicVector<T>::operator=(const DynamicVector<T>& v)
{
	if (this == &v)
		return *this;

	this->size = v.size;
	this->capacity = v.capacity;

	delete[] this->elements;
	this->elements = new T[this->capacity];
	for (int i = 0; i < this->size; ++i)
		this->elements[i] = v.elements[i];
	return *this;
}

/*
	Comparison operator overload. Checks if two vectors are equal.
	Input: ( vectorA == vectorB )
	Output: true/false
*/
template<typename T>
inline bool DynamicVector<T>::operator==(const DynamicVector<T>& v)
{
	if (this == &v)
		return true;

	if (this->capacity != v.capacity)
		return false;
	if (this->size != v.size)
		return false;

	for (int i = 0; i < this->size; ++i)
		if (v.elements[i] != this->elements[i])
			return false;

	return true;
}

/*
	Indexing operator. Returns the element in the array at position "pos".
	Input:
		int pos - position of the desired element
	Output:
		this->elements[pos]
	Errors:
		Will throw exception if trying to index something outside the array.
*/
template <typename T>
T& DynamicVector<T>::operator[](int pos)
{
	return this->elements[pos];
}
