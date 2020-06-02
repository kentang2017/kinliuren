# -*- coding: utf-8 -*-
"""
Created on Sun Dec  22 16:22:37 2019

@author: ken tang
@email: kinyeah@gmail.com
"""

from collections import Counter
from liurendict import *

class Liuren():
    def __init__(self, jieqi, daygangzhi, hourgangzhi):
        self.jieqi = jieqi
        self.daygangzhi = daygangzhi
        self.hourgangzhi = hourgangzhi

    def sky_n_earth_list(self):
        earth = new_zhi_list(self.hourgangzhi[1])
        sky = sky_pan_list(self.jieqi)[0]
        return dict(zip(earth, sky))
    
    def earth_n_sky_list(self):
        earth = new_zhi_list(self.hourgangzhi[1])
        sky = sky_pan_list(self.jieqi)[0]
        return dict(zip(sky, earth))

    def all_sike(self):
        yike = self.sky_n_earth_list()[shigangjigong.get(self.daygangzhi[0])] + self.daygangzhi[0]
        sky_n_earth = self.sky_n_earth_list()
        erke = sky_n_earth.get(yike[0]) + yike[0]
        sanke = sky_n_earth.get(self.daygangzhi[1]) + self.daygangzhi[1]
        sike = sky_n_earth.get(sanke[0]) + sanke[0]
        return [sike, sanke, erke, yike]

    def fanyin(self):
        sky_earth = self.sky_n_earth_list()
        sky =  list(sky_earth.values())
        earth = list(sky_earth.keys())
        earth_sky_combine = [ ganzhiwuxing(sky[i]) +  ganzhiwuxing(earth[i]) for i in range(0,len(sky_earth))]
        earth_sky_combine_wuxing = [multi_key_dict_get(wuxing_relation_2, earth_sky_combine[i]) for i in range(0,len(earth_sky_combine))]
        count_ke_and_being_ke = earth_sky_combine_wuxing.count("被尅") + earth_sky_combine_wuxing.count("尅")
        return count_ke_and_being_ke, earth_sky_combine_wuxing

    def find_sike_shangke(self):
        sike_list = []
        sike = self.all_sike()
        for i in sike:
            b = find_ke_relation(i)
            sike_list.append(b)
        return sike_list

    def find_sike_relations(self):
        sike_list = []
        sike = self.all_sike()
        for i in sike:
            b = find_ke_relation(i)
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
        elif sike_list.count("下賊上") == 2 and sike_list.count("上尅下") == 0 :
            classify = "下賊上"
        elif sike_list.count("下賊上") >= 2 and sike_list.count("上尅下") <= 1 :
            classify = "下賊上"
        elif sike_list.count("上尅下") == 0 and sike_list.count("下賊上") == 0 :
            classify = "試其他"
        elif sike_list.count("上尅下") >= 2 and sike_list.count("下賊上") == 0 :
            classify = "上尅下"
        dayganzhi_wuxing = ganzhiwuxing(self.daygangzhi[0])
        dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
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
        fanyin_day_dict = {tuple(fanyin_days):"反吟",tuple(bazhuan_fanyin_days):"反吟八專",tuple(jiazi_remove_fanyin+bazhuan_fanyin_days):"非反吟"}
        checkdayganzhi = multi_key_dict_get(checkdayganzhi_dict, self.daygangzhi)
        checkfanyin = multi_key_dict_get(fanyin_day_dict, self.daygangzhi)
        moon_general = sky_pan_list(self.jieqi)[1]
        checkmoongeneralconflicttohour = multi_key_dict_get(wuxing_relation_2, ganzhiwuxing(moon_general)+ganzhiwuxing(self.hourgangzhi[1]))
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
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(self.daygangzhi[0]), fan_yin
            
        elif sike_list.count("上尅下") == 1 and sike_list.count("下賊上") == 0:
            findtrue = ["試賊尅", sike_list.index("上尅下"),  "沒有", classify, "沒有", "沒有"]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(self.daygangzhi[0]), fan_yin
        
        elif sike_list.count("下賊上") == 1:
            findtrue = ["試賊尅", sike_list.index("下賊上"),  "沒有", classify, "沒有", "沒有"]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(self.daygangzhi[0]), fan_yin
        
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
            for i in range(0, len(zeikeshang_list)):
                b = zeikeshang_list[i][0]
                blist.append(b)
            check_same = len(set(blist))
            if check_same == 1:
                findtrue = ["試賊尅", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same] #結果, 尅克位置, 課式
                
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True")==0:
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
                
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True") >=1 and nn_list.count("False") >=1: 
                findtrue = ["試比用", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
                
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True") >=2 and nn_list.count("False") ==0:
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
                
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(self.daygangzhi[0]), fan_yin
    
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
            
            for i in range(0, len(zeikeshang_list)):
                b = zeikeshang_list[i][0]
                blist.append(b)
            check_same = len(set(blist))
            if check_same == 1:
                findtrue = ["試賊尅", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same] #結果, 尅克位置, 課式
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True")==0:
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) >= 2 and nn_list.count("True")>=1  and nn_list.count("False") >=1: 
                findtrue = ["試比用", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            elif len(set(zeikeshang_list)) == 2 and nn_list.count("True")>=2  and nn_list.count("False") ==0: 
                findtrue = ["試涉害", find_ke,  zeikeshang_list, classify, nn_list, yy_list, check_same]
            return sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, gangzhi_yinyang(self.daygangzhi[0]), fan_yin

    def sike_dict(self):
        sike = self.all_sike()
        sike_list = self.find_sike_relations()[0]
        dyingyang = gangzhi_yinyang(self.daygangzhi[0])
        sike_yingyan = [gangzhi_yinyang(i[0]) for i in sike]
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
        elif sike_list[0].count("下賊上") > 2 and sike_list[7][6] > 1:
            findtrue =  "不適用，或試他法" 
            return findtrue
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
        elif sike_list[0].count("上尅下") > 2 and sike_list[0].count("下賊上") == 0: 
            findtrue =  "不適用，或試他法" 
            return findtrue
        elif sike_list[0].count("上尅下") > 2 and sike_list[0].count("下賊上") == 0 and sike_list[7][0] == "試賊尅" and set(sike_list[7][1]) == 1:
            findtrue =  ["賊尅","元首", self.find_three_pass(sike_list[7][2][0][0])]
            return findtrue
        
        #一個下賊上
        elif sike_list[0].count("下賊上") == 1 and sike_list[9] == '天地盤沒有返吟':
            findtrue =  ["賊尅","重審", self.find_three_pass(sike[sike_list[0].index("下賊上")][0])]
            return findtrue
        
        elif sike_list[0].count("下賊上") >= 1 and sike_list[9] == '天地盤返吟':
            findtrue =  ["返吟","無依", [sike[sike_list[0].index("下賊上")][0], self.daygangzhi[1], self.guiren_starting_gangzhi(0)]]
            return findtrue
        elif sike_list[0].count("下賊上") == 2 and sike_list[0].count("下賊上") == 0 and  sike_list[9] == '天地盤沒有返吟': 
            if sike_list[7][2][0] == sike_list[7][2][1]:
                findtrue =  ["賊尅","重審", self.find_three_pass(sike_list[7][2][0][0])]
            elif sike_list[7][2][0] != sike_list[7][2][1]:
                findtrue =   "不適用，或試他法" 
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
            findtrue =  ["返吟","無依", [sike[sike_list[0].index("上尅下")][0], ying.get(sike[sike_list[0].index("上尅下")][0]), chong2.get(sike[sike_list[0].index("上尅下")][0])] ]
            return findtrue

    def biyung(self):
        sike_list = self.all_sike()
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
            findtrue = ["返吟", "無依", [sike_list[filter_list[4].index("True")][1], chong(sike_list[filter_list[4].index("True")][1]), chong(chong(sike_list[filter_list[4].index("True")][1]))]]
            return findtrue
        elif relation[0].count("下賊上") == 3 and relation[9] == '天地盤返吟':
            findtrue = ["返吟", "無依", [sike_list[filter_list[4].index("True")][0], chong(sike_list[filter_list[4].index("True")][0]), chong(chong(sike_list[filter_list[4].index("True")][0]))]]
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
        d = duplicates(b, "True")
        e = duplicates(b, "False")
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
            if shigangjigong.get(t[-1]) == None:
                t = t
            elif shigangjigong.get(t[-1]) is not None:
                t[-1] = shigangjigong.get(t[-1])
            
            try:
                for i in range(0,len(a)):
                    for k, v in self.sky_n_earth_list().items():
                            if v == a[i][0]:
                                khead.append(k)
                for i in range(0,len(a)):
                    biyung_result_reorder = new_zhigangcangong_list(khead[i])[0: new_zhigangcangong_list(khead[i]).index(a[i][0])+1]
                    biyung_result_reorder_list3.append([ganzhiwuxing(c[i][0])+k  for k in [ganzhiwuxing(j) for j in biyung_result_reorder]].count((ganzhiwuxing(a[i][0])+ganzhiwuxing(a[i][1]))))
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

    def convert_munchongji(self):
        munconji = {tuple("寅申巳亥"):"孟",  tuple("子午卯酉"):"仲", tuple("辰戌丑未"):"季"}
        head = self.compare_shehai_number()[2]
        tail = self.compare_shehai_number()[3]
        head_convert = []
        tail_convert = []
        for a in head:
            g =  multi_key_dict_get(munconji, a)
            head_convert.append(g)
        for k in tail:
            l = multi_key_dict_get(munconji, k)
            tail_convert.append(l)
        if self.compare_shehai_number()[0] == "找孟仲季地":
            result = [head, head_convert, tail, tail_convert]
        else:
            result = ["不適用"]
        return result
        
    def convert_munchongji_shehai_number(self):
        munconji = {tuple("寅申巳亥"):"孟",  tuple("子午卯酉"):"仲", tuple("辰戌丑未"):"季"}
        head = [shigangjigong.get(i) for i in self.compare_shehai_number()[2]]
        tail = [shigangjigong.get(i) for i in self.compare_shehai_number()[3]]
        head_convert = []
        tail_convert = []
        for a in head:
            g =  multi_key_dict_get(munconji, a)
            head_convert.append(g)
        for k in tail:
            l = multi_key_dict_get(munconji, k)
            tail_convert.append(l)
        if self.compare_shehai_number()[0] == "找孟仲季地":
            result = [head, head_convert, tail, tail_convert]
        else:
            result = "不適用"
        return result

    def shehai(self):
        shangke = self.find_sike_relations()[0]
        blist = []
        z = self.fiter_four_ke()
        for i in range(0, len(z)):
            b = z[i][0]
            blist.append(b)
        d = len(set(blist))
        if d == 1:
            result = "不適用，或試他法"
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
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(Max(self.find_sike_relations()[7][1]))]
            result =  ["返吟", "無依", self.find_three_pass(chuchuan[0])] 
            return result
        
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤返吟":
            chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(Max(self.find_sike_relations()[7][1]))]
            result =  ["返吟", "無依", find_three_pass(jieqi, hourgangzhi, chuchuan[0])] 
            return result
        
        elif self.compare_shehai_number() == ["不適用，或試他法"] and self.find_sike_relations()[9] == '天地盤返吟':
            if self.find_sike_relations()[7][1] == 1:
                chuchuan = self.find_sike_relations()[1][1][0]
                result = ["返吟", "無依",  self.find_three_pass(chuchuan[0])] 
            elif self.find_sike_relations()[7][1] == 2:
                chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][1].index(Max(self.find_sike_relations()[7][1]))]
                result = ["返吟", "無依",  self.find_three_pass(chuchuan[0])] 
            elif self.find_sike_relations()[7][1] >= 3:
                chuchuan = self.find_sike_relations()[7][2][self.find_sike_relations()[7][4].index("True")]
                result = ["返吟", "無依",   self.find_three_pass(chuchuan[0])] 
            return result
        
        elif self.find_sike_relations()[7][0] == "試涉害": 
            reducing = self.compare_shehai_number()
            if self.find_sike_relations()[7][2][0] == self.find_sike_relations()[7][2][1]:
                chuchuan = self.find_sike_relations()[7][2][0][0]
                result = ["涉害", "涉害",  self.find_three_pass(chuchuan)] 
                return result
            elif shangke.count("上尅下") == 0 and shangke.count("下賊上") == 0:
                result = "不適用，或試他法"
                return result
    
            elif shangke.count("上尅下") >= 0 and shangke.count("下賊上") == 1:
                result = "不適用，或試他法"
                return result
            
            elif shangke.count("上尅下") == 0 and shangke.count("下賊上") == 2:
                chuchuan = self.compare_shehai_number()[0]
                result = ["涉害", "涉害",  self.find_three_pass(chuchuan)] 
                return result
            
            elif shangke.count("上尅下") >= 2 and shangke.count("下賊上") == 0:
                if len(reducing[0]) == 1:
                    result = ["涉害", "涉害", self.find_three_pass(reducing[0])]
                    return result
    
                elif reducing[0] == "不適用，或試他法":
                    tail = [self.find_sike_relations()[7][2][i][1] for i in range(0, len(self.find_sike_relations()[7][2]))]
                    if tail[0] == self.daygangzhi[0]:
                        chuchuan = self.find_sike_relations()[7][2][0][0]
                        result = ["涉害", "涉害", self.find_three_pass(chuchuan)]
                        return result
                        
                    elif tail[1] == self.daygangzhi[0]:
                        chuchuan = self.find_sike_relations()[7][2][1][0]
                        result = ["涉害", "涉害", self.find_three_pass()]
                        return result
                        
                elif reducing[0] == "找孟仲季地":
                    convert = self.convert_munchongji_shehai_number()
                    convert_dict = {convert[0][0]+convert[2][0]: convert[1][0]+convert[3][0], convert[0][1]+convert[2][1]: convert[1][1]+convert[3][1] }
                    change_daygangzhi =  shigangjigong.get(self.daygangzhi[0])
                    convert_result_k = list(convert_dict.keys())
                    convert_result_v = list(convert_dict.values())
                    convert_result_head = [i[0] for i in convert_result_k]
                    convert_result_tail = [i[1] for i in convert_result_k]
                    dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
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
        
        elif shangke.count("下賊上") == 2 and self.find_sike_relations()[9] == "天地盤沒有返吟":
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
                change_daygangzhi = shigangjigong.get(self.daygangzhi[0])

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

    def yaoke(self):
        if self.find_sike_relations()[3] == "日干支同位":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif self.find_sike_relations()[4] == "伏吟":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        sike = self.all_sike()
        sike_list = self.find_sike_relations()[0]
        dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
       
        if sike_list.count("下賊上") == 1 and sike_list.count("上尅下") == 1:
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list.count("下賊上") > 0 or sike_list.count("上尅下") > 0:
            chuchuan = "不適用，或試他法" 
            return chuchuan
    
        if self.find_sike_relations()[2].count("尅") == 1:
            if self.find_sike_relations()[6] == "反吟":
                chuchuan = ["返吟", "無親", [yima_dict.get(hourgangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(shigangjigong.get(shigangjigong.get(self.daygangzhi[0])))]]
                return chuchuan
            else:
                chuchuan = ["遙尅","遙尅", self.find_three_pass(sike[self.find_sike_relations()[2].index("尅")][0] )]
                return chuchuan
        elif self.find_sike_relations()[2].count("尅") > 1:
            filterlist = [sike[i][0] for i in duplicates(self.find_sike_relations()[2], "尅")]
            filterlist2 = [gangzhi_yinyang(b) for b in filterlist]
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
                chuchuan = ["返吟","無親", [yima_dict.get(hourgangzhi[1]), self.sky_n_earth_list().get(daygangzhi[1]), self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0])) ]]
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
        dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
        sikehead = [b[0] for b in sike]
        d =  Counter(sikehead)
        res = [k for k, v in d.items() if v > 1]
        if len(set(sike)) <4:
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
                        chuchuan = ["返吟", "無親", [yima_dict.get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0])) ]]
                        return chuchuan
                    elif self.find_sike_relations()[6] == "反吟八專":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
                        chuchuan = ["昴星", "虎視", [self.sky_n_earth_list().get("酉"), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.sky_n_earth_list().get(self.sky_n_earth_list().get("酉")))]]
                        return chuchuan
            if dayganzhi_yy == "陰":
                try:
                    if len(res[0]) >= 1:
                        chuchuan = "不適用，或試他法"  
                        return chuchuan
                except IndexError:
                    if self.find_sike_relations()[6] == "反吟":
                        chuchuan = ["返吟","無親", [yima_dict.get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0])) ]]
                        return chuchuan
                    elif self.find_sike_relations()[6] == "反吟八專":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
                        chuchuan = ["昴星","冬蛇掩目", [self.earth_n_sky_list().get("酉"), self.sky_n_earth_list().get(multi_key_dict_get(ganlivezhi, self.daygangzhi[0])), self.sky_n_earth_list().get(self.daygangzhi[1])]]
                        return chuchuan
        else:
            chuchuan = "不適用，或試他法"  
            return chuchuan
    
    def bieze(self):
        sike = [ i[0] for i in self.all_sike()]
        dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
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
                ganhe_result1 = shigangjigong.get(sky_ganhe.get(self.daygangzhi[0]))
                
                if self.find_sike_relations()[6] == "反吟八專":
                    chuchuan = "不適用，或試他法" 
                    return chuchuan
                elif self.find_sike_relations()[4] == "伏吟":
                    chuchuan =  "不適用，或試他法" 
                    return chuchuan
                else:
                    chuchuan = ["別責", "別責", [self.sky_n_earth_list().get(ganhe_result1), self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0])),  self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0]))]]
                    return chuchuan
            if dayganzhi_yy == "陰":
                result = multi_key_dict_get(earth_zhihe, self.daygangzhi[1])
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
                    chuchuan = ["別責", "別責", [a, self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0])), self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0]))]]
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
        dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
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
            chuchuan = ["返吟", "無親", [yima_dict.get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(shigangjigong.get(self.daygangzhi[0]))]]
            return chuchuan
        elif self.find_sike_relations()[3] == "日干支同位":
            if sike_list.count("下賊上") == 0 and sike_list.count("上尅下") == 0 :
                if dayganzhi_yy == "陽":
                    pos = Zhi.index(sike[3][0])+2
                    if pos == 13:
                        pos = 1
                    elif pos == 14:
                        pos = 0
                    pos = Zhi[pos]
                    if self.find_sike_relations()[4] == "伏吟":
                        chuchuan = "不適用，或試他法" 
                        return chuchuan
                    else:
                        chuchuan = ["八專","八專", [pos, self.sky_n_earth_list().get(self.daygangzhi[1]), self.sky_n_earth_list().get(self.daygangzhi[1])]]
                        return chuchuan
                elif dayganzhi_yy == "陰":
                    pos = Zhi.index(sike[0][0])-2
                    if pos == -2:
                        pos = 10
                    elif pos == -1:
                        pos = 11
                    pos = Zhi[pos]
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
        sike_list = self.find_sike_relations()
        dayganzhi_yy = gangzhi_yinyang(self.daygangzhi[0])
        if sike_list[4] == "非伏吟":
            chuchuan = "不適用，或試他法" 
            return chuchuan
        elif sike_list[4] == "伏吟":
            if sike_list[0].count("上尅下") == 1 or sike_list[0].count("下賊上") == 1:
                chuchuan = ["伏吟", "不虞",  [unique(sike_list[1])[0], ying.get(unique(sike_list[1])[0]), ying.get(ying.get(unique(sike_list[1])[0])) ]]
                return chuchuan
            elif sike_list[0].count("上尅下") == 0 and sike_list[0].count("下賊上") == 0:
                if dayganzhi_yy == "陽":
                    if multi_key_dict_get(ying_chong, shigangjigong.get(self.daygangzhi[0])) =="刑":
                        chuchuan = ["伏吟","自任", [shigangjigong.get(self.daygangzhi[0]), ying.get(shigangjigong.get(self.daygangzhi[0])), ying.get(ying.get(shigangjigong.get(self.daygangzhi[0])))]]
                        return chuchuan
                    elif multi_key_dict_get(ying_chong, shigangjigong.get(self.daygangzhi[0])) =="自刑":
                        chuchuan = ["伏吟", "杜傳", [shigangjigong.get(self.daygangzhi[0]), self.daygangzhi[1], ying.get(self.daygangzhi[1])]]
                        return chuchuan
                elif dayganzhi_yy == "陰":
                    if multi_key_dict_get(ying_chong, shigangjigong.get(self.daygangzhi[1])) =="刑":
                        chuchuan = ["伏吟","自任", [shigangjigong.get(self.daygangzhi[1]), ying.get(shigangjigong.get(self.daygangzhi[0])), ying.get(ying.get(shigangjigong.get(self.daygangzhi[0])))]]
                        return chuchuan
                    elif multi_key_dict_get(ying_chong, shigangjigong.get(self.daygangzhi[1])) =="自刑":
                        chuchuan = ["伏吟", "杜傳", [shigangjigong.get(self.daygangzhi[1]), chong2.get(ying.get(shigangjigong.get(self.daygangzhi[0]))), ying.get(chong2.get(ying.get(shigangjigong.get(self.daygangzhi[0]))))]]
                        return chuchuan
    
                    chuchuan = ["伏吟", "自信", [self.daygangzhi[1], ying.get(self.daygangzhi[1]), chong2.get(self.daygangzhi[1])]]
                    return chuchuan

    def guiren_starting_gangzhi(self, num):
        option  = {0: guiren_dict2, 1: guiren_dict}
        get_day = multi_key_dict_get(option.get(num), self.daygangzhi[0])
        find_day_or_night = multi_key_dict_get(daynight_richppl_dict, self.hourgangzhi[1])
        return get_day.get(find_day_or_night)
    
    def guiren_order_list(self, num):
        #sky_generals_list = [sky_generals[i:i+2] for i in range(0, len(sky_generals), 2)]
        find_day_or_night = multi_key_dict_get(daynight_richppl_dict, self.hourgangzhi[1])
        starting_gangzhi = self.guiren_starting_gangzhi(num)
        clock_anti_clock = multi_key_dict_get(rotation, self.hourgangzhi[1])
        new_zhi_list_guiren = new_zhi_list(starting_gangzhi)
        result_dict = {"晝":{"順佈": dict(zip(new_zhi_list_guiren, sky_generals)),
          "逆佈": dict(zip(new_list(list(reversed( new_zhi_list_guiren)),starting_gangzhi), new_list(list(reversed(sky_generals)), "貴")))},
          "夜":{"順佈": dict(zip(new_zhi_list_guiren, sky_generals)),
          "逆佈": dict(zip(new_list(new_zhi_list_guiren, starting_gangzhi), new_list(list(reversed(sky_generals)), "貴")))}}
        return result_dict.get(find_day_or_night).get(clock_anti_clock)
        
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
        
        day_gz_vs_three_pass = [  liuqing_dict.get(multi_key_dict_get(wuxing_relation_2,ganzhiwuxing(self.daygangzhi[0])+ganzhiwuxing(three_pass_zhi[i])))for i in range(0,len(three_pass_zhi))]
        three_pass = {"初傳":[three_pass_zhi[0], three_pass_generals[0], day_gz_vs_three_pass[0], shunkong(self.daygangzhi,three_pass_zhi[0])], "中傳":[three_pass_zhi[1], three_pass_generals[1], day_gz_vs_three_pass[1], shunkong(self.daygangzhi,three_pass_zhi[1])], "末傳":[three_pass_zhi[2], three_pass_generals[2], day_gz_vs_three_pass[2], shunkong(self.daygangzhi,three_pass_zhi[2])]}
        sike_zhi = self.all_sike()
        sike_generals = [ guiren_order_list_2.get(i[0]) for i in sike_zhi]
        sike = {"四課":[sike_zhi[0], sike_generals[0]], "三課":[sike_zhi[1], sike_generals[1]], "二課":[sike_zhi[2], sike_generals[2]], "一課":[sike_zhi[3], sike_generals[3]]}
        dyima = multi_key_dict_get(yimadict, self.daygangzhi[1])
        return {"節氣":self.jieqi, "日期":self.daygangzhi+"日"+self.hourgangzhi+"時", "格局":ju, "日馬": dyima, "三傳":three_pass, "四課":sike, "天地盤":sky_earth_guiren_dict, "地轉天盤":sky_earth, "地轉天將": earth_to_general}

#print(Liuren("小滿", "甲戌", "庚午").guiren_order_list(0))
#print(Liuren("穀雨", "庚子", "癸未").find_sike_relations())
 