#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import pathcompute_manager

PATH = 'dat/ted.json' 

def check_ted(linkstate, addr):
    '''check TED'''

    if os.path.exists(PATH):
        with open(PATH, 'r') as f:
            ted = json.load(f)

        if linkstate == ted[addr[0]]:
            return 0

    return -1


def update_ted(linkstate, addr):
    '''update TED'''

    with open(PATH, 'w') as f:
        json.dump({addr[0]: linkstate}, f)

    return


def manager(addr, linkstate):
    '''main of TED manager'''
    ret = check_ted(linkstate, addr)
    if ret != 0:
        update_ted(linkstate, addr);
        pathcompute_manager.manager(addr[0])

    return
