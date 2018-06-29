# uTorrent-client-python
uTorrent API Client for Python3

## How to use

### 1. Setup up virtual environment

This library uses ["requests"](http://docs.python-requests.org/en/master/), so you need to run pip3 install -r requirements.txt to download the depedencies.

Swithc to the virtual env by typing;
```sh
$ source env/bin/activate
```

### 2. Activate uTorrent WEB UI
To use this library you first need to activate uTorrent/bitTorrent Web UI and configure the credentials and ports.

### 3. inport UTorrentAPI
In your code import the library as;

```python
from utorrentapi import UTorrentAPI
```

And initalize as;
```python
apiclient = UTorrentAPI(<url>, <user name>, <password>)
```

Ex;
```python
apiclient = UTorrentAPI('http://127.0.0.1:35653/gui', 'admin', 'laky123')
```

### 4. use helper class
Import this

```python
from utorrentapi import TorrentListInfo
```

Use like this
```python
data = apiclient.get_list()
tor_list = TorrentListInfo(data)
filename = tor_list.torrents[0].name 
```

## API Methods

- `get_list():`
List all torrents.

- `get_files(torrentid):`
List all filed of a torrent.

- `start(torrentid):`
Start torrent.

- `stop(torrentid):`
Stop torrent.

- `pause(torrentid):`
Pause torrent.

- `forcestart(torrentid):`
Force start torrent.

- `unpause(torrentid):`
Start a pause torrent, same as start.

- `recheck(torrentid):`
Recehck torrent status.

- `remove(torrentid):`
Remove torrent file.

- `removedata(torrentid):`
Remove torrent file with data.

- `set_priority(torrentid, priority, fileindex):`
Set priority to each file in a torrent.

- `add_file(file_path):`
Add torrent file to download.

- `add_url(fiel_path):`
Add torrent URL to download (magnet link).

MIT License
