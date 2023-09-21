import os, urllib
import streamlit as st

import pendulum as pdlm
from contextlib import contextmanager, redirect_stdout
from sxtwl import fromSolar
from io import StringIO
import streamlit.components.v1 as components
from kinliuren import kinliuren
from kinqimen import kinqimen
from jieqi import *

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write
        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        stdout.write = new_write
        yield

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/kentang2017/kinliuren/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

def lunar_date_d(y, m, d):
    day = fromSolar(y,m,d)
    return {"月": str(day.getLunarMonth())+"月", "日":str(day.getLunarDay())}
        
st.set_page_config(layout="wide",page_title="堅六壬-六壬排盤")
pan,example,guji,links = st.tabs([' 排盤 ', ' 案例 ', ' 古籍 ',' 連結 ' ])
with st.sidebar:
    pp_date=st.date_input("日期",pdlm.now(tz='Asia/Shanghai').date())
    pp_time=st.time_input("時間",pdlm.now(tz='Asia/Shanghai').time())
    p = str(pp_date).split("-")
    pp = str(pp_time).split(":")
    y = int(p[0])
    m = int(p[1])
    d = int(p[2])
    h = int(pp[0])
    min = int(pp[1])

with guji:
    st.header('古籍')
    st.markdown(get_file_content_as_string("guji.md"))

with links:
    st.header('連結')
    st.markdown(get_file_content_as_string("update.md"))
  
with pan:
    st.header('堅六壬')
    cm =  dict(zip(list(range(1,13)), list("正二三四五六七八九十")+["十一","十二"])).get(int(lunar_date_d(y, m, d).get("月").replace("月", "")))
    qgz = kinqimen.Qimen(y,m,d,h).gangzhi()
    jq = jq(y, m, d, h, min)
    ltext = kinliuren.Liuren(jq, cm, qgz[1], qgz[2]).result(0)
    ltext_day =  kinliuren.Liuren(jq, cm, qgz[2], qgz[3]).result(0)

    output2 = st.empty()
    with st_capture(output2.code):
        print("{}年{}月{}日{}時".format(y,m,d,h))
        print("{} | 節氣:{} | {}課 \n".format(ltext.get("日期"),ltext.get("節氣"), ltext.get("格局")[0]))
        print("　　　{}".format("".join(ltext.get("三傳").get("初傳"))))
        print("　　　{}".format("".join(ltext.get("三傳").get("中傳"))))
        print("　　　{}\n".format("".join(ltext.get("三傳").get("末傳"))))
        print("　　　{}".format("".join([ltext.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']])))
        print("　　　{}\n".format("".join([ltext.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']])))
        print("　　　{}".format("".join([ltext.get("地轉天將").get(i) for i in list("巳午未申")])))
        print("　　　{}".format("".join([ltext.get("地轉天盤").get(i) for i in list("巳午未申")])))
        print("　　{}{}　　{}{}".format(ltext.get("地轉天將").get("辰"), ltext.get("地轉天盤").get("辰"), ltext.get("地轉天盤").get("酉"), ltext.get("地轉天將").get("酉")))
        print("　　{}{}　　{}{}".format(ltext.get("地轉天將").get("卯"), ltext.get("地轉天盤").get("卯"), ltext.get("地轉天盤").get("戌"), ltext.get("地轉天將").get("戌")))
        print("　　　{}".format("".join([ltext.get("地轉天盤").get(i) for i in list("寅丑子亥")])))
        print("　　　{}".format("".join([ltext.get("地轉天將").get(i) for i in list("寅丑子亥")])))
    expander = st.expander("原始碼")
    expander.write(str(ltext))
