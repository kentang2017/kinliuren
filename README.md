# **Python 大六壬 Kinliuren 堅大六壬 堅六壬**
[![Python](https://img.shields.io/pypi/pyversions/kinliuren)](https://pypi.org/project/kinliuren/)
[![PIP](https://img.shields.io/pypi/v/kinliuren)](https://pypi.org/project/kinliuren/)
[![Downloads](https://img.shields.io/pypi/dm/kinliuren)](https://pypi.org/project/kinliuren/)
[![TG](https://img.shields.io/badge/chat-on%20telegram-blue)](https://t.me/gnatnek)
[![TG Channel](https://img.shields.io/badge/chat-on%20telegram-red)](https://t.me/numerology_coding)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal&style=flat-square)](https://www.paypal.me/kinyeah)&nbsp;


![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%E7%BA%8C%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%AC%AC1057%E5%86%8A.pdf/page568-428px-%E7%BA%8C%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%AC%AC1057%E5%86%8A.pdf.jpg "六壬軍帳神機")

## 1. 導讀 Introduction
大六壬，或稱六壬神課，簡稱六壬，是中國古老三大占卜術之一。大六壬與奇門遁甲、太乙神數並稱三式。大六壬盛行於漢朝、三國、魏晉南北朝，文人名士多有以此為休閒，常以懷中藏物互相占卜猜測，名曰「射覆」。唐宋以來，明清相繼，相承至今。然六壬演式繁雜，主要在士大夫之間流傳，在民間社會中漸被文王卦所代替。當今社會，在中國大陸、香港和台灣均有一部分人在研習六壬。六壬術傳至日本後，在平安時代由陰陽師安倍晴明發揚光大。為現代算命相術之一。

堅六壬排盤 https://kinliuren.streamlit.app/

Da Liu Ren is a form of Chinese calendrical astrology dating from the later Warring States period. It is also a member of the Three Styles (三式; sānshì; 'three rites') of divination, along with Qi Men Dun Jia (奇门遁甲) and Taiyi (太乙).

In the words of a contemporary Chinese master of Da Liu Ren, the six rén indicate an entire movement of the sexagenary cycle, during which an something may appear, rise to maturity and then decline and disappear. Thus the six rén indicate the life cycle of phenomena. There is a homonym in the Chinese language which carries the meaning of pregnancy and so the six rén also carry the meaning of the birth of a phenomenon.

## 2. 安裝套件 Installation
```python
	pip install kinliuren
```
## 3. 起課方式 Quickstart
```python
	from kinliuren import kinliuren
	kinliuren.Liuren( 節氣, 農曆月份, 日干支, 時干支).result(0)
	例如 Liuren("驚蟄","二","己未","甲午").result(0)
{'節氣': '驚蟄', '日期': '己未日甲午時', '格局': ['賊尅', '重審'], '日馬': '巳', '三傳': {'初傳': ['巳', '虎', '父', '丁'], '中傳': ['戌', '雀', '兄', '壬'], '末傳': ['卯', '玄', '官', '乙']}, '四課': {'四課': ['巳子', '虎'], '三課': ['子未', '貴'], '二課': ['巳子', '虎'], '一課': ['子己', '貴']}, '天地盤': {'天盤': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'], '地盤': ['午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳'], '天將': ['蛇', '貴', '后', '陰', '玄', '常', '虎', '空', '龍', '勾', '合', '雀']}, '地轉天盤': {'午': '亥', '未': '子', '申': '丑', '酉': '寅', '戌': '卯', '亥': '辰', '子': '巳', '丑': '午', '寅': '未', '卯': '申', '辰': '酉', '巳': '戌'}, '地轉天將': {'午': '蛇', '未': '貴', '申': '后', '酉': '陰', '戌': '玄', '亥': '常', '子': '虎', '丑': '空', '寅': '龍', '卯': '勾', '辰': '合', '巳': '雀'}, '神煞': {'天城': '申', '天吏': '寅', '皇書': '寅', '天喜': '戌', '天耳': '申', '戲神': '巳', '遊神': '丑', '天車': '巳', '月馬': '辰', '日馬': '巳', '丁馬': '巳', '日德': '寅', '日祿': '午', '賢貴': '丑', '進神': '卯', '進神二': '酉', '五合': '寅', '支德': '午', '將星': '卯', '六合': '午', '天馬': '申', '聖心': '巳', '天恩': '酉', '天財': '午', '飛廉': '巳', '會神': '戌', '成神': '申', '生氣': '丑', '月合': '戌', '閃電': '丑'}}
```


