import logging
import inspect
from logging.handlers import RotatingFileHandler

class Logger:
    @staticmethod
    def __init__():
        max_size = 1024 * 1024 * 100
        backup_count = 1
        file_handler = RotatingFileHandler('app.log', maxBytes=max_size, backupCount=backup_count)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    @staticmethod
    def _getCallingFunctionName():
        stack = inspect.stack()
        if str(stack[1][0].f_code.co_name) == "main":
            return
        frame = stack[2][0]
        calling_function_name = frame.f_code.co_name
        return calling_function_name
    
    @staticmethod
    def callFunction(exMessage=None):
        frame = inspect.currentframe().f_back 
        argAll = inspect.getargvalues(frame) 
        argsAndValues = zip(argAll.args, argAll.locals.values())
        logging.info(f'''Function Call Into: {Logger._getCallingFunctionName()}(); Args: {[(i, j) for i, j in argsAndValues]}, ExMessage: {exMessage}''')

    @staticmethod
    def retFunction(exMessage=None):
        logging.info(f'''Function Ret From {Logger._getCallingFunctionName()}(), ExMessage: {exMessage}''')
