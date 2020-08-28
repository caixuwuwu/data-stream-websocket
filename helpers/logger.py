#!/usr/bin/env python
# coding=utf-8

import sys
import logging


def generate_logger(logname, loglevel=logging.INFO):
    '''
        生成stream logger, 日誌級別默認為INFO.
        Args:
            logname (str): 日誌名稱.
            loglevel (enum, optional): 日誌級別, 默認為logging.INFO
        Returns:
            logger 對象.
    '''
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger