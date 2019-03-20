#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BGPDumpyError(Exception):
    def __init__(self, message):
        super(BGPDumpyError, self).__init__(message)
        self.message = message

class LibraryNotFound(BGPDumpyError):
        pass
