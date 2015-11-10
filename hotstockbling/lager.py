#!/usr/bin/env python

import logging

datefmt = '%Y-%m-%d %H:%M:%S'
fmt = '[%(asctime)s|%(module)s:%(lineno)d|%(levelname)s] %(message)s'

logging.basicConfig(format=fmt, datefmt=datefmt)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
