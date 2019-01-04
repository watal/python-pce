#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import os
import sys
import socket
import pickle 
import compute_manager

BUFSIZE = 4096


class ServAttr:
    def __init__(self):
        self.ip = ''
        self.port = 0


def ssocket():
    '''Socket of segmentlist'''

    serv = ServAttr()
    serv.ip = '172.16.1.254'
    serv.port = 55384

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((serv.ip, serv.port))
    s.listen(16)
    while True:
        (conn, addr) = s.accept()

        pid = os.fork()
        if pid == 0:
            # child process
            s.close()
            print('[Segment list] Get path-computation request from {}'.format(addr[0]), file=sys.stderr)
            request = conn.recv(BUFSIZE)
            # send segmentlist infomation (src, dst, nexthop, segmentlist)
            print('[Segment list] Start create sl_info')
            sl_info = compute_manager.manager(pickle.loads(request))
            print('[Segment list] Send sl_info: {} To {}'.format(sl_info, addr[0]), file=sys.stderr)
            conn.send(pickle.dumps(sl_info))
            conn.close()
            sys.exit()

        elif pid > 0:
            # parent process
            conn.close()
            os.wait()

        else:
            # fork error
            conn.close()

    s.close()

    return
