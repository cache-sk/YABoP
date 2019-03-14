# -*- coding: utf-8 -*-
# Module: default
# Author: cache
# Created on: 9.3.2019
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import json
import resolveurl
import requests
import time
import io
import os
import traceback
import re
#import webbrowser

_url = sys.argv[0]
_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_session = requests.Session()
_profile = xbmc.translatePath( _addon.getAddonInfo('profile')).decode("utf-8")

SEARCH_DATA_MAX_AGE = 43200 #12h

BOMBUJ_API = 'http://www.bombuj.eu/android_api/'
HEADERS={'User-Agent': 'android', 'Referer': BOMBUJ_API}
COVERS_MOVIES = 'http://www.bombuj.eu/images/covers/all/'
COVERS_SERIES = 'http://serialy.bombuj.eu/images/covers/'

CTYPES = [{'type':'movies','msg':_addon.getLocalizedString(30101)},
	{'type':'series','msg':_addon.getLocalizedString(30102)}]

CATEGORIES = [
	{'cat':'','msg':_addon.getLocalizedString(30201)},
	{'cat':'Akční','msg':_addon.getLocalizedString(30202)},
	{'cat':'Dobrodružný','msg':_addon.getLocalizedString(30203)},
	{'cat':'Animovaný','msg':_addon.getLocalizedString(30204)},
	{'cat':'Komedie','msg':_addon.getLocalizedString(30205)},
	{'cat':'Krimi','msg':_addon.getLocalizedString(30206)},
	{'cat':'Dráma','msg':_addon.getLocalizedString(30207)},
	{'cat':'Rodinný','msg':_addon.getLocalizedString(30208)},
	{'cat':'Horor','msg':_addon.getLocalizedString(30209)},
	{'cat':'Romantický','msg':_addon.getLocalizedString(30210)},
	{'cat':'Sci-Fi','msg':_addon.getLocalizedString(30211)},
	{'cat':'Thriller','msg':_addon.getLocalizedString(30212)},
	{'cat':'Fantasy','msg':_addon.getLocalizedString(30213)},
	{'cat':'Životopisný','msg':_addon.getLocalizedString(30214)},
	{'cat':'Mysteriózní','msg':_addon.getLocalizedString(30215)},
	{'cat':'Dokumentární','msg':_addon.getLocalizedString(30216)},
	{'cat':'Sportovní','msg':_addon.getLocalizedString(30217)},
	{'cat':'Válečný','msg':_addon.getLocalizedString(30218)},
	{'cat':'Historický','msg':_addon.getLocalizedString(30219)},
	{'cat':'Psychologický','msg':_addon.getLocalizedString(30220)},
	{'cat':'Pohádka','msg':_addon.getLocalizedString(30221)},
	{'cat':'Katastrofický','msg':_addon.getLocalizedString(30222)},
	{'cat':'Erotický','msg':_addon.getLocalizedString(30223)},
	{'cat':'Hudební','msg':_addon.getLocalizedString(30224)},
	{'cat':'Western','msg':_addon.getLocalizedString(30225)}]

LISTS = [
	{'list':'najnovsie','msg':_addon.getLocalizedString(30301),'series':True},
	{'list':'popularne','msg':_addon.getLocalizedString(30302),'series':False}, #note - series too, but error?
	{'list':'filmy_podla_roku','msg':_addon.getLocalizedString(30303),'series':False},
	{'list':'najlepsie_hodnotene','msg':_addon.getLocalizedString(30304),'series':True},
	{'list':'top_dnes','msg':_addon.getLocalizedString(30305),'series':False},
	{'list':'top_celkovo','msg':_addon.getLocalizedString(30306),'series':True}]

def get_url(**kwargs):
	return '{0}?{1}'.format(_url, urlencode(kwargs, 'utf-8'))

def check_profile():
	if not os.path.exists(_profile):
		os.makedirs(_profile)

