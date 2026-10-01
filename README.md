# 🔮 堅大六壬 · Kinliuren — Python 大六壬排盤庫

<p align="center">
  <b>中國三式重中之重 · The Premier Art of China's Three Divination Styles</b><br>
  <i>大六壬 | Da Liu Ren | Six Ren Astrology</i>
</p>

<p align="center">
  <a href="https://pypi.org/project/kinliuren/"><img src="https://img.shields.io/pypi/pyversions/kinliuren" alt="Python Version"></a>
  <a href="https://pypi.org/project/kinliuren/"><img src="https://img.shields.io/pypi/v/kinliuren" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/kinliuren/"><img src="https://img.shields.io/pypi/dm/kinliuren" alt="Monthly Downloads"></a>
  <a href="https://github.com/kentang2017/kinliuren/stargazers"><img src="https://img.shields.io/github/stars/kentang2017/kinliuren?style=flat" alt="GitHub Stars"></a>
  <a href="https://github.com/kentang2017/kinliuren/blob/master/LICENSE"><img src="https://img.shields.io/github/license/kentang2017/kinliuren" alt="License"></a>
  <a href="https://t.me/haizhonggum"><img src="https://img.shields.io/badge/chat-Telegram-blue?logo=telegram" alt="Telegram"></a>
  <a href="https://t.me/numerology_coding"><img src="https://img.shields.io/badge/channel-Telegram-red?logo=telegram" alt="Telegram Channel"></a>
  <a href="https://www.paypal.me/kinyeah"><img src="https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal" alt="Donate"></a>
</p>

<p align="center">
  <a href="https://kinliuren.streamlit.app/">
    <img src="https://img.shields.io/badge/🌐%20線上排盤-Live%20Demo-brightgreen?style=for-the-badge" alt="Live Demo">
  </a>
</p>

---

<p align="center">
  <img src="https://github.com/kentang2017/kinliuren/blob/master/pic/Untitled-33.png" alt="堅六壬排盤截圖" width="80%">
</p>

---

## 📖 導讀 · Introduction

**大六壬**（Da Liu Ren），又稱六壬神課，是中國古老三大占卜術之一，與**奇門遁甲**、**太乙神數**並稱「三式」。大六壬盛行於漢朝、三國、魏晉南北朝，文人名士多以此為休閒雅趣，常以懷中藏物互相占卜猜測，名曰「射覆」。唐宋以來，明清相繼，相承至今。六壬術傳至日本後，在平安時代由陰陽師安倍晴明發揚光大，成為現代算命相術之一。

本庫（**堅六壬**）以 Python 實現大六壬完整排盤，涵蓋三傳、四課、天地盤、神煞及各類格局判斷，並提供線上排盤 Web App，供研習者使用。

> 如有遺漏紕繆，請向本人提出報錯，定必適時修正，謝謝！

---

**Da Liu Ren** (大六壬, "Six Ren Astrology") is one of the Three Styles (三式 *sānshì*) of classical Chinese divination, together with **Qi Men Dun Jia** (奇門遁甲) and **Taiyi** (太乙). It originated during the Warring States period and flourished through the Han, Three Kingdoms, and Tang–Qing dynasties. The art later spread to Japan, where it was championed by the legendary *onmyōji* Abe no Seimei during the Heian period.

**Kinliuren** is a fully-featured Python library that computes Da Liu Ren charts — including the Three Transmissions (三傳), Four Courses (四課), Celestial & Earthly Disk (天地盤), Spiritual Auspices (神煞), and pattern recognition (格局) — and ships with a live Streamlit web app.

---

## ✨ 功能特色 · Features

| 功能 Feature | 說明 Description |
|---|---|
| 📅 三傳推算 Three Transmissions | 初傳、中傳、末傳完整計算 Full calculation of Initial, Middle & Final Transmissions |
| 📐 四課排列 Four Courses | 一二三四課精準排列 Accurate Four-Course layout |
| 🌀 天地盤 Celestial–Earthly Disk | 十二支天盤、地盤及十二天將對應 12-branch sky/earth disk with 12 generals |
| 🔮 神煞計算 Spiritual Auspices | 日馬、天馬、將星等三十餘神煞 30+ auspicious/inauspicious indicators |
| 🗂️ 格局判斷 Pattern Recognition | 賊尅、重審、元首等課體格局 Pattern identification (Thief-Clashing, Retrial, etc.) |
| 🗓️ 節氣支援 Solar Term Support | 自動對應二十四節氣 Auto-mapping to 24 solar terms |
| 🌐 線上排盤 Web App | Streamlit 即時互動排盤 Real-time interactive chart via Streamlit |
| 📦 PyPI 套件 PyPI Package | `pip install kinliuren` 一行安裝 One-line install |

---

## 🚀 安裝套件 · Installation

```bash
pip install kinliuren
```

> 需要 Python 3.7+  ·  Requires Python 3.7+

---

## ⚡ 起課方式 · Quickstart

```python
from kinliuren import kinliuren

# 格式: Liuren(節氣, 農曆月份, 日干支, 時干支).result(0)
# Format: Liuren(solar_term, lunar_month, day_ganzhi, hour_ganzhi).result(0)

result = kinliuren.Liuren("驚蟄", "二", "己未", "甲午").result(0)
print(result)
```

