#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def add_path():

    paths = [
        '..',
        '../../pylibs'
    ]

    for path in paths:
        sys.path.append(os.path.join(os.path.dirname(__file__), path))
        logger.info('added reference path: "%s"', path)
