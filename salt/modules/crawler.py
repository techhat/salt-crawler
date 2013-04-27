'''
Salt-Based Web Crawler
'''

# Import python libs
import logging
import urllib2
import random
import time

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Basic Python libs are all that are needed
    '''
    return 'crawler'


def download(urls=None, wait=0, random_wait=False):
    '''
    Download a URL

    CLI Example::

        salt myminion crawler.download http://www.mydomain.com/
    '''
    ret = {}
    if type(urls) is str:
        ret[urls] = _query(urls)
    elif type(urls) is list:
        for url in urls:
            _wait(wait, random_wait)
            ret[url] = _query(url)
    return ret
    

def _query(url):
    '''
    The actual call to download a url
    '''
    result = urllib2.urlopen(url)
    return {
        'url': result.url,
        'code': result.code,
        'msg': result.msg,
        'headers': result.headers.dict,
        'content': result.read(),
    }


def _wait(wait, random_wait):
    '''
    Wait X amount of wait.
    If random_wait is True, multiply wait by random number from 0.5 to 1.5
    '''
    if random_wait is True:
        time.sleep(wait * random.uniform(0.5, 1.5))
        return
    time.sleep(wait)
