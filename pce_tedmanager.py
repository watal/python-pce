#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3

DBPATH = './ted.sqlite'


def checkdb(lsdb, ip):
    '''check DB'''

    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    lsdb_pattern = 'SELECT * FROM ted WHERE ip = ' + \
        lsdb['ip'] + ' AND  router-id = ' + \
        lsdb['router-id'] + ' AND label = ' + lsdb['label']

    exist = cur.execute('SELECT * FROM ted WHERE EXISTS ip = ' + lsdb['ip'])
    rslt = cur.execute(lsdb_pattern)
    if exist == False:
        return -1
    else if rslt != '':
        return 0
    else:  # diffあり
        return 1


def insertdb():
    '''insert DB'''


def updatedb():
    '''update DB'''

    return


def cspf_request():
    '''request to pce_cspf'''

    return


def manager(lsdb, ip):
    '''main of TED manager'''

    ret = checkdb(lsdb, ip)
    if ret != 0:
        if ret == -1:
            # DB作成
            insertdb(lsdb, ip):
        else:
            # DB更新
            updatedb(lsdb, ip):

                # 計算要求
        cspf_request(ip):

    return
