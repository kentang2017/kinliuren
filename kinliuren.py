# -*- coding: utf-8 -*-
"""
Created on Sun Dec  22 16:22:37 2019

@author: ken tang
@email: kinyeah@gmail.com
"""

from collections import Counter

Gan = list("甲乙丙丁戊己庚辛壬癸")
Zhi = list("子丑寅卯辰巳午未申酉戌亥")
ganlivezhi = {("甲","寅"):"寅", ("乙","辰"):"辰", ("丙","戊", "巳"):"巳",("丁","己", "未"):"未",("庚","申"):"申", ("辛","戌"):"戌", ("壬", "亥"):"亥", ("癸", "丑"):"丑"}
wuxing_relation = {("火水","金火", "木金", "水土", "土木"):"下賊上", ("水火","火金", "金木", "土水", "木土"):"上尅下", ("火火", "金金", "水水", "土土", "木木"):"比和", ("火木", "水金", "木水", "土火", "金土"):"下生上", ("木火", "金水", "水木", "火土", "土金"):"上生下"}
wuxing_relation_2 = {("火水","金火", "木金", "水土", "土木"):"被尅", ("水火","火金", "金木", "土水", "木土"):"尅", ("火火", "金金", "水水", "土土", "木木"):"比和", ("火木", "水金", "木水", "土火", "金土"):"被生", ("木火", "金水", "水木", "火土", "土金"):"生"}
liuqing_dict = {"被生":"父母", "生":"子孫", "尅":"妻財", "比和":"兄弟", "被尅":"官鬼"}
shigangjigong = {"甲":"寅", "乙":"辰", "丙":"巳", "丁":"未", "戊":"巳", "己":"未", "庚":"申",  "辛":"戌", "壬":"亥", "癸":"丑", "寅":"寅", "辰":"辰", "巳":"巳", "未":"未", "巳":"巳", "未":"未", "申":"申",  "戌":"戌", "亥":"亥", "丑":"丑", "子":"子", "卯":"卯", "酉":"酉", "午":"午"}
sky_ganhe = {"甲":"巳", "乙":"庚", "丙":"辛", "丁":"壬", "戊":"癸"}
yima_dict = {"丑":"亥", "未":"巳"}
earth_zhihe = {tuple(list("巳酉丑")):"巳酉丑", tuple(list("寅午戌")):"寅午戌", tuple(list("亥卯未")):"亥卯未", tuple(list("申子辰")):"申子辰"}

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
    tiangan = '甲乙丙丁戊己庚辛壬癸'
    dizhi = '子丑寅卯辰巳午未申酉戌亥'
    jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
    return jiazi

def sky_pan_list(jieqi):
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
    get_moon_general = multi_key_dict_get(moon_general_dict, jieqi)
    return [new_zhi_list(get_moon_general), get_moon_general]

def new_zhi_list(zhi):
    zhihead_code = Zhi.index(zhi)
    res1 = []
    for i in range(len(Zhi)):
        res1.append( Zhi[zhihead_code % len(Zhi)])
        zhihead_code = zhihead_code + 1
    return res1

def new_shigangcangong_list(zhi):
    shigangcangong = list("子丑癸寅甲卯辰乙巳丙戊午未己申庚酉戌辛亥壬")
    zhihead_code = shigangcangong.index(zhi)
    res1 = []
    for i in range(len(shigangcangong)):
        res1.append( shigangcangong[zhihead_code % len(shigangcangong)])
        zhihead_code = zhihead_code + 1
    return res1

def chong(zhi):
    chong = {"子":"午", "丑":"未", "寅":"申", "卯":"酉", "辰":"戌", "巳":"亥", "申":"寅"}
    return chong.get(zhi)

def sky_n_earth_list(jieqi, hourgangzhi):
    earth = new_zhi_list(hourgangzhi[1])
    sky = sky_pan_list(jieqi)[0]
    return dict(zip(earth, sky))

def earth_n_sky_list(jieqi, hourgangzhi):
    earth = new_zhi_list(hourgangzhi[1])
    sky = sky_pan_list(jieqi)[0]
    return dict(zip(sky, earth))

def all_sike(jieqi, daygangzhi, hourgangzhi):
    yike = sky_n_earth_list(jieqi,hourgangzhi)[shigangjigong.get(daygangzhi[0])] + daygangzhi[0]
    sky_n_earth = sky_n_earth_list(jieqi,hourgangzhi)
    erke = sky_n_earth.get(yike[0]) + yike[0]
    sanke = sky_n_earth.get(daygangzhi[1]) + daygangzhi[1]
    sike = sky_n_earth.get(sanke[0]) + sanke[0]
    return [sike, sanke, erke, yike]

