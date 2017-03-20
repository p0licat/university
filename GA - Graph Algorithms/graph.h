//
// Created by p0licat on 3/20/17.
//

#ifndef GRAPHALGORITHMS_GRAPH_H
#define GRAPHALGORITHMS_GRAPH_H

#include "vertex.h"

#include <vector>

/*
 * MatrixGraph interface for Graph abstract data type.
 * DirectedMatrixGraph and UndirectedMatrixGraph inherit this interface.
 *
 * This class family uses an STL vector matrix for storing the adjacency matrix. ( as seen in the typedefs )
 * For the list of vertices, a vector<Vertex<T>> is used.
 *
 * This is a template class. The type T will specify the type that the value of the vertices will be.
 * Example: MatrixGraph<int> is a graph where every vertex has an integer value.
 */
template <typename T>
class MatrixGraph {

private:
    /*
     * mat_t is a matrix type ( std::vector<std::vector<bool>> )
     * v_vector is a vertex vector ( std::vector<Vertex<T>> )
     */
    typedef std::vector<bool> VB;
    typedef std::vector<VB> mat_t;
    typedef std::vector<Vertex<T>> v_vector;

protected:
    mat_t adj;          // adjacency matrix
    v_vector vertices;  // vector of vertices

public:
    // Default Constructor
    MatrixGraph()
    {
        this->adj.resize(0);
        this->vertices.resize(0);
    }

    // Constructor with size
    // @param: size ( const int& ) - number of vertices
    MatrixGraph(const unsigned long& size)
    {
        this->adj.resize(size);
        this->vertices.resize(size);
        for (unsigned long i = 0; i < size; ++i)
            this->adj[i].resize(size);
    }

    // Copy Constructor
    MatrixGraph(const MatrixGraph& obj) : adj(obj.get_adj()), vertices(obj.get_vertices())
    {
    }

    // Purely Virtual Destructor ( this is an interface )
    virtual ~MatrixGraph() = 0; // purely virtual destructor


    // getter for adjacency matrix
    virtual mat_t get_adj() const
    {
        return this->adj;
    }

    // getter for number of vertices
    virtual unsigned long get_size() const
    {
        return this->vertices.size();
    }

    // getter for vertex list
    virtual std::vector<Vertex<T>> get_vertices() const
    {
        return this->vertices;
    }

    // check if vertex with a certain value exists
    virtual bool vertex_exists(const T& value) const
    {
        for (auto it = this->vertices.begin(); it != this->vertices.end(); ++it)
            if ( it->get_value() == value )
                return true;
        return false;
    }

    // check if vertex exists
    virtual bool vertex_exists(const Vertex<T>& vertex) const
    {
        for (auto it = this->vertices.begin(); it != this->vertices.end(); ++it)
            if ( it->get_value() == vertex.get_value() )
                return true;
        return false;
    }

    // gets the position of a vertex in the vertex array
    virtual int get_vertex_key(const Vertex<T>& vertex) const
    {
        for (auto it = this->vertices.begin(); it != this->vertices.end(); ++it)
            if ( *it == vertex )
                return it - this->vertices.begin();
        return -1;
    }

    // check if two vertices are adjacent
    virtual bool adjacent(const int& src_v, const int& dst_v) const
    {
        if (this->adj[src_v][dst_v])
            return true;
        return false;
    }

    // return a vector of the neighbours of vertex src_v
    virtual std::vector<Vertex<T>> neighbors(const Vertex<T>& src_v) const
    {
        int pos = get_vertex_key(src_v);
        std::vector<Vertex<T>> result;
        for (int column = 0; column < this->get_size(); ++column)
            if (this->adj[pos][column])
                result.push_back(column);
        return result;
    }

    virtual void add_edge(const int& src_v, const int& dst_v) = 0;
    virtual void remove_edge(const int& src_v, const int& dst_v) = 0;


    virtual T get_vertex_value(const int& vertex) const
    {
        return this->vertices[vertex].get_value();
    }

    virtual void set_vertex_value(const int& vertex, const T& value)
    {
        this->vertices[vertex].set_value(value);
    }

    virtual void add_vertex(const Vertex<T>& vertex)
    {
        for (auto it = this->vertices.begin(); it != this->vertices.end(); ++it)
            if ( it->get_value() == T() )
                it->set_value(vertex.get_value());
    }


    virtual void remove_vertex(const Vertex<T>& vertex)
    {
        typename std::vector<Vertex<T>>::iterator it;
        for (it = this->vertices.begin(); it != this->vertices.end(); ++it)
            if ( *it == vertex )
                this->vertices.erase(it);
    }
};

template <typename T>
inline MatrixGraph<T>::~MatrixGraph() {}

#endif //GRAPHALGORITHMS_GRAPH_H
