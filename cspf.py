#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json


def construct_lsalist(linkstate):
    '''construct LSA list'''

    lsalist = {}

    for i in range(len(linkstate)):
        if linkstate[i].get('Opaque-Type') == 1:
            # Get link information(ID, Bandwidth)
            if not linkstate[i].get('Router-Address') in lsalist:
                lsalist[linkstate[i].get('Router-Address')] = [0, {}]
            if not linkstate[i].get('Link-ID') in lsalist[linkstate[i].get('Router-Address')][1]:
                lsalist[linkstate[i].get('Router-Address')][1][linkstate[i].get('Link-ID')] = [0, 0, 0]

            lsalist[linkstate[i].get('Router-Address')][1][linkstate[i].get('Link-ID')][0] \
                = linkstate[i]['Local Interface IP Addresses'][0].get('0')
            lsalist[linkstate[i].get('Router-Address')][1][linkstate[i].get('Link-ID')][2] \
                = linkstate[i].get('Maximum Bandwidth')

        elif linkstate[i].get('Opaque-Type') == 4:
            # Get SRGB
            if not linkstate[i].get('Advertising Router') in lsalist:
                lsalist[linkstate[i].get('Advertising Router')] = [0, {}]
            lsalist[linkstate[i].get('Advertising Router')][0] \
                += linkstate[i].get('Segment Routing Range TLV')[1].get('SID Label')

        elif linkstate[i].get('Opaque-Type') == 7:
            # Get Node SID (Index)
            if not linkstate[i].get('Advertising Router') in lsalist:
                lsalist[linkstate[i].get('Advertising Router')] = [0, {}]
            lsalist[linkstate[i].get('Advertising Router')][0] \
                += linkstate[i].get('Prefix SID Sub-TLV')[4].get('Index')

    for i in range(len(linkstate)):
        if linkstate[i].get('Opaque-Type') == 8:
            # Get Adjacency SID
            for j in lsalist[linkstate[i].get('Advertising Router')][1].values():
                if linkstate[i].get('Extended Link TLV')[3].get('Link data') == j[0]:
                    if linkstate[i].get('Adj-SID Sub-TLV') is not None:
                        j[1] = linkstate[i].get('Adj-SID Sub-TLV')[4].get('Label')
                    else:
                        j[1] = linkstate[i].get('LAN-Adj-SID Sub-TLV')[5].get('Label')

    return lsalist


def construct_graph(lsalist):
    '''construct graph from linkstate'''

    graph = []
    list_keys = []

    for i in lsalist.keys():
        list_keys.append(i)

    print(lsalist)
    for i in range(len(list_keys)):
        for j in range(i + 1, len(list_keys)):
            print(list_keys[i], list_keys[j])
            for k in lsalist[list_keys[i]][1]:
                if k in lsalist[list_keys[j]][1]:
                    graph.append([list_keys[i], list_keys[j], k])

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


def cspf(src, dst, via, graph, policy):
    ''''''
    close_list = dijkstra(src, dst, graph)


def path_verification():
    pass


def hoge(src, via, graph):
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


# def create_segmentlist(linkstate, src, dst, via):
def create_segmentlist():
    '''create segmentlist'''

    '''debug'''
    with open('dat/ted.json', 'r') as f:
        linkstate = json.load(f)
    src = '192.168.0.1'
    via = ['192.168.0.2', '192.168.0.3', '192.168.0.4', '192.168.0.5']
    '''debug'''

    # Linkstate list from TED
    lsalist = construct_lsalist(linkstate)
    # Make graph for Dijkstra [nodeA, nodeB, cost, ...]
    graph = construct_graph(lsalist)
    print(graph)
#     segmentlist = create_segmentlist(src, via, graph)

#     return segmentlist
    return 0


if __name__ == '__main__':
    create_segmentlist()
