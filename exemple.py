#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from BGPDump import TableDumpV2, BGPDump
from pathlib import Path
import os

from socket import AF_INET


def routeview(bview_file: Path):

    to_return = {'v4': [], 'v6': []}

    with BGPDump('latest-bview.gz', Path(os.path.dirname(os.path.realpath(__file__)),
                 'libbgpdump.so')) as bgp:

        for entry in bgp:

            # entry.body can be either be TableDumpV1 or TableDumpV2

            if not isinstance(entry.body, TableDumpV2):
                continue  # I expect an MRT v2 table dump file

            # get a string representation of this prefix
            prefix = f'{entry.body.prefix}/{entry.body.prefixLength}'

            # get a list of each unique originating ASN for this prefix
            originatingASs = ([re.split(rb'\s+', route.attr.asPath)[-1] for route in entry.body.routeEntries])

            best_as = originatingASs[-1].decode()

            if entry.body.afi == AF_INET:
                to_return['v4'].append((prefix, best_as))
            else:
                to_return['v6'].append((prefix, best_as))

        return to_return


if __name__ == '__main__':
    routes = routeview('latest-bview.gz')
    print(len(routes['v4']), len(routes['v6']))
