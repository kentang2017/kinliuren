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
pan,example,guji,links,update = st.tabs([' 🧮排盤 ', ' 📜案例 ', ' 📚古籍 ',' 🔗連結 ',' 🆕更新 ' ])

with st.sidebar:
    st.header("日期與時間選擇")
    
    # Set default datetime to current time in Asia/Shanghai
    default_datetime = pdlm.now(tz='Asia/Shanghai')
    
    # Combined datetime input
    selected_date = st.date_input(
        "選擇日期",
        value=default_datetime.date(),
        min_value=pdlm.datetime(1900, 1, 1).date(),
        help="選擇占卜的日期"
    )
    
    selected_time = st.time_input(
        "選擇時間",
        value=default_datetime.time(),
        help="選擇占卜的時間 (24小時制)"
    )
    
    # Quick-select buttons for common times
    st.subheader("快速選擇")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("現在"):
            selected_date = pdlm.now(tz='Asia/Shanghai').date()
            selected_time = pdlm.now(tz='Asia/Shanghai').time()
    with col2:
        if st.button("午夜"):
            selected_time = pdlm.time(0, 0)
    with col3:
        if st.button("中午"):
            selected_time = pdlm.time(12, 0)
    
    # Convert selected date and time to components for existing logic
    p = str(selected_date).split("-")
    pp = str(selected_time).split(":")
    y = int(p[0])
    m = int(p[1])
    d = int(p[2])
    h = int(pp[0])
    min = int(pp[1])
    
    # Display selected datetime
    st.write(f"已選擇: {y}年{m}月{d}日 {h:02d}:{min:02d}")
    
    # Timezone info
    st.caption(f"時區: Asia/Shanghai")

with guji:
    st.header('古籍')
    st.markdown(get_file_content_as_string("guji.md"))

with links:
    st.header('連結')
    st.markdown(get_file_content_as_string("update.md"), unsafe_allow_html=True)

with update:
    st.header('更新')
    st.markdown(get_file_content_as_string("log.md"))
  
with pan:
    st.header('堅六壬')
    cm =  dict(zip(list(range(1,13)), list("正二三四五六七八九十")+["十一","十二"])).get(int(lunar_date_d(y, m, d).get("月").replace("月", "")))
    qgz = gangzhi(y, m, d, h, min)
    jq = jq(y, m, d, h, min)
    liuren_month = kinliuren.Liuren(jq, cm, qgz[1], qgz[2]).result_d(0)
    liuren_day =  kinliuren.Liuren(jq, cm, qgz[2], qgz[3]).result(0)
    liuren_hour =  kinliuren.Liuren(jq, cm, qgz[3], qgz[4]).result_m(0)
    dhorse1 = liuren_month.get("日馬")
    dhorse2 = liuren_day.get("日馬")
    dhorse3 = liuren_hour.get("日馬")
    ltext = liuren_month
    ltext1 = liuren_day
    ltext2 = liuren_hour
    a = "日期︰{}年{}月{}日{}時{}分\n".format(y,m,d,h,min)
    b = "格局︰{}\n".format(ltext.get("格局")[0])
    c = "節氣︰{}\n".format(jq)      
    d = "干支︰{}年 {}月 {}日 {}時 {}分\n".format(qgz[0], qgz[1], qgz[2], qgz[3], qgz[4])
    d2 = "日馬︰{}(月) {}(日) {}(時)\n\n".format(dhorse1, dhorse2, dhorse3)
    d1="　　月課　　　　　　　日課　　　　　　　時課\n\n"
    e ="　{}　　　　　{}　　　　　{}\n".format("".join(ltext.get("三傳").get("初傳")),"".join(ltext1.get("三傳").get("初傳")),"".join(ltext2.get("三傳").get("初傳")))
    f ="　{}　　　　　{}　　　　　{}\n".format("".join(ltext.get("三傳").get("中傳")),"".join(ltext1.get("三傳").get("中傳")),"".join(ltext2.get("三傳").get("中傳")))
    g ="　{}　　　　　{}　　　　　{}\n\n".format("".join(ltext.get("三傳").get("末傳")),"".join(ltext1.get("三傳").get("末傳")),"".join(ltext2.get("三傳").get("末傳")))
    h ="　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']]),"".join([ltext1.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']]), "".join([ltext2.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']]))
    i ="　{}　　　　　{}　　　　　{}\n\n".format("".join([ltext.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']]),"".join([ltext1.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']]), "".join([ltext2.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']]))
    j ="　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("地轉天將").get(i) for i in list("巳午未申")]),"".join([ltext1.get("地轉天將").get(i) for i in list("巳午未申")]), "".join([ltext2.get("地轉天將").get(i) for i in list("巳午未申")]))
    k ="　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("地轉天盤").get(i) for i in list("巳午未申")]),"".join([ltext1.get("地轉天盤").get(i) for i in list("巳午未申")]), "".join([ltext2.get("地轉天盤").get(i) for i in list("巳午未申")]))
    l ="{}{}　　{}{}　　　{}{}　　{}{}　　　{}{}　　{}{}\n".format(ltext.get("地轉天將").get("辰"), ltext.get("地轉天盤").get("辰"), ltext.get("地轉天盤").get("酉"), ltext.get("地轉天將").get("酉"),ltext1.get("地轉天將").get("辰"), ltext1.get("地轉天盤").get("辰"), ltext1.get("地轉天盤").get("酉"), ltext1.get("地轉天將").get("酉"), ltext2.get("地轉天將").get("辰"), ltext2.get("地轉天盤").get("辰"), ltext2.get("地轉天盤").get("酉"), ltext2.get("地轉天將").get("酉"))
    m ="{}{}　　{}{}　　　{}{}　　{}{}　　　{}{}　　{}{}\n".format(ltext.get("地轉天將").get("卯"), ltext.get("地轉天盤").get("卯"), ltext.get("地轉天盤").get("戌"), ltext.get("地轉天將").get("戌"),ltext1.get("地轉天將").get("卯"), ltext1.get("地轉天盤").get("卯"), ltext1.get("地轉天盤").get("戌"), ltext1.get("地轉天將").get("戌"), ltext2.get("地轉天將").get("卯"), ltext2.get("地轉天盤").get("卯"), ltext2.get("地轉天盤").get("戌"), ltext2.get("地轉天將").get("戌"))
    n ="　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("地轉天盤").get(i) for i in list("寅丑子亥")]), "".join([ltext1.get("地轉天盤").get(i) for i in list("寅丑子亥")]), "".join([ltext2.get("地轉天盤").get(i) for i in list("寅丑子亥")]))
    o ="　{}　　　　　{}　　　　　{}\n\n\n".format("".join([ltext.get("地轉天將").get(i) for i in list("寅丑子亥")]), "".join([ltext1.get("地轉天將").get(i) for i in list("寅丑子亥")]), "".join([ltext2.get("地轉天將").get(i) for i in list("寅丑子亥")]))
    output2 = st.empty()
    with st_capture(output2.code):
        print(a+b+c+d+d2+d1+e+f+g+h+i+j+k+l+m+n+o)
    expander = st.expander("原始碼")
    expander.write(str(ltext))
