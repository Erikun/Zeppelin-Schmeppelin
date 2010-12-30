import logging

#The file name where log output is written
LOG_FILENAME = "output.log"
#Set which level of logging should be done.possible values:
# logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG)

def get_module_logger(module_name):
    module_logger = logging.getLogger(module_name)
    return module_logger
