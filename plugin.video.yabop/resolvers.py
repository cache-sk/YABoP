# -*- coding: utf-8 -*-
# Module: default
# Author: cache
# Created on: 9.3.2019
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html


import re
import requests
import string


HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def resolve_mixdrop(code, url, default_headers={}):
    def processData(data, attr, current):
        prefix = 'MDCore.'+attr
        value = current
        if data.startswith(prefix):
            value = data[len(prefix):-1]
            while '"' in value:
                value = value[1:]
            if value.startswith('//'):
                value = 'https:' + value
        return value

    headers = {}
    headers.update(HEADERS)
    headers.update(default_headers)

    session = requests.Session()

    headers.update({'Referer': 'http://www.bombuj.tv/prehravace/mixdrop.co.php?url='+url+'&id78=12025'})
    embed = 'https://mixdrop.co/e/' + code
    embed_data = session.get(embed, headers=headers)

    packed = re.findall('<script>\s+MDCore.ref = "' + code + '";\s+([^\n]+)\s+</script>', embed_data.text, re.MULTILINE)
    if len(packed) == 1:
        s = packed[0]
        print s
        js = eval('unpack' + s[s.find('}(')+1:-1])
        print js
        mdcore = js.split(';')
        print mdcore
        sub = None
        referrer = embed
        path = ''
        for data in mdcore:
            if data.startswith('MDCore.vsr'):
                path = processData(data, 'vsr', path)
            elif data.startswith('MDCore.remotesub="'):
                sub = processData(data, 'remotesub', sub)
            #elif data.startswith('MDCore.referrer="'):
                #referrer = processData(data, 'referrer', referrer)

        result = {}
        if sub is not None:
            result.update({'sub':sub})
        if referrer is not None:
            path = path + '|Referer=' + referrer
        
        result.update({'path':path})

        return result
    else:
        return None


def resolve_netu(code, default_headers={}):
    headers = {}
    headers.update(HEADERS)
    headers.update(default_headers)

    session = requests.Session()

    path = 'https://hqq.tv/player/embed_player.php?vid=' + code + '&autoplay=no'

    response = session.get(path, headers=headers)

    cookie_obj = requests.cookies.create_cookie(domain='hqq.tv',name='bg6936066c1d4c2d5b4413428651de8ebf',value='0')
    #cookie_obj = requests.cookies.create_cookie(domain='hqq.tv',name='bg6936066c1d4c2d5b4413428651de8ebf',value='0')
    session.cookies.set_cookie(cookie_obj)
    #cookie_obj = requests.cookies.create_cookie(domain='hqq.tv',name='gt',value='796b0214ed51730ef6f4d632e227ef05')
    cookie_obj = requests.cookies.create_cookie(domain='hqq.tv',name='gt',value='36062398b0b97567587f60df5bda1363')
    session.cookies.set_cookie(cookie_obj)

    #TODO parse out url for wise

    #wise_data = session.get('https://storage.googleapis.com/loadermain.appspot.com/main.js').text
    #wise = wise_data[1:]
    #data_unwise = jswise(wise).replace("\\", "")


    #TODO get adb, token captcha?

    headers.update({'X-Requested-With': 'XMLHttpRequest', 'Referer': path, 'TE':'Trailers',
                    'Accept': '*/*, */*','Accept-Language': 'sk,cs;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Connection': 'keep-alive','Pragma': 'no-cache','Cache-Control': 'no-cache'})
                    #'Accept-Encoding': 'gzip, deflate, br',

    ip = session.get("https://hqq.tv/player/ip.php", headers=headers).text
    #TODO ?

    #md5url = "https://hqq.tv/player/get_md5.php?ver=2&secure=0&adb=0%2F&v=" + code + "&token=&gt="
    #response = session.get(md5url, headers=headers)
    print session.cookies

#{"Cookies požiadavky":{"bg6936066c1d4c2d5b4413428651de8ebf":"0","GED_PLAYLIST_ACTIVITY":"W3sidSI6IjNHWlYiLCJ0c2wiOjE1NzI3NDA4OTQsIm52IjoxLCJ1cHQiOjE1NzI3NDA4OTEsImx0IjoxNTcyNzQwODkxfV0.","gip":"no","gt":"6b96acf0c463696e7f6216799b0f78e1"}}
#cookie_obj = requests.cookies.create_cookie(domain='hqq.tv',name='bg6936066c1d4c2d5b4413428651de8ebf',value='0')
#cookie_obj = requests.cookies.create_cookie(domain='hqq.tv',name='gt',value='796b0214ed51730ef6f4d632e227ef05')

