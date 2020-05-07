from requests import request, Session
import datetime
from time import sleep
from json import loads
import atexit

POE_PUBLIC_STASH_API_BASE_URL = 'http://www.pathofexile.com/api/public-stash-tabs'
POE_NINJA_URL = 'https://poe.ninja/api/Data/GetStats'

class PublicStashApi:

    def __init__(self, rate_limit_seconds=2, next_id=None, logger=None):
        self.rate_limit_seconds=rate_limit_seconds
        self.next_id=next_id
        self.last_fetch = None
        self.logger=logger
        self.session=Session()
        atexit.register(self.cleanup)

    def cleanup(self):
        self.session.close()

    def rate_limit_wait(self):
        now = datetime.datetime.now()

        if self.last_fetch is not None:
            diff = now - self.last_fetch
            if diff.total_seconds() < self.rate_limit_seconds:
                sleep(diff.total_seconds())

        self.last_fetch = datetime.datetime.now()

    def get_next_id(self):
        self.rate_limit_wait()
        fetch_data = self.get_data()
        data_dict = loads(fetch_data)

        self.next_id = data_dict['next_change_id']
        return data_dict

    def get_data(self):
        if self.next_id is None:
            self.next_id = self.get_initial_next_id()

        request_url = POE_PUBLIC_STASH_API_BASE_URL + '?id=' + self.next_id
        
        self.logger.info('Requesting next stash api, with next_id: %s', self.next_id)

        return self.session.get(request_url).text

    def get_initial_next_id(self):
        with Session() as s:
            initial_id_info = s.get(POE_NINJA_URL)
            id_dict = loads(initial_id_info.text)
            return id_dict['next_change_id']

