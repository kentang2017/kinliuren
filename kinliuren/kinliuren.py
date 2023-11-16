# -*- coding: utf-8 -*-
"""
Created on Sun Dec  22 16:22:37 2019
@author: ken tang
@email: kinyeah@gmail.com
@description:  2021年12月中旬，優化編碼內容
"""
from collections import Counter
import re, itertools, time

class Liuren():
    def __init__(self, jieqi, cmonth, daygangzhi, hourgangzhi):
        self.jieqi = jieqi
        self.daygangzhi = daygangzhi
        self.hourgangzhi = hourgangzhi
        self.cmonth = cmonth
        self.Gan = list("甲乙丙丁戊己庚辛壬癸")
        self.Zhi = list("子丑寅卯辰巳午未申酉戌亥")
        self.Cmonth = list("正二三四五六七八九十")+["十一","十二"]
        #字典庫
        self.yima_dict = {"丑":"亥", "未":"巳"}
        self.shigangjigong  = dict(zip(self.Gan + self.Zhi, list("寅辰巳未巳未申戌亥丑") + self.Zhi))
        #日馬
        self.yimadict = dict(zip(list(map(lambda x: tuple(x),"戌寅午,酉丑巳,子辰申,亥卯未".split(","))), list("申亥寅巳")))
        #生尅六親
        self.liuqing_dict = dict(zip("被生,生,尅,比和,被尅".split(","),re.findall("..", "父母子孫財妻兄弟官鬼")))
        self.wuxing = "火水金火木金水土土木,水火火金金木土水木土,火火金金木木土土水水,火木水金木水土火金土,木火金水水木火土土金"
        self.wuxing_relation_2 = dict(zip(list(map(lambda x: tuple(re.findall("..",x)), self.wuxing.split(","))), "被尅,尅,比和,被生,生".split(",")))
        #干支五行
        self.ganzhiwuxing = dict(zip(list(map(lambda x: tuple(x),"甲寅乙卯,丙巳丁午,壬亥癸子,庚申辛酉,未丑戊己未辰戌".split(","))), list("木火水金土")))
        #日貴人 甲羊戊庚牛。乙猴已鼠求。丙雞丁豬位。壬癸兔蛇游。六辛逢虎上。陽貴日中 。
        #夜貴人 甲牛戊庚羊乙鼠鄉。丙豬丁難上。壬中蛇癸兔藏。六辛逢午馬。陰貴夜時當。
        self.daynight_richppl_dict = dict(zip(list(map(lambda x: tuple(x), "卯辰巳午未申,酉戌亥子丑寅".split(","))), list("晝夜")))
        #刑沖
        self.ying = dict(zip("寅巳申丑戌未子卯辰亥酉午","巳申寅戌未丑卯子辰亥酉午"))
        self.ying_chong = dict(zip(list(map(lambda x: tuple(x), "寅巳申丑戌未子卯,午辰酉亥".split(","))),"刑,自刑".split(","))) 
        self.chong2 = dict(zip("子午丑未寅申卯酉辰戌巳亥","午子未丑申寅酉卯戌辰亥巳"))
        #天將
        self.sky_generals  = "貴蛇雀合勾龍空虎常玄陰后"
        self.sky_generals_r  = self.new_list(list(reversed(self.sky_generals)), "貴")
        #甲旬
        self.liujiashun_dict = dict(zip(list(map(lambda x: tuple(x), [self.jiazi()[i:i + 10] for i in range(0, len(self.jiazi()), 10)])), self.jiazi()[0::10]))
        #廿八宿
        self.hoursu = {tuple(list("甲己")):{"子":"角亢", "丑":"翼軫", "寅":"柳星張", "卯":"井鬼" , "辰":"參觜",  "巳":"胃昴畢", "午":"婁奎", "未":"危室壁", "申":"女虛", "酉":"斗牛", "戌":"尾箕", "亥":"氐房心"},
                  tuple(list("乙庚")):{"子":"參觜", "丑":"昴畢", "寅":"奎婁胃", "卯":"危室壁" , "辰":"女虛",  "巳":"斗牛", "午":"尾箕", "未":"氐房心", "申":"角亢", "酉":"翼軫", "戌":"柳星張", "亥":"井鬼"},
                  tuple(list("丙辛")):{"子":"奎婁", "丑":"危室壁", "寅":"女虛", "卯":"斗牛" , "辰":"尾箕",  "巳":"氐房心", "午":"角亢", "未":"翼軫", "申":"井鬼", "酉":"柳星張", "戌":"參觜", "亥":"胃昴畢"},
                  tuple(list("戊癸")):{"子":"尾箕", "丑":"氐房心", "寅":"角亢", "卯":"翼軫" , "辰":"柳星張",  "巳":"井鬼", "午":"畢參觜", "未":"胃昴", "申":"奎婁", "酉":"危室壁", "戌":"女虛", "亥":"斗牛"},
                  tuple(list("丁壬")):{"子":"女虛", "丑":"斗牛", "寅":"尾箕", "卯":"氐房心" , "辰":"角亢",  "巳":"翼軫", "午":"柳星張", "未":"井鬼", "申":"畢參觜", "酉":"胃昴", "戌":"奎婁", "亥":"危室壁"}}

        self.generals_zhi = {**dict(zip(['貴'+i for i in self.Zhi], "吉,吉,凶,吉,凶,凶,凶,吉,吉,凶,凶,吉".split(","))),
                **dict(zip(['后'+i for i in self.Zhi], "凶,凶,吉,凶,凶,凶,凶,凶,吉,凶,凶,吉".split(","))),
                **dict(zip(['陰'+i for i in self.Zhi], "凶,凶,凶,凶,吉,凶,凶,吉,吉,吉,凶,凶".split(","))),
                **dict(zip(['玄'+i for i in self.Zhi], "吉,吉,凶,凶,吉,凶,凶,凶,吉,吉,吉,凶".split(","))),
                **dict(zip(['常'+i for i in self.Zhi], "凶,吉,凶,凶,吉,吉,吉,吉,吉,吉,凶,吉".split(","))),
                **dict(zip(['虎'+i for i in self.Zhi], "凶,凶,凶,凶,凶,凶,凶,凶,吉,凶,凶,凶".split(","))),
                **dict(zip(['空'+i for i in self.Zhi], "凶,凶,凶,凶,凶,凶,凶,吉,凶,凶,凶,凶".split(","))),
                **dict(zip(['龍'+i for i in self.Zhi], "吉,凶,吉,吉,吉,凶,凶,凶,凶,凶,吉,吉".split(","))),
                **dict(zip(['勾'+i for i in self.Zhi], "凶,凶,凶,凶,吉,吉,凶,吉,凶,凶,凶,凶".split(","))),
                **dict(zip(['合'+i for i in self.Zhi], "凶,吉,吉,吉,凶,凶,吉,吉,吉,凶,凶,吉".split(","))),
                **dict(zip(['雀'+i for i in self.Zhi], "凶,凶,吉,吉,凶,吉,吉,凶,吉,凶,凶,凶".split(","))),
                **dict(zip(['蛇'+i for i in self.Zhi], "吉,吉,吉,凶,吉,吉,吉,吉,吉,凶,凶,吉".split(",")))}


    def gangzhi_yinyang(self, gangorzhi):
        gangzhi_yingyang = dict(zip(list(map(lambda x: tuple(x), [self.Gan[0::2] + self.Zhi[0::2], self.Gan[1::2] + self.Zhi[1::2]])), list("陽陰")))
        yinyang = self.multi_key_dict_get(gangzhi_yingyang, gangorzhi)
        return yinyang
    
    def duplicates(self, lst, item):
        result = [i for i, x in enumerate(lst) if x == item]
        if len(result) > 1:
            result =result
        elif len(result) ==1:
            result = lst.index(item)
        return result
    
    def multi_key_dict_get(self, d, k):
        for keys, v in d.items():
            if k in keys:
                return v
        return None
    
    def Max(self, list):
        if len(list) == 1:
            return list[0]
        else:
            m = max(list[1:])
            return m if m > list[0] else list[0]
    
    def new_list(self, olist, o):
        zhihead_code = olist.index(o)
        res1 = []
        for i in range(len(olist)):
            res1.append( olist[zhihead_code % len(olist)])
            zhihead_code = zhihead_code + 1
        return res1
    
    def jiazi(self):
        tiangan = self.Gan
        dizhi = self.Zhi
        jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
        return jiazi
    
    def shunkong(self,daygangzhi,zhi):
        liujiashun_dict = self.liujiashun_dict 
        dayshun = self.multi_key_dict_get(liujiashun_dict, daygangzhi)
        findshun =  dict(zip(self.jiazi()[0::10], list(map(lambda x: dict(zip(self.Zhi,x)), list(map(lambda x: self.new_list(self.Gan+list("空空"), x), "甲丙戊庚壬空"))))))
        return self. multi_key_dict_get(findshun,dayshun).get(zhi)
    
    def Ganzhiwuxing(self, gangorzhi):
        return self.multi_key_dict_get(self.ganzhiwuxing, gangorzhi)
    
    def find_ke_relation(self, ke):
        wuxing_relation = dict(zip(list(map(lambda x: tuple(re.findall("..",x)), self.wuxing.split(","))), "下賊上,上尅下,比和,下生上,上生下".split(",")))
        top_botton = self.Ganzhiwuxing(ke[0])+self.Ganzhiwuxing(ke[1])
        return self.multi_key_dict_get(wuxing_relation, top_botton)

    def sky_pan_list(self):
        #找月將
        jq =re.findall('..','小寒大寒立春雨水驚蟄春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至')
        moon_general_dict = dict(zip(list(zip(self.new_list(jq, "大寒")[0::2] , self.new_list(jq, "大寒")[1::2])), self.new_list(list(reversed(self.Zhi)), "子")))
        get_moon_general = self.multi_key_dict_get(moon_general_dict, self.jieqi)
        return [self.new_zhi_list(get_moon_general), get_moon_general]
    
    def find_season(self, s):
        jq = re.findall('..','立春雨水驚蟄春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒')
        season = list("春春春春春春夏夏夏夏夏夏秋秋秋秋秋秋冬冬冬冬冬冬")
        return dict(zip(jq, season)).get(s)
    
    def moongeneral(self):
        return self.sky_pan_list()[1]
    
    def new_zhi_list(self, zhi):
        zhihead_code = self.Zhi.index(zhi)
        res1 = []
        for i in range(len(self.Zhi)):
            res1.append( self.Zhi[zhihead_code % len(self.Zhi)])
            zhihead_code = zhihead_code + 1
        return res1

    def sky_n_earth_list(self):
        earth = self.new_zhi_list(self.hourgangzhi[1])
        sky = self.sky_pan_list()[0]
        return dict(zip(earth, sky))
    
    def earth_n_sky_list(self):
        earth = self.new_zhi_list(self.hourgangzhi[1])
        sky = self.sky_pan_list()[0]
        return dict(zip(sky, earth))

    def all_sike(self):
        yike = self.sky_n_earth_list()[self.shigangjigong.get(self.daygangzhi[0])] + self.daygangzhi[0]
        sky_n_earth = self.sky_n_earth_list()
        erke = sky_n_earth.get(yike[0]) + yike[0]
        sanke = sky_n_earth.get(self.daygangzhi[1]) + self.daygangzhi[1]
        sike = sky_n_earth.get(sanke[0]) + sanke[0]
        return [sike, sanke, erke, yike]

    def new_zhigangcangong_list(self, zhi):
        zhigangcangong = list("子丑癸寅甲卯辰乙巳丙戊午未己申庚酉戌辛亥壬")
        zhihead_code = zhigangcangong.index(zhi)
        res1 = []
        for i in range(len(zhigangcangong)):
            res1.append( zhigangcangong[zhihead_code % len(zhigangcangong)])
            zhihead_code = zhihead_code + 1
        return res1

    def fanyin(self):
        sky_earth = self.sky_n_earth_list()
        sky =  list(sky_earth.values())
        earth = list(sky_earth.keys())
        earth_sky_combine = [ self.Ganzhiwuxing(sky[i]) +  self.Ganzhiwuxing(earth[i]) for i in range(0,len(sky_earth))]
        earth_sky_combine_wuxing = [self.multi_key_dict_get(self.wuxing_relation_2, earth_sky_combine[i]) for i in range(0,len(earth_sky_combine))]
        count_ke_and_being_ke = earth_sky_combine_wuxing.count("被尅") + earth_sky_combine_wuxing.count("尅")
        return count_ke_and_being_ke, earth_sky_combine_wuxing

    def find_sike_shangke(self):
        sike_list = []
        sike = self.all_sike()
        for i in sike:
            b = self.find_ke_relation(i)
            sike_list.append(b)
        return sike_list

    def find_sike_relations(self):
        sike_list = []
        sike = self.all_sike()
        for i in sike:
            b = self.find_ke_relation(i)
            sike_list.append(b)
        if sike_list.count("下賊上") == 2 and sike_list.count("上尅下") == 2:
            classify = "下賊上"
        elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 1 :
            classify = "下賊上"
        elif sike_list.count("上尅下") == 0 and sike_list.count("下賊上") == 4 :
            classify = "下賊上"
        elif sike_list.count("上尅下") > 1 and sike_list.count("下賊上") == 1:
            classify = "下賊上"
        elif sike_list.count("上尅下") == 0 and sike_list.count("下賊上") == 1:
            classify = "下賊上"
        elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 0:
            classify = "上尅下"
        elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 3:
            classify = "下賊上"
        elif sike_list.count("下賊上") == 2 and sike_list.count("上尅下") == 1 :
            classify = "下賊上"
        elif sike_list.count("下賊上") == 4 and sike_list.count("上尅下") == 0 :
            classify = "下賊上"
        elif sike_list.count("下賊上") == 2 and sike_list.count("上尅下") == 0 :
            classify = "下賊上"
        elif sike_list.count("下賊上") >= 2 and sike_list.count("上尅下") <= 1 :
            classify = "下賊上"
        elif sike_list.count("上尅下") == 0 and sike_list.count("下賊上") == 0 :
            classify = "試其他"
        elif sike_list.count("上尅下") >= 2 and sike_list.count("下賊上") == 0 :
            classify = "上尅下"
        dayganzhi_wuxing = self.Ganzhiwuxing(self.daygangzhi[0])
        dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
        wuxing_ke = [self.Ganzhiwuxing(i[0]) for i in sike]
        shangke_list = []
        for d in wuxing_ke:
            shangke = self.multi_key_dict_get(self.wuxing_relation_2, d+dayganzhi_wuxing) 
            shangke_list.append(shangke)
        dayganzhi_same_location = re.findall("..", "甲寅丁未己未庚申癸丑")
        res = [i for i in self.jiazi() if i not in dayganzhi_same_location] 
        checkdayganzhi_dict = {tuple(dayganzhi_same_location) :"日干支同位", tuple(res):"日干支不同位"}
        fanyin_days = re.findall("..", "丁丑己丑辛丑辛未")
        bazhuan_fanyin_days = ["丁未", "己未"]
        jiazi_remove_fanyin =  [i for i in self.jiazi() if i not in fanyin_days] 
        fanyin_day_dict = {tuple(fanyin_days):"反吟",tuple(bazhuan_fanyin_days):"反吟八專",tuple(jiazi_remove_fanyin+bazhuan_fanyin_days):"非反吟"}
        checkdayganzhi = self.multi_key_dict_get(checkdayganzhi_dict, self.daygangzhi)
        checkfanyin = self.multi_key_dict_get(fanyin_day_dict, self.daygangzhi)
        #moon_general = self.moongeneral(self.jieqi)
        moon_general = self.sky_pan_list()[1]
        checkmoongeneralconflicttohour = self.multi_key_dict_get(self.wuxing_relation_2, self.Ganzhiwuxing(moon_general)+self.Ganzhiwuxing(self.hourgangzhi[1]))
        sky_earth_fanyin = self.fanyin()[0]
        blist = []
        if sky_earth_fanyin >= 8 and self.fanyin()[1].count("比和")==4 or self.fanyin()[1].count("比和")==12:
            fan_yin = "天地盤返吟"
        else:
            fan_yin = "天地盤沒有返吟"
        if self.hourgangzhi[1] == moon_general:
            checkfuyin = "伏吟"
        else:
            checkfuyin = "非伏吟"
        
        if sike_list.count("上尅下") == 0 and sike_list.count("下賊上") == 0:
            findtrue = ["試賊尅涉害以外方法",  "沒有",   "沒有", classify,  "沒有",  "沒有"]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, self.gangzhi_yinyang(self.daygangzhi[0]), fan_yin
            
        elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 0:
            findtrue = ["試賊尅", sike_list.index("上尅下"),  "沒有", classify, "沒有", "沒有"]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, self.gangzhi_yinyang(self.daygangzhi[0]), fan_yin
        
        elif sike_list.count("下賊上") == 1:
            findtrue = ["試賊尅", sike_list.index("下賊上"),  "沒有", classify, "沒有", "沒有"]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, self.gangzhi_yinyang(self.daygangzhi[0]), fan_yin
        
        elif sike_list.count("下賊上") >1:
            find_ke = self.duplicates(sike_list, "下賊上")
            zeikeshang_list = []
            for i in find_ke:
                zeike = sike[i]
                zeikeshang_list.append(zeike)
            yy_list = []
            for y in zeikeshang_list:
                yy = self.gangzhi_yinyang(y[0])
                yy_list.append(yy)
            nn_list = []
            for n in yy_list:
                if n == dayganzhi_yy:
                    p = "True"
                else:
                    p = "False"
                nn_list.append(p)
            for i in range(0, len(zeikeshang_list)):
                b = zeikeshang_list[i][0]
                blist.append(b)
            check_same = len(set(blist))
            if check_same == 1 or len(set(sike_list)) == 1:
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True") >=0 and nn_list.count("False") >=0:
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, self.gangzhi_yinyang(self.daygangzhi[0]), fan_yin
    
        
        elif sike_list.count("上尅下")>1:
            find_ke = self.duplicates(sike_list, "上尅下")
            zeikeshang_list = []
            for i in find_ke:
                zeike = sike[i]
                zeikeshang_list.append(zeike)
            yy_list = []
            for y in zeikeshang_list:
                yy = self.gangzhi_yinyang(y[0])
                yy_list.append(yy)
            nn_list = []
            for n in yy_list:
                if n == dayganzhi_yy:
                    p = "True"
                else:
                    p = "False"
                nn_list.append(p)
            for i in range(0, len(zeikeshang_list)):
                b = zeikeshang_list[i][0]
                blist.append(b)
            check_same = len(set(blist))
            if check_same == 1:
                findtrue = ["試賊尅", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same] #結果, 尅克位置, 課式
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True")==0:
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True") ==1  and nn_list.count("False") ==1: 
                findtrue = ["試比用", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True")>=1  and nn_list.count("False") >=1: 
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) == 2 and nn_list.count("True")>=2  and nn_list.count("False") ==0: 
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True")>=2  and nn_list.count("False") ==0: 
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, self.gangzhi_yinyang(self.daygangzhi[0]), fan_yin

    def sike_dict(self):
        sike = self.all_sike()
        sike_list = self.find_sike_relations()[0]
        dyingyang = self.gangzhi_yinyang(self.daygangzhi[0])
        sike_yingyan = [self.gangzhi_yinyang(i[0]) for i in sike]
        return sike, sike_list, dyingyang, sike_yingyan

    def find_three_pass(self, firstpass):
        secondpass = self.sky_n_earth_list().get(firstpass)
        thirdpass = self.sky_n_earth_list().get(secondpass)
        return [firstpass, secondpass, thirdpass]

    def zeike(self):
        sike = self.all_sike()
        sike_list = self.find_sike_relations()
        #沒有上尅下或下賊上
        if sike_list[0].count("上尅下") == 0 and sike_list[0].count("下賊上") == 0:
            findtrue =  "不適用，或試他法" 
            return findtrue
        #多於一個上尅下或下賊上
        elif sike_list[7][0] == "試涉害" or sike_list[7][0] == "試比用":
            findtrue =  "不適用，或試他法" 
            return findtrue
        elif sike_list[0].count("下賊上") > 2 and sike_list[7][6] > 1 and sike_list[2].count("尅") > 1:
            findtrue =  "不適用，或試他法" 
            return findtrue
        elif sike_list[0].count("下賊上") > 2 and sike_list[7][6] > 1 and sike_list[2].count("尅") == 1:
            findtrue =  ["賊尅","重審"]
            return ["賊尅","重審", self.find_three_pass(sike_list[7][2][sike_list[2].index("尅")][0])]
        elif sike_list[0].count("下賊上") > 2 and sike_list[7][6] > 1 and sike_list[2].count("尅") == 0:
            findtrue =  ["賊尅","重審"]
            return ["賊尅","重審", self.find_three_pass(sike_list[7][2][sike_list[2].index("生")][0])]
        elif sike_list[0].count("下賊上") > 2 and sike_list[7][6] == 1  and sike_list[9] == '天地盤沒有返吟':
            findtrue =  ["賊尅","重審", self.find_three_pass(sike_list[7][2][0][0])]
            return findtrue
        elif sike_list[0].count("下賊上") >= 2 and sike_list[7][0] == "試賊尅" and sike_list[7][6] == 1  and sike_list[9] == '天地盤沒有返吟':
            findtrue =  ["賊尅","重審", self.find_three_pass(sike_list[7][2][0][0])]
            return findtrue
        #多於一個上尅下或下賊上
        elif sike_list[0].count("上尅下") == 2 and sike_list[0].count("下賊上") == 0 and sike_list[7][2][0] != sike_list[7][2][1] and sike_list[7][6] > 1: 
            findtrue =  "不適用，或試他法" 
            return findtrue
        elif sike_list[0].count("上尅下") == 2 and sike_list[0].count("下賊上") == 0 and sike_list[7][2][0] != sike_list[7][2][1] and sike_list[7][6] == 1: 
            findtrue =   ["賊尅","元首", self.find_three_pass(sike_list[7][2][0][0])]
            return findtrue
        elif sike_list[0].count("上尅下") == 2 and sike_list[0].count("下賊上") == 0 and sike_list[7][2][0] == sike_list[7][2][1]:
            findtrue =   ["賊尅","元首", self.find_three_pass(sike_list[7][2][0][0])]
            return findtrue
        elif sike_list[0].count("上尅下") >= 2 and sike_list[0].count("下賊上") == 0: 
            findtrue =  "不適用，或試他法" 
        elif sike_list[0].count("上尅下") >= 2 and sike_list[0].count("下賊上") == 1: 
            findtrue =  ["賊尅","重審", self.find_three_pass(sike[sike_list[0].index("下賊上")][0])]
            return findtrue
        elif sike_list[0].count("上尅下") > 2 and sike_list[0].count("下賊上") == 0 and sike_list[7][0] == "試賊尅" and set(sike_list[7][1]) == 1:
            findtrue =  ["賊尅","元首", self.find_three_pass(sike_list[7][2][0][0])]
            return findtrue
        #一個下賊上
        elif sike_list[0].count("下賊上") == 1 and sike_list[9] == '天地盤沒有返吟':
            findtrue =  ["賊尅","重審", self.find_three_pass(sike[sike_list[0].index("下賊上")][0])]
            return findtrue
        elif sike_list[0].count("下賊上") >= 1 and sike_list[0].count("上尅下") == 0 and sike_list[9] == '天地盤返吟':
            findtrue =  ["返吟","無依", self.find_three_pass(sike[sike_list[0].index("下賊上")][0])]
            return findtrue
        elif sike_list[0].count("下賊上") == 2 and sike_list[0].count("上尅下") == 0 and  sike_list[9] == '天地盤沒有返吟': 
            if sike_list[7][2][0] == sike_list[7][2][1]:
                findtrue =  ["賊尅","重審", self.find_three_pass(sike_list[7][2][0][0])]
                return findtrue
            elif sike_list[7][2][0] != sike_list[7][2][1]:
                findtrue =   "不適用，或試他法" 
                return findtrue
        elif sike_list[0].count("下賊上") == 2 and sike_list[0].count("上尅下") == 2  and sike_list[9] == '天地盤返吟':
            findtrue =  ["返吟","無依", self.find_three_pass(sike[sike_list[0].index("下賊上")][0])]
            return findtrue
    
        #一個上尅下
        elif sike_list[0].count("上尅下") == 1 and sike_list[0].count("下賊上") == 0 and sike_list[9] == '天地盤沒有返吟':
            findtrue =  ["賊尅","元首", self.find_three_pass(sike[sike_list[0].index("上尅下")][0])]
            return findtrue
        elif sike_list[0].count("上尅下") >= 2 and sike_list[0].count("下賊上") == 0 and sike_list[9] == '天地盤沒有返吟':  
            if sike_list[7][2][0] == sike_list[7][2][1]:
                findtrue =  ["賊尅","元首", self.find_three_pass(sike_list[7][2][0][0])]
            elif  sike_list[7][2][0] != sike_list[7][2][1]:
                findtrue =   "不適用，或試他法" 
            return findtrue 
        elif sike_list[0].count("上尅下") == 1 and sike_list[9] == '天地盤沒有返吟':
            findtrue =  ["返吟","無依", self.find_three_pass(sike[sike_list[0].index("上尅下")][0])]
            return findtrue
        elif sike_list[0].count("上尅下") == 1 and sike_list[9] == '天地盤返吟':
            findtrue =  ["伏吟","無依", [self.chong2.get(self.chong2.get(sike[sike_list[0].index("上尅下")][0])), self.chong2.get(self.hourgangzhi[1]), self.chong2.get(sike[sike_list[0].index("上尅下")][0])]]
            return findtrue


    def biyung(self):
        relation = self.find_sike_relations()
        filter_list = self.find_sike_relations()[7]
        filter_list_four_ke = self.find_sike_relations()[7][2]
        filter_list_yy = self.find_sike_relations()[7][5]
        dayganzhi_yy = self.find_sike_relations()[8]
        if filter_list[0] == "試賊尅":
            findtrue =  "不適用，或試他法"
            return findtrue
        elif filter_list[0] == "試涉害":
            findtrue =  "不適用，或試他法"
            return findtrue
        elif filter_list[0] == "試賊尅涉害以外方法":
            findtrue =  "不適用，或試他法"
            return findtrue
        elif relation[0].count("下賊上") == 2 and relation[9] == '天地盤返吟':
            findtrue = ["返吟", "無依", [self.all_sike()[1][0], self.all_sike()[1][1],  self.all_sike()[0][1] ]]
            return findtrue
        elif relation[0].count("下賊上") == 3 and relation[9] == '天地盤返吟':
            #findtrue = ["返吟", "無依", [sike_list[filter_list[4].index("True")][0], chong(sike_list[filter_list[4].index("True")][0]), chong(chong(sike_list[filter_list[4].index("True")][0]))]]
            findtrue = ["返吟", "返吟", [self.all_sike()[1][1],  self.all_sike()[0][1],self.all_sike()[1][1] ]]
            return findtrue    
        
        elif relation[0].count("下賊上") >= 2 and relation[9] == '天地盤沒有返吟':
            if filter_list_yy[0] == dayganzhi_yy:
                findtrue = ["比用", "比用", self.find_three_pass(filter_list_four_ke[0][0])]
            elif filter_list_yy[1] == dayganzhi_yy:
                findtrue = ["比用", "比用", self.find_three_pass(filter_list_four_ke[1][0])]
            else:
                findtrue = ["比用", "比用", self.find_three_pass(filter_list[2][filter_list[4].index("True")][0])]
            return findtrue
        elif relation[0].count("上尅下") >= 2 and relation[0].count("下賊上") == 0 and relation[9] == '天地盤沒有返吟':
            if filter_list_yy[0] == dayganzhi_yy:
                findtrue = ["比用", "知一", self.find_three_pass(filter_list_four_ke[0][0])]
            elif filter_list_yy[1] == dayganzhi_yy:
                findtrue = ["比用", "知一", self.find_three_pass(filter_list_four_ke[1][0])]
            return findtrue

    def fiter_four_ke(self):
        a = self.find_sike_relations()[7][2]
        b = self.find_sike_relations()[7][4]
        d = self.duplicates(b, "True")
        e = self.duplicates(b, "False")
        ilist = []
        jlist = []
        try:
            for i in d:
                item = a[i]
                ilist.append(item)
            for g in e:
                item = a[g]
                jlist.append(item)    
        except TypeError:
            ilist = "不適用，或試他法"
        if len(ilist) == 0 and len(jlist) != 0:
            ilist = jlist
        elif len(ilist) == 0 and len(jlist) == 0:
            ilist = "不適用，或試他法"
        elif len(ilist) == 3:
            ilist = list(set(ilist))
        return ilist

    def compare_shehai_number(self):
        a = self.fiter_four_ke()
        shehai_number2 = []
        khead = []
        biyung_result_reorder_list3 = []
        if self.find_sike_relations()[9] == "天地盤返吟":
            result = ["不適用，或試他法"]
            return result
        elif self.fiter_four_ke() == "不適用，或試他法":
            result = ["不適用，或試他法"]
            return result
        elif self.find_sike_relations()[7][0] == "試涉害":
            c = [a[i][0] for i in range(0, len(a))]
            t = [a[i][1] for i in range(0, len(a))]
            if self.shigangjigong.get(t[-1]) == None:
                t = t
            elif self.shigangjigong.get(t[-1]) is not None:
                t[-1] = self.shigangjigong.get(t[-1]) 
            try:
                for i in range(0,len(a)):
                    for k, v in self.sky_n_earth_list().items():
                            if v == a[i][0]:
                                khead.append(k)
                for i in range(0,len(a)):
                    biyung_result_reorder = self.new_zhigangcangong_list(khead[i])[0: self.new_zhigangcangong_list(khead[i]).index(a[i][0])+1]
                    biyung_result_reorder_list3.append([self.ganzhiwuxing(c[i][0])+k  for k in [self.ganzhiwuxing(j) for j in biyung_result_reorder]].count((self.ganzhiwuxing(a[i][0])+self.ganzhiwuxing(a[i][1]))))
                for s in biyung_result_reorder_list3:
                    shehai_number = c[biyung_result_reorder_list3.index(s)]
                    shehai_number2.append(shehai_number)
                shehai_dict = dict(zip(biyung_result_reorder_list3, shehai_number2))
                if biyung_result_reorder_list3[0] == biyung_result_reorder_list3[1]:
                    result = ["找孟仲季地", a, t, c]
                    return result
                elif biyung_result_reorder_list3[0] > biyung_result_reorder_list3[1]:
                    result = [shehai_dict.get(biyung_result_reorder_list3[0]), shehai_dict] 
                    return result
                elif biyung_result_reorder_list3[1] > biyung_result_reorder_list3[0]:
                    result = [shehai_dict.get(biyung_result_reorder_list3[1]), shehai_dict] 
                    return result
            except (TypeError, IndexError):
                result = ["不適用，或試他法"]
                return result
        else:
            result = ["不適用，或試他法"]
            return result

    def convert_munchongji(self):
        munconji = dict(zip(list(map(lambda x: tuple(x),"寅申巳亥,子午卯酉,辰戌丑未".split(","))), list("孟仲季")))
        head = self.compare_shehai_number()[2]
        tail = self.compare_shehai_number()[3]
        head_convert = []
        tail_convert = []
        for a in head:
            g =  self.multi_key_dict_get(munconji, a)
            head_convert.append(g)
        for k in tail:
            l = self.multi_key_dict_get(munconji, k)
            tail_convert.append(l)
        if self.compare_shehai_number()[0] == "找孟仲季地":
            result = [head, head_convert, tail, tail_convert]
        else:
            result = ["不適用"]
        return result
        
    def convert_munchongji_shehai_number(self):
        munconji = dict(zip(list(map(lambda x: tuple(x),"寅申巳亥,子午卯酉,辰戌丑未".split(","))), list("孟仲季")))
        head = [self.shigangjigong.get(i) for i in self.compare_shehai_number()[2]]
        tail = [self.shigangjigong.get(i) for i in self.compare_shehai_number()[3]]
        head_convert = []
        tail_convert = []
        for a in head:
            g =  self.multi_key_dict_get(munconji, a)
            head_convert.append(g)
        for k in tail:
            l = self.multi_key_dict_get(munconji, k)
            tail_convert.append(l)
        if self.compare_shehai_number()[0] == "找孟仲季地":
            result = [head, head_convert, tail, tail_convert]
        else:
            result = "不適用"
        return result
    
    #Debug用
    def shehai2(self):
        blist = []
        z = self.fiter_four_ke()
        for i in range(0, len(z)):
            b = z[i][0]
            blist.append(b)
        #if d == 1:
            #result = "不適用，或試他法"
            #return result
        return self.find_sike_relations()
    
    def shehai(self):
        shangke = self.find_sike_relations()[0]
        blist = []
        z = self.fiter_four_ke()
        for i in range(0, len(z)):
            b = z[i][0]
            blist.append(b)
        d = len(set(blist))
        if d == 1 and self.find_sike_relations()[7][0] != "試涉害":
            result = "不適用，或試他法"
            return result
        elif len(self.compare_shehai_number()[0]) == 1:
            reducing = self.compare_shehai_number()
            result = ["涉害", "涉害", self.find_three_pass(reducing[0])]
            return result
        elif shangke.count("比和") == 3:
            result = "不適用，或試他法"
            return result
        elif shangke.count("上尅下") == 0 and shangke.count("下賊上") == 0:
            result = "不適用，或試他法"
            return result
        elif self.find_sike_relations()[7][0] == "試比用":
            result = "不適用，或試他法"
            return result
        elif shangke.count("上尅下") == 1 and shangke.count("下賊上") == 1:
            result = "不適用，或試他法"
            return result
        elif shangke.count("比和") == 2 and shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤返吟":
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(self.Max(self.find_sike_relations()[7][1]))]
            result =  ["返吟", "無依", self.find_three_pass(chuchuan[0])]
            return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤返吟" and self.find_sike_relations()[2].count("尅") == 0 and self.find_sike_relations()[2].count("被尅") == 0:
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(self.Max(self.find_sike_relations()[7][1]))], 1
            result =  ["返吟", "無依", self.find_three_pass(chuchuan[0])]
            return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤返吟" and self.find_sike_relations()[2].count("尅") == 0 and self.find_sike_relations()[2].count("被尅") == 1:
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(self.Max(self.find_sike_relations()[7][1]))]
            result =  ["返吟", "涉害", self.find_three_pass(chuchuan[0])] 
            return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") >= 2 and self.find_sike_relations()[2].count("被尅") == 0:
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(self.Max(self.find_sike_relations()[7][1]))]
            result =  ["返吟", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])] 
            return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") >= 2 and self.find_sike_relations()[2].count("被尅") >= 1:
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(self.Max(self.find_sike_relations()[7][1]))]
            result =  ["返吟", "涉害", self.find_three_pass(chuchuan[0])] 
            return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") == 1:
            if self.find_sike_relations()[2].count("尅") == 1 and self.find_sike_relations()[2].count("被尅") == 0:
                if self.find_sike_relations()[5] == "被尅":
                    if self.find_sike_relations()[8] == "陰":
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                        return result 
                    else:
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                        return result 
                else:   
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                    return result 
            
            elif self.find_sike_relations()[2].count("尅") > 1 and self.find_sike_relations()[2].count("被尅") == 0:
                if self.find_sike_relations()[5] == "被尅":
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                    return result 
                else:
                    
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                    return result 
            
            elif self.find_sike_relations()[2].count("被尅") >= 1 and self.find_sike_relations()[2].count("尅") == 0:
                result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][1])]
                return result
            
            elif self.find_sike_relations()[2].count("被尅") >= 1 and self.find_sike_relations()[2].count("尅") >= 1:
                if self.find_sike_relations()[5] != "被尅":
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])] 
                    return result
                elif self.find_sike_relations()[5] == "被尅":
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                    return result
                    
            else:
                result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][1])]
                return result
        
        elif shangke.count("下賊上") == 3 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("被尅") >= 1 and shangke.count("上尅下") == 0:
            result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
            return result
        
        elif shangke.count("下賊上") == 3 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") == 1 and shangke.count("上尅下") == 0:
            if self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 1:
                if self.find_sike_relations()[5] != "被尅"  and self.find_sike_relations()[5] != "尅":
                    result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                    return result
                else:
                    result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][1][0])]
                    return result
            elif self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 0:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                return result
            elif self.find_sike_relations()[2].count("被尅") == 0 and self.find_sike_relations()[2].count("尅") == 1:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][1])]
                return result
        
        elif shangke.count("下賊上") == 3 and shangke.count("上尅下") == 1: 
          
            if self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 1:
                if self.find_sike_relations()[5] == "尅" or self.find_sike_relations()[5] ==  "被尅":
                    result = ["涉害", "涉害", self.find_three_pass( self.daygangzhi[1])]
                    return result
                elif self.find_sike_relations()[5] != "尅" or self.find_sike_relations()[5] !=   "被尅":
                    result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                    return result
            elif self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 0:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][1])]
                return result
            elif self.find_sike_relations()[2].count("被尅") == 0 and self.find_sike_relations()[2].count("尅") == 1:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                return result
            
            
            else:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][2][0])]
                return result
            
  
        elif shangke.count("下賊上") == 3 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("被尅") == 1 and  self.find_sike_relations()[2].count("尅") == 1:
            result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
            return result
        
        elif shangke.count("下賊上") == 3 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") >= 1:
            result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][2][0])]
            return result
     
        elif shangke.count("下賊上") == 4:
            if self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 1:
                if self.find_sike_relations()[5] == "被尅" or "尅":
                    result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                    return result
                else:   
                    result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][2][0])]
                    return result
            elif self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 0:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                return result
            elif self.find_sike_relations()[2].count("被尅") == 0 and self.find_sike_relations()[2].count("尅") == 1:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                return result
            else:
                result = ["涉害", "涉害", self.find_three_pass( self.find_sike_relations()[7][2][0][0])]
                return result
            
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") == 0 and self.find_sike_relations()[2].count("被尅") == 0:
            result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
            return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") == 0 and self.find_sike_relations()[2].count("被尅") >= 1:
            if  self.find_sike_relations()[5] != "尅":
                
                if self.find_sike_relations()[2].count("被尅") > 1 :
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                    return result
                    
                elif self.find_sike_relations()[5] != "尅":
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                    
                    
                    return result
            elif self.find_sike_relations()[5] == "尅":
                result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                return result
            
            else:
                result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                return result
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟" and self.find_sike_relations()[2].count("尅") > 1:
            reducing = self.compare_shehai_number()
            if len(reducing[0]) == 1:
                result = ["涉害", "涉害", self.find_three_pass(reducing[0])]
                return result
            elif reducing[0] == "找孟仲季地":
                converting = self.convert_munchongji_shehai_number()
                if converting[2][0] == converting[2][1]:
                    result =  ["返吟", "涉害", self.find_three_pass(converting[2][0])] 
                    return result
                elif converting[1][0] + converting[3][0] == "季季":
                    result = ["涉害", "涉害", self.find_three_pass(converting[2][0])]
                    return result
                elif converting[1][1] + converting[3][1] == "季季":
                    result = ["涉害", "涉害", self.find_three_pass(converting[2][0])]
                    return result
                elif converting[1][0] + converting[3][0] == "孟仲" or "仲孟":
                    result = ["涉害", "涉害", self.find_three_pass(converting[2][0])]
                    return result
        elif self.compare_shehai_number() == ["不適用，或試他法"] and self.find_sike_relations()[9] == '天地盤返吟':
            if len([self.find_sike_relations()[7][1]]) == 1:
                chuchuan = self.find_sike_relations()[1][1][0]
                result = ["涉害", "涉害",  self.find_three_pass(self.find_sike_relations()[7][2][1][0])] 
            elif len(self.find_sike_relations()[7][1]) == 2:
                chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(self.Max(self.find_sike_relations()[7][1]))]
                result = ["返吟", "無依",  self.find_three_pass(chuchuan[0])] 
            elif len(self.find_sike_relations()[7][1]) >= 3:
                chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][4].index("True")]
                result = ["返吟", "無依",   self.find_three_pass(chuchuan[0])] 
            return result
        elif self.find_sike_relations()[7][0] == "試涉害": 
            reducing = self.compare_shehai_number()
            if self.find_sike_relations()[7][2][0] == self.find_sike_relations()[7][2][1]:
                chuchuan = self.find_sike_relations()[7][2][0][0]
                result = ["涉害", "涉害",  self.find_three_pass( chuchuan)] 
                return result
            elif shangke.count("上尅下") == 0 and shangke.count("下賊上") == 0:
                result = "不適用，或試他法"
                return result
            elif shangke.count("上尅下") >= 0 and shangke.count("下賊上") == 1:
                result = "不適用，或試他法"
                return result
            elif shangke.count("上尅下") == 2 and shangke.count("下賊上") == 0:
                if self.find_sike_relations()[2].count("尅") >= 1 and self.find_sike_relations()[2].count("被尅") == 0:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                    return result 
                
                elif self.find_sike_relations()[2].count("被尅") ==  1 and self.find_sike_relations()[2].count("尅") == 0:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                    return result
                
                elif self.find_sike_relations()[2].count("被尅") >  1 and self.find_sike_relations()[2].count("尅") == 0:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][1])]
                    return result
          
                
                elif self.find_sike_relations()[2].count("被尅") >  1 and self.find_sike_relations()[2].count("尅") == 0:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                    return result
          
                elif self.find_sike_relations()[2].count("被尅") == 1 and self.find_sike_relations()[2].count("尅") == 1:
                    if  self.find_sike_relations()[5] == "尅":
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][0])]
                        return result
                    
                    elif self.find_sike_relations()[5] == "被尅":
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                        return result
                    
                    elif self.find_sike_relations()[5] == "生":
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                        return result
                    
                    elif self.find_sike_relations()[5] == "被生":
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][1])]
                        return result
                    
                    else:
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                        return result
                
                else:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                    return result
            
            elif shangke.count("上尅下") == 4 and shangke.count("下賊上") == 0:
                if self.find_sike_relations()[5] == "尅" or self.find_sike_relations()[5] ==  "被尅" :
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                    return result
                elif self.find_sike_relations()[5] == "被生":
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][2][0])]
                    return result
            
                else:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][1][1])]
                    return result
            
            elif shangke.count("上尅下") > 2 and shangke.count("下賊上") == 0:
                if len(reducing[0]) == 1:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                    return result
                elif len(reducing[0]) > 1 and self.find_sike_relations()[2].count("尅") == 1:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][1])]                
                    return result
                
                elif len(reducing[0]) > 1 and self.find_sike_relations()[2].count("尅") == 0 and self.find_sike_relations()[2].count("被尅")==1:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[1][self.find_sike_relations()[2].index("被尅")][0])]
                    return result
                elif len(reducing[0]) > 1 and self.find_sike_relations()[2].count("尅") == 0 and self.find_sike_relations()[2].count("被尅") >1:
                    result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[1][self.find_sike_relations()[2].index("被尅")][0])]
                    return result
                elif  len(reducing[0]) > 1 and self.find_sike_relations()[2].count("尅") >= 2:
                    if self.find_sike_relations()[7][4].count('True') == 1 and self.find_sike_relations()[7][4].count('False')>1:
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[1][self.find_sike_relations()[7][4].index("True")][0])]
                        return result
                    elif self.find_sike_relations()[7][4].count('True') > 1 and self.find_sike_relations()[7][4].count('False') ==1:
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[1][self.find_sike_relations()[7][4].index("False")][0])]
                        return result
                    elif self.find_sike_relations()[7][4].count('True') == 0:
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][0])]
                        return result
                    elif self.find_sike_relations()[7][4].count('False') == 0:
                        result = ["涉害", "涉害", self.find_three_pass(self.find_sike_relations()[7][2][0][1])]
                        return result

                elif reducing[0] == "不適用，或試他法":
                    tail = [self.find_sike_relations()[7][2][i][1] for i in range(0, len(self.find_sike_relations()[7][2]))]
                    if tail[0] == self.daygangzhi[0]:
                        chuchuan = self.find_sike_relations()[7][2][0][0]
                        result = ["涉害", "涉害", self.find_three_pass(chuchuan)]
                        return result
                        
                    elif tail[1] == self.daygangzhi[0]:
                        chuchuan = self.find_sike_relations()[7][2][1][0]
                        result = ["涉害", "涉害", self.find_three_pass(chuchuan)]
                        return result
                elif reducing[0] == "找孟仲季地":
                    convert = self.convert_munchongji_shehai_number()
                    convert_dict = {convert[0][0]+convert[2][0]: convert[1][0]+convert[3][0], convert[0][1]+convert[2][1]: convert[1][1]+convert[3][1] }
                    change_daygangzhi =  self.shigangjigong.get(self.daygangzhi[0])
                    convert_result_k = list(convert_dict.keys())
                    convert_result_v = list(convert_dict.values())
                    #convert_result_head = [i[0] for i in convert_result_k]
                    convert_result_tail = [i[1] for i in convert_result_k]
                    dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
                    if len(convert[2]) == 3:
                        if convert[2][0] == change_daygangzhi:
                            chuchuan = convert[2][0]
                        elif convert[2][1] == change_daygangzhi:
                            chuchuan = convert[2][1]
                        elif convert[2][2] == change_daygangzhi:
                            chuchuan = convert[2][2]
                        name = "見機"
                    elif len(convert[2]) == 2:
                        if convert_result_v[0] == "季孟" or "仲孟":  
                            chuchuan = convert_result_k[1][1]
                            name = "見機"
                        elif  convert_result_v[0] == "孟季" or "仲季" or "季季":  
                            chuchuan = convert_result_k[1][0]
                            name = "見機"
                        elif convert_result_v[0][0] == convert_result_v[0][1]:
                            if dayganzhi_yy == convert_result_k[0][0]:
                                chuchuan = convert_result_k[0][0]
                            elif dayganzhi_yy == convert_result_k[1][0]:
                                chuchuan = convert_result_k[1][0]
                            name = "綴瑕"
                    result = ["涉害", name, self.find_three_pass(chuchuan)] 
                    return result
        elif shangke.count("下賊上") >= 3:
            reducing = self.compare_shehai_number()
            if len(reducing[0]) == 1:
                result = ["涉害", "涉害", self.find_three_pass(reducing[0])]
                return result
            else: 
                result = "不適用，或試他法"
            return result
        elif shangke.count("上尅下") == 1 and shangke.count("下賊上") == 3:
            reducing = self.compare_shehai_number()
            if self.find_sike_relations()[7][0] == "試比用":
                result = "不適用，或試他法"
                return result
            elif len(reducing[0]) == 1:
                result = ["涉害","涉害", self.find_three_pass(reducing[0])]
                return result
            elif reducing[0] == "找孟仲季地":
                convert = self.convert_munchongji_shehai_number()
                convert_dict = {convert[2][0]+convert[0][0]: convert[3][0]+convert[1][0], convert[2][1]+convert[0][1]: convert[3][1]+convert[1][1] }
                convert_result_k = list(convert_dict.keys())
                convert_result_v = list(convert_dict.values())
                convert_result_tail = [i[1] for i in convert_result_k]
                change_daygangzhi = self.shigangjigong.get(self.daygangzhi[0])
                if convert_result_v[0] == "孟季" or "仲季" or "季季":
                    if convert_result_v[1][1] == "孟":
                        if convert_result_tail[0] or convert_result_tail[1] ==  change_daygangzhi:
                             name = "綴瑕"
                        else:
                             name = "見機"
                    elif convert_result_v[1][1] == "仲":
                        name = "察微" 
                chuchuan = convert_result_k[1][0]
                result = ["涉害", name, self.find_three_pass(chuchuan)]
                return result
            else:
                result = "不適用，或試他法"
                return result
           
    def yaoke(self):
        if self.find_sike_relations()[3] == "日干支同位":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[4] == "伏吟":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        sike = self.all_sike()
        sike_list = self.find_sike_relations()[0]
        dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
       
        if sike_list.count("下賊上") == 1 and sike_list.count("上尅下") == 1:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list.count("下賊上") > 0 or sike_list.count("上尅下") > 0:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        if self.find_sike_relations()[2].count("尅") == 1:
            if self.find_sike_relations()[6] == "反吟":
                chuchuan = ["返吟", "無親", [self.yima_dict.get(self.hourgangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.shigangjigong.get(self.shigangjigong.get(self.daygangzhi[0])))]]
                return chuchuan
            else:
                chuchuan = ["遙尅","遙尅", self.find_three_pass(sike[self.find_sike_relations()[2].index("尅")][0] )]
                return chuchuan
        elif self.find_sike_relations()[2].count("尅") > 1:
            filterlist = [sike[i][0] for i in self.duplicates(self.find_sike_relations()[2], "尅")]
            filterlist2 = [self.gangzhi_yinyang(b) for b in filterlist]
            nn_list = []
            for n in filterlist2:
                if n == dayganzhi_yy:
                    p = "True"
                else:
                    p = "False"
                nn_list.append(p)
                if nn_list.count('True') > 0:
                    chuchuan = ["遙尅","蒿矢", self.find_three_pass(sike[nn_list.index('True')][0] )] or  ["遙尅","蒿矢", self.find_three_pass(sike[nn_list.index('False')][0] )]
                    return chuchuan
                elif nn_list.count('False') > 0:
                    chuchuan = ["遙尅","蒿矢", self.find_three_pass(self.daygangzhi[1])] 
                    return chuchuan
        elif self.find_sike_relations()[2].count("被尅") == 1:
            chuchuan = ["遙尅","彈射", self.find_three_pass(sike[self.find_sike_relations()[2].index("被尅")][0] )]
            return chuchuan
        elif self.find_sike_relations()[2].count("被尅") == 2:
            if self.find_sike_relations()[6] == "反吟":
                chuchuan = ["返吟","無親", [self.yima_dict.get(self.hourgangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0])) ]]
                return chuchuan
            else:
                chuchuan = ["遙尅","彈射", self.find_three_pass(sike[self.find_sike_relations()[2].index("被尅")][0] )]
                return chuchuan
        elif self.find_sike_relations()[2].count("被尅") == 0 and self.find_sike_relations()[2].count("尅") == 0:
            chuchuan = "不適用，或試他法"  
            return chuchuan
    
    def maosing(self):
        sike = self.all_sike()
        sike_list = self.find_sike_relations()[0]
        dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
        sikehead = [b[0] for b in sike]
        d =  Counter(sikehead)
        res = [k for k, v in d.items() if v > 1]
        if len(set(sike)) <4 and self.find_sike_relations()[2].count("尅") > 1:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[2].count("尅") >0:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
            if dayganzhi_yy == "陽":
                try:
                    if len(res[0]) >= 1:
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                except IndexError:
                    if self.find_sike_relations()[6] == "反吟":
                        chuchuan = ["返吟", "無親", [self.yima_dict.get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0])) ]]
                        return chuchuan
                    elif self.find_sike_relations()[6] == "反吟八專":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
                        chuchuan = ["昴星", "虎視", [self.sky_n_earth_list().get("酉"), self.sky_n_earth_list().get(self.daygangzhi[1]), self.all_sike()[3][0]]]
                        return chuchuan
            if dayganzhi_yy == "陰":
                try:
                    if len(res[0]) >= 1:
                        ganlivezhi = self.shigangjigong
                        chuchuan = ["昴星","冬蛇掩目", [self.earth_n_sky_list().get("酉"), self.sky_n_earth_list().get(ganlivezhi.get(self.daygangzhi[0])), self.all_sike()[1][0]]]
                        return chuchuan
                except IndexError:
                    if self.find_sike_relations()[6] == "反吟":
                        chuchuan = ["返吟","無親", [self.yima_dict.get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0])) ]]
                        return chuchuan
                    elif self.find_sike_relations()[6] == "反吟八專":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
			ganlivezhi = self.shigangjigong
                        chuchuan = ["昴星","冬蛇掩目", [self.earth_n_sky_list().get("酉"), self.sky_n_earth_list().get(ganlivezhi.get(self.daygangzhi[0])), self.all_sike()[1][0]]]
                        return chuchuan
        else:
            chuchuan = "不適用，或試他法"  
            return chuchuan
    
    def bieze(self):
        sike = [ i[0] for i in self.all_sike()]
        dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
        sike_list = self.find_sike_relations()[0]
        if len(set(sike)) == 4:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[3] == "日干支同位":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[4] == "伏吟":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
            if dayganzhi_yy == "陽":
                #寄干藏支
                sky_ganhe = dict(zip(self.Gan[0:5], self.Gan[5:10]))
                ganhe_result1 = self.shigangjigong.get(sky_ganhe.get(self.daygangzhi[0]))
                if self.find_sike_relations()[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                elif self.find_sike_relations()[4] == "伏吟":
                    chuchuan =  "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["別責", "別責", [self.sky_n_earth_list().get(ganhe_result1), self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0])),  self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0]))]]
                    return chuchuan
            if dayganzhi_yy == "陰":
                sep = "巳酉丑,寅午戌,亥卯未,申子辰".split(",")
                earth_zhihe = dict(zip(list(map(lambda x: tuple(x), sep)), sep))
                result = self.multi_key_dict_get(earth_zhihe, self.daygangzhi[1])
                position = result.index(self.daygangzhi[1])
                if position == 0:
                    a = result[1]
                elif position == 1:
                    a = result[2]
                elif position == 2:
                    a = result[0]
                if self.find_sike_relations()[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                elif self.find_sike_relations()[4] == "伏吟":
                    chuchuan =  "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["別責", "別責", [self.sky_n_earth_list().get(a), self.shigangjigong.get(self.daygangzhi[0]), self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0]))]]
                    return chuchuan
        elif self.find_sike_relations()[4] == "伏吟":
            chuchuan =  "不適用，或試他法" 
            return chuchuan
        if sike_list.count("下賊上") + sike_list.count("上尅下") >= 1 :
            chuchuan =  "不適用，或試他法" 
            return chuchuan
    
    def bazhuan(self):
        sike = self.all_sike()
        sike_list = self.find_sike_relations()[0]
        dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
        if sike_list.count("下賊上") == 1 and sike_list.count("上尅下") == 1:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list.count("下賊上") > 0 or sike_list.count("上尅下") > 0:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[4] == "伏吟" :
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[6] == "反吟八專" and self.find_sike_relations()[4] == "伏吟" :
            chuchuan = ["返吟", "無親", [self.yima_dict.get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.shigangjigong.get(self.daygangzhi[0]))]]
            return chuchuan
        elif self.find_sike_relations()[3] == "日干支同位":
            if sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
                if dayganzhi_yy == "陽":
                    pos = self.Zhi.index(sike[3][0])+2
                    if pos == 13:
                        pos = 1
                    elif pos == 14:
                        pos = 0
                    pos = self.Zhi[pos]
                    if self.find_sike_relations()[4] == "伏吟":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
                        chuchuan = ["八專","八專", [pos, self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1])]]
                        return chuchuan
                elif dayganzhi_yy == "陰":
                    pos = self.Zhi.index(sike[0][0])-2
                    if pos == -2:
                        pos = 10
                    elif pos == -1:
                        pos = 11
                    pos = self.Zhi[pos]
                    if self.find_sike_relations()[4] == "伏吟" and self.find_sike_relations()[6] == "反吟八專":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
                        chuchuan = ["八專", "八專",[pos, self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1])]]   
                        return chuchuan 
        elif self.find_sike_relations()[3] == "日干支不同位":
            chuchuan = "不適用，或試他法" 
            return chuchuan
    
    def fuyin(self):
        def unique(list1): 
            unique_list = [] 
            for x in list1: 
                if x not in unique_list: 
                    unique_list.append(x) 
                return x
        sike_list = self.find_sike_relations()
        dayganzhi_yy = self.gangzhi_yinyang(self.daygangzhi[0])
        if sike_list[4] == "非伏吟" or len(self.zeike())> 2:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list[4] == "伏吟":
            if sike_list[0].count("上尅下") == 1 or sike_list[0].count("下賊上") == 1:
                chuchuan = ["伏吟", "不虞",  [unique(sike_list[1])[0], self.ying.get(unique(sike_list[1])[0]), self.ying.get(self.ying.get(unique(sike_list[1])[0])) ]]
                return chuchuan
            elif sike_list[0].count("上尅下") == 0 and sike_list[0].count("下賊上") == 0:
                if dayganzhi_yy == "陽":
                    if self.multi_key_dict_get(self.ying_chong, self.shigangjigong.get(self.daygangzhi[0])) =="刑":
                        chuchuan = ["伏吟","自任", [self.shigangjigong.get(self.daygangzhi[0]), self.ying.get(self.shigangjigong.get(self.daygangzhi[0])), self.ying.get(self.ying.get(self.shigangjigong.get(self.daygangzhi[0])))]]
                        return chuchuan
                    elif self.multi_key_dict_get(self.ying_chong, self.shigangjigong.get(self.daygangzhi[0])) =="自刑":
                        chuchuan = ["伏吟", "杜傳", [self.shigangjigong.get(self.daygangzhi[0]), self.daygangzhi[1], self.ying.get(self.daygangzhi[1])]]
                        return chuchuan
                elif dayganzhi_yy == "陰":
                    if self.multi_key_dict_get(self.ying_chong, self.shigangjigong.get(self.daygangzhi[1])) =="刑":
                        chuchuan = ["伏吟","自任", [self.shigangjigong.get(self.daygangzhi[1]), self.ying.get(self.shigangjigong.get(self.daygangzhi[0])), self.ying.get(self.ying.get(self.shigangjigong.get(self.daygangzhi[0])))]]
                        return chuchuan
                    elif self.multi_key_dict_get(self.ying_chong, self.shigangjigong.get(self.daygangzhi[1])) =="自刑":
                        chuchuan = ["伏吟", "杜傳", [self.shigangjigong.get(self.daygangzhi[1]), self.chong2.get(self.ying.get(self.shigangjigong.get(self.daygangzhi[0]))), self.ying.get(self.chong2.get(self.ying.get(self.shigangjigong.get(self.daygangzhi[0]))))]]
                        return chuchuan
                    chuchuan = ["伏吟", "自信", [self.daygangzhi[1], self.ying.get(self.daygangzhi[1]), self.chong2.get(self.daygangzhi[1])]]
                    return chuchuan

    #丁馬    
    def dinhorse(self):
        dinhorsedict = dict(zip(self.jiazi()[0::10], list("卯丑亥酉未巳")))
        liujiashun_dict = self.liujiashun_dict 
        shun =  self.multi_key_dict_get(liujiashun_dict, self.daygangzhi)
        return self.multi_key_dict_get(dinhorsedict, shun)

    #月馬
    def moonhorse(self):
        moonhorsedict = dict(zip(list(map(lambda x: tuple(x) ,"寅申,卯酉,辰戌,巳亥,午子,丑未".split(","))), list("午申戌子寅辰")))
        return self.multi_key_dict_get(moonhorsedict, self.daygangzhi[1])
    
    #日馬
    def dayhorse(self):
        return dict(zip(self.Zhi, "寅亥申巳寅亥申巳寅亥申巳")).get(self.daygangzhi[1])
    
    #華蓋
    def wahgai(self):
        return dict(zip(self.Zhi, "戌丑戌未戌丑戌未戌丑戌未")).get(self.daygangzhi[1])

    #閃電
    def lightning(self):
        lightningd = dict(zip(self.Zhi, list(itertools.chain.from_iterable(map(lambda x: x*2, list("辰未戌丑寅卯"))))))
        return lightningd.get(self.daygangzhi[1])
    
    #排貴人起點
    def guiren_starting_gangzhi(self, num):        
        guiren_dict = dict(zip(list(map(lambda x: tuple(x), list("甲,戊庚,丙,丁,壬,癸,乙,己,辛".split(",")))), list(map(lambda x: dict(zip(list("晝夜"), x)) ,"未丑,丑未,酉亥,亥酉,卯巳,巳卯,申子,子申,寅午".split(",")))))
        guiren_dict2 = dict(zip(list(map(lambda x: tuple(x), list("甲戊庚,乙己,丙丁,壬癸,辛".split(",")))), list(map(lambda x: dict(zip(list("晝夜"), x)) ,"丑未,子申,亥酉,巳卯,午寅".split(",")))))
        option  = {0: guiren_dict2, 1: guiren_dict}
        get_day = self.multi_key_dict_get(option.get(num), self.daygangzhi[0])
        find_day_or_night = self.multi_key_dict_get(self.daynight_richppl_dict, self.hourgangzhi[1])
        return get_day.get(find_day_or_night)
    
    def guiren_start_earth(self, num):
        sky = self.earth_n_sky_list()
        return sky.get(self.guiren_starting_gangzhi(num))
    
    def guiren_order_list(self, num):
        starting_gangzhi = self.guiren_starting_gangzhi(num)
        rotation = dict(zip(list(map(lambda x: tuple(x), [list(i) for i in "巳午未申酉戌,亥子丑寅卯辰".split(",")])), "逆佈,順佈".split(",")))
        new_zhi_list_guiren = self.new_zhi_list(starting_gangzhi)
        guiren = self.guiren_start_earth(num) 
        pai_gui = self.new_list(self.sky_generals, "貴")
        rotation_results = self.multi_key_dict_get(rotation, guiren)
        if rotation_results == "順佈":
            return dict(zip(new_zhi_list_guiren, pai_gui))
        elif rotation_results == "逆佈":
            return dict(zip(new_zhi_list_guiren, self.new_list(list(reversed(self.sky_generals)), "貴")))
    
    def result(self, num):
        answer =  [self.zeike(), self.biyung(), self.shehai(), self.yaoke(), self.maosing(), self.bieze(), self.bazhuan(), self.fuyin()]
        nouse = ["不適用，或試他法" ]
        ju_three_pass = [i for i in answer if i not in nouse] 
        sky_earth = self.sky_n_earth_list()
        sky = list(sky_earth.values())
        earth = list(sky_earth.keys())
        guiren_order_list_2 = self.guiren_order_list(num)
        guiren_order_list_3 = [guiren_order_list_2.get(i) for i in sky]
        earth_to_general = dict(zip(earth, guiren_order_list_3))
        sky_earth_guiren_dict = {"天盤":sky, "地盤":earth, "天將":guiren_order_list_3}
        ju = [ju_three_pass[0][0], ju_three_pass[0][1]]
        three_pass_zhi = ju_three_pass[0][2]
        three_pass_generals = [guiren_order_list_2.get(i) for i in three_pass_zhi]
        day_gz_vs_three_pass = [self.liuqing_dict.get(self.multi_key_dict_get(self.wuxing_relation_2,self.Ganzhiwuxing(self.daygangzhi[0])+self.Ganzhiwuxing(three_pass_zhi[i])))for i in range(0,len(three_pass_zhi))]
        three_pass = {"初傳":[three_pass_zhi[0], three_pass_generals[0], day_gz_vs_three_pass[0][0], self.shunkong(self.daygangzhi,three_pass_zhi[0])], "中傳":[three_pass_zhi[1], three_pass_generals[1], day_gz_vs_three_pass[1][0], self.shunkong(self.daygangzhi,three_pass_zhi[1])], "末傳":[three_pass_zhi[2], three_pass_generals[2], day_gz_vs_three_pass[2][0], self.shunkong(self.daygangzhi,three_pass_zhi[2])]}
        sike_zhi = self.all_sike()
        sike_generals = [ guiren_order_list_2.get(i[0]) for i in sike_zhi]
        sike = {"四課":[sike_zhi[0], sike_generals[0]], "三課":[sike_zhi[1], sike_generals[1]], "二課":[sike_zhi[2], sike_generals[2]], "一課":[sike_zhi[3], sike_generals[3]]}
        dyima = self.multi_key_dict_get(self.yimadict, self.daygangzhi[1])
        #starpan = dict(zip(self.new_zhi_list("巳"), [self.multi_key_dict_get(self.hoursu, self.daygangzhi[0]).get(i) for i in self.new_zhi_list("巳")]))
        return {"節氣":self.jieqi, "日期":self.daygangzhi+"日"+self.hourgangzhi+"時", "格局":ju, "日馬": dyima, "三傳":three_pass, "四課":sike, "天地盤":sky_earth_guiren_dict, "地轉天盤":sky_earth, "地轉天將": earth_to_general }
        
    def result_m(self, num):
        answer =  [self.zeike(), self.biyung(), self.shehai(), self.yaoke(), self.maosing(), self.bieze(), self.bazhuan(), self.fuyin()]
        nouse = ["不適用，或試他法" ]
        ju_three_pass = [i for i in answer if i not in nouse]
        sky_earth = self.sky_n_earth_list()
        sky = list(sky_earth.values())
        earth = list(sky_earth.keys())
        guiren_order_list_2 = self.guiren_order_list(num)
        guiren_order_list_3 = [guiren_order_list_2.get(i) for i in sky]
        earth_to_general = dict(zip(earth, guiren_order_list_3))
        sky_earth_guiren_dict = {"天盤":sky, "地盤":earth, "天將":guiren_order_list_3}
        ju = [ju_three_pass[0][0], ju_three_pass[0][1]]
        three_pass_zhi = ju_three_pass[0][2]
        three_pass_generals = [guiren_order_list_2.get(i) for i in three_pass_zhi]
        day_gz_vs_three_pass = [  self.liuqing_dict.get(self.multi_key_dict_get(self.wuxing_relation_2,self.Ganzhiwuxing(self.hourgangzhi[0])+self.Ganzhiwuxing(three_pass_zhi[i])))for i in range(0,len(three_pass_zhi))]
        three_pass = {"初傳":[three_pass_zhi[0], three_pass_generals[0], day_gz_vs_three_pass[0], self.shunkong(self.hourgangzhi,three_pass_zhi[0])], "中傳":[three_pass_zhi[1], three_pass_generals[1], day_gz_vs_three_pass[1], self.shunkong(self.hourgangzhi,three_pass_zhi[1])], "末傳":[three_pass_zhi[2], three_pass_generals[2], day_gz_vs_three_pass[2], self.shunkong(self.hourgangzhi,three_pass_zhi[2])]}
        sike_zhi = self.all_sike()
        sike_generals = [ guiren_order_list_2.get(i[0]) for i in sike_zhi]
        sike = {"四課":[sike_zhi[0], sike_generals[0]], "三課":[sike_zhi[1], sike_generals[1]], "二課":[sike_zhi[2], sike_generals[2]], "一課":[sike_zhi[3], sike_generals[3]]}
        dyima = self.multi_key_dict_get(self.yimadict, self.hourgangzhi[1])
        #starpan = dict(zip(self.new_zhi_list("巳"), [self.multi_key_dict_get(self.hoursu, self.hourgangzhi[0]).get(i) for i in self.new_zhi_list("巳")]))
        return {"節氣":self.jieqi, "日期":self.daygangzhi+"時"+self.hourgangzhi+"分", "格局":ju, "日馬": dyima, "三傳":three_pass, "四課":sike, "天地盤":sky_earth_guiren_dict, "地轉天盤":sky_earth, "地轉天將": earth_to_general}

    
if __name__ == '__main__':
	#print(Liuren("雨水","癸卯","己未").find_sike_relations())
    j = "白露"
    d =  "辛巳"
    h =  "戊子"
    m = "八"
    tic = time.perf_counter()
    print(d +"     " + h)
    print(Liuren(j, m, d, h).result(0))
    print("    ")
    print(Liuren(j, m, d, h).guiren_order_list(0))
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")
    
