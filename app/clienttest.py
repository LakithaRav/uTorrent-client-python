from utorrentapi import UTorrentAPI

apiclient = UTorrentAPI('http://127.0.0.1:35653/gui', 'admin', 'laky123')

if apiclient is not None:
    torrents = apiclient.get_list()

    INDEX = 0
    for torrent in torrents['torrents']:
        name = f'{INDEX} - {torrent[2]}'
        INDEX += 1
        print(name)
    # apiclient.get_files(torrent[0])
    # apiclient.recheck(torrent[0])
    # apiclient.set_priority(torrent[0], 1, 1)
