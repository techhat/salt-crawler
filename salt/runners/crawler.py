'''
This is a Salt runner for managing the crawler module on multiple servers
'''

# Import salt libs
import logging
import salt.key
import salt.client
import salt.output

log = logging.getLogger(__name__)


def fetch(urls=None):
    '''
    Select a minion (or minions) and tell them to download a page
    '''
    minions = up()
    client = salt.client.LocalClient(__opts__['conf_file'])
    data = client.cmd(minions[0],
                      'crawler.fetch',
                      arg=[urls],
                      timeout=__opts__['timeout'])
    for minion in data.keys():
        for url in data[minion]:
            data[minion][url]['content'] = '<hidden>'
    salt.output.display_output(data, '', __opts__)


def status(output=True):
    '''
    Print the status of all known salt minions
    '''
    client = salt.client.LocalClient(__opts__['conf_file'])
    minions = client.cmd('crawler.enabled:True',
                         'test.ping',
                         timeout=__opts__['timeout'],
                         expr_form='pillar')

    key = salt.key.Key(__opts__)
    keys = key.list_keys()

    ret = {}
    ret['up'] = sorted(minions)
    ret['down'] = sorted(set(keys['minions']) - set(minions))
    if output:
        salt.output.display_output(ret, '', __opts__)
    return ret


def down():
    '''
    Print a list of all the down or unresponsive salt minions
    '''
    ret = status(output=False).get('down', [])
    for minion in ret:
        salt.output.display_output(minion, '', __opts__)
    return ret


def up():  # pylint: disable-msg=C0103
    '''
    Print a list of all of the minions that are up
    '''
    ret = status(output=False).get('up', [])
    for minion in ret:
        salt.output.display_output(minion, '', __opts__)
    return ret
