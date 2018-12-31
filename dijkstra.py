#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json


def construct_lsalist(linkstate):
    '''construct LSA list'''

    lsalist = {}
    for i in range(len(linkstate)):
        if linkstate[i].get('Opaque-Type') == 1:
            if linkstate[i].get('Router-Address') in lsalist:
                lsalist[linkstate[i].get('Router-Address')].append(
                    {linkstate[i].get('Link-ID'): linkstate[i].get('Maximum Bandwidth')})
            else:
                lsalist[linkstate[i].get(
                    'Router-Address')] = [{linkstate[i].get('Link-ID'):linkstate[i].get('Maximum Bandwidth')}]

    return lsalist


def construct_graph(lsalist):
    '''construct graph from linkstate'''

    graph = {}
    for i in lsalist.keys():
        for j in lsalist.keys():
            if j != i and lsalist.get(i)[0].keys() == lsalist.get(j)[0].keys():
                graph[i] = [j]

    return graph


def dijkstra():
    return

def main(source, dest):
    '''compute shortest path'''

    with open('dat/test.json', 'r') as f:
        linkstate = json.load(f)

    lsalist = construct_lsalist(linkstate)
    graph = construct_graph(lsalist)
    shortest_path = dijkstra(lsalist, source, dist)
    segmentlist = construct_segmentlist(shortest_path)

    return 0


if __name__ == '__main__':
    main()
