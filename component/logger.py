import logging
import inspect

class Logger:
    @staticmethod
    def __init__():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='app.log',
            filemode='w'
        )

    def getCallingFunctionName():
        stack = inspect.stack()
        if str(stack[1][0].f_code.co_name) == "main":
            return
        frame = stack[2][0]
        calling_function_name = frame.f_code.co_name
        return calling_function_name
    
    def callFuction(exMessage = None):
        frame = inspect.currentframe().f_back 
        argAll = inspect.getargvalues(frame) 
        argsAndValues = zip(argAll.args, argAll.locals.values())
        logging.info(f'''Fuction Call Into : {Logger.getCallingFunctionName()}(); Args : {[(i, j) for i, j in argsAndValues]}, ExMessage : {exMessage}''')

    def retFuction(exMessage = None):
        logging.info(f'''Fuction Ret From {Logger.getCallingFunctionName()}(), ExMessage : {exMessage}''')
    