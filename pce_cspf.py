#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json


def cspf():
    '''computing cspf'''
    with open('segment_lists.json') as f:
        segment_lists = json.load(f)

    return segment_lists
