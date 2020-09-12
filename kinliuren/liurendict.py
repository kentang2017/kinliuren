# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 09:37:59 2020

@author: kentang
@email: kinyeah@gmail.com
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

#日馬
yimadict = {tuple(list("戌寅午")):"申", tuple(list("酉丑巳")):"亥", tuple(list("子辰申")):"寅", tuple(list("亥卯未")):"巳"}

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

rotation = {tuple(list("巳午未酉戌辰卯")): "逆佈",  tuple(list("亥子丑寅申")):"順佈"}

guiren_dict = {"甲":{"晝":"未", "夜":"丑"}, tuple(list("戊庚")):{"晝":"丑", "夜":"未"}, "丙":{"晝":"酉", "夜":"亥"}, "丁":{"晝":"亥", "夜":"酉"}, "壬":{"晝":"卯", "夜":"巳"}, "癸":{"晝":"巳", "夜":"卯"}, "乙":{"晝":"申", "夜":"子"}, "己":{"晝":"子", "夜":"申"}, "辛":{"晝":"寅", "夜":"午"} }

guiren_dict2 = { tuple(list("甲戊庚")):{"晝":"丑", "夜":"未"}, tuple(list("乙己")):{"晝":"子", "夜":"申"}, tuple(list("丙丁")):{"晝":"亥", "夜":"酉"}, tuple(list("壬癸")):{"晝":"巳", "夜":"卯"}, "辛":{"晝":"午", "夜":"寅"}}


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

def new_list(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append( olist[zhihead_code % len(olist)])
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

#天將
sky_generals  = "貴蛇雀合勾龍空虎常玄陰后"
sky_generals_r  = new_list(list(reversed(sky_generals)), "貴")

#刑沖
ying_chong = {tuple(list("寅巳申丑戌未子卯")):"刑", tuple(list("午辰酉亥")):"自刑"}
ying = {"寅":"巳", "巳":"申", "申":"寅", "丑":"戌", "戌":"未", "未":"丑", "子":"卯", "卯":"子", "辰":"戌"}
chong = {"子":"午","午":"子", "丑":"未","未":"丑", "寅":"申","申":"寅", "卯":"酉", "酉":"卯", "辰":"戌","戌":"辰", "巳":"亥", "亥":"巳"}
chong2 = {"子":"午","午":"子", "丑":"未","未":"丑", "寅":"申","申":"寅", "卯":"酉", "酉":"卯", "辰":"戌","戌":"辰", "巳":"亥", "亥":"巳"}

#神將
generals_zhi = {**dict(zip(['貴'+i for i in Zhi], "解紛,升堂,憑幾,登車,天牢,受貢,受貢,列席,移途,入私室,地獄,登天門".split(","))),
**dict(zip(['后'+i for i in Zhi], "守閏,偷窺,理發,臨門,毀妝,裸體,伏枕,沐浴,修容,倚戶,褰帷,治事".split(","))),
**dict(zip(['陰'+i for i in Zhi], "垂簾,入內,跣足,微行,造庭,伏枕,脫巾,觀書,執政,閉戶,被察,裸形".split(","))),
**dict(zip(['玄'+i for i in Zhi], "散發,升堂,入林,窺戶,失路,反顧,截路,入城,折足,拔劍,遭囚,伏藏".split(","))),
**dict(zip(['常'+i for i in Zhi], "遭枷,受爵,側目,遺冠,佩印,鑄印,乘軒,捧觴,銜杯,券書,逆命,征召".split(","))),
**dict(zip(['虎'+i for i in Zhi], "溺水,在野,登山,臨門,咥人,焚身,焚身,在野,銜牒,臨門,落阱,溺水".split(","))),
**dict(zip(['空'+i for i in Zhi], "伏室,侍側,被制,乘侮,凶惡,受辱,識字,趨進,鼓舌,巧說,居家,誣詞".split(","))),
**dict(zip(['龍'+i for i in Zhi], "入海,蟠泥,乘雲,驅雷,飛天,掩目,焚身,在陸,傷鱗,摧角,登魁,游江".split(","))),
**dict(zip(['勾'+i for i in Zhi], "投機,受越,遭囚,臨門,升堂,捧印,反目,入驛,趨戶,披刃,下獄,褰裳".split(","))),
**dict(zip(['合'+i for i in Zhi], "反目,嚴妝,乘軒,入室,違理,不諧,升堂,納采,結髮,私竄,亡羞,待命".split(","))),
**dict(zip(['雀'+i for i in Zhi], "投江,掩目,安巢,安巢,投網,晝翔,銜符,臨墳,厲嘴,夜噪,投網,入水".split(","))),
**dict(zip(['蛇'+i for i in Zhi], "掩目,蟠龜,生角,當門,象龍,乘霧,飛空,入林,銜劍,露齒,入冢,墜水".split(",")))}

#廿八宿
hoursu = {tuple(list("甲己")):{"子":"角亢", "丑":"翼軫", "寅":"柳星張", "卯":"井鬼" , "辰":"參觜",  "巳":"胃昴畢", "午":"婁奎", "未":"危室壁", "申":"女虛", "酉":"斗牛", "戌":"尾箕", "亥":"氐房心"},
tuple(list("乙庚")):{"子":"參觜", "丑":"昴畢", "寅":"奎婁胃", "卯":"危室壁" , "辰":"女虛",  "巳":"斗牛", "午":"尾箕", "未":"氐房心", "申":"角亢", "酉":"翼軫", "戌":"柳星張", "亥":"井鬼"},
tuple(list("丙辛")):{"子":"奎婁", "丑":"危室壁", "寅":"女虛", "卯":"斗牛" , "辰":"尾箕",  "巳":"氐房心", "午":"角亢", "未":"翼軫", "申":"井鬼", "酉":"柳星張", "戌":"參觜", "亥":"胃昴畢"},
tuple(list("戊癸")):{"子":"尾箕", "丑":"氐房心", "寅":"角亢", "卯":"翼軫" , "辰":"柳星張",  "巳":"井鬼", "午":"畢參觜", "未":"胃昴", "申":"奎婁", "酉":"危室壁", "戌":"女虛", "亥":"斗牛"},
tuple(list("丁壬")):{"子":"女虛", "丑":"斗牛", "寅":"尾箕", "卯":"氐房心" , "辰":"角亢",  "巳":"翼軫", "午":"柳星張", "未":"井鬼", "申":"畢參觜", "酉":"胃昴", "戌":"奎婁", "亥":"危室壁"}}
