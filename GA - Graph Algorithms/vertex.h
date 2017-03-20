//
// Created by p0licat on 3/20/17.
//

#ifndef GRAPHALGORITHMS_VERTEX_H
#define GRAPHALGORITHMS_VERTEX_H

template <typename T>
class Vertex
{
protected:
    T* value;

public:
    Vertex()
    {
        this->value = nullptr;
    }

    Vertex(const T& object)
    {
        this->value = new T(object);
    }

    Vertex(const Vertex& object)
    {
        this->value = object.get_value();
    }

    ~Vertex()
    {
        delete this->value;
        this->value = nullptr;
    }

    virtual void set_value(const T& value)
    {
        *this->value = value;
    }

    virtual T get_value() const
    {
        return *this->value;
    }

    virtual bool operator==(const Vertex<T>& other)
    {
        if ( this->value == other.get_value() )
            return true;
        return false;
    }

    virtual bool operator>(const Vertex<T>& other)
    {
        if ( this->value > other.get_value() )
            return true;
        return false;
    }

    virtual bool operator<(const Vertex<T>& other)
    {
        if ( this->value < other.get_value() )
            return true;
        return false;
    }

    virtual bool operator<=(const Vertex<T>& other)
    {
        if ( this->value <= other.get_value() )
            return true;
        return false;
    }

    virtual bool operator>=(const Vertex<T>& other)
    {
        if ( this->value >= other.get_value() )
            return true;
        return false;
    }
};


#endif //GRAPHALGORITHMS_VERTEX_H
