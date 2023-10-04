# -*- coding: utf-8 -*-
"""
Created on Tue May  9 20:32:01 2023

@author: kentang
"""

import re
from math import pi
import ephem
from ephem import Sun, Date, Ecliptic, Equatorial
from sxtwl import fromSolar
from datetime import datetime
from itertools import cycle, repeat
import re
from lunar_python import Solar
from datetime import datetime
import opencc


tiangan = list('甲乙丙丁戊己庚辛壬癸')
dizhi = list('子丑寅卯辰巳午未申酉戌亥')

jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "驚蟄", "春分", "清明", "谷雨", "立夏",
     "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑","白露", "秋分", "寒露", "霜降", 
     "立冬", "小雪", "大雪"]
jieqi_name = re.findall('..', '春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒立春雨水驚蟄')

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

def new_list(olist, o):
    a = olist.index(o)
    res1 = olist[a:] + olist[:a]
    return res1

def ecliptic_lon(jd_utc):
    s=Sun(jd_utc)
    equ=Equatorial(s.ra,s.dec,epoch=jd_utc)
    e=Ecliptic(equ)
    return e.lon

def sta(jd):
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)
    return n

def iteration(jd,sta):
    s1=sta(jd)
    s0=s1
    dt=1.0
    while True:
        jd+=dt
        s=sta(jd)
        if s0!=s:
            s0=s
            dt=-dt/2
        if abs(dt)<0.0000001 and s!=s1:
            break
    return jd

def change(year, month, day, hour, minute):
    changets = Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)))
    return Date(changets - 24 * ephem.hour *30)

def jq(year, month, day, hour, minute):#从当前时间开始连续输出未来n个节气的时间
    #current =  datetime.strptime("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)), '%Y/%m/%d %H:%M:%S')
    current = Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2), str(minute).zfill(2)))
    jd = change(year, month, day, hour, minute)
    #jd = Date("{}/{}/{} {}:{}:00.00".format(str(b.year).zfill(4), str(b.month).zfill(2), str(b.day).zfill(2), str(b.hour).zfill(2), str(b.minute).zfill(2)  ))
    result = []
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)+1
    for i in range(3):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=Date(jd+1/3).tuple()
        dt = Date("{}/{}/{} {}:{}:00.00".format(d[0],d[1],d[2],d[3],d[4]).split(".")[0])
        time_info = {  dt:jieqi_name[n]}
        n+=1    
        result.append(time_info)
    j = [list(i.keys())[0] for i in result]
    if current > j[0] and current > j[1] and current > j[2]:
        return list(result[2].values())[0]
    if current > j[0] and current > j[1] and current <= j[2]:
        return list(result[1].values())[0]
    if current >= j[1] and current < j[2]:
        return list(result[1].values())[0]
    if current < j[1] and current < j[2]:
        return list(result[0].values())[0]

def gong_wangzhuai(j_q):
    wangzhuai = list("旺相胎沒死囚休廢")
    #wangzhuai_num = [3,4,9,2,7,6,1,8]
    wangzhuai_num = list("震巽離坤兌乾坎艮")
    wangzhuai_jieqi = {('春分','清明','穀雨'):'春分',
                        ('立夏','小滿','芒種'):'立夏',
                        ('夏至','小暑','大暑'):'夏至',
                        ('立秋','處暑','白露'):'立秋',
                        ('秋分','寒露','霜降'):'秋分',
                        ('立冬','小雪','大雪'):'立冬',
                        ('冬至','小寒','大寒'):'冬至',
                        ('立春','雨水','驚蟄'):'立春'}
    r1 = dict(zip(new_list(wangzhuai_num, dict(zip(jieqi_name[0::3],wangzhuai_num )).get(multi_key_dict_get(wangzhuai_jieqi, j_q))), wangzhuai))
    r2 = {v: k for k, v in r1.items()}
    return r1, r2



def jiazi():
    jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
    return jiazi
     
def repeat_list(n, thelist):
    return [repetition for i in thelist for repetition in repeat(i,n) ]
#分干支
def minutes_jiazi_d():
    t = []
    for h in range(0,24):
        for m in range(0,60):
            b = str(h)+":"+str(m)
            t.append(b)
    minutelist = dict(zip(t, cycle(repeat_list(2, jiazi()))))
    return minutelist
     
def gangzhi(year, month, day, hour, minute):
    if hour == 23:
        d = Date(round((Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2))) + 1 * hour), 3))
    else:
        d = Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG,mTG,dTG,hTG = "{}{}".format(tiangan[cdate.getYearGZ().tg], dizhi[cdate.getYearGZ().dz]), "{}{}".format(tiangan[cdate.getMonthGZ().tg],dizhi[cdate.getMonthGZ().dz]), "{}{}".format(tiangan[cdate.getDayGZ().tg], dizhi[cdate.getDayGZ().dz]), "{}{}".format(tiangan[cdate.getHourGZ(dd[3]).tg], dizhi[cdate.getHourGZ(dd[3]).dz])
    gangzhi_minute = minutes_jiazi_d().get(str(hour)+":"+str(minute))
    return [yTG, mTG, dTG, hTG, gangzhi_minute]
