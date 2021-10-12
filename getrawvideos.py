import requests
import json

import yt_dlp
import os


results =[]


session = requests.session()


def stringify(obj: dict) -> dict:
    """turn every value in the dictionary to a string"""
    for k, v in obj.items():
        if isinstance(v, dict):
            # if value is a dictionary, stringifiy recursively
            stringify(v)
            continue
        if not isinstance(v, str):
            if isinstance(v, bool):
                # False/True -> false/true
                obj[k] = str(v).lower()
            else:
                obj[k] = str(v)
    return obj


with open('cookies.json') as f:
    cookie_list: list = json.load(f)
    # create the cookie jar from the first cookie
    cookie_jar = requests.utils.cookiejar_from_dict(stringify(cookie_list[0]))
    # append the rest of the cookies
    for cookie in cookie_list[1:]:
        requests.utils.add_dict_to_cookiejar(cookie_jar, stringify(cookie))
    session.cookies = cookie_jar
    for i in range(1,20):
        payload = {'search_type': 'video', 'keyword': '哈利波特魔法觉醒','order':'pubdate','duration':'2','page':i}
        r = session.get('http://api.bilibili.com/x/web-interface/search/type', params=payload)
        # print(r.json().keys())
        results.extend(r.json()["data"]["result"])
idlist=[]
titlelist=[]
for i,item in enumerate(results):
    idlist.append(item['arcurl'])
    result={"title":item['title'],
    "tag":item['tag'],
    "description":item['description']+"original video from\r\n"+item['arcurl']}
    if not os.path.exists(str(item['id'])):
        os.makedirs(str(item['id']))
    os.chdir(str(item['id']))
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(item['arcurl'])
                # ydl.download([item['arcurl']])

        with open(str(item['id'])+'.json', 'w') as outfile:
            json.dump(result, outfile)        
    # titlelist.append(item['title']+' '+item['description'])
    os.chdir("..")

print('found videos numbers',len(idlist))
with open('videolist.txt', 'w') as outfile:
    json.dump(idlist, outfile)