def get_search_data(ctype, isSeries):
	check_profile()
	data = []
	last_data = ''
	already_tried = False
	current = time.time()
	try:
		with io.open(_profile + ctype+"_last_data", 'r', encoding='utf8') as file:
			last_data = file.read()
			file.close()
	except Exception as e:
		xbmc.log('Can\'t load ' + ctype + '_last_data\n'+str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
	
	if last_data != '': # there are some stored data
		try:
			last = float(last_data)
			age = current - last
			if age < SEARCH_DATA_MAX_AGE: #fresh data - load it
				with io.open(_profile + ctype+"_data", 'r', encoding='utf8') as file:
					fdata = file.read()
					file.close()
					data = json.loads(fdata, "utf-8")
		except Exception as e:
			xbmc.log('Old data is there (' + last_data + '), but can\'t be loaded..\n'+str(e),level=xbmc.LOGNOTICE)
			traceback.print_exc()
			already_tried = True
	
	if not data: #old data was not fresh, download it
		try:
			current = time.time()
			url = BOMBUJ_API + 'searchjson.php'
			if isSeries:
				url = BOMBUJ_API + 'searchserialyjson.php'
			wdata = _session.get(url, headers=HEADERS)
			loaded = json.loads(wdata.text, "utf-8")
			data = []
			if isSeries:
				data = loaded['results_serialy']
			else:
				data = loaded['results']
			with io.open(_profile + ctype+"_data", 'w', encoding='utf8') as file:
				file.write(json.dumps(data).decode('utf8'))
				file.close()
			with io.open(_profile + ctype+"_last_data", 'w', encoding='utf8') as file:
				file.write(str(current).decode('utf-8'))
				file.close()
		except Exception as e:
			xbmc.log('Can\'t load or store data from bombuj\n'+str(e),level=xbmc.LOGNOTICE)
			traceback.print_exc()
	
	if not data and last_data != '' and not already_tried: # there are some not fresh stored data, but couldn't load new ones
		try:
			with io.open(_profile + ctype+"_data", 'r', encoding='utf8') as file:
				fdata = file.read()
				file.close()
				data = json.loads(fdata, "utf-8")
		except Exception as e:
			xbmc.log('Old data is there (' + last_data + '), but can\'t be loaded..\n'+str(e),level=xbmc.LOGNOTICE)
			traceback.print_exc()
	
	return data

def list_types():
	xbmcplugin.setPluginCategory(_handle, '')
	xbmcplugin.setContent(_handle, 'videos')
	for ctype in CTYPES:
		list_item = xbmcgui.ListItem(label=ctype['msg'])
		list_item.setInfo('video', {'title': ctype['msg'],
									'genre': ctype['msg'],
									'mediatype': 'video'})
		link = get_url(action='categories', ctype=ctype['type'])
		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.endOfDirectory(_handle)

def list_categories(ctype):
	isSeries = ctype == 'series'
	xbmcplugin.setPluginCategory(_handle, (_addon.getLocalizedString(30102) if isSeries else _addon.getLocalizedString(30101))) # + " / " + _addon.getLocalizedString(30200)
	xbmcplugin.setContent(_handle, 'videos')
	for category in CATEGORIES:
		list_item = xbmcgui.ListItem(label=category['msg'])
		list_item.setInfo('video', {'title': category['msg'],
									'genre': category['msg'],
									'mediatype': 'video'})
		link = get_url(action='lists', category=category['cat'], ctype=ctype)
		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	list_item = xbmcgui.ListItem(label=_addon.getLocalizedString(30005))
	list_item.setInfo('video', {'title': _addon.getLocalizedString(30005),
								'genre': _addon.getLocalizedString(30005),
								'mediatype': 'video'})
	link = get_url(action='search', ctype=ctype)
	is_folder = True
	xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.endOfDirectory(_handle)

def is_found(query,name):
	if query in name:
		return True
	if isinstance(query, unicode): #strip
		query = query.encode('utf-8').strip()
	query = query.lower()
	if isinstance(name, unicode): #strip
		name = name.encode('utf-8').strip()
	name = name.lower()
	if query in name:
		return True
	return False

def list_search(ctype):
	isSeries = ctype == 'series'
	xbmcplugin.setPluginCategory(_handle, (_addon.getLocalizedString(30102) if isSeries else _addon.getLocalizedString(30101) ) + " / " + _addon.getLocalizedString(30005))
	xbmcplugin.setContent(_handle, 'videos')
	data = get_search_data(ctype,isSeries)
	if not data:
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009))
		xbmcplugin.endOfDirectory(_handle)
		return
	
	kb = xbmc.Keyboard('', _addon.getLocalizedString(30007))
	kb.doModal() # Onscreen keyboard appears
	if kb.isConfirmed():
		query = kb.getText() # User input
		if not query:
			xbmcplugin.endOfDirectory(_handle)
			return
		for item in data:
			name = ''
			if isSeries:
				name = item['nazov_1']
			else:
				name = item['name']
			if is_found(query,name):
				list_item = xbmcgui.ListItem(label=name)
				list_item.setInfo('video', {'title': name,
											'mediatype': 'video'})
				link = get_url(action=ctype+'_searched', iid=item['id'])
				is_folder = True
				xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.endOfDirectory(_handle)

