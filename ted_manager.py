#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import os
import sys
import json
# import linkstate_sockcli

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
    # fork (Hierarchical SR-PCE)
    # ChildProcess: Call linkstate_sockcli

    # ParentProcess: Recode linkstate to TED
    ret = check_ted(linkstate, addr)
    if ret != 0:
        update_ted(linkstate, addr);
        print('[Link State] Update TED information from {}'.format(addr[0]), file=sys.stderr)

    return