def ganzhiwuxing(gangorzhi):
    ganzhiwuxing = {("甲","寅", "乙", "卯"):"木", ("丙", "巳", "丁", "午"):"火",  ("壬", "亥", "癸", "子"):"水", ("庚", "申", "辛", "酉"):"金", ("未", "丑", "戊","己","未", "辰", "戌"):"土"}
    return multi_key_dict_get(ganzhiwuxing, gangorzhi)

def find_ke_relation(ke):
    top_botton = ganzhiwuxing(ke[0])+ganzhiwuxing(ke[1])
    return multi_key_dict_get(wuxing_relation, top_botton)

def find_sike_relations(jieqi, daygangzhi, hourgangzhi):
    sike_list = []
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    if sike_list.count("下賊上") == 2 and sike_list.count("上尅下") == 2:
        classify = "下賊上"
    elif sike_list.count("上尅下") > 1 and sike_list.count("下賊上") == 1:
        classify = "下賊上"
    elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 3:
        classify = "下賊上"
    elif sike_list.count("下賊上") == 2 and sike_list.count("上尅下") == 1 :
        classify = "下賊上"
    elif sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
        classify = "試其他"
    dayganzhi_wuxing = ganzhiwuxing(daygangzhi[0])
    dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
    for i in sike:
        b = find_ke_relation(i)
        sike_list.append(b)
    wuxing_ke = [ganzhiwuxing(i[0]) for i in sike]
    shangke_list = []
    for d in wuxing_ke:
        shangke = multi_key_dict_get(wuxing_relation_2, d+dayganzhi_wuxing) 
        shangke_list.append(shangke)
    dayganzhi_same_location = ["甲寅", "丁未", "己未", "庚申", "癸丑"]
    res = [i for i in jiazi() if i not in dayganzhi_same_location] 
    checkdayganzhi_dict = {tuple(dayganzhi_same_location) :"日干支同位", tuple(res):"日干支不同位"}
    fanyin_days = ["丁丑","己丑", "辛丑", "辛未"]
    bazhuan_fanyin_days = ["丁未", "己未"]
    jiazi_remove_fanyin =  [i for i in jiazi() if i not in fanyin_days] 
    fanyin_day_dict = {tuple(fanyin_days):"反吟",tuple(fanyin_days):"反吟八專",tuple(jiazi_remove_fanyin+bazhuan_fanyin_days):"非反吟"}
    checkdayganzhi = multi_key_dict_get(checkdayganzhi_dict, daygangzhi)
    checkfanyin = multi_key_dict_get(fanyin_day_dict, daygangzhi)
    moon_general = sky_pan_list(jieqi)[1]
    checkmoongeneralconflicttohour = multi_key_dict_get(wuxing_relation_2, ganzhiwuxing(moon_general)+ganzhiwuxing(hourgangzhi[1]))
    if hourgangzhi[1] == moon_general:
        checkfuyin = "伏吟"
    else:
        checkfuyin = "非伏吟"
    
    if sike_list.count("上尅下") == 0 and sike_list.count("下賊上") == 0:
        findtrue = ["試賊尅涉害以外方法",  "沒有",   "沒有", classify,  "沒有",  "沒有"]
        return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])
        
    elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 0:
        findtrue = ["試賊尅", sike_list.index("上尅下"),  "沒有", classify, "沒有", "沒有"]
        return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])
    
    elif sike_list.count("下賊上") == 1:
        findtrue = ["試賊尅", sike_list.index("下賊上"),  "沒有", classify, "沒有", "沒有"]
        return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])
    
    elif sike_list.count("下賊上") >1:
        find_ke = duplicates(sike_list, "下賊上")
        zeikeshang_list = []
        for i in find_ke:
            zeike = sike[i]
            zeikeshang_list.append(zeike)
        yy_list = []
        for y in zeikeshang_list:
            yy = gangzhi_yinyang(y[0])
            yy_list.append(yy)
        nn_list = []
        for n in yy_list:
            if n == dayganzhi_yy:
                p = "True"
            else:
                p = "False"
            nn_list.append(p)
        if nn_list.count("True") == len(nn_list)  or nn_list.count("False") == len(nn_list):
            findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list]
        else:
            findtrue = ["試比用", find_ke,  zeikeshang_list, classify, nn_list, yy_list]
        return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])

    elif sike_list.count("上尅下")>1:
        find_ke = duplicates(sike_list, "上尅下")
        zeikeshang_list = []
        for i in find_ke:
            zeike = sike[i]
            zeikeshang_list.append(zeike)
        yy_list = []
        for y in zeikeshang_list:
            yy = gangzhi_yinyang(y[0])
            yy_list.append(yy)
        nn_list = []
        for n in yy_list:
            if n == dayganzhi_yy:
                p = "True"
            else:
                p = "False"
            nn_list.append(p)
        if nn_list.count("True") > 1:
            findtrue = ["試涉害", find_ke,  zeikeshang_list, "上尅下", nn_list, yy_list] #結果, 尅克位置, 課式
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])
       
        try:
            findtrue = ["試比用", find_ke,  zeikeshang_list, classify , nn_list, yy_list]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])

        except ValueError :
            findtrue = ["沒涉害", find_ke,  zeikeshang_list, [zeikeshang_list[b] for b in duplicates(nn_list, "True")]] #結果, 尅克位置, 課式
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(daygangzhi[0])

