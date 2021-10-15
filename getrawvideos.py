import requests
import json

import yt_dlp
import os
import subprocess

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
    idlist=[]    
    for i in range(1,20):
        payload = {'search_type': 'video', 'keyword': '阿瓦达索命咒','order':'pubdate','duration':'0','page':i}
        r = session.get('http://api.bilibili.com/x/web-interface/search/type', params=payload)
        # print(r.json().keys())
        results.extend(r.json()["data"]["result"])
        # result={"title":'阿瓦达索命咒 compilation'+str(i),
        # "tag":item['tag'],        
        # "description":"automatically bot  generate from internet.any copyright issue pls contact us\r\n"}        

        if not os.path.exists('harry'+os.sep+str(i)):
            os.makedirs('harry'+os.sep+str(i))
        os.chdir('harry'+os.sep+str(i))
        for i,item in enumerate(r.json()["data"]["result"]):



            ydl_opts = {'retries': 10}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print('donwloading----',item['arcurl'])
                # ydl.download(item['arcurl'])

                ydl.download([item['arcurl']])
        with open('test.sh','w') as f:
            f.write('for f in *.flv ; do echo file \'$f\' >> list.txt; done && ffmpeg -f concat -safe 0 -i list.txt -s 1280x720 -crf 24 stitched-video.mp4 && rm list.txt')
            f.write('\r')
            f.write('for f in *.mp4 ; do echo file \'$f\' >> list.txt; done && ffmpeg -f concat -safe 0 -i list.txt -s 1280x720 -crf 24 stitched-video.mp4 && rm list.txt')

        subprocess.call(['sh', './test.sh'])                        
 
        os.chdir('../../')


# 哈利波特 魔法覺醒,哈利波特魔法覺醒卡組,哈利波特 教學,索命咒,索命咒卡組,佛地魔卡組,啊哇呾喀呾啦,哈利波特 秒殺流,    Action-adventure game,Action game,Role-playing video game,Strategy video game,Video game culture
