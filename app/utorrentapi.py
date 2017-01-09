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

        token    = -1
        cookies  = -1

        try:
            response = requests.get(url, auth=self.auth)

            token = -1

            if response.status_code == 200:
                xtree = html.fromstring(response.content)
                token = xtree.xpath('//*[@id="token"]/text()')[0]
                guid  = response.cookies['GUID']
            else:
                token = -1

            cookies = dict(GUID = guid)

        except requests.ConnectionError as error:
            token = 0
            cookies = 0
            print(error)
        except:
            print('error')

        return token, cookies

    def is_online(self):
        if self.token != -1 and self.token != 0:
            return True
        else:
            return False

# public sectin -->
    def get_list(self):
        torrents = []
        try:
            status, response = self._action('list=1')
            if status == 200:
                torrents = response.json()
            else:
                print(response.status_code)

        except requests.ConnectionError as error:
            print(error)
        except:
            print('error')

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

    def recheck(self, torrentid):
        return self._torrentaction('recheck', torrentid)

    def set_priority(self, torrentid, fileindex, priority):
        # 0 = Don't Download
        # 1 = Low Priority
        # 2 = Normal Priority
        # 3 = High Priority
        path = 'action=%s&hash=%s&p=%s&f=%s' % ('setprio', torrentid, priority, fileindex)
        status, response = self._action(path)

        files = []

        if status == 200:
            files = response.json()
        else:
            print(response.status_code)

        return files

    def add_file(self, file_path):

        file = []

        url = '%s/?%s&token=%s' % (self.base_url, 'action=add-file', self.token)
        headers = {
        'Content-Type': "multipart/form-data"
        }

        files = {'torrent_file': open(file_path, 'rb')}

        try:
            if files:
                response = requests.post(url, files=files, auth=self.auth, cookies=self.cookies)
                if response.status_code == 200:
                    file = response.json()
                    print('file added')
                else:
                    print(response.status_code)
            else:
                print('file not found')

            pass
        except requests.ConnectionError as error:
            print(error)
        except Exception as e:
            print(e)

        return file

    def add_url(self, fiel_path):
        path = 'action=add-url&s=%s' % (fiel_path)
        status, response = self._action(path)

        files = []

        try:
            if status == 200:
                files = response.json()
            else:
                print(response.status_code)

            pass
        except requests.ConnectionError as error:
            print(error)
        except Exception as e:
            print(e)

        print(files)

        return files


# private section -->
    def _torrentaction(self, action, torrentid):
        path = 'action=%s&hash=%s' % (action, torrentid)

        files = []

        try:
            status, response = self._action(path)

            if status == 200:
                files = response.json()
            else:
                print(response.status_code)

        except requests.ConnectionError as error:
            print(error)
        except:
            print('error')

        return files

    def _action(self, path):
        url = '%s/?%s&token=%s' % (self.base_url, path, self.token)
        headers = {
        'Content-Type': "application/json"
        }
        try:
            response = requests.get(url, auth=self.auth, cookies=self.cookies, headers=headers)
        except requests.ConnectionError as error:
            print(error)
        except:
            pass

        return response.status_code, response