def duplicates(lst, item):
    result = [i for i, x in enumerate(lst) if x == item]
    if len(result) > 1:
        result =result
    elif len(result) ==1:
        result = lst.index(item)
    return result

def sike_dict(jieqi, daygangzhi, hourgangzhi):
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0]
    dyingyang = gangzhi_yinyang(daygangzhi[0])
    sike_yingyan = [gangzhi_yinyang(i[0]) for i in sike]
    return sike, sike_list, dyingyang, sike_yingyan
    
def gangzhi_yinyang(gangorzhi):
    gangzhi_yingyang = {tuple(Gan[0::2] + Zhi[0::2]):"陽", tuple(Gan[1::2] + Zhi[1::2]):"陰"}
    yinyang = multi_key_dict_get(gangzhi_yingyang, gangorzhi)
    return yinyang

def find_three_pass(jieqi, hourgangzhi, firstpass):
    secondpass = sky_n_earth_list(jieqi, hourgangzhi).get(firstpass)
    thirdpass = sky_n_earth_list(jieqi, hourgangzhi).get(secondpass)
    return [firstpass, secondpass, thirdpass]
    
def zeike(jieqi, daygangzhi, hourgangzhi):
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)
    #沒有上尅下或下賊上
    if sike_list[0].count("上尅下") == 0 and sike_list[0].count("下賊上") == 0:
        findtrue =  "不適用，或試他法" 
        return findtrue
    #多於一個上尅下或下賊上
    elif sike_list[0].count("下賊上") > 1:
        findtrue =  "不適用，或試他法" 
        return findtrue
     #多於一個上尅下或下賊上
    elif sike_list[0].count("上尅下") >= 2 and sike_list[0].count("下賊上") == 0: 
        findtrue =  "不適用，或試他法" 
        return findtrue
    #一個下賊上
    elif sike_list[0].count("下賊上") == 1 :
        findtrue =  ["賊尅","重審", find_three_pass(jieqi, hourgangzhi, sike[sike_list[0].index("下賊上")][0])]
        return findtrue
    #一個上尅下
    elif sike_list[0].count("上尅下") == 1 and sike_list[0].count("下賊上") == 0:
        findtrue =  ["賊尅","元首", find_three_pass(jieqi, hourgangzhi, sike[sike_list[0].index("上尅下")][0])]
        return findtrue

def biyung(jieqi, daygangzhi, hourgangzhi):
    sike_list = all_sike(jieqi, daygangzhi, hourgangzhi)
    filter_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7]
    filter_list_four_ke = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][2]
    filter_list_yy = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][5]
    filter_list_nature = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][3]
    dayganzhi_yy = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[8]
    if filter_list[0] == "試賊尅":
        findtrue =  "不適用，或試他法"
        return findtrue
    elif filter_list[0] == "試賊尅涉害以外方法":
        findtrue =  "不適用，或試他法"
        return findtrue
    elif filter_list[0] == "試涉害":
        findtrue =  "不適用，或試他法"
        return findtrue
    elif len(find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][4]) == 2 and find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][4].count("True") == 2:
        findtrue =  "不適用，或試他法"
        return findtrue
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[5] == "尅" and sike_list[0].count("下賊上") > 1:
        findtrue = ["比用", "無依", [sike[nn_list.index("True")], chong(sike[nn_list.index("True")]), chong(chong(sike[nn_list.index("True")]))]]
        return findtrue
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0].count("下賊上") == 2:
        if filter_list_yy[0] == dayganzhi_yy:
            findtrue = ["比用", "比用", find_three_pass(jieqi, hourgangzhi,filter_list_four_ke[0][0])]
        elif filter_list_yy[1] == dayganzhi_yy:
            findtrue = ["比用", "比用", find_three_pass(jieqi, hourgangzhi,filter_list_four_ke[1][0])]
        return findtrue
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0].count("上尅下") ==2 and find_sike_relations(jieqi, daygangzhi, hourgangzhi).count("下賊上") == 0:
        if filter_list_yy[0] == dayganzhi_yy:
            findtrue = ["比用", "知一", find_three_pass(jieqi, hourgangzhi, filter_list_four_ke[0][0])]
        elif filter_list_yy[1] == dayganzhi_yy:
            findtrue = ["比用", "知一", find_three_pass(jieqi, hourgangzhi, filter_list_four_ke[1][0])]
        return findtrue

