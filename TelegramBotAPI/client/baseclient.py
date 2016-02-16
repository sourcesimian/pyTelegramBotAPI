import logging

from TelegramBotAPI.types.compound import Error

log = logging.getLogger(__name__)


class BaseClient(object):
    def __init__(self, token, debug=False):
        self.__token = token
        self._debug = debug

    def _get_post_url(self, method):
        return 'https://api.telegram.org/bot%s/%s' % (self.__token, method._name)

    def _interpret_response(self, value, method):
        if self._debug:
            log.debug('RSP: %s', value)

        if value['ok'] is not True:
            e = Error()
            e._from_raw(value)
            raise Exception("method: %s\nresponse: %s" % (method, e,))

        if isinstance(value['result'], list):
            responses = []
            for result in value['result']:
                m = method._response()
                m._from_raw(result)
                dropped = m._from_raw_dropped()
                if dropped:
                    log.warning('%s dropped %s', m.__class__.__name__, dropped)
                responses.append(m)
            return responses
        else:
            try:
                m = method._response()
            except TypeError:
                raise Exception('%s._response not defined' % method.__class__.__name__)
            m._from_raw(value['result'])
            dropped = m._from_raw_dropped()
            if dropped:
                log.warning('%s dropped %s', m.__class__.__name__, dropped)
            return m

    def _check_response_status(self, status, url, proxy, get_body):
        if status != 200:
            raise Exception("Server error: %s: %s\n%s\n%s" %
                            (status, url, proxy, get_body()))