def list_lists(ctype,category):
	isSeries = ctype == 'series'
	catName = category
	for cat in CATEGORIES:
		if cat['cat'] == category:
			catName = cat['msg']
			break
			
	xbmcplugin.setPluginCategory(_handle, (_addon.getLocalizedString(30102) if isSeries else _addon.getLocalizedString(30101) ) + " / " + catName)
	xbmcplugin.setContent(_handle, 'videos')
	for listt in LISTS:
		if (ctype == 'series' and listt['series'] == True) or ctype == 'movies':
			list_item = xbmcgui.ListItem(label=listt['msg'])
			list_item.setInfo('video', {'title': listt['msg'],
										'genre': listt['msg'],
										'mediatype': 'video'})
			link = get_url(action=ctype, category=category, listt=listt['list'])
			is_folder = True
			xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.endOfDirectory(_handle)
	
def list_movies(category,listt):
	catName = category
	for cat in CATEGORIES:
		if cat['cat'] == category:
			catName = cat['msg']
			break
	lstName = listt
	for lst in LISTS:
		if lst['list'] == listt:
			lstName = lst['msg']
			break

	xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30101) + " / " + catName + " / " + lstName)
	xbmcplugin.setContent(_handle, 'videos')
	movies = []
	
	try:
		data = _session.get(BOMBUJ_API + 'filmy/get_items_as_json.php?type=' + listt + '&zaner=' + category + '&sort=aj_s_titulkami', headers=HEADERS) #aj_s_titulkami/len_dabovane/len_s_titulkami
		loaded = json.loads(data.text, "utf-8")
		movies = loaded[listt]
	except Exception as e:
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return

	for movie in movies:
		list_item = xbmcgui.ListItem(label=movie['name'])
		list_item.setInfo('video', {'title': movie['name'],
									'genre': movie['zanre'],
									'year': movie['year'],
									'mediatype': 'video'})
		list_item.setArt({'thumb': COVERS_MOVIES + movie['url'] + '.jpg',
							'icon': COVERS_MOVIES + movie['url'] + '.jpg'})
		link = get_url(action='movie_streams', url=movie['url'], iid=movie['id'])
		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	
	xbmcplugin.endOfDirectory(_handle)

def get_movie_info(iid):
	movie_data = _session.get('https://www.bombuj.eu/android_api/filmy/getfilmjson.php?id=' + iid + '', headers=HEADERS)
	movie_loaded = json.loads(movie_data.text, "utf-8")
	movie = movie_loaded['film'][0]
	return movie
	
def list_searched_movie_streams(iid):
	try:
		movie = get_movie_info(iid)
	except Exception as e:
		xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30003))
		xbmcplugin.setContent(_handle, 'videos')
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return
	list_movie_streams(movie['url'],iid,movie)
	
