//
// Created by p0licat on 3/20/17.
//

#ifndef GRAPHALGORITHMS_DIRECTED_GRAPH_H
#define GRAPHALGORITHMS_DIRECTED_GRAPH_H

#include "graph.h"
#include "vertex.h"


template <typename T>
class DirectedMatrixGraph : MatrixGraph<T>
{
public:
    virtual ~DirectedMatrixGraph() override
    {

    }

    virtual void add_edge(const int& src_v, const int& dst_v) override
    {
        this->adj[src_v][dst_v] = true;
        this->adj[dst_v][src_v] = true;
    }

    virtual void remove_edge(const int& src_v, const int& dst_v) override
    {
        this->adj[src_v][dst_v] = false;
        this->adj[dst_v][src_v] = false;
    }
};

#endif //GRAPHALGORITHMS_DIRECTED_GRAPH_H
