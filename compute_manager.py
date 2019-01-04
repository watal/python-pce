#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import yaml
from yaml import Loader, SafeLoader
import create_segmentlist


def get_linkstate():
    '''Linkstate from TED'''

    with open('dat/ted.json', 'r') as f:
        ted = json.load(f)

    linkstate = []
    # Get all LSA
    for i in ted.values():
        linkstate += i

    return linkstate


def get_policy(src, dst):
    '''Open Policy file'''

    with open('config/policy.yaml', 'r') as f:
        policies = yaml.load(f)

    # get constrain of src to dst
    constrain = policies[src][dst]
    if constrain == '':
        # If policy undefined, return void policy
        return {'via': [''], 'policy': {'bandwidth': 0, 'avoid_nodes': ['']}}
    else:
        return constrain

def create_sl_info(request, constrain, linkstate):
    '''Constrained Shortest Path First'''

    src = request[0]
    dst = request[1]
    via = constrain['via']
    policy = constrain['policy']
    # sl_info: List of src, dst, nexthop, segmentlist
    sl_info = create_segmentlist.create_sl(src, dst, via, policy, linkstate)
    print('[Segment list] Finished create sl_info')

    return sl_info


def manager(request):
    '''Manager of computing segmentlist'''

    print('[Segment list] Get Linkstate from TED')
    linkstate = get_linkstate()
    # constrain:  via_list and policy (QoS, Avoid_nodes)
    constrain  = get_policy(*request)
    # sl_info: List of src, dst, nexthop, segmentlist
    sl_info = create_sl_info(request, constrain, linkstate)

    return sl_info