def fiter_four_ke(jieqi, daygangzhi, hourgangzhi):
    a = find_sike_relations(jieqi, daygangzhi, hourgangzhi )[7][2]
    b = find_sike_relations(jieqi, daygangzhi, hourgangzhi )[7][4]
    d = duplicates(b, "True")
    ilist = []
    for i in d:
        item = a[i]
        ilist.append(item)
    return ilist

def compare_shehai_number(jieqi, daygangzhi, hourgangzhi):
    a = fiter_four_ke(jieqi, daygangzhi, hourgangzhi)
    if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][0] == "試涉害":
        c = [a[i][0] for i in range(0, len(a))]
        t = [a[i][1] for i in range(0, len(a))]
        if shigangjigong.get(t[-1]) == None:
            t = t
        elif shigangjigong.get(t[-1]) is not None:
            t[-1] = shigangjigong.get(t[-1])
    shehai_number2 = []
    khead = []
    biyung_result_reorder_list3 = []
    try:
        for i in range(0,len(a)):
            for k, v in sky_n_earth_list(jieqi, hourgangzhi).items():
                    if v == a[i][0]:
                        khead.append(k)
        for i in range(0,len(a)):
            biyung_result_reorder = new_shigangcangong_list(khead[i])[0: new_shigangcangong_list(khead[i]).index(a[i][0])+1]
            biyung_result_reorder_list3.append([ganzhiwuxing(c[i][0])+k  for k in [ganzhiwuxing(j) for j in biyung_result_reorder]].count((ganzhiwuxing(a[i][0])+ganzhiwuxing(a[i][1]))))
        for s in biyung_result_reorder_list3:
            shehai_number = c[biyung_result_reorder_list3.index(s)]
            shehai_number2.append(shehai_number)
        shehai_dict = dict(zip(biyung_result_reorder_list3, shehai_number2))
        if biyung_result_reorder_list3[0] == biyung_result_reorder_list3[1]:
            result = ["找孟仲季地", a, t, c]
        elif biyung_result_reorder_list3[0] > biyung_result_reorder_list3[1]:
            result = [shehai_dict.get(biyung_result_reorder_list3[0]), shehai_dict] 
        elif biyung_result_reorder_list3[1] > biyung_result_reorder_list3[0]:
            result = [shehai_dict.get(biyung_result_reorder_list3[1]), shehai_dict] 
    except TypeError:
        result = ["不適用，或試他法"]
    return result

def convert_munchongji(jieqi, daygangzhi, hourgangzhi):
    munconji = {tuple("寅申巳亥"):"孟",  tuple("子午卯酉"):"仲", tuple("辰戌丑未"):"季"}
    head = compare_shehai_number(jieqi, daygangzhi, hourgangzhi)[2]
    tail = compare_shehai_number(jieqi, daygangzhi, hourgangzhi)[3]
    head_convert = []
    tail_convert = []
    for a in head:
        g =  multi_key_dict_get(munconji, a)
        head_convert.append(g)
    for k in tail:
        l = multi_key_dict_get(munconji, k)
        tail_convert.append(l)
    if compare_shehai_number(jieqi, daygangzhi, hourgangzhi)[0] == "找孟仲季地":
        result = [head, head_convert, tail, tail_convert]
    else:
        result = ["不適用"]
    return result
        
