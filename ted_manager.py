#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import path_compute

DBPATH = './ted.sqlite'


def checkdb(linkstate, addr):
    '''check DB'''

    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    linkstate_pattern = 'SELECT * FROM ted WHERE ip = ' + \
        linkstate['addr'] + ' AND  router-id = ' + \
        linkstate['router-id'] + ' AND label = ' + linkstate['label']

    exist = cur.execute('SELECT * FROM ted WHERE EXISTS ip = ' + linkstate['addr'])
    rslt = cur.execute(linkstate_pattern)
    if exist == False:
        return -1
    else if rslt != '':
        return 0
    else:  # diffあり
        return 1


def insertdb(linkstate, addr):
    '''insert DB'''


def updatedb(linkstate, addr):
    '''update DB'''

    return


def pc_request(addr):
    '''request to path_compute'''
    path_compute.compute(addr)

    return


def manager(addr, linkstate):
    '''main of TED manager'''

    ret = checkdb(linkstate, addr)
    if ret != 0:
        if ret == -1:
            insertdb(linkstate, addr):
        else:
            updatedb(linkstate, addr):

        pc_request(addr):

    return
