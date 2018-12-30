#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import threading
import pce_linkstate
import pce_segmentlist
import pce_cspf


def ls_socket():
    '''socket of linkstate'''

    pce_linkstate.lsocket()

    return


def sl_socket():
    '''socket of segmentlist'''

    time.sleep(5)
    segment_lists = pce_cspf.cspf()
    pce_segmentlist.ssocket(segment_lists)

    return


def main():
    '''simple PCE for FRRouting'''

    # receive linkstate
    thread_ls = threading.Thread(target=ls_socket)
    # send segment list
    thread_sl = threading.Thread(target=sl_socket)

    thread_ls.start()
    thread_sl.start()

    return 0


if __name__ == '__main__':
    main()
