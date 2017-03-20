//
// Created by p0licat on 3/20/17.
//

#ifndef GRAPHALGORITHMS_VERTEX_H
#define GRAPHALGORITHMS_VERTEX_H

template <typename T>
class Vertex
{
protected:
    T value;

public:
    Vertex() : value() {}

    Vertex(const T& object)
    {
        this->value = object;
    }

    Vertex(const Vertex<T>& object)
    {
        this->value = object.get_value();
    }

    ~Vertex() = default;

    virtual void set_value(const T& value)
    {
        this->value = value;
    }

    virtual T get_value() const
    {
        return this->value;
    }

    virtual bool operator==(const Vertex<T>& other) const
    {
        return this->value == other.value;
    }

    virtual bool operator>(const Vertex<T>& other) const
    {
        return this->value > other.get_value();
    }

    virtual bool operator<(const Vertex<T>& other) const
    {
        return this->value < other.get_value();
    }

    virtual bool operator<=(const Vertex<T>& other) const
    {
        return this->value <= other.get_value();
    }

    virtual bool operator>=(const Vertex<T>& other) const
    {
        return this->value >= other.get_value();
    }
};


#endif //GRAPHALGORITHMS_VERTEX_H