def convert_munchongji_shehai_number(jieqi, daygangzhi, hourgangzhi):
    munconji = {tuple("寅申巳亥"):"孟",  tuple("子午卯酉"):"仲", tuple("辰戌丑未"):"季"}
    head = [shigangjigong.get(i) for i in compare_shehai_number(jieqi, daygangzhi, hourgangzhi)[2]]
    tail = [shigangjigong.get(i) for i in compare_shehai_number(jieqi, daygangzhi, hourgangzhi)[3]]
    head_convert = []
    tail_convert = []
    for a in head:
        g =  multi_key_dict_get(munconji, a)
        head_convert.append(g)
    for k in tail:
        l = multi_key_dict_get(munconji, k)
        tail_convert.append(l)
    if compare_shehai_number(jieqi, daygangzhi, hourgangzhi)[0] == "找孟仲季地":
        result = [head, head_convert, tail, tail_convert]
    else:
        result = "不適用"
    return result

def shehai(jieqi, daygangzhi, hourgangzhi):
    shangke = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0]
    if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][0] == "試涉害": 
        if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][2][0] == find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][2][1]:
            chuchuan = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][2][0][0]
            result = ["涉害", "涉害",  find_three_pass(jieqi, hourgangzhi, chuchuan)] 
        elif compare_shehai_number(jieqi, daygangzhi, hourgangzhi) == "不適用":
            result = "不適用，或試他法"
            return result

        elif shangke.count("上尅下") == 0 and shangke.count("下賊上") == 0:
            result = "不適用，或試他法"
            return result

        elif shangke.count("上尅下") >= 0 and shangke.count("下賊上") == 1:
            result = "不適用，或試他法"
            return result

        elif shangke.count("上尅下") >= 2 and shangke.count("下賊上") == 0:
            reducing = compare_shehai_number(jieqi, daygangzhi, hourgangzhi)

            if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][0] == "試比用":
                result = "不適用，或試他法"
                return result

            if len(reducing[0]) == 1:
                result = ["涉害", find_three_pass(jieqi, hourgangzhi, reducing[0])]

            elif reducing[0] == "找孟仲季地":
                convert = convert_munchongji_shehai_number(jieqi, daygangzhi, hourgangzhi)
                convert_dict = {convert[0][0]+convert[2][0]: convert[1][0]+convert[3][0], convert[0][1]+convert[2][1]: convert[1][1]+convert[3][1] }
                change_daygangzhi =  shigangjigong.get(daygangzhi[0])
                convert_result_k = list(convert_dict.keys())
                convert_result_v = list(convert_dict.values())
                convert_result_head = [i[0] for i in convert_result_k]
                convert_result_tail = [i[1] for i in convert_result_k]
                dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
                if convert_result_v[0] == "孟季" or "仲季" or "季季" or "季仲" or "季孟":
                    if convert_result_v[1][0] == "孟" or "仲":
                        chuchuan = convert_result_k[1][0]
                        name = "見機"
                
                elif convert_result_v[0][0] == convert_result_v[0][1]:
                    if dayganzhi_yy == convert_result_k[0][0]:
                        chuchuan = convert_result_k[0][0]

                    elif dayganzhi_yy == convert_result_k[1][0]:
                        chuchuan = convert_result_k[1][0]
                        name = "綴瑕"
                
                result = ["涉害", name,  find_three_pass(jieqi, hourgangzhi, chuchuan)] 
                return result


        if shangke.count("上尅下") <= 2 and shangke.count("下賊上") >= 2:
            reducing = compare_shehai_number(jieqi, daygangzhi, hourgangzhi)
            if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][0] == "試比用":
                result = "不適用，或試他法"
                return result

            elif len(reducing[0]) == 1:
                result = ["涉害", "涉害", find_three_pass(jieqi, hourgangzhi, reducing[0])]
                return result

            elif reducing[0] == "找孟仲季地":
                converting = convert_munchongji_shehai_number(jieqi, daygangzhi, hourgangzhi)
                if converting[2][0] == converting[2][1]:
                    result =  ["返吟", "涉害", find_three_pass(jieqi, hourgangzhi, converting[2][0])]
                    
                return result


        if shangke.count("上尅下") == 1 and shangke.count("下賊上") == 3:
            reducing = compare_shehai_number(jieqi, daygangzhi, hourgangzhi)
            if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[7][0] == "試比用":
                result = "不適用，或試他法"
                return result

            elif len(reducing[0]) == 1:
                result = ["涉害","涉害", find_three_pass(jieqi, hourgangzhi, reducing[0])]
                return result

            elif reducing[0] == "找孟仲季地":
                convert = convert_munchongji_shehai_number(jieqi, daygangzhi, hourgangzhi)
                convert_dict = {convert[2][0]+convert[0][0]: convert[3][0]+convert[1][0], convert[2][1]+convert[0][1]: convert[3][1]+convert[1][1] }
                convert_result_k = list(convert_dict.keys())
                convert_result_v = list(convert_dict.values())
                convert_result_head = [i[0] for i in convert_result_k]
                convert_result_tail = [i[1] for i in convert_result_k]
                change_daygangzhi = shigangjigong.get(daygangzhi[0])

                if convert_result_v[0] == "孟季" or "仲季" or "季季":
                    if convert_result_v[1][1] == "孟":
                        if convert_result_tail[0] or convert_result_tail[1] ==  change_daygangzhi:
                             name = "綴瑕"
                        else:
                             name = "見機"
                    elif convert_result_v[1][1] == "仲":
                        name = "察微" 
                chuchuan = convert_result_k[1][0]
                result = ["涉害", name, find_three_pass(jieqi, hourgangzhi, chuchuan)]
    else:
        result = "不適用，或試他法"
    
    return result

