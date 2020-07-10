#!/usr/bin/env python3 
import os
import os.path
from path import resource_path


def createplaylist(urls, names, dir):
    with open(resource_path('./Playlist/begin.txt'), 'r') as file:
        data = file.read()
    vc = 0
    for i in range(len(urls)):
        data += "\n"
        with open(resource_path('./Playlist/entry.txt'), 'r') as file:
            data += (file.read() % (urls[i], names[i], str(vc),))
        vc += 1
    with open(resource_path('./Playlist/end.txt'), 'r') as file:
        data += "\n"
        data += file.read()
    for i in range(vc):
        with open(resource_path('./Playlist/vlcitem.txt'), 'r') as file:
            data += "\n"
            info = file.read()
            data += (info % (str(i),))
    with open(resource_path('./Playlist/end2.txt'), 'r') as file:
        data += "\n"
        data += file.read()

    i = 0
    target = (dir + "/delos_playlist(%s)" + ".xspf").rstrip()
    while os.path.isfile(target % i):
        i += 1
    f = open(target % i, 'wb')
    f.write(data.encode('utf8'))
    f.close()
