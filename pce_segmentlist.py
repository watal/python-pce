#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import json


class ServAttr:
    def __init__(self):
        self.ip = ''
        self.port = 0


def ssocket(segment_lists):
    '''socket of segmentlist'''
    serv = ServAttr()
    serv.ip = '172.16.1.1'
    serv.port = 55384

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serv.ip, serv.port))
    s.send(json.dumps(segment_lists))
    s.close()

    return
