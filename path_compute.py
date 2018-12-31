#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import json
import segmentlist_sockcli


def cspf(addr):
    '''Constrained Shortest Path First'''

    with open('segment_lists.json') as f:
        segment_lists = json.load(f)

    return segment_lists

def get_ted():


def compute(addr):
    '''computing cspf'''

    linkstate = get_ted()
    policy = get_policy(addr)
    segment_lists = cspf(addr)
    segmentlist_sockcli.ssocket(addr, segment_lists)

    return
