//
// Created by p0licat on 3/20/17.
//

#ifndef GRAPHALGORITHMS_GRAPH_H
#define GRAPHALGORITHMS_GRAPH_H

#include <vector>
#include "vertex.h"



template <typename T>
class MatrixGraph {

private:
    typedef std::vector<bool> VB;
    typedef std::vector<VB> mat_t;
    typedef std::vector<Vertex<T>> v_vector;

protected:
    mat_t adj;          // adjacency matrix
    v_vector vertices;  // vector of vertices

public:
    // constructors
    MatrixGraph()
    {
        this->adj.resize(0);
    }

    MatrixGraph(const int& size)
    {
        this->adj.resize(size);
        for (int i = 0; i < size; ++i)
            this->adj[i].resize(size);
    }

    MatrixGraph(const MatrixGraph& obj)
    {
        // TODO: optimize code : size(), :adj() {}
        this->adj = obj.get_adj();
    }

    // destructor
    ~MatrixGraph()
    {
        this->adj.clear();
    }

    // getters
    virtual mat_t get_adj() const
    {
        return this->adj;
    }

    virtual int get_size() const
    {
        return this->vertices.size();
    }

    // utility
    virtual bool vertex_exists(const int& vertex_number) const
    {
        if ( vertex_number > this->get_size() )
            return false;

        for (int i = 0; i < this->get_size(); ++i)
            if (this->adj[i][vertex_number] || this->adj[vertex_number][i] )
                return true;
        return false;
    }

    virtual bool adjacent(const int& src_v, const int& dst_v) const
    {
        if (this->adj[src_v][dst_v])
            return true;
        return false;
    }

    virtual std::vector<int> neighbors(const int& src_v) const
    {
        std::vector<int> result;
        for (int column = 0; column < this->get_size(); ++column)
            if (this->adj[src_v][column])
                result.push_back(column);
        return result;
    }

    virtual void add_edge(const int& src_v, const int& dst_v)
    {
        this->adj[src_v][dst_v] = true;
    }

    virtual void remove_edge(const int& src_v, const int& dst_v)
    {
        this->adj[src_v][dst_v] = false;
    }

    virtual T get_vertex_value(const int& vertex) const
    {
        return this->vertices[vertex].get_value();
    }

    virtual void set_vertex_value(const int& vertex, const T& value)
    {
        this->vertices[vertex].set_value(value);
    }

};

#endif //GRAPHALGORITHMS_GRAPH_H
