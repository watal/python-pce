#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import yaml
import create_segmentlist
import segmentlist_sockcli


def get_linkstate(src):
    '''Linkstate from TED'''

    with open('dat/ted.json', 'w') as f:
        ted = json.loads(f)

    return ted[src]


def get_policy(src):
    '''Open Policy file'''

    with open('config/policy.yaml', 'w') as f:
        policies = yaml.load(f)

    return policies['src']


def create_sl_info(src, policy_info, linkstate):
    '''Constrained Shortest Path First'''

    dst = policy_info['dst']
    via = policy_info['via']
    policy = policy_info['policy']
    sl_info = create_segmentlist(src, dst, via, policy, linkstate)

    return sl_info


def manager(src):
    '''manage computing segmentlist'''

    linkstate = get_linkstate(src)
    policies = get_policy(src)
    for policy_info in range(len(policies)):
        # list of src, dst, nexthop, segmentlist
        sl_info = create_sl_info(src, policy_info, linkstate)
        # Can't create policy-based path
        if sl_info['segmentlist'] == 'Unreachable':
            return -1
        segmentlist_sockcli.ssocket(sl_info)

    return
