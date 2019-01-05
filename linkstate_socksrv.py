#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import os
import sys
import socket
import pickle
import ted_manager

BUFSIZE = 4096


class ServAttr:
    def __init__(self):
        self.ip = ''
        self.port = 0


def lsocket():
    '''Socket of linkstate'''

    serv = ServAttr()
    serv.ip = '172.16.2.253'
    serv.port = 17932

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((serv.ip, serv.port))
    s.listen(16)
    linkstate = b''
    while True:
        (conn, addr) = s.accept()

        pid = os.fork()
        if pid == 0:
            # child process
            s.close()
            print('[Link State] Get linkstate information from {}'.format(
                addr[0]), file=sys.stderr)
            while True:
                data = conn.recv(BUFSIZE)
                if not data:
                    ted_manager.manager(addr, pickle.loads(linkstate))
                    break
                linkstate += data
            conn.close()
            s.close()
            sys.exit()

        elif pid > 0:
            # parent process
            conn.close()
            os.wait()

        else:
            # fork error
            conn.close()

    return
