from datetime import datetime, timedelta
import logging
import os

client_secret = os.getenv("client_secret")

client_id = os.getenv("client_id")

async def get_time():
    # Get the current time
    current_time = datetime.now()

    # Calculate the time 24 hours from now
    updated_after_time = current_time - timedelta(hours=100)

    # Format the time as a string in the required format ("YYYY-MM-DDTHH:MM:SS")
    updatedTime = updated_after_time.strftime("%Y-%m-%dT%H:%M:%S")
    return updatedTime


#function to create logger so I didnt have to repeat logger for every file
def get_logger(    
        LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        LOG_NAME       = '',
        LOG_FILE_INFO  = 'loggingz\infoLog.log',
        LOG_FILE_ERROR = 'loggingz\errorLog.log',
        LOG_FILE_WARNING = 'loggingz\errorLog.log',
        LOG_FILE_CRITICAL = 'loggingz\critical.log'):

    log           = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # Comment these lines to suppress console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    file_handler_warning = logging.FileHandler(LOG_FILE_WARNING, mode='w')
    file_handler_warning.setFormatter(log_formatter)
    file_handler_warning.setLevel(logging.WARNING)
    log.addHandler(file_handler_warning)

    file_handler_critical = logging.FileHandler(LOG_FILE_CRITICAL, mode='w')
    file_handler_critical.setFormatter(log_formatter)
    file_handler_critical.setLevel(logging.CRITICAL)
    log.addHandler(file_handler_critical)

    log.setLevel(logging.INFO)

    return log