def yaoke(jieqi, daygangzhi, hourgangzhi):
    if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[3] == "日干支同位":
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
        chuchuan = "不適用，或試他法" 
        return chuchuan
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0]
    dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
   
    if sike_list.count("下賊上") == 1 and sike_list.count("上尅下") == 1:
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif sike_list.count("下賊上") > 0 or sike_list.count("上尅下") > 0:
        chuchuan = "不適用，或試他法" 
        return chuchuan

    if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].count("尅") == 1:
        if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
            chuchuan = ["返吟", "無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(shigangjigong.get(daygangzhi[0])))]]
            return chuchuan
        else:
            chuchuan = ["遙尅","遙尅", find_three_pass(jieqi, hourgangzhi, sike[find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].index("尅")][0] )]
            return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].count("尅") > 1:
        filterlist = [sike[i][0] for i in duplicates(find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2], "尅")]
        filterlist2 = [gangzhi_yinyang(b) for b in filterlist]
        nn_list = []
        for n in filterlist2:
            if n == dayganzhi_yy:
                p = "True"
            else:
                p = "False"
            nn_list.append(p)
            if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
                chuchuan = ["返吟", "無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(shigangjigong.gedaygangzhi[0]))]]
                return chuchuan
            elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
                chuchuan =  "不適用，或試他法" 
                return chuchuan
            else:
                chuchuan = ["遙尅","蒿矢", find_three_pass(jieqi, hourgangzhi, sike[nn_list.index('True')][0] )]
                return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].count("被尅") == 1:
        if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
            chuchuan = ["返吟","無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])) ]]
            return chuchuan
        else:
            chuchuan = ["遙尅","彈射", find_three_pass(jieqi, hourgangzhi, sike[find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].index("被尅")][0] )]
            return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].count("被尅") == 0 and find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].count("尅") == 0:
        chuchuan = "不適用，或試他法"  
        return chuchuan
    
def maosing(jieqi, daygangzhi, hourgangzhi):
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0]
    dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
    sikehead = [b[0] for b in sike]
    d =  Counter(sikehead)
    res = [k for k, v in d.items() if v > 1]
    if len(set(sike)) <4:
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[2].count("尅") >0:
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
        if dayganzhi_yy == "陽":
            try:
                if len(res[0]) >= 1:
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
            except IndexError:
                if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
                    chuchuan = ["返吟", "無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])) ]]
                    return chuchuan
                elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["昴星", "虎視", [sky_n_earth_list(jieqi, hourgangzhi).get("酉"), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(sky_n_earth_list(jieqi, hourgangzhi).get(sky_n_earth_list(jieqi, hourgangzhi).get("酉")))]]
                    return chuchuan
        if dayganzhi_yy == "陰":
            try:
                if len(res[0]) >= 1:
                    chuchuan = "不適用，或試他法"  
                    return chuchuan
            except IndexError:
                if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
                    chuchuan = ["返吟","無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])) ]]
                    return chuchuan
                elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["昴星","冬蛇掩目", [earth_n_sky_list(jieqi, hourgangzhi).get("酉"), sky_n_earth_list(jieqi, hourgangzhi).get(multi_key_dict_get(ganlivezhi, daygangzhi[0])), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1])]]
                    return chuchuan
    else:
        chuchuan = "不適用，或試他法"  
        return chuchuan

