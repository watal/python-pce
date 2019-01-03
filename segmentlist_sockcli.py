#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import json


class ServAttr:
    def __init__(self):
        self.ip = ''
        self.port = 0


def ssocket(addr, sl_info):
    '''socket of segmentlist'''
    serv = ServAttr()
    serv.ip = addr
    serv.port = 55384

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serv.ip, serv.port))
    # send segmentlist infomation (src, dst, nexthop, segmentlist)
    s.send(json.dumps(sl_info))
    s.close()

    return
