#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from socket import AF_INET
from pathlib import Path

from .BGPDump import TableDumpV2, BGPDump

from .exceptions import LibraryNotFound


def routeview(bview_file: Path, libbgpdump_path: Path=None):

    def find_best_non_AS_set(originatingASs):
        pass

    if not libbgpdump_path:
        libbgpdump_path = Path(sys.modules['bgpdumpy'].__file__).parent / 'clib' / 'libbgpdump.so'
        if not libbgpdump_path.exists():
            raise LibraryNotFound(f'The path to the library is invalid: {libbgpdump_path}')

    routes = {'v4': [], 'v6': []}

    with BGPDump(bview_file, libbgpdump_path) as bgp:

        for entry in bgp:

            # entry.body can be either be TableDumpV1 or TableDumpV2

            if not isinstance(entry.body, TableDumpV2):
                continue  # I expect an MRT v2 table dump file

            # get a string representation of this prefix
            prefix = f'{entry.body.prefix}/{entry.body.prefixLength}'

            # get a list of each unique originating ASN for this prefix
            all_paths = []
            for route in entry.body.routeEntries:
                as_path = [asn.decode() for asn in re.split(rb'\s+', route.attr.asPath)]
                all_paths.append(as_path)

            # Cleanup the AS Sets
            for asn in reversed(all_paths[-1]):
                if asn.isnumeric():
                    best_as = asn
                    break
                elif asn[1:-1].isnumeric():
                    best_as = asn[1:-1]
                    break

            if entry.body.afi == AF_INET:
                routes['v4'].append((prefix, best_as))
            else:
                routes['v6'].append((prefix, best_as))

        return routes
