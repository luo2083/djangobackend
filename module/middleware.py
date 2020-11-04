import time
import logging

from backend import settings

logger = logging.getLogger('statistics')
class StatisticsMiddleware:
    def __int__(self, get_response):
        self.get_response = get_response
        logger.info('Build StatisticsMiddleware.')

    def __call__(self, request):
        tick = time.time()
        response = self.get_response(request)
        path = request.path
        full_path = request.get_full_path()
        tock = time.time()
        cost = tock - tick
        content_list = []
        content_list.append('now=[%d]' % tock)
        content_list.append('path=[%s]' % path)
        content_list.append('full_path=[%s]' % full_path)
        content_list.append('cost=[%.6f]' % cost)
        content = settings.STATISTICS_SPLIT_FLAG.join(content_list)
        logger.info(content)

        return response