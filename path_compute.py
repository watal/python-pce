#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import json
import pce_segmentlist.py


def cspf():
    '''Constrained Shortest Path First'''
    with open('segment_lists.json') as f:
        segment_lists = json.load(f)

    return segment_lists


def compute(addr):
    '''computing cspf'''


        pce_segmentlist.ssocket(addr, segment_lists)

    return