import requests
import base64
import json
from lxml import html

class UTorrentAPI(object):

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth     = requests.auth.HTTPBasicAuth(self.username, self.password)
        self.token, self.cookies  = self._get_token()

    def _get_token(self):
        url = self.base_url + '/token.html'
        response = requests.get(url, auth=self.auth)

        token = -1
        guid  = -1

        if response.status_code == 200:
            xtree = html.fromstring(response.content)
            token = xtree.xpath('//*[@id="token"]/text()')[0]
            guid  = response.cookies['GUID']
        else:
            token = -1

        cookies = dict(GUID = guid)

        return token, cookies

# public sectin -->
    def get_list(self):
        status, response = self._action('list=1')

        torrents = []

        if status == 200:
            torrents = response.json()
        else:
            print(response.status_code)

        return torrents

    def get_files(self, torrentid):
        path = 'action=getfiles&hash=%s' % (torrentid)
        status, response = self._action(path)

        files = []

        if status == 200:
            files = response.json()
        else:
            print(response.status_code)

        return files

    def start(self, torrentid):
        return self._torrentaction('start', torrentid)

    def stop(self, torrentid):
        return self._torrentaction('stop', torrentid)

    def pause(self, torrentid):
        return self._torrentaction('pause', torrentid)

    def forcestart(self, torrentid):
        return self._torrentaction('forcestart', torrentid)

    def unpause(self, torrentid):
        return self._torrentaction('unpause', torrentid)

    def recheck(self, torrentid):
        return self._torrentaction('recheck', torrentid)

    def remove(self, torrentid):
        return self._torrentaction('remove', torrentid)

    def removedata(self, torrentid):
        return self._torrentaction('removedata', torrentid)

    # def recheck(self, torrentid):
    #     return self._torrentaction('recheck', torrentid)

    def set_priority(self, torrentid, priority, fileindex):
        path = 'action=%s&hash=%s&p=%s&f=%s' % ('setprio', torrentid, priority, fileindex)
        status, response = self._action(path)

        files = []

        if status == 200:
            files = response.json()
        else:
            print(response.status_code)

        return files

# private section -->
    def _torrentaction(self, action, torrentid):
        path = 'action=%s&hash=%s' % (action, torrentid)
        status, response = self._action(path)

        files = []

        if status == 200:
            files = response.json()
        else:
            print(response.status_code)

        return files

    def _action(self, path):
        url = '%s/?%s&token=%s' % (self.base_url, path, self.token)
        headers = {
        'Content-Type': "application/json"
        }
        response = requests.get(url, auth=self.auth, cookies=self.cookies, headers=headers)
        return response.status_code, response