def list_movie_streams(url,iid,movie):
	xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30003))
	xbmcplugin.setContent(_handle, 'videos')
	streams = []
	
	try:
		streams_data = _session.get('https://www.bombuj.eu/android_api/filmy/getlanguagesjson.php?url=' + url + '', headers=HEADERS)
		streams_loaded = json.loads(streams_data.text, "utf-8")
		streams = streams_loaded['typ']
		if not movie:
			movie = get_movie_info(iid)
	except Exception as e:
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return
		
	for stream in streams:
		list_item = xbmcgui.ListItem(label=stream['type'] + ' | ' + stream['vh'])
		list_item.setInfo('video', {'title': movie['name'],
									'genre': movie['zanre'],
									'year': movie['year'],
									'mediatype': 'video'})
		list_item.setArt({'thumb': COVERS_MOVIES + stream['url'] + '.jpg',
							'icon': COVERS_MOVIES + stream['url'] + '.jpg'})
		list_item.setProperty('IsPlayable', 'true')
		link = get_url(action='play', code=stream['code'], vh=stream['vh'], url=url, iid=iid)
		is_folder = False
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.endOfDirectory(_handle)

def list_series(category,listt):
	catName = category
	for cat in CATEGORIES:
		if cat['cat'] == category:
			catName = cat['msg']
			break
	lstName = listt
	for lst in LISTS:
		if lst['list'] == listt:
			lstName = lst['msg']
			break

	xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30102) + " / " + catName + " / " + lstName)
	xbmcplugin.setContent(_handle, 'videos')
	series = []
	
	try:
		data = _session.get(BOMBUJ_API + 'serialy/get_items_as_json.php?type=' + listt + '&zaner=' + category, headers=HEADERS)
		loaded = json.loads(data.text, "utf-8")
		series = loaded[listt]
	except Exception as e:
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return

	for serie in series:
		list_item = xbmcgui.ListItem(label=serie['nazov_1'])
		list_item.setInfo('video', {'title': serie['nazov_1'],
									'genre': serie['zaner'],
									'year': serie['rok'],
									'mediatype': 'video'})
		list_item.setArt({'thumb': COVERS_SERIES + serie['url'] + '.jpg',
							'icon': COVERS_SERIES + serie['url'] + '.jpg'})
		link = get_url(action='series_series', url=serie['url'], iid=serie['id'])
		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	
	xbmcplugin.endOfDirectory(_handle)

def get_series_info(iid):
	series_data = _session.get('https://www.bombuj.eu/android_api/serialy/getserialjson.php?id=' + iid + '', headers=HEADERS)
	series_loaded = json.loads(series_data.text, "utf-8")
	series = series_loaded['serial'][0]
	return series

def list_searched_series_series(iid):
	try:
		series = get_series_info(iid)
	except Exception as e:
		xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30106))
		xbmcplugin.setContent(_handle, 'videos')
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return
	list_series_series(series['url'],iid,series)
	
def list_series_series(url,iid,series):
	xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30106))
	xbmcplugin.setContent(_handle, 'videos')
	series_series = []
	
	try:
		series_series_data = _session.get('https://www.bombuj.eu/android_api/serialy/seriejson.php?url=' + url + '', headers=HEADERS)
		series_series_loaded = json.loads(series_series_data.text, "utf-8")
		series_series = series_series_loaded['serie']
		if not series:
			series = get_series_info(iid)
	except Exception as e:
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return
		
	for sse in series_series:
		name = _addon.getLocalizedString(30103) + ' ' + sse['cislo_serie']
		list_item = xbmcgui.ListItem(label=name)
		list_item.setInfo('video', {'title': series['nazov_1'],
									'genre': series['zaner'],
									'year': series['rok'],
									'mediatype': 'video'})
		list_item.setArt({'thumb': COVERS_SERIES + series['url'] + '.jpg',
							'icon': COVERS_SERIES + series['url'] + '.jpg'})
		link = get_url(action='series_episodes', serie=sse['cislo_serie'], url=url, iid=iid)
		is_folder = True
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.endOfDirectory(_handle)