#https://hqq.tv/player/get_md5.php?ver=3&secure=0&adb=0%2F&v=eGhmdkZhMkdadFdGYTNFUWVtTEcxQT09&token=03AOLTBLQ0ol1eVuJLMrDgKCcb2YAgeWmiX7eTjy8riITPF7s5-EZ5RU3qVVnYgiJrTo4gLkjoCPtQZ62-OPmMes5qnyDt8aj-4BKghRnphfokpUg1f4UqJLWc4u-f95r0skfj4IpaH4DXgshw3ksEaFjBuGe6TsywlpJyLkzuytgXfh6KMM-4BdU_RwRH5EH3awqo8249aOuLtYYiSgtPMVtUy9gQjh0cxiDTb2O64ufpka7ogLck7SVQle6eNdTg1PZzwrT_ExJH_IUaE9t_1bVPunU92XAUs2Ik_QUzVtwaSxSN8eE9VSrps1se-L_mcozabMvG7eXHcBPWqRPhdtf3vjotCYuR2vlwvy2ErUh8SezJ09qtP78M91UD_SpZjHmNxPPqDLfwFvb89mFFZSUwg0qOnARsRaRMk_JbQrvw53a23DJuheSuu9RLisqVonxYCPO7vIFpkeVAyBVYdXKa7ibchQXwfS4ACijsKOcVid_DwNJN0Qzd-LNDN4977QaCIPLlN2Yk&gt=

    md5url = "https://hqq.tv/player/get_md5.php?ver=3&secure=0&adb=0%2F&v=" + code + "&token=&gt="
    response = session.get(md5url, headers=headers)
    print response.text
    data = response.json()
    media_url = "https:" + tb(data["obf_link"][1:])
    del headers['X-Requested-With']
    del headers['Accept']
    headers.update({'Origin': 'https://hqq.tv'})

    print headers

    return {'path':media_url,'headers':headers}

def tb(b_m3u8_2):
    j = 0
    s2 = ""
    while j < len(b_m3u8_2):
        s2 += "\\u0" + b_m3u8_2[j:(j + 3)]
        j += 3

    return s2.decode('unicode-escape').encode('ASCII', 'ignore')

## loop2unobfuscated
def jswise(wise):
    print wise
    while True:
        wise = re.search("var\s.+?\('([^']+)','([^']+)','([^']+)','([^']+)'\)", wise, re.DOTALL)
        if not wise: break
        ret = wise = self.js_wise(wise.groups())

    return ret

## js2python
def js_wise(wise):
    w, i, s, e = wise

    v0 = 0;
    v1 = 0;
    v2 = 0
    v3 = [];
    v4 = []

    while True:
        if v0 < 5:
            v4.append(w[v0])
        elif v0 < len(w):
            v3.append(w[v0])
        v0 += 1
        if v1 < 5:
            v4.append(i[v1])
        elif v1 < len(i):
            v3.append(i[v1])
        v1 += 1
        if v2 < 5:
            v4.append(s[v2])
        elif v2 < len(s):
            v3.append(s[v2])
        v2 += 1
        if len(w) + len(i) + len(s) + len(e) == len(v3) + len(v4) + len(e): break

    v5 = "".join(v3);
    v6 = "".join(v4)
    v1 = 0
    v7 = []

    for v0 in range(0, len(v3), 2):
        v8 = -1
        if ord(v6[v1]) % 2: v8 = 1
        v7.append(chr(int(v5[v0:v0 + 2], 36) - v8))
        v1 += 1
        if v1 >= len(v4): v1 = 0

    return "".join(v7)

# thanks to https://stackoverflow.com/a/2267446
def int2base(x, base):
    digs = string.digits + string.ascii_letters
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

# thanks to https://stackoverflow.com/a/5995122
def unpack(p, a, c, k, e=None, d=None):
    ''' unpack
    Unpacker for the popular Javascript compression algorithm.

    @param  p  template code
    @param  a  radix for variables in p
    @param  c  number of variables in p
    @param  k  list of c variable substitutions
    @param  e  not used
    @param  d  not used
    @return p  decompressed string
    '''
    # Paul Koppen, 2011
    for i in xrange(c-1,-1,-1):
        if k[i]:
            p = re.sub('\\b'+int2base(i,a)+'\\b', k[i], p)
    return p
