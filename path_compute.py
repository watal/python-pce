#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import yaml
import cspf
import segmentlist_sockcli


def get_linkstate(src):
    '''Linkstate from TED'''

    with open('dat/ted.json', 'w') as f:
        ted = json.loads(f)

    return ted[src]


def get_policy(src):
    '''Open Policy file'''

    with open('config/policy.yaml', 'w') as f:
        policies = yaml.loads(f)

    return policies['src']


def create_sl_info(linkstate, src, policy):
    '''Constrained Shortest Path First'''

    sl_info = {}
    sl_info['from'] = src
    sl_info['to'], sl_info['via'] = policy[i]['to'], policy[i]['via']
    sl_info['segmnent_list'] = create_segmentlist(linkstate, src, policy[0], policy[1])
#     sl_info['segmnent_list'] = cspf.cspf(src, policy)

    return sl_info


def compute(src):
    '''computing cspf'''

    linkstate = get_linkstate(src)
    policies = get_policy(src)
    for policy range(len(policies)):
        sl_info = create_sl_info(linkstate, src, policy):
        segmentlist_sockcli.ssocket(src, sl_info)

    return
