# **Python 大六壬 Kinliuren 堅大六壬**
[![Python](https://img.shields.io/pypi/pyversions/kinliuren)](https://pypi.org/project/kinliuren/)
[![PIP](https://img.shields.io/pypi/v/kinliuren)](https://pypi.org/project/kinliuren/)
[![Downloads](https://img.shields.io/pypi/dm/kinliuren)](https://pypi.org/project/kinliuren/)
[![TG](https://img.shields.io/badge/chat-on%20telegram-blue)](https://t.me/gnatnek)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal&style=flat-square)](https://www.paypal.me/kinyeah)&nbsp;

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%E7%BA%8C%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%AC%AC1057%E5%86%8A.pdf/page568-428px-%E7%BA%8C%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%AC%AC1057%E5%86%8A.pdf.jpg "六壬軍帳神機")

## **1. 導讀**︰
大六壬，或稱六壬神課，簡稱六壬，是中國古老三大占卜術之一。大六壬與奇門遁甲、太乙神數並稱三式。大六壬盛行於漢朝、三國、魏晉南北朝，文人名士多有以此為休閒，常以懷中藏物互相占卜猜測，名曰「射覆」。唐宋以來，明清相繼，相承至今。然六壬演式繁雜，主要在士大夫之間流傳，在民間社會中漸被文王卦所代替。當今社會，在中國大陸、香港和台灣均有一部分人在研習六壬。六壬術傳至日本後，在平安時代由陰陽師安倍晴明發揚光大。為現代算命相術之一。

## **2. 安裝套件**
```python
	pip install kinliuren
```
## **3. 起課方式**
```python
	from kinliuren import kinliuren
	kinliuren.Liuren( 節氣, 日干支, 時干支).result(0)
	例如 Liuren("冬至", "丁未", "乙巳")
{'節氣': '冬至', '日期': '丁未日乙巳時', '格局': ['賊尅', '元首'], '三傳': {'初傳': ['卯', '勾陳', '父母', '空'], '中傳': ['亥', '貴人', '官鬼', '辛'], '末傳': ['未', '太常', '子孫', '丁']}, '四課': {'四課': ['亥卯', '貴人'], '三課': ['卯未', '勾陳'], '二課': ['亥卯', '貴人'], '一課': ['卯丁', '勾陳']}, '天地盤': {'天盤': ['丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子'], '地盤': ['巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰'], '天將': ['朱雀', '六合', '勾陳', '青龍', '天空', '白虎', '太常', '玄武', '太陰', '天后', '貴人', '螣蛇']}, '地轉天盤': {'巳': '丑', '午': '寅', '未': '卯', '申': '辰', '酉': '巳', '戌': '午', '亥': '未', '子': '申', '丑': '酉', '寅': '戌', '卯': '亥', '辰': '子'}, '地轉天將': {'巳': '朱雀', '午': '六合', '未': '勾陳', '申': '青龍', '酉': '天空', '戌': '白虎', '亥': '太常', '子': '玄武', '丑': '太陰', '寅': '天后', '卯': '貴人', '辰': '螣蛇'}}
```