<details>
<summary>📄 查看輸出範例 · Sample Output (click to expand)</summary>

```python
{
  '節氣': '驚蟄',
  '日期': '己未日甲午時',
  '格局': ['賊尅', '重審'],
  '日馬': '巳',
  '三傳': {
    '初傳': ['巳', '虎', '父', '丁'],
    '中傳': ['戌', '雀', '兄', '壬'],
    '末傳': ['卯', '玄', '官', '乙']
  },
  '四課': {
    '四課': ['巳子', '虎'],
    '三課': ['子未', '貴'],
    '二課': ['巳子', '虎'],
    '一課': ['子己', '貴']
  },
  '天地盤': {
    '天盤': ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'],
    '地盤': ['午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳'],
    '天將': ['蛇', '貴', '后', '陰', '玄', '常', '虎', '空', '龍', '勾', '合', '雀']
  },
  '地轉天盤': {'午': '亥', '未': '子', '申': '丑', '酉': '寅', '戌': '卯',
               '亥': '辰', '子': '巳', '丑': '午', '寅': '未', '卯': '申',
               '辰': '酉', '巳': '戌'},
  '地轉天將': {'午': '蛇', '未': '貴', '申': '后', '酉': '陰', '戌': '玄',
               '亥': '常', '子': '虎', '丑': '空', '寅': '龍', '卯': '勾',
               '辰': '合', '巳': '雀'},
  '神煞': {
    '天城': '申', '天吏': '寅', '皇書': '寅', '天喜': '戌',
    '天耳': '申', '戲神': '巳', '遊神': '丑', '天車': '巳',
    '月馬': '辰', '日馬': '巳', '丁馬': '巳', '日德': '寅',
    '日祿': '午', '賢貴': '丑', '進神': '卯', '進神二': '酉',
    '五合': '寅', '支德': '午', '將星': '卯', '六合': '午',
    '天馬': '申', '聖心': '巳', '天恩': '酉', '天財': '午',
    '飛廉': '巳', '會神': '戌', '成神': '申', '生氣': '丑',
    '月合': '戌', '閃電': '丑'
  }
}
```
</details>

---

## 🌐 線上排盤 · Live Demo

體驗即時互動排盤，無需安裝任何軟件。  
Try the live interactive chart — no installation required.

👉 **[https://kinliuren.streamlit.app/](https://kinliuren.streamlit.app/)**

---

## 📚 三式相關項目 · Related Three-Style Projects

本庫是「堅三式」系列的一部分，涵蓋中國三式占卜的完整實現。  
This library is part of the **Kin Three Styles** (堅三式) series, covering all three classical Chinese divination arts.

| 項目 Project | 說明 Description | 連結 Link |
|---|---|---|
| 🔮 堅大六壬 | 大六壬排盤 Da Liu Ren | [kinliuren.streamlit.app](https://kinliuren.streamlit.app/) |
| ☯️ 堅奇門 | 奇門遁甲 Qi Men Dun Jia | [kinqimen.streamlit.app](https://kinqimen.streamlit.app/) |
| ⭐ 堅太乙 | 太乙神數 Taiyi | [kintaiyi.streamlit.app](https://kintaiyi.streamlit.app/) |
| 🀄 堅筮 | 易經筮法 IChing | [iching.streamlit.app](https://iching.streamlit.app/) |
| 🏮 堅皇極 | 皇極經世 Wangji | [kinwangji.streamlit.app](https://kinwangji.streamlit.app/) |
| 🌟 堅太玄 | 太玄筮法 Taixuan | [kintaixuan.streamlit.app](https://kintaixuan.streamlit.app/) |
| 💫 堅五兆 | 五兆 Wuzhao | [kinwuzhao.streamlit.app](https://kinwuzhao.streamlit.app/) |
| 🎴 堅金口 | 金口訣 Jingjue | [jingjue.streamlit.app](https://jingjue.streamlit.app/) |
| 🪙 堅分定經 | 兩頭鉗 Liangtouqian | [liangtouqian.streamlit.app](https://liangtouqian.streamlit.app/) |

---

## 🤝 聯絡與支持 · Contact & Support

- 💬 **Telegram 群組**: [@haizhonggum](https://t.me/haizhonggum)
- 📢 **Telegram 頻道**: [@numerology_coding](https://t.me/numerology_coding)
- 💰 **贊助支持**: [PayPal](https://www.paypal.me/kinyeah)
- 📱 **微信公眾號**: 堅系賽博玄學

<p align="center">
  <img src="https://raw.githubusercontent.com/kentang2017/kinliuren/refs/heads/master/pic/%E5%9C%96%E7%89%87_20260316084148.jpg" alt="微信公眾號二維碼" width="200">
</p>

> 如有任何建議或合作事宜，可加微信 **gnatnek**（請註明是在 GitHub 加的）  
> 或加入 QQ 群組「堅三式軟件交流群」（群號：770621021）
>
> For suggestions or collaboration, add WeChat **gnatnek** (please note you found me on GitHub),  
> or join the QQ group "堅三式軟件交流群" (Group ID: 770621021).

---

## 📜 授權 · License

本項目採用 MIT 授權條款。  
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.



