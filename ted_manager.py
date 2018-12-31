#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import path_compute

DBPATH = './ted.sqlite'


def checkdb(lsdb, addr):
    '''check DB'''

    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    lsdb_pattern = 'SELECT * FROM ted WHERE ip = ' + \
        lsdb['addr'] + ' AND  router-id = ' + \
        lsdb['router-id'] + ' AND label = ' + lsdb['label']

    exist = cur.execute('SELECT * FROM ted WHERE EXISTS ip = ' + lsdb['addr'])
    rslt = cur.execute(lsdb_pattern)
    if exist == False:
        return -1
    else if rslt != '':
        return 0
    else:  # diffあり
        return 1


def insertdb(lsdb, addr):
    '''insert DB'''


def updatedb(lsdb, addr):
    '''update DB'''

    return


def pc_request(addr):
    '''request to path_compute'''
    path_compute.compute(addr)

    return


def manager(addr, lsdb):
    '''main of TED manager'''

    ret = checkdb(lsdb, addr)
    if ret != 0:
        if ret == -1:
            # DB作成
            insertdb(lsdb, addr):
        else:
            # DB更新
            updatedb(lsdb, addr):

                # 計算要求
        pc_request(addr):

    return
