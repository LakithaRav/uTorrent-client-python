import requests
from lxml import html


class StatusInfo:
    def __init__(self, data):
        mask = 1
        self.started = (data & mask) != 0
        mask *= 2
        self.checking = (data & mask) != 0
        mask *= 2
        self.start_after_check = (data & mask) != 0
        mask *= 2
        self.checked = (data & mask) != 0
        mask *= 2
        self.error = (data & mask) != 0
        mask *= 2
        self.paused = (data & mask) != 0
        mask *= 2
        self.queued = (data & mask) != 0
        mask *= 2
        self.loaded = (data & mask) != 0
        mask *= 2


class TorrentInfo:
    def __init__(self, data):
        self.data = data
        self.hash = data[0]
        self.status = StatusInfo(data[1])
        self.name = data[2]
        self.size = data[3]  # in bytes
        self.percent_progress = data[4]  # in mils
        self.downloaded = data[5]  # in bytes
        self.uploaded = data[6]  # in bytes
        self.ratio = data[7]  # in mils
        self.upload_speed = data[8]  # in bytes per second
        self.download_speed = data[9]  # in bytes per second
        self.eta = data[10]  # in seconds
        self.label = data[11]
        self.peers_connected = data[12]
        self.peers_in_swarm = data[13]
        self.seeds_connected = data[14]
        self.seeds_in_swarm = data[15]
        self.availability = data[16]  # int in 1/65535
        self.torrent_queue_order = data[17]
        self.remaining = data[18]  # in bytes
        self.download_url = data[19]
        self.status_message = data[21]
        self.date_added = data[23]  # epoch
        self.date_completed = data[24]  # epoch


class LabelInfo:
    def __init__(self, data):
        self.label = data[0]
        self.torrents_in_label = data[1]


class TorrentListInfo:
    def __init__(self, data):
        self.build = data['build']
        self.labels = [LabelInfo(x) for x in data['label']]
        self.torrents = [TorrentInfo(x) for x in data['torrents']]
        self.torrent_cache_id = data['torrentc']


class UTorrentAPI():
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        self.token, self.cookies = self._get_token()

    def _get_token(self):
        url = self.base_url + '/token.html'

        token = -1
        cookies = -1

        try:
            response = requests.get(url, auth=self.auth)

            token = -1

            if response.status_code == 200:
                xtree = html.fromstring(response.content)
                token = xtree.xpath('//*[@id="token"]/text()')[0]
                guid = response.cookies['GUID']
            else:
                token = -1

            cookies = dict(GUID=guid)

        except requests.ConnectionError as error:
            token = 0
            cookies = 0
            print(error)

        return token, cookies

    def is_online(self):
        return bool(self.token not in [-1, 0])

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

        return torrents

    def get_files(self, torrentid):
        path = f'action=getfiles&hash={torrentid}'
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

    def set_priority(self, torrentid, fileindex, priority):
        # 0 = Don't Download
        # 1 = Low Priority
        # 2 = Normal Priority
        # 3 = High Priority
        path = f'action=setprio&hash={torrentid}&p={priority}&f={fileindex}'
        status, response = self._action(path)

        files = []

        if status == 200:
            files = response.json()
        else:
            print(response.status_code)

        return files

    def add_file(self, file_path):

        file = []

        url = f'{self.base_url}/?action=add-file&token={self.token}'
        headers = {
            'Content-Type': "multipart/form-data"
        }

        with open(file_path, 'rb') as fref:
            files = {'torrent_file': fref}

            try:
                if files:
                    response = requests.post(
                        url, files=files, headers=headers, auth=self.auth,
                        cookies=self.cookies)
                    if response.status_code == 200:
                        file = response.json()
                        print('file added')
                    else:
                        print(response.status_code)
                else:
                    print('file not found')

            except requests.ConnectionError as error:
                print(error)

            return file

    def add_url(self, file_path):
        path = f'action=add-url&s={file_path}'
        status, response = self._action(path)

        files = []

        try:
            if status == 200:
                files = response.json()
            else:
                print(response.status_code)

        except requests.ConnectionError as error:
            print(error)

        return files

# private section -->
    def _torrentaction(self, action, torrentid):
        path = f'action={action}&hash={torrentid}'

        files = []

        try:
            status, response = self._action(path)

            if status == 200:
                files = response.json()
            else:
                print(response.status_code)

        except requests.ConnectionError as error:
            print(error)

        return files

    def _action(self, path):
        url = f'{self.base_url}/?{path}&token={self.token}'
        headers = {
            'Content-Type': "application/json"
        }
        try:
            response = requests.get(
                url, auth=self.auth, cookies=self.cookies, headers=headers)
            # use utf8 for multi-language
            # default is ISO-8859-1
            response.encoding = 'utf8'
        except requests.ConnectionError as error:
            print(error)

        return response.status_code, response
