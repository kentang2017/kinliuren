# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 09:37:59 2020

@author: hooki
"""


#干支
Gan = list("甲乙丙丁戊己庚辛壬癸")
Zhi = list("子丑寅卯辰巳午未申酉戌亥")
tiangan = '甲乙丙丁戊己庚辛壬癸'
dizhi = '子丑寅卯辰巳午未申酉戌亥'
Zhi2 = list("亥戌酉申未午巳辰卯寅丑子")

#寄干藏支
ganlivezhi = {("甲","寅"):"寅", ("乙","辰"):"辰", ("丙","戊", "巳"):"巳",("丁","己", "未"):"未",("庚","申"):"申", ("辛","戌"):"戌", ("壬", "亥"):"亥", ("癸", "丑"):"丑"}
shigangjigong = {"甲":"寅", "乙":"辰", "丙":"巳", "丁":"未", "戊":"巳", "己":"未", "庚":"申",  "辛":"戌", "壬":"亥", "癸":"丑", "寅":"寅", "辰":"辰", "巳":"巳", "未":"未", "巳":"巳", "未":"未", "申":"申",  "戌":"戌", "亥":"亥", "丑":"丑", "子":"子", "卯":"卯", "酉":"酉", "午":"午"}
sky_ganhe = {"甲":"巳", "乙":"庚", "丙":"辛", "丁":"壬", "戊":"癸"}

#驛馬
yima_dict = {"丑":"亥", "未":"巳"}

#生尅六親
liuqing_dict = {"被生":"父母", "生":"子孫", "尅":"妻財", "比和":"兄弟", "被尅":"官鬼"}
earth_zhihe = {tuple(list("巳酉丑")):"巳酉丑", tuple(list("寅午戌")):"寅午戌", tuple(list("亥卯未")):"亥卯未", tuple(list("申子辰")):"申子辰"}

#找旬
findshun = {'甲子':{'子':'甲', '丑':'乙', '寅':'丙', '卯':'丁', '辰':'戊', '巳':'己', '午':'庚', '未':'辛', '申':'壬',  '酉':'癸', '戌':'空', '亥':'空'}, '甲戌': {'子':'丙', '丑':'丁', '寅':'戊', '卯':'己', '辰':'庚', '巳':'辛', '午':'壬', '未':'癸', '申':'空',  '酉':'空', '戌':'甲', '亥':'乙'},  '甲申': {'子':'戊', '丑':'己', '寅':'庚', '卯':'辛', '辰':'壬', '巳':'癸', '午':'空', '未':'空', '申':'甲',  '酉':'乙', '戌':'丙', '亥':'丁'}, '甲午': {'子':'庚', '丑':'辛', '寅':'壬', '卯':'癸', '辰':'空', '巳':'空', '午':'甲', '未':'乙', '申':'丙',  '酉':'丁', '戌':'戊', '亥':'己'},  '甲辰': {'子':'壬', '丑':'癸', '寅':'空', '卯':'空', '辰':'甲', '巳':'乙', '午':'丙', '未':'丁', '申':'戊',  '酉':'己', '戌':'庚', '亥':'辛'},  '甲寅': {'子':'空', '丑':'空', '寅':'甲', '卯':'乙', '辰':'丙', '巳':'丁', '午':'戊', '未':'己', '申':'庚',  '酉':'辛', '戌':'壬', '亥':'癸'}}

#找月將
moon_general_dict = {("雨水","驚蟄"):"亥", 
       ("春分","清明"):"戌", 
       ("穀雨","立夏"):"酉", 
       ("小滿","芒種"):"申", 
       ("夏至","小暑"):"未", 
       ("大暑","立秋"):"午", 
       ("處暑","白露"):"巳",
       ("秋分","寒露"):"辰",
       ("霜降","立冬"):"卯",
       ("小雪","大雪"):"寅", 
       ("冬至","小寒"):"丑", 
       ("大寒","立春"):"子"}

#支干藏宮
zhigangcangong = list("子丑癸寅甲卯辰乙巳丙戊午未己申庚酉戌辛亥壬")

#干支五行
wuxing_relation = {("火水","金火", "木金", "水土", "土木"):"下賊上", ("水火","火金", "金木", "土水", "木土"):"上尅下", ("火火", "金金", "水水", "土土", "木木"):"比和", ("火木", "水金", "木水", "土火", "金土"):"下生上", ("木火", "金水", "水木", "火土", "土金"):"上生下"}
wuxing_relation_2 = {("火水","金火", "木金", "水土", "土木"):"被尅", ("水火","火金", "金木", "土水", "木土"):"尅", ("火火", "金金", "水水", "土土", "木木"):"比和", ("火木", "水金", "木水", "土火", "金土"):"被生", ("木火", "金水", "水木", "火土", "土金"):"生"}
ganzhiwuxing = {("甲","寅", "乙", "卯"):"木", ("丙", "巳", "丁", "午"):"火",  ("壬", "亥", "癸", "子"):"水", ("庚", "申", "辛", "酉"):"金", ("未", "丑", "戊","己","未", "辰", "戌"):"土"}
  
#日貴人 甲羊戊庚牛。乙猴已鼠求。丙雞丁豬位。壬癸兔蛇游。六辛逢虎上。陽貴日中 。
#夜貴人 甲牛戊庚羊乙鼠鄉。丙豬丁難上。壬中蛇癸兔藏。六辛逢午馬。陰貴夜時當。
daynight_richppl_dict = {tuple(list("卯辰巳午未申")):"晝", tuple(list("酉戌亥子丑寅")):"夜" }
guiren_dict = {"甲":{"晝":"丑", "夜":"未"}, tuple(list("戊庚")):{"晝":"丑", "夜":"未"}, "丙":{"晝":"酉", "夜":"亥"}, "丁":{"晝":"亥", "夜":"酉"}, "壬":{"晝":"卯", "夜":"巳"}, "癸":{"晝":"巳", "夜":"卯"}, "乙":{"晝":"申", "夜":"子"}, "己":{"晝":"子", "夜":"申"}, "辛":{"晝":"寅", "夜":"午"} }
rotation = {tuple(list("巳午未申酉戌")): "逆佈",  tuple(list("亥子丑寅卯辰")):"順佈"}

#天將
sky_generals = "貴蛇雀合勾龍空虎常玄陰后"
#sky_generals_rev ="貴后陰玄常虎空龍勾合雀蛇"

#刑沖
ying_chong = {tuple(list("寅巳申丑戌未子卯")):"刑", tuple(list("午辰酉亥")):"自刑"}
ying = {"寅":"巳", "巳":"申", "申":"寅", "丑":"戌", "戌":"未", "未":"丑", "子":"卯", "卯":"子"}
chong = {"子":"午","午":"子", "丑":"未","未":"丑", "寅":"申","申":"寅", "卯":"酉", "酉":"卯", "辰":"戌","戌":"辰", "巳":"亥", "亥":"巳"}
chong2 = {"子":"午","午":"子", "丑":"未","未":"丑", "寅":"申","申":"寅", "卯":"酉", "酉":"卯", "辰":"戌","戌":"辰", "巳":"亥", "亥":"巳"}


#基本東西
def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

def unique(list1): 
        unique_list = [] 
        for x in list1: 
            if x not in unique_list: 
                unique_list.append(x) 
            return x

def jiazi():
    jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
    return jiazi

def shunkong(daygangzhi,zhi):
    liujiashun_dict = {tuple(jiazi()[0:10]):'甲子', tuple(jiazi()[10:20]):"甲戌", tuple(jiazi()[20:30]):"甲申", tuple(jiazi()[30:40]):"甲午", tuple(jiazi()[40:50]):"甲辰",  tuple(jiazi()[50:60]):"甲寅"  }
    dayshun = multi_key_dict_get(liujiashun_dict, daygangzhi)
    return  multi_key_dict_get(findshun,dayshun).get(zhi)

def sky_pan_list(jieqi):
    get_moon_general = multi_key_dict_get(moon_general_dict, jieqi)
    return [new_zhi_list(get_moon_general), get_moon_general]

def new_zhi_list(zhi):
    zhihead_code = Zhi.index(zhi)
    res1 = []
    for i in range(len(Zhi)):
        res1.append( Zhi[zhihead_code % len(Zhi)])
        zhihead_code = zhihead_code + 1
    return res1

def new_zhi_list_reverse(zhi):
    Zhi2 = list("亥戌酉申未午巳辰卯寅丑子")
    zhihead_code = Zhi2.index(zhi)
    res1 = []
    for i in range(len(Zhi2)):
        res1.append( Zhi2[zhihead_code % len(Zhi2)])
        zhihead_code = zhihead_code + 1
    return res1

def Max(list):
    if len(list) == 1:
        return list[0]
    else:
        m = Max(list[1:])
        return m if m > list[0] else list[0]

def new_zhigangcangong_list(zhi):
    zhigangcangong = list("子丑癸寅甲卯辰乙巳丙戊午未己申庚酉戌辛亥壬")
    zhihead_code = zhigangcangong.index(zhi)
    res1 = []
    for i in range(len(zhigangcangong)):
        res1.append( zhigangcangong[zhihead_code % len(zhigangcangong)])
        zhihead_code = zhihead_code + 1
    return res1

def chong(zhi):
    chong = {"子":"午","午":"子", "丑":"未","未":"丑", "寅":"申","申":"寅", "卯":"酉", "酉":"卯", "辰":"戌","戌":"辰", "巳":"亥", "亥":"巳"}
    return chong.get(zhi)

def ganzhiwuxing(gangorzhi):
    ganzhiwuxing = {("甲","寅", "乙", "卯"):"木", ("丙", "巳", "丁", "午"):"火",  ("壬", "亥", "癸", "子"):"水", ("庚", "申", "辛", "酉"):"金", ("未", "丑", "戊","己","未", "辰", "戌"):"土"}
    return multi_key_dict_get(ganzhiwuxing, gangorzhi)


def find_ke_relation(ke):
    top_botton = ganzhiwuxing(ke[0])+ganzhiwuxing(ke[1])
    return multi_key_dict_get(wuxing_relation, top_botton)

def gangzhi_yinyang(gangorzhi):
    gangzhi_yingyang = {tuple(Gan[0::2] + Zhi[0::2]):"陽", tuple(Gan[1::2] + Zhi[1::2]):"陰"}
    yinyang = multi_key_dict_get(gangzhi_yingyang, gangorzhi)
    return yinyang

def duplicates(lst, item):
    result = [i for i, x in enumerate(lst) if x == item]
    if len(result) > 1:
        result =result
    elif len(result) ==1:
        result = lst.index(item)
    return result

    
def new_guiren_list(guiren):
    guirenhead_code = list(sky_generals)[::-1].index(guiren)
    res1 = []
    for i in range(len(list(sky_generals)[::-1])):
        res1.append( list(sky_generals)[::-1][guirenhead_code % len(list(sky_generals)[::-1])])
        guirenhead_code = guirenhead_code + 1
    return res1
    
    