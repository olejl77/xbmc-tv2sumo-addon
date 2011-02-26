# -*- coding: utf-8 -*-
'''
TV2 Sumo plugin for XBMC
Copyright (C) 2011 olejl77@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import urllib
import re
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import BeautifulSoup
from Item import Item

# Debugger
#import rpdb2
#rpdb2.start_embedded_debugger('pw')
# Debugger

__settings__ = xbmcaddon.Addon(id="plugin.video.tv2sumo")
__language__ = __settings__.getLocalizedString

def createMainMenu(baseUrl, handle):
	listing = []
	listing.append(Item(title=__language__(30101), url=baseUrl+"?node=live", category='Live'))
	listing.append(Item(title=__language__(30102), url=baseUrl+"?node=news", category='News'))
	listing.append(Item(title=__language__(30103), url=baseUrl+"?node=nonfiction", category='Non-fiction'))
	listing.append(Item(title=__language__(30104), url=baseUrl+"?node=entertainment", category='Entertainment'))
	listing.append(Item(title=__language__(30105), url=baseUrl+"?node=sport", category='Sport'))
	listing.append(Item(title=__language__(30106), url=baseUrl+"?node=alphabetically"))
	listing.append(Item(title=__language__(30107), url=baseUrl+"?node=search"))
	sendToXbmc(handle, listing)

def getLiveSub(url):
	soup = BeautifulSoup(urllib.urlopen(url))
	items = soup.findAll('a', attrs={'class':re.compile('icebergItem'),'onclick':re.compile('userNav') })
	listing = []
	for item in items:
		title = item.contents[1]
		url = item['href']
		listing.append(Item(title=title, url=url))
	return listing

def getNormalSub(url, tag_class):
	soup = BeautifulSoup(urllib.urlopen(url))
	items = soup.findAll('div', attrs={'class':re.compile(tag_class)})
	listing = []
	for item in items:
		title = item.find('a').string
		url = item.find('a')['href']
		listing.append(Item(title=title, url=url))
	return listing

def getOtherSub(url):
	soup = BeautifulSoup(urllib.urlopen(url))
	items = soup.findAll('a', attrs={'class':re.compile('categoryHeader more')})
	listing = []
	for item in items:
		title = item.find('img')['alt']
		url = item['href']
		listing.append(Item(title=title, url=url))
	return listing

def getSearchResult(url):
	soup = BeautifulSoup(urllib.urlopen(url))
	items = soup.findAll('div', attrs={'class':re.compile('item')})
	listing = []
	for item in items:
		title = item.findAll('a')[1].string.strip()
		url = item.find('a')['href'].strip()
		thumb = item.find('img')['src'].strip()
		date = item.findAll('p')[0].string.strip()
		desc = item.findAll('p')[1].string.strip()
		listing.append(Item(title=title, url=url, thumb=thumb, date=date, description=desc))
	return listing

def createLiveMenu(baseUrl, handle):
	listing = getLiveSub('http://webtv.tv2.no/webtv/sumo/?treeId=200002')
	sendToXbmc(handle, listing)

def createNewsMenu(baseUrl, handle):
	listing = getOtherSub('http://webtv.tv2.no/webtv/sumo/?treeId=11')
	sendToXbmc(handle, listing)

def createNonFictionMenu(baseUrl, handle):
	listing = getNormalSub('http://webtv.tv2.no/webtv/sumo/?treeId=4', 'subCategory')
	sendToXbmc(handle, listing)

def createEntertainmentMenu(baseUrl, handle):
	listing = getNormalSub('http://webtv.tv2.no/webtv/sumo/?treeId=3', 'subCategory')
	sendToXbmc(handle, listing)

def createAlphabeticallyMenu(baseUrl, handle):
	listing = getNormalSub('http://webtv.tv2.no/webtv/sumo/?treeId=9991', 'program ')
	sendToXbmc(handle, listing)

def createSportMenu(baseUrl, handle):
	listing = getOtherSub('http://webtv.tv2.no/webtv/sumo/?treeId=2')
	sendToXbmc(handle, listing)

def createSearch(baseUrl, handle):
	kb = xbmc.Keyboard()
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		text = text.replace(' ', '+')
		url = 'http://webtv.tv2.no/webtv/sumo/search.do?keywords=%s&treeId=9992' % (text)
		listing = getSearchResult(url)
		sendToXbmc(handle, listing)

def sendToXbmc(handle, listing):
	"""
	Sends a listing to XBMC for display as a directory listing
	Plugins always result in a listing
	@param list listing
	@retur n void
	"""
	# send each item to xbmc
	for item in listing:
		listItem = xbmcgui.ListItem(item.title)
		xbmcplugin.addDirectoryItem(handle, item.url, listItem, not item.isPlayable, len(listing))

	# tell xbmc we have finished creating the directory listing
	xbmcplugin.endOfDirectory(handle)

if ( __name__ == "__main__" ):
	xbmcplugin.setContent(int(sys.argv[1]), "episodes")
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

	arg = sys.argv[2].split('=', 1)

	if (arg[0] == "?node"):
		if(arg[1] == "live"):
			createLiveMenu(sys.argv[0], int(sys.argv[1]))
		elif(arg[1] == "news"):
			createNewsMenu(sys.argv[0], int(sys.argv[1]))
		elif(arg[1] == "nonfiction"):
			createNonFictionMenu(sys.argv[0], int(sys.argv[1]))
		elif(arg[1] == "entertainment"):
			createEntertainmentMenu(sys.argv[0], int(sys.argv[1]))
		elif(arg[1] == "sport"):
			createSportMenu(sys.argv[0], int(sys.argv[1]))
		elif(arg[1] == "alphabetically"):
			createAlphabeticallyMenu(sys.argv[0], int(sys.argv[1]))
		elif(arg[1] == "search"):
			createSearch	(sys.argv[0], int(sys.argv[1]))

	elif (arg[0] == "?url"):
		node_url(sys.argv[0], int(sys.argv[1]), arg[1])

	else:
		createMainMenu(sys.argv[0], int(sys.argv[1]))


