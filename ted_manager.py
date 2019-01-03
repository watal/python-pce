#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pathcompute_manager


def check_ted(linkstate, addr):
    '''check TED'''

    with open('dat/ted.json', 'w') as f:
        ted = json.loads(f)

    if linkstate == ted:
        return 0
    else:
        return -1


def update_ted(linkstate, addr):
    '''update TED'''

    with open('dat/ted.json', 'w') as f:
        json.dumps(linkstate, f)

    return


def manager(addr, linkstate):
    '''main of TED manager'''

    ret = check_ted(linkstate, addr)
    if ret != 0:
        update_ted(linkstate, ted);
        pathcompute_manager.manager(addr)

    return