def bieze(jieqi, daygangzhi, hourgangzhi):
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0]
    if len(set(sike)) == 4:
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[3] == "日干支同位":
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
        if dayganzhi_yy == "陽":
            ganhe_result1 = shigangjigong.get(sky_ganhe.get(daygangzhi[0]))
            if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
                chuchuan = ["返吟", "無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])) ]]
                return chuchuan
            elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟八專":
                chuchuan = "不適用，或試他法" 
                return chuchuan
            elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
                chuchuan =  "不適用，或試他法" 
                return chuchuan
            else:
                chuchuan = ["別責", "別責", [sky_n_earth_list(jieqi, hourgangzhi).get(ganhe_result1), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])),  sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0]))]]
                return chuchuan
        if dayganzhi_yy == "陰":
            ganhe_result1 = shigangjigong.get(earth_zhihe.get(daygangzhi[1]))
            result = multi_key_dict_get(earth_zhihe, daygangzhi[1])
            position = multi_key_dict_get(earth_zhihe, daygangzhi[1]).index(daygangzhi[1])
            if position == 0:
                a = result[1]
            elif position == 1:
                a = result[2]
            elif position == 2:
                a = result[0]
                if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟":
                    chuchuan = ["返吟","無親", [yima_dict.get(hourgangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])) ]]
                    return chuchuan
                elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
                    chuchuan =  "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["別責", "別責", [a, sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0])), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0]))]]
                    return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
        chuchuan =  "不適用，或試他法" 
        return chuchuan
    if sike_list.count("下賊上") + sike_list.count("上尅下") >= 1 :
        chuchuan =  "不適用，或試他法" 
        return chuchuan

def bazhuan(jieqi, daygangzhi, hourgangzhi):
    sike = all_sike(jieqi, daygangzhi, hourgangzhi)
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)[0]
    dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
    if sike_list.count("下賊上") == 1 and sike_list.count("上尅下") == 1:
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif sike_list.count("下賊上") > 0 or sike_list.count("上尅下") > 0:
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟" :
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟八專" and find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] is not "伏吟" :
        chuchuan = ["返吟", "無親", [yima_dict.get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(shigangjigong.get(daygangzhi[0]))]]
        return chuchuan
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[3] == "日干支同位":
        if sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
            if dayganzhi_yy == "陽":
                pos = Zhi.index(sike[3][0])+2
                if pos == 13:
                    pos = 1
                elif pos == 14:
                    pos = 0
                pos = Zhi[pos]
                if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["八專","八專", [pos, sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1])]]
                    return chuchuan
            elif dayganzhi_yy == "陰":
                pos = Zhi.index(sike[0][0])-2
                if pos == -2:
                    pos = 10
                elif pos == -1:
                    pos = 11
                pos = Zhi[pos]
                if find_sike_relations(jieqi, daygangzhi, hourgangzhi)[4] == "伏吟" and find_sike_relations(jieqi, daygangzhi, hourgangzhi)[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["八專", "八專",[pos, sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1]), sky_n_earth_list(jieqi, hourgangzhi).get(daygangzhi[1])]]   
                    return chuchuan 
    elif find_sike_relations(jieqi, daygangzhi, hourgangzhi)[3] == "日干支不同位":
        chuchuan = "不適用，或試他法" 
        return chuchuan

def fuyin(jieqi, daygangzhi, hourgangzhi):
    ying_chong = {tuple(list("寅巳申丑戌未子卯")):"刑", tuple(list("午辰酉亥")):"自刑"}
    ying = {"寅":"巳", "巳":"申", "申":"寅", "丑":"戌", "戌":"未", "未":"丑", "子":"卯", "卯":"子"}
    chong2 = {"子":"午", "丑":"未", "寅":"申", "卯":"酉", "辰":"戌", "巳":"亥"}
    sike_list = find_sike_relations(jieqi, daygangzhi, hourgangzhi)
    dayganzhi_yy = gangzhi_yinyang(daygangzhi[0])
    if sike_list[4] == "非伏吟":
        chuchuan = "不適用，或試他法" 
        return chuchuan
    elif sike_list[4] == "伏吟":
        if sike_list[0].count("上尅下") == 1 or sike_list[0].count("下賊上") == 1:
            chuchuan = ["伏吟", "不虞",  [unique(sike_list[1])[0], ying.get(unique(sike_list[1])[0]), ying.get(ying.get(unique(sike_list[1])[0])) ]]
            return chuchuan
        elif sike_list[0].count("上尅下") == 0 and sike_list[0].count("下賊上") == 0:
            if dayganzhi_yy == "陽":
                if multi_key_dict_get(ying_chong, shigangjigong.get(daygangzhi[0])) =="刑":
                    chuchuan = ["伏吟","自任", [shigangjigong.get(daygangzhi[0]), ying.get(shigangjigong.get(daygangzhi[0])), ying.get(ying.get(shigangjigong.get(daygangzhi[0])))]]
                    return chuchuan
                elif multi_key_dict_get(ying_chong, shigangjigong.get(daygangzhi[0])) =="自刑":
                    chuchuan = ["伏吟", "杜傳", [shigangjigong.get(daygangzhi[0]), daygangzhi[1], chong(daygangzhi[1])]]
                    return chuchuan
            elif dayganzhi_yy == "陰":
                chuchuan = ["伏吟", "自信", [daygangzhi[1], ying.get(daygangzhi[1]), chong2.get(daygangzhi[1])]]
                return chuchuan

