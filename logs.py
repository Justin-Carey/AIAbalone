'''
Copyright (C) BCIT AI/ML Option 2018 Team with Members Following - All Rights Reserved.
- Jake Jonghun Choi     jchoi179@my.bcit.ca
- Justin Carey          justinthomascarey@gmail.com
- Pashan Irani          pashanirani@gmail.com
- Tony Huang	        tonyhuang1996@hotmail.ca
- Chil Yuqing Qiu       yuqingqiu93@gmail.com
Unauthorized copying of this file, via any medium is strictly prohibited.
Written by Jake Jonghun Choi <jchoi179@my.bcit.ca>
'''

import logging
import datetime
import os

"""
0. CALLER's responsibility to specify the log message content
1. logs all actions into log stream
2. show necessary logs in console
3. give all message time stamp to clarify when exactly they happened

USAGE:
 
"""
# LOG_FORMAT = '%(asctime)s %(funcName)s %(levelname)s'
# the location of logged files
log_dir = "action_log"
info_log = log_dir + "/info_log_%s.log" % (str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '_'))
warning_log = log_dir + "/warning_log_%s.log" % (str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '_'))
error_log = log_dir + "/error_log_%s.log" % (str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '_'))
# Logger names
ERR_LOG = 'ERROR LOG'
WRN_LOG = 'WARNING LOG'
INF_LOG = 'INFO LOG'


class FileLogger:
    def __init__(self):
        self.LOG_STARTED = 0
        self.log_names = []

    def set_file(self, log_name, file_name, level=logging.WARNING):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = logging.FileHandler(file_name)
        # handler.setFormatter(LOG_FORMAT)
        logger = logging.getLogger(log_name)
        logger.setLevel(level)
        if file_name not in self.log_names:
            logger.addHandler(handler)
            self.log_names.append(file_name)
        return logger

    def error_msg(self, msg, file=error_log, level=logging.WARNING):
        # time stamp of current message
        ts = str(datetime.datetime.now()).split('.')[0]
        err_logger = self.set_file(ERR_LOG, file, level)
        err_logger.error(ts+' :\t'+msg)

    def warning_msg(self, msg, file=warning_log, level=logging.WARNING):
        # time stamp of current message
        ts = str(datetime.datetime.now()).split('.')[0]
        wrn_logger = self.set_file(WRN_LOG, file, level)
        wrn_logger.warning(ts+' :\t'+msg)

    def info_msg(self, msg, file=info_log, level=logging.WARNING):
        # time stamp of current message
        ts = str(datetime.datetime.now()).split('.')[0]
        inf_logger = self.set_file(INF_LOG, file, level)
        print(msg)
        inf_logger.info(ts+' :\t'+msg)


# test logs.py individually
if __name__ == '__main__':
    logger = FileLogger()
    logger.error_msg('testing error message', level=logging.DEBUG)
    logger.warning_msg("testing warning message", level=logging.DEBUG)
    logger.info_msg("testing info message", level=logging.DEBUG)
    logger.info_msg("second test", level=logging.DEBUG)
    logger.info_msg("third test", level=logging.DEBUG)
