#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import math
from collections import defaultdict
from heapq import *


def construct_lsalist(linkstate):
    '''construct LSA list'''

    lsalist = {}

    for i in range(len(linkstate)):
        if linkstate[i].get('Opaque-Type') == 4:
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

        elif linkstate[i].get('Opaque-Type') == 8:
            # Get Adjacency SID
            if not linkstate[i].get('Advertising Router') in lsalist:
                lsalist[linkstate[i].get('Advertising Router')] = [0, {}]
            if not linkstate[i].get('Extended Link TLV')[2].get('Link ID') in lsalist[linkstate[i].get('Advertising Router')][1]:
                lsalist[linkstate[i].get('Advertising Router')][1][linkstate[i].get(
                    'Extended Link TLV')[2].get('Link ID')] = [0, 0, 0]

            lsalist[linkstate[i].get('Advertising Router')][1][linkstate[i].get('Extended Link TLV')[2].get('Link ID')][0]\
                = linkstate[i].get('Extended Link TLV')[3].get('Link data')

            if linkstate[i].get('Adj-SID Sub-TLV') is not None:
                lsalist[linkstate[i].get('Advertising Router')][1][linkstate[i].get('Extended Link TLV')[2].get('Link ID')][1]\
                    = linkstate[i].get('Adj-SID Sub-TLV')[4].get('Label')
            else:
                lsalist[linkstate[i].get('Advertising Router')][1][linkstate[i].get('Extended Link TLV')[2].get('Link ID')][1]\
                    = linkstate[i].get('LAN-Adj-SID Sub-TLV')[5].get('Label')

    for i in range(len(linkstate)):
        if linkstate[i].get('Opaque-Type') == 1:
            # Get link information(ID, Bandwidth)
            for j in lsalist[linkstate[i].get('Advertising Router')][1].values():
                if linkstate[i].get('Local Interface IP Addresses')[0].get('0') == [j][0][0]:
                    [j][0][2] = linkstate[i].get(
                        'Maximum Reservable Bandwidth')

    return lsalist


def construct_graph(lsalist):
    '''construct graph from linkstate'''

    graph = []
    list_keys = []

    for i in lsalist.keys():
        list_keys.append(i)

    for i in range(len(list_keys)):
        for j in range(i + 1, len(list_keys)):
            for k in lsalist[list_keys[i]][1]:
                if k in lsalist[list_keys[j]][1]:
                    graph.append([list_keys[i], list_keys[j],
                                  lsalist[list_keys[i]][1].get(k)[2]])

    return graph


def with_info_graph(graph):
    for i in range(len(graph)):
        graph[i].insert(2, math.ceil(1000000 / graph[i][2]))
    return graph


def cspf_dijkstra(src, dst, graph, policy):
    '''CSPF (constrained dijkstra algorithm)'''

    directed_graph = defaultdict(list)

    # create directed graph
    for i in range(len(graph)):
        # BW constrain and avoid node
        if graph[i][3] >= policy['bandwidth'] and set([graph[i][0], graph[i][1]]) & set(policy['avoid_nodes']) == set():
            directed_graph[graph[i][0]].append((graph[i][2], graph[i][1]))

    # queue, closedlist
    q, seen = [(0, src, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            # clean output
            if v1 == dst:
                stack=[]
                while len(path) > 1:
                    stack.insert(0, path[0])
                    path = path[1]
                return (stack)

            for c, v2 in directed_graph.get(v1, ()):
                if v2 in seen:
                    continue
                next = cost + c
                heappush(q, (next, v2, path))
    # if unreachable
    return 'inf'


def dijkstra(src, dst, graph):
    '''general dijkstra algorithm'''
    directed_graph = defaultdict(list)
    # create directed graph
    for i in range(len(graph)):
        directed_graph[graph[i][0]].append((graph[i][2], graph[i][1]))

    # queue, closedlist
    q, seen = [(0, src, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            # clean output to stack
            if v1 == dst:
                stack=[]
                while len(path) > 1:
                    stack.insert(0, path[0])
                    path = path[1]
                return (stack)

            for c, v2 in directed_graph.get(v1, ()):
                if v2 in seen:
                    continue
                next = cost + c
                heappush(q, (next, v2, path))
    # if unreachable
    return 'inf'


def retour(src, dst, info_graph, constrained_path, lsalist):

    retour_list = []

    for i in range(len(constrained_path)):
        # 宛先よりiノード前までが最短経路かを調べる
        if constrained_path[:i] == dijkstra(src, constrained_path[j], info_graph):
            # 最短が見つかったらそこまでのNode SIDをappend
            segmentlist.append(lsalist[retour_path[:i]])
            # 中間ノードから先が最短経路と一致しないなら
            if constrained_path[:i] != dijkstra(src, constrained_path[j], info_graph):
                # 中間ノードをsrcに変えてもう一度検索
                segmentlist.append(retour(constrained_path[i], dst, info_graph. constrained_path[i:]))

            else:
                # dstまでが最短経路ならそのNodeを加えて終了
                segmentlist.append(lsalist[constrained_path[i]][0])
                return retour_list

    # 一個前でも最短経路でないならば，そこへのAdj SIDをsegmentlistにappend
    segmentlist.append(lsalist[src][2][constrained_path[1]])
    # 隣接ノードがdstでないならば
    if constrained_path[1] != dst:
        # 一つ先からもう一度検索
        segmentlist.append(retour(constrained_path[i], dst, info_graph. constrained_path[1:], lsalist))

    return retour_list

def path_verification(src, via, info_graph, policy, lsalist):
    '''convert CSPF path to segmentlist'''

    segmentlist = []
    nexthop = ''

    # パスを経由ごとに分解し経路計算
    for i in range(len(via)):
        # 制約付き，制約なしを計算し比較
        constrained_path = cspf_dijkstra(src, via[i], info_graph, policy)
        if constrained_path == 'inf':
            return None, 'Unreachable'

        # next hopを記録
        if i == 0:
            # Convert nexthop to nextaddress，あとで直す
            for j in lsalist[constrained_path[1]][1].keys():
                if lsalist[constrained_path[1]][1][j][0] in lsalist[constrained_path[0]][1]:
                    nexthop = lsalist[constrained_path[1]][1][j][0]

        shortest_path = dijkstra(src, via[i], info_graph)

        # 制約付き最短経路が最短経路と異なる場合はNode SIDで直接指定不可
        if constrained_path != shortest_path:
            # 迂回路のセグメントリストを構築し追記
            segmentlist.append(retour(src, via[i], info_graph, constrained_path, lsalist))
        else:
            # 直接Node SIDを追加
            segmentlist.append(lsalist[via[i]][0])

    # convert segmentlist format [16000, 16001] to '16000/16001'
    segmentlist_stack = ''
    for i in range(len(segmentlist)):
        segmentlist_stack += str(segmentlist[i])
        if i+1 != len(segmentlist):
            segmentlist_stack += '/'

    return nexthop, segmentlist_stack


def create_sl(src, dst, via, policy, linkstate):
    '''create segmentlist'''

    # Linkstate list from TED
    lsalist = construct_lsalist(linkstate)
    # Make graph for Dijkstra [nodeA, nodeB, cost, ...]
    graph = construct_graph(lsalist)
    # Add information in graph
    info_graph = with_info_graph(graph)
    # Make segmentlist
    print('src: {}\nvia: {}\ninfo_graph: {}\npolicy: {}'.format(src, via, info_graph, policy))
    nexthop, segmentlist_stack = path_verification(src, via, info_graph, policy, lsalist)

#     print('Router Info: {}\n'.format(lsalist))
    print('Topology: {}'.format(graph))
    print('Policy:')
    print('\tQoS (Minimum BandWidth): {}'.format(policy['bandwidth']))
    print('\tAvoid Node: {}'.format(policy['avoid_nodes']))
    print('Src: {}'.format(src))
    print('Dst: {}'.format(dst))
    print('Via: {}\n'.format(via))
    print('-> Next Hop P2P Addr: {}'.format(nexthop))
    print('   Segment List: {}'.format(segmentlist_stack))


    sl_info = {'src':src ,'dst':dst ,'nexthop': nexthop,'segmentlist': segmentlist_stack}
    return (sl_info)


if __name__ == '__main__':
    create_sl('192.168.0.1', '192.168.0.4', ['192.168.0.2', '192.168.0.3', '192.168.0.4'], {'bandwidth': 0, 'avoid_nodes': ['']}, [{'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.3', 'Local Interface IP Addresses': [{'0': '172.16.0.6'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 1, 'LS age': 1527, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 6, 'Checksum': 17324, 'Link State ID': '1.0.0.1', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.3', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.4', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.2', 'Local Interface IP Addresses': [{'0': '172.16.0.2'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 2, 'LS age': 1535, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 6, 'Checksum': 9428, 'Link State ID': '1.0.0.2', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.2', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.0', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.3', 'Local Interface IP Addresses': [{'0': '172.16.0.10'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 2, 'LS age': 1537, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 6, 'Checksum': 19100, 'Link State ID': '1.0.0.2', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.3', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.8', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.4', 'Local Interface IP Addresses': [{'0': '172.16.0.14'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 2, 'LS age': 1484, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 6, 'Checksum': 24445, 'Link State ID': '1.0.0.2', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.4', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.12', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.1', 'Local Interface IP Addresses': [{'0': '172.16.0.1'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 3, 'LS age': 1511, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 1, 'Checksum': 61195, 'Link State ID': '1.0.0.3', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.1', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.0', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.2', 'Local Interface IP Addresses': [{'0': '172.16.0.9'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 3, 'LS age': 1525, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 6, 'Checksum': 21140, 'Link State ID': '1.0.0.3', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.2', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.10', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.3', 'Local Interface IP Addresses': [{'0': '172.16.0.13'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 3, 'LS age': 1477, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 6, 'Checksum': 11187, 'Link State ID': '1.0.0.3', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.3', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.12', 'LS Type': 'Area-Local Opaque-LSA'}, {'Traffic Engineering Metric': 0, 'LS Seq Number': 2147483652, 'Router-Address': '192.168.0.1', 'Local Interface IP Addresses': [{'0': '172.16.0.5'}], 'Maximum Bandwidth': 1250000.0, 'Opaque-ID': 4, 'LS age': 1481, 'Opaque-Type': 1, 'Maximum Reservable Bandwidth': 1250000.0, 'Options': 66, 'Link': '84 octets of data', 'Local Interface IP Address': 1, 'LS Flags': 1, 'Checksum': 63226, 'Link State ID': '1.0.0.4', 'Length': 116, 'Opaque-Info': '96 octets of data', 'Advertising Router': '192.168.0.1', 'Link-Type': 'Multiaccess', 'Unreserved Bandwidth per Class Type in Byte/s': [{'0': 1250000.0}, {'1': 1250000.0}, {'2': 1250000.0}, {'3': 1250000.0}, {'4': 1250000.0}, {'5': 1250000.0}, {'6': 1250000.0}, {'7': 1250000.0}], 'Link-ID': '172.16.0.4', 'LS Type': 'Area-Local Opaque-LSA'}, {'Segment Routing MSD TLV': [{'Node Maximum Stack Depth': 10}], 'Segment Routing Algorithm TLV': [{'Algorithm 0': 'SPF'}], 'LS age': 1541, 'Opaque-Type': 4, 'Advertising Router': '192.168.0.1', 'LS Seq Number': 2147483652, 'Checksum': 46351, 'LS Type': 'Area-Local Opaque-LSA', 'Link State ID': '4.0.0.0', 'Router Capabilities': 268435456, 'Segment Routing Range TLV': [{'Range Size': 4000}, {'SID Label': 16000}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 0, 'LS Flags': 1, 'Options': 66}, {'Segment Routing MSD TLV': [{'Node Maximum Stack Depth': 10}], 'Segment Routing Algorithm TLV': [{'Algorithm 0': 'SPF'}], 'LS age': 1495, 'Opaque-Type': 4, 'Advertising Router': '192.168.0.2', 'LS Seq Number': 2147483652, 'Checksum': 44820, 'LS Type': 'Area-Local Opaque-LSA', 'Link State ID': '4.0.0.0', 'Router Capabilities': 268435456, 'Segment Routing Range TLV': [{'Range Size': 4000}, {'SID Label': 16000}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 0, 'LS Flags': 6, 'Options': 66}, {'Segment Routing MSD TLV': [{'Node Maximum Stack Depth': 10}], 'Segment Routing Algorithm TLV': [{'Algorithm 0': 'SPF'}], 'LS age': 1497, 'Opaque-Type': 4, 'Advertising Router': '192.168.0.3', 'LS Seq Number': 2147483652, 'Checksum': 43289, 'LS Type': 'Area-Local Opaque-LSA', 'Link State ID': '4.0.0.0', 'Router Capabilities': 268435456, 'Segment Routing Range TLV': [{'Range Size': 4000}, {'SID Label': 16000}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 0, 'LS Flags': 6, 'Options': 66}, {'Segment Routing MSD TLV': [{'Node Maximum Stack Depth': 10}], 'Segment Routing Algorithm TLV': [{'Algorithm 0': 'SPF'}], 'LS age': 1474, 'Opaque-Type': 4, 'Advertising Router': '192.168.0.4', 'LS Seq Number': 2147483652, 'Checksum': 41758, 'LS Type': 'Area-Local Opaque-LSA', 'Link State ID': '4.0.0.0', 'Router Capabilities': 268435456, 'Segment Routing Range TLV': [{'Range Size': 4000}, {'SID Label': 16000}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 0, 'LS Flags': 6, 'Options': 66}, {'LS age': 1561, 'Opaque-Type': 7, 'Advertising Router': '192.168.0.1', 'LS Seq Number': 2147483652, 'Checksum': 63404, 'Link State ID': '7.0.0.1', 'LS Type': 'Area-Local Opaque-LSA', 'Prefix SID Sub-TLV': [{'Length': 8}, {'Algorithm': 0}, {'Flags': 0}, {'MT-ID': 0}, {'Index': 1}], 'Length': 44, 'Opaque-Info': '24 octets of data', 'Extended Prefix TLV': [{'Length': 20}, {'Route Type': 1}, {'Address Family': 0}, {'Flags': 64}, {'Address': '192.168.0.1/32'}], 'Opaque-ID': 1, 'LS Flags': 1, 'Options': 66}, {'LS age': 1535, 'Opaque-Type': 7, 'Advertising Router': '192.168.0.2', 'LS Seq Number': 2147483652, 'Checksum': 6791, 'Link State ID': '7.0.0.1', 'LS Type': 'Area-Local Opaque-LSA', 'Prefix SID Sub-TLV': [{'Length': 8}, {'Algorithm': 0}, {'Flags': 0}, {'MT-ID': 0}, {'Index': 2}], 'Length': 44, 'Opaque-Info': '24 octets of data', 'Extended Prefix TLV': [{'Length': 20}, {'Route Type': 1}, {'Address Family': 0}, {'Flags': 64}, {'Address': '192.168.0.2/32'}], 'Opaque-ID': 1, 'LS Flags': 6, 'Options': 66}, {'LS age': 1477, 'Opaque-Type': 7, 'Advertising Router': '192.168.0.3', 'LS Seq Number': 2147483652, 'Checksum': 15458, 'Link State ID': '7.0.0.1', 'LS Type': 'Area-Local Opaque-LSA', 'Prefix SID Sub-TLV': [{'Length': 8}, {'Algorithm': 0}, {'Flags': 0}, {'MT-ID': 0}, {'Index': 3}], 'Length': 44, 'Opaque-Info': '24 octets of data', 'Extended Prefix TLV': [{'Length': 20}, {'Route Type': 1}, {'Address Family': 0}, {'Flags': 64}, {'Address': '192.168.0.3/32'}], 'Opaque-ID': 1, 'LS Flags': 6, 'Options': 66}, {'LS age': 1554, 'Opaque-Type': 7, 'Advertising Router': '192.168.0.4', 'LS Seq Number': 2147483652, 'Checksum': 24125, 'Link State ID': '7.0.0.1', 'LS Type': 'Area-Local Opaque-LSA', 'Prefix SID Sub-TLV': [{'Length': 8}, {'Algorithm': 0}, {'Flags': 0}, {'MT-ID': 0}, {'Index': 4}], 'Length': 44, 'Opaque-Info': '24 octets of data', 'Extended Prefix TLV': [{'Length': 20}, {'Route Type': 1}, {'Address Family': 0}, {'Flags': 64}, {'Address': '192.168.0.4/32'}], 'Opaque-ID': 1, 'LS Flags': 6, 'Options': 66}, {'LS age': 1474, 'Opaque-Type': 8, 'LAN-Adj-SID Sub-TLV': [{'Length': 11}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Neighbor ID': '192.168.0.3'}, {'Label': 50001}], 'Advertising Router': '192.168.0.4', 'LS Seq Number': 2147483652, 'Checksum': 23284, 'Extended Link TLV': [{'Length': 44}, {'Link Type': 2}, {'Link ID': '172.16.0.14'}, {'Link data': '172.16.0.14'}], 'Link State ID': '8.0.0.2', 'LS Type': 'Area-Local Opaque-LSA', 'Length': 68, 'Opaque-Info': '48 octets of data', 'Opaque-ID': 2, 'LS Flags': 6, 'Options': 66}, {'LS age': 1521, 'Opaque-Type': 8, 'Advertising Router': '192.168.0.1', 'LS Seq Number': 2147483652, 'Checksum': 48543, 'Extended Link TLV': [{'Length': 36}, {'Link Type': 2}, {'Link ID': '172.16.0.2'}, {'Link data': '172.16.0.1'}], 'Link State ID': '8.0.0.3', 'LS Type': 'Area-Local Opaque-LSA', 'Adj-SID Sub-TLV': [{'Length': 7}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Label': 50001}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 3, 'LS Flags': 1, 'Options': 66}, {'LS age': 1545, 'Opaque-Type': 8, 'LAN-Adj-SID Sub-TLV': [{'Length': 11}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Neighbor ID': '192.168.0.1'}, {'Label': 50001}], 'Advertising Router': '192.168.0.2', 'LS Seq Number': 2147483652, 'Checksum': 16938, 'Extended Link TLV': [{'Length': 44}, {'Link Type': 2}, {'Link ID': '172.16.0.2'}, {'Link data': '172.16.0.2'}], 'Link State ID': '8.0.0.3', 'LS Type': 'Area-Local Opaque-LSA', 'Length': 68, 'Opaque-Info': '48 octets of data', 'Opaque-ID': 3, 'LS Flags': 6, 'Options': 66}, {'LS age': 1511, 'Opaque-Type': 8, 'Advertising Router': '192.168.0.1', 'LS Seq Number': 2147483652, 'Checksum': 46744, 'Extended Link TLV': [{'Length': 36}, {'Link Type': 2}, {'Link ID': '172.16.0.6'}, {'Link data': '172.16.0.5'}], 'Link State ID': '8.0.0.5', 'LS Type': 'Area-Local Opaque-LSA', 'Adj-SID Sub-TLV': [{'Length': 7}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Label': 50003}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 5, 'LS Flags': 1, 'Options': 66}, {'LS age': 1537, 'Opaque-Type': 8, 'LAN-Adj-SID Sub-TLV': [{'Length': 11}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Neighbor ID': '192.168.0.1'}, {'Label': 50001}], 'Advertising Router': '192.168.0.3', 'LS Seq Number': 2147483652, 'Checksum': 32988, 'Extended Link TLV': [{'Length': 44}, {'Link Type': 2}, {'Link ID': '172.16.0.6'}, {'Link data': '172.16.0.6'}], 'Link State ID': '8.0.0.9', 'LS Type': 'Area-Local Opaque-LSA', 'Length': 68, 'Opaque-Info': '48 octets of data', 'Opaque-ID': 9, 'LS Flags': 6, 'Options': 66}, {'LS age': 1527, 'Opaque-Type': 8, 'LAN-Adj-SID Sub-TLV': [{'Length': 11}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Neighbor ID': '192.168.0.2'}, {'Label': 50005}], 'Advertising Router': '192.168.0.3', 'LS Seq Number': 2147483652, 'Checksum': 33478, 'Extended Link TLV': [{'Length': 44}, {'Link Type': 2}, {'Link ID': '172.16.0.10'}, {'Link data': '172.16.0.10'}], 'Link State ID': '8.0.0.11', 'LS Type': 'Area-Local Opaque-LSA', 'Length': 68, 'Opaque-Info': '48 octets of data', 'Opaque-ID': 11, 'LS Flags': 6, 'Options': 66}, {'LS age': 1527, 'Opaque-Type': 8, 'Advertising Router': '192.168.0.3', 'LS Seq Number': 2147483652, 'Checksum': 26064, 'Extended Link TLV': [{'Length': 36}, {'Link Type': 2}, {'Link ID': '172.16.0.14'}, {'Link data': '172.16.0.13'}], 'Link State ID': '8.0.0.12', 'LS Type': 'Area-Local Opaque-LSA', 'Adj-SID Sub-TLV': [{'Length': 7}, {'Flags': 96}, {'MT-ID': 0}, {'Weight': 0}, {'Label': 50003}], 'Length': 60, 'Opaque-Info': '40 octets of data', 'Opaque-ID': 12, 'LS Flags': 6, 'Options': 66}])
('192.168.0.1', '192.168.0.2', [['192.168.0.2', '192.168.0.1', 1.0, 1250000.0], ['192.168.0.3', '192.168.0.1', 1.0, 1250000.0], ['192.168.0.3', '192.168.0.4', 1.0, 1250000.0]], {'bandwidth': 0, 'avoid_nodes': ['']})
