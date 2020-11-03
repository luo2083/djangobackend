import time
import datetime
import logging

logger = logging.getLogger('django')
def demo():
    message = 'Job log in crontab,now time is :' + str(datetime.datetime.now())
    print(message)
    logger.info(message)