def liuren(jieqi, daygangzhi, hourgangzhi):
    answer =  [zeike(jieqi, daygangzhi, hourgangzhi), biyung(jieqi, daygangzhi, hourgangzhi), shehai(jieqi, daygangzhi, hourgangzhi), yaoke(jieqi, daygangzhi, hourgangzhi) ,maosing(jieqi, daygangzhi, hourgangzhi),bieze(jieqi, daygangzhi, hourgangzhi),bazhuan(jieqi, daygangzhi, hourgangzhi),fuyin(jieqi, daygangzhi, hourgangzhi)]
    nouse = ["不適用，或試他法" ]
    ju_three_pass = [i for i in answer if i not in nouse] 
    sky_earth = sky_n_earth_list(jieqi, hourgangzhi)
    sky = list(sky_earth.values())
    earth = list(sky_earth.keys())
    guiren_order_list_2 = guiren_order_list(daygangzhi, hourgangzhi)
    guiren_order_list_3 = [guiren_order_list_2.get(i) for i in sky]
    sky_earth_guiren_dict = {"天盤":sky, "地盤":earth, "天將":guiren_order_list_3}
    ju = [ju_three_pass[0][0], ju_three_pass[0][1]]
    three_pass_zhi = ju_three_pass[0][2]
    three_pass_generals = [guiren_order_list_2.get(i) for i in three_pass_zhi]
    day_gz_vs_three_pass = [  liuqing_dict.get(multi_key_dict_get(wuxing_relation_2,ganzhiwuxing(daygangzhi[0])+ganzhiwuxing(three_pass_zhi[i])))for i in range(0,len(three_pass_zhi))]
    three_pass = {"初傳":[three_pass_zhi[0], three_pass_generals[0], day_gz_vs_three_pass[0]], "中傳":[three_pass_zhi[1], three_pass_generals[1], day_gz_vs_three_pass[1]], "末傳":[three_pass_zhi[2], three_pass_generals[2], day_gz_vs_three_pass[2]]}
    sike_zhi = all_sike(jieqi, daygangzhi, hourgangzhi)
    sike_generals = [ guiren_order_list_2.get(i[0]) for i in sike_zhi]
    sike = {"四課":[sike_zhi[0], sike_generals[0]], "三課":[sike_zhi[1], sike_generals[1]], "二課":[sike_zhi[2], sike_generals[2]], "一課":[sike_zhi[3], sike_generals[3]]}
    return {"節氣":jieqi, "日期":daygangzhi+"日"+hourgangzhi+"時", "格局":ju, "三傳":three_pass, "四課":sike, "天地盤":sky_earth_guiren_dict, "地轉天盤":sky_earth }

def guiren_starting_gangzhi(daygangzhi, hourgangzhi):
    daynight_richppl_dict = {tuple(list("卯辰巳午未申")):"晝", tuple(list("酉戌亥子丑寅")):"夜" }
    guiren_dict = {tuple(list("甲戊庚")):{"晝":"丑", "夜":"未"}, tuple(list("丙丁")):{"晝":"亥", "夜":"酉"},  tuple(list("壬癸")):{"晝":"巳", "夜":"卯"},  tuple(list("乙己")):{"晝":"子", "夜":"申"}, "辛":{"晝":"午", "夜":"寅"} }
    get_day = multi_key_dict_get(guiren_dict, daygangzhi[0])
    find_day_or_night = multi_key_dict_get(daynight_richppl_dict, hourgangzhi[1])
    return get_day.get(find_day_or_night)

def guiren_order_list(daygangzhi, hourgangzhi):
    sky_generals = "貴人螣蛇朱雀六合勾陳青龍天空白虎太常玄武太陰天后"
    sky_generals_list = [sky_generals[i:i+2] for i in range(0, len(sky_generals), 2)]
    starting_gangzhi = guiren_starting_gangzhi(daygangzhi, hourgangzhi)
    new_zhi_list_guiren = new_zhi_list(starting_gangzhi)
    return dict(zip(new_zhi_list_guiren, sky_generals_list))
    
#print(liuren("冬至", "癸巳", "辛酉"))