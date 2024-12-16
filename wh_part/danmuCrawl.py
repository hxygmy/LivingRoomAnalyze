import os
import re
import time

import pandas as pd
import requests
from tqdm import trange


def get_url(oid, start, end):
    '''
    获取指定日期的弹幕
    oid：视频oid
    start，end：起止日期
    '''
    url_list = []

    date_list = [i for i in pd.date_range(start, end).strftime('%Y-%m-%d')]

    for date in date_list:
        url = f"https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={oid}&date={date}"
        url_list.append(url)

    return url_list


def get_danmu(url_list, name):
    '''
    下载弹幕存至本地txt
    '''
    headers = {"cookie": "buvid3=BBDEBCBE-948F-3B84-C24F-4CC35B6943EE52230infoc; b_nut=1717251852; _uuid=C3E37DAD-46FD-10C10A-5F87-AAAEB7EEB421054679infoc; enable_web_push=DISABLE; buvid4=68A1A5DA-D480-FDD8-8334-A4513215715A56267-024060114-vlv%2BbT2KnwilWpmeJ%2BRwTw%3D%3D; header_theme_version=CLOSE; DedeUserID=513717222; DedeUserID__ckMd5=91fbf483813dc3da; rpdid=|()klluY)m~0J'u~u~kmYk|u; is-2022-channel=1; buvid_fp_plain=undefined; LIVE_BUVID=AUTO1417179306652727; CURRENT_BLACKGAP=0; share_source_origin=QQ; hit-dyn-v2=1; fingerprint=79b0383ea68ba3bacbf28948aa230633; CURRENT_QUALITY=116; buvid_fp=79b0383ea68ba3bacbf28948aa230633; match_float_version=ENABLE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM4MjQzMTgsImlhdCI6MTczMzU2NTA1OCwicGx0IjotMX0.-NcSkgkY00EdMA32DR58OyKgdBEmYWbhAmJX6DNOHhM; bili_ticket_expires=1733824258; home_feed_column=5; browser_resolution=1707-838; SESSDATA=ab549bd4%2C1749281506%2C2e3b2%2Ac1CjCttOCPnvb_cZAEevyAXhbdP3BMLiVcWMWYtbQvZrrWDOg20-psXDsF_2aGwWlx4TwSVlg4eFN0VFlJQkFMTnB3NkdxNUp5WHprcFEwN0RWQ2xFLTE2UlRKZFZfQ0hTQW5LWXRYYW9rRDVpUFR6MXQ5Y2N4NWxPbXE3aDlyY0NkRU02MVZDZ1VRIIEC; bili_jct=34364e7b7de11415610b528ca61a93df; sid=8ofiobn9; bsource=search_google; CURRENT_FNVAL=4048; PVID=11; b_lsid=1044423106_193AF69BA96; bp_t_offset_513717222=1009222481682104320",
               "origin": "https://www.bilibili.com",
               "referer": "https://www.bilibili.com/video/BV1yt4y1Q7SS/?spm_id_from=333.337.search-card.all.click&vd_source=e949b11f18ed52e277150a9b969a1452",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-site",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

    file_name = f"{name}_danmu.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        for i in trange(len(url_list)):
            url = url_list[i]
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            content_list = re.findall('[\u4e00-\u9fa5]+', res.text)
            print(len(content_list))
            for items in content_list:
                file.write(items)
                file.write("\n")
            time.sleep(2)



if __name__ == '__main__':
    start="2024-12-06"
    end="2024-12-10"
    # name="敢杀我的马"
    # oid="210738676"
    name="华为"
    oid="27199866041"
    url_list=get_url(oid,start,end)
    get_danmu(url_list,name)
    print(f"{name}.txt已生成")
