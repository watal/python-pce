#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import linkstate_socksrv
import segmentlist_socksrv
import argparse


def main():
    '''simple PCE for FRRouting'''

    # Receive linkstate
    thread_ls = threading.Thread(target=linkstate_socksrv.lsocket)
    # Receive segment list
    thread_sl = threading.Thread(target=segmentlist_socksrv.ssocket)

    thread_ls.start()
    thread_sl.start()

    return 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simple SR PCE')
    args = parser.parse_args()

    main()
