#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import version

from mitorrent import mitorrent as program

if version < '3.2':
    print('Requires Python 3.2 or newer.')
    exit(1)

if __name__ == '__main__':
    program.main()
