#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import socket
import json
import ted_manager

BUFSIZE = 4096


class ServAttr:
    def __init__(self):
        self.ip = ''
        self.port = 0


def lsocket():
    '''socket of linkstate'''

    serv = ServAttr()
    serv.ip = '172.16.1.254'
    serv.port = 17932

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((serv.ip, serv.port))
    s.listen(16)
    linkstate = ''
    while True:
        (conn, addr) = s.accept()

        pid = os.fork()

        if pid == 0:
            # child process
            while True:
                data = conn.recv(BUFSIZE)
                if not data:
                    ted_manager.manager(addr, json.loads(linkstate))
                    break
                linkstate += data
            conn.close()
            sys.exit()

        elif pid > 0:
            # parent process
            conn.close()

        else:
            # fork error
            conn.close()

    s.close()

    return
