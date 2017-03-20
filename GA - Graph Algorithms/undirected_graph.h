//
// Created by p0licat on 3/21/17.
//

#ifndef GRAPHALGORITHMS_UNDIRECTED_GRAPH_H
#define GRAPHALGORITHMS_UNDIRECTED_GRAPH_H

#include "graph.h"
#include "vertex.h"

template <typename T>
class UndirectedMatrixGraph : MatrixGraph<T>
{
public:

    UndirectedMatrixGraph() : MatrixGraph<T>() {}
    UndirectedMatrixGraph(const unsigned long& size) : MatrixGraph<T>(size){}
    UndirectedMatrixGraph(const UndirectedMatrixGraph& object) : MatrixGraph<T>(object) {}

    virtual ~UndirectedMatrixGraph() {}

    virtual void add_edge(const int& src_v, const int& dst_v) override
    {
        this->adj[src_v][dst_v] = true;
    }

    virtual void remove_edge(const int& src_v, const int& dst_v) override
    {
        this->adj[src_v][dst_v] = false;
    }
};

#endif //GRAPHALGORITHMS_UNDIRECTED_GRAPH_H
