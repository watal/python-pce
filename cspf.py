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

    graph = []
#     for i in lsalist.keys():
#         for j in lsalist.keys():
#             if i != j:
#                 for k in lsalist[i]:
#                     if k in lsalist[j]:
#                         if i in graph:
#                             graph[i].append({j: list(k.values())[0]})
#                         else:
#                             graph[i] = [{j: list(k.values())[0]}]
#
    list_keys = []

    for i in lsalist.keys():
        list_keys.append(i)


    for i in range(len(list_keys)):
        for j in range(i + 1, len(list_keys)):
            if i != j:
                for k in lsalist[list_keys[i]]:
                    if k in lsalist[list_keys[j]]:
                        graph.append([list_keys[i],list_keys[j], list(k.values())[0]])

    return graph


def dijkstra(src, dst, graph):
#     shortest_path = ['192.168.0.2', '192.168.0.3', '192.168.0.4', '192.168.0.5']
    shortest_path = []



    return shortest_path


def isinclude(population, part):
    '''Determine elements are included population'''
    ptr = 0
    for i in part:
        if not i in population[ptr:]:
            return False

        ptr = population[ptr:].index(i) + 1

    return True


def create_segmentlist(src, via, graph):
    '''CSPF (create segmentlist)'''

    segmentlist = []
    for i in range(len(via)):
        path = dijkstra(src, via[i], graph)
        if not isinclude(path, via[i:]):
            segmentlist.append(via[i-1])
            segmentlist.append(
                create_segmentlist(via[i-1], via[i:], graph)
            )
            break

    segmentlist.append(via)
    return segmentlist


# def cspf(linkstate, src, dst, via):
def cspf():
    '''compute shortest path'''

    with open('dat/ted.json', 'r') as f:
        linkstate = json.load(f)
    src = '192.168.0.1'
    via = ['192.168.0.2', '192.168.0.3', '192.168.0.4', '192.168.0.5']

    lsalist = construct_lsalist(linkstate)
    graph = construct_graph(lsalist)
    segmentlist = create_segmentlist(src, via, graph)
    print(segmentlist)

#     return segmentlist
    return 0


if __name__ == '__main__':
    cspf()
