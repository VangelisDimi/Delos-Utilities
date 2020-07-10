#!/usr/bin/env python3
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
import ssl
import certifi

FILE_BASE_URL = "https://delos-media.uoa.gr:443/delosrc/resources/vl/"
WEB_BASE_URL = "https://delos.uoa.gr/opendelos/player?rid="

DELOS_LINK = "delos.uoa.gr/opendelos"
SEARCH_LINK = "search?crs"
VIDEO_LINK = "?rid="


def getFileURL(id):
    return FILE_BASE_URL + id + "/" + id + ".mp4"


def getWebSiteURL(id):
    return WEB_BASE_URL + id


def getId(url):
    return url.split("=", 1)[1]


def getVideoName(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    metas = soup.find_all('meta')
    name = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description']
    name = name[0].strip('\t\n\r')
    name = name.replace('OpenDelos:', '')[1:]
    response.close()
    return name


def getlinks(url):
    links = []
    names = []
    http = httplib2.Http(ca_certs=certifi.where())
    status, response = http.request(url)
    for link in BeautifulSoup(response, features="html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href') and 'opendelos/videolecture/show?rid' in link['href'] and (
                links == [] or link['href'] != links[-1]):
            links.append(link['href'])
            names.append(getVideoName(getWebSiteURL(getId(link['href']))))
    return list(zip(links, names))


def inputLinks(input, traverse, findsr=False):
    lectures = []
    sr = False
    input = input.replace(" ", "")
    links = input.splitlines()
    print(links)
    if not traverse:
        for link in links:
            if DELOS_LINK in link:
                if VIDEO_LINK in link:
                    lectures += (list(zip([link], [getVideoName(getWebSiteURL(getId(link)))])))
                elif SEARCH_LINK in link:
                    lectures += getlinks(link)
                    sr = True
    else:
        for link in links:
            if DELOS_LINK in link:
                if VIDEO_LINK in link:
                    lectures += (list(zip([link], [getVideoName(getWebSiteURL(getId(link)))])))
                elif SEARCH_LINK in link:
                    i = 1
                    while True:
                        if "&sa=" in link:
                            i = int(link.rsplit("&sa=", 1)[1])
                            link = link.rsplit("&sa=", 1)[0]
                        resources = getlinks(link + "&sa=%s" % i)
                        if resources == []:
                            break
                        lectures += resources
                        i += 1
                    sr = True
    lectures.sort(key=lambda lectures: lectures[1], reverse=True)
    if findsr:
        return [lectures, sr]
    return lectures
