#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from bgpdumpy import routeview
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dump routes from a bview file')
    parser.add_argument('--file', type=str, required=True, help='Bview file to process.')
    args = parser.parse_args()

    routes = routeview(args.file)
    print(json.dumps(routes, indent=2))