def list_series_episodes(serie,url,iid):
	xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30104))
	xbmcplugin.setContent(_handle, 'videos')
	episodes = []
	
	try:
		episodes_data = _session.get('https://www.bombuj.eu/android_api/serialy/epizodyjson.php?url=' + url + '&seria=' + serie, headers=HEADERS)
		episodes_loaded = json.loads(episodes_data.text, "utf-8")
		episodes = episodes_loaded['epizody']
		series = get_series_info(iid)
	except Exception as e:
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30005), _addon.getLocalizedString(30006), _addon.getLocalizedString(30009), str(e))
		xbmcplugin.endOfDirectory(_handle)
		return
		
	for episode in episodes:
		name = _addon.getLocalizedString(30105) + ' ' + episode['cislo_epizody'] + " | " + episode['jazyk']
		list_item = xbmcgui.ListItem(label=name)
		list_item.setInfo('video', {'title': series['nazov_1'],
									'genre': series['zaner'],
									'mediatype': 'video'})
		list_item.setArt({'thumb': COVERS_SERIES + series['url'] + '.jpg',
							'icon': COVERS_SERIES + series['url'] + '.jpg'})
		list_item.setProperty('IsPlayable', 'true')
		link = get_url(action='play', code=episode['code'], vh='openload.io', url=url, iid=iid)
		is_folder = False
		xbmcplugin.addDirectoryItem(_handle, link, list_item, is_folder)
	xbmcplugin.endOfDirectory(_handle)


#import webbrowser
#webbrowser.open('https://olpair.com', new=1, autoraise=True)

def play_stream(code,vh,url,iid):
	path = ''
	subtitles = []
	if vh == 'openload.io':
		path = 'https://openload.co/embed/' + code
		try:
			embed_data = _session.get(path)
			captions = re.findall("<track.*kind=\"captions\".*/>", embed_data.text)
			if captions:
				srcreg = re.compile("<track.*src=\"((?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+)\".*/>")
				for cap in captions:
					src = srcreg.search(cap)
					if src:
						subtitles.append(src.group(1))
		except Exception as e:
			xbmc.log(str(e),level=xbmc.LOGNOTICE)
			traceback.print_exc()
			
		# TODO - open olpair? fork resolveurl?
		# webbrowser.open('https://olpair.com', new=1, autoraise=True)
	elif vh == 'streamango.com':
		path = 'https://streamango.com/embed/' + code
	elif vh == 'exashare.com' or vh == 'netu.tv':
		xbmcgui.Dialog().ok(vh, _addon.getLocalizedString(30010))
		
	else:
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30003), _addon.getLocalizedString(30004), 'URL: '+url + ' / ID: '+iid + ' / VH: '+vh)
	
	if path == '':
		xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())
		return
		
	try:
		resolved_url = resolveurl.resolve(path)
		listitem = xbmcgui.ListItem(path=resolved_url)
		if subtitles:
			listitem.setSubtitles(subtitles)
		xbmcplugin.setResolvedUrl(_handle, True, listitem)
	except Exception as e:
		xbmc.log(str(e),level=xbmc.LOGNOTICE)
		traceback.print_exc()
		xbmcgui.Dialog().ok(_addon.getLocalizedString(30000), _addon.getLocalizedString(30008), str(e))

def router(paramstring):
	params = dict(parse_qsl(paramstring))
	if params:
		if params['action'] == 'categories':
			list_categories(params['ctype'])
		elif params['action'] == 'search':
			list_search(params['ctype'])
		elif params['action'] == 'lists':
			category = ''
			if 'category' in params:
				category = params['category']
			list_lists(params['ctype'],category)
		elif params['action'] == 'movies':
			category = ''
			if 'category' in params:
				category = params['category']
			list_movies(category,params['listt'])
		elif params['action'] == 'movies_searched':
			list_searched_movie_streams(params['iid'])
		elif params['action'] == 'movie_streams':
			list_movie_streams(params['url'],params['iid'],{})
		elif params['action'] == 'series':
			category = ''
			if 'category' in params:
				category = params['category']
			list_series(category,params['listt'])
		elif params['action'] == 'series_searched':
			list_searched_series_series(params['iid'])
		elif params['action'] == 'series_series':
			list_series_series(params['url'],params['iid'],{})
		elif params['action'] == 'series_episodes':
			list_series_episodes(params['serie'],params['url'],params['iid'])
		elif params['action'] == 'play':
			play_stream(params['code'],params['vh'],params['url'],params['iid'])
		else:
			raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
	else:
		list_types()


if __name__ == '__main__':
	router(sys.argv[2][1:])
