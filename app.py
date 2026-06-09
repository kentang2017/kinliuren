import os, sys, urllib, calendar, json, datetime, html

# Add src/ to the module search path so that library modules can be imported by name.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import streamlit as st
import pendulum as pdlm
from contextlib import contextmanager, redirect_stdout
from sxtwl import fromSolar
from io import StringIO
from bidict import bidict
import streamlit.components.v1 as components
from kinliuren import kinliuren
from kinqimen import kinqimen
from jieqi import *
import jieqi
from cerebras_client import CerebrasClient, CustomAIClient, DEFAULT_MODEL as DEFAULT_CEREBRAS_MODEL

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

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

def new_list(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append( olist[zhihead_code % len(olist)])
        zhihead_code = zhihead_code + 1
    return res1

def weekday(y, m, d):
    cweekdays = ["星期"+i for i in list("日一二三四五六")]
    dayNumber = calendar.weekday(y, m, d)
    return dict(zip([int(i) for i in list("6012345")], cweekdays)).get(dayNumber)

def day_chin(zhi, weekday):
    three_zhi = "申子辰,巳酉丑,寅午戌,亥卯未".split(",")
    head = ["虛畢翼箕奎鬼氐", "房危觜軫斗婁柳", "星心室參角牛胃", "昴張尾壁井亢女"]
    cweekdays = ["星期"+i for i in list("日一二三四五六")]
    ydict = {}
    for i in range(4):
        b = {tuple(list(three_zhi[i])): dict(zip(cweekdays , list(head[i])))}
        ydict.update(b)
    return multi_key_dict_get(ydict, zhi).get(weekday)

PALACE_POSITIONS = {
    "巳": (12.5, 12.5),
    "午": (37.5, 12.5),
    "未": (62.5, 12.5),
    "申": (87.5, 12.5),
    "酉": (87.5, 37.5),
    "戌": (87.5, 62.5),
    "亥": (87.5, 87.5),
    "子": (62.5, 87.5),
    "丑": (37.5, 87.5),
    "寅": (12.5, 87.5),
    "卯": (12.5, 62.5),
    "辰": (12.5, 37.5),
}
MANSION_RING = list("角亢氐房心尾箕斗牛女虛危室壁奎婁胃昴畢觜參井鬼柳星張翼軫")
# 為參考 shipan/index.html 的 rotate_circle.svg 構圖，活盤環使用反序（軫→角 方向）
MANSION_RING_DISPLAY = list(reversed(MANSION_RING))
ZI_TARGET_ANGLE = 161.565051177078
SHIPAN_STYLE = """
<style>
/* 式盤專屬美學 - 朱砂金碧風 */
.shipan-section {
    margin-top: 0.5rem;
    font-family: "Noto Serif SC", "Songti SC", serif;
}

/* 讓三傳四課 只佔很小地方 (緊湊版，像經典排盤那樣不佔空間) */
h3 {
    color: #F4E9D8 !important;
    font-size: 0.75rem !important;
    margin: 0.05rem 0 !important;
    font-weight: 600;
}
.shipan-card, .shipan-course-card {
    padding: 0.15rem 0.3rem !important;
    font-size: 0.7rem !important;
    line-height: 1.1;
}
.shipan-grid, .shipan-course-grid {
    gap: 0.15rem !important;
    margin: 0.05rem 0 0.2rem !important;
}
.shipan-card-value, .shipan-course-value {
    font-size: 0.75rem !important;
}
.shipan-card-subtle, .shipan-course-subtle {
    font-size: 0.6rem !important;
    margin-top: 0.05rem !important;
}

/* 確保 iframe 內無黑色文字 */
body, html, div, span, p, h1, h2, h3, h4, label {
    color: #F4E9D8 !important;
}

.shipan-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
    margin: 0.4rem 0 1rem;
}

.shipan-meta-card,
.shipan-card,
.shipan-course-card,
.shipan-note {
    border: 1px solid #3C352C;
    border-radius: 10px;
    padding: 0.9rem 1.05rem;
    background: #1F1B16;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
}

.shipan-meta-label,
.shipan-card-label,
.shipan-course-label,
.shipan-cell-label {
    font-size: 0.8rem;
    color: #B8A78A;
    letter-spacing: 0.04em;
}

.shipan-meta-value,
.shipan-card-value,
.shipan-course-value {
    margin-top: 0.25rem;
    font-size: 1.15rem;
    font-weight: 600;
    color: #F4E9D8;
}

.shipan-grid,
.shipan-course-grid {
    display: grid;
    gap: 0.7rem;
    margin: 0.4rem 0 0.9rem;
}

.shipan-grid { grid-template-columns: repeat(auto-fit, minmax(178px, 1fr)); }
.shipan-course-grid { grid-template-columns: repeat(auto-fit, minmax(158px, 1fr)); }

.shipan-card-subtle,
.shipan-course-subtle,
.shipan-note-subtle {
    margin-top: 0.25rem;
    font-size: 0.82rem;
    color: #8A7F68;
}

.shipan-board-shell {
    position: relative;
    width: min(92vw, 900px);  /* 總體尺寸 = 外圍方盤 + 內部十二宮 */
    aspect-ratio: 1 / 1;
    margin: 0.9rem 0 0.6rem;
}

/* 28宿方盤外框：固定正方形 (四四正正，不隨活盤旋轉)，在十二宮外圍 */
.shipan-outer-ring {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    border: 2px solid #D4AF37;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    /* 明確方形，無圓角，框架本身不旋轉 */
}

/* 內部十二宮方盤主體 (固定比例，保持十二宮文字與格子大小) */
.shipan-board {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 68%;   /* 縮小十二宮框，讓外圍28宿方框在手機上有足夠空間可見 */
    height: 68%;
    transform: translate(-50%, -50%);
    z-index: 2;
    border: 2.5px solid #D4AF37;
    border-radius: 12px;
    background: #16130F;
    box-shadow: 
        0 12px 36px rgba(0, 0, 0, 0.65),
        inset 0 0 70px rgba(0, 0, 0, 0.55),
        inset 0 2px 0 rgba(212, 175, 55, 0.2);
}

/* 三傳四課放在中間 */
.shipan-center-large {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 50%;
    height: 48%;
    transform: translate(-50%, -50%);
    border-radius: 6px;
    border: 1.5px solid #D4AF37;
    background: rgba(15, 13, 10, 0.85);
    z-index: 3;
    padding: 2px 4px;
    box-shadow: inset 0 0 15px rgba(0,0,0,0.8), 0 0 8px rgba(212, 175, 55, 0.15);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}
.shipan-center-large pre {
    margin: 0;
    width: 100%;
    text-align: left;
    font-family: monospace;
    color: #F4E9D8;
}

.shipan-cell {
    position: absolute;
    width: 23%;
    height: 23%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.15rem;
    background: rgba(31, 27, 22, 0.72);
    border: 1px solid #3C352C;
    border-radius: 8px;
}

.shipan-cell-sky {
    font-size: clamp(0.95rem, 2vw, 1.25rem);
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #D4AF37;
}

.shipan-cell-general {
    font-size: 0.92rem;
    color: #D4C5A3;
}

.shipan-cell-label {
    font-size: 0.72rem;
    color: #8A7F68;
}

.shipan-circle {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 50%;
    height: 50%;
    transform: translate(-50%, -50%);
    border-radius: 999px;
    border: 2.5px solid #D4AF37;
    background: radial-gradient(circle at 38% 32%, #25211B 0%, #16130F 72%);
    box-shadow: inset 0 0 35px rgba(0, 0, 0, 0.75);
}

.shipan-ring {
    position: absolute;
    inset: 0;
}

.shipan-mansion {
    position: absolute;
    transform-origin: center center;
    font-size: clamp(0.75rem, 1.15vw, 0.95rem);
    font-weight: 600;
    color: #D4C5A3;
    text-shadow: 0 1px 2px rgba(0,0,0,0.65);
}

.shipan-center {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 33%;
    height: 33%;
    transform: translate(-50%, -50%);
    border-radius: 999px;
    border: 2px solid #D4AF37;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 0.1rem;
    background: #0F0D0A;
    box-shadow: 
        0 0 0 5px #16130F, 
        inset 0 0 25px rgba(0,0,0,0.85),
        0 0 12px rgba(184, 51, 46, 0.25); /* 微弱朱砂光 */
}

.shipan-center-title {
    font-size: 0.78rem;
    color: #8A7F68;
    letter-spacing: 0.08em;
}

.shipan-center-value {
    font-size: clamp(1.4rem, 2.35vw, 1.9rem);
    font-weight: 700;
    color: #B8332E; /* 朱砂紅強調「活盤」 */
}

@media (max-width: 768px) {
    .shipan-board { width: 55%; height: 55%; }  /* 手機縮小十二宮框，讓外圍28宿方框有空間不被遮 */
    .shipan-cell { width: 24%; height: 24%; }
    .shipan-cell-sky { font-size: 0.8rem; }
}
</style>
"""

def format_transmission_value(values):
    pieces = [item for item in values if item]
    return " ".join(map(str, pieces))

def render_transmission_cards(chart):
    cards = []
    for key in ["初傳", "中傳", "末傳"]:
        values = chart.get("三傳", {}).get(key, [])
        cards.append(
            f"""
            <div class="shipan-card">
                <div class="shipan-card-label">{html.escape(key)}</div>
                <div class="shipan-card-value">{html.escape(format_transmission_value(values))}</div>
                <div class="shipan-card-subtle">支 / 將 / 六親 / 遁干</div>
            </div>
            """
        )
    return '<div class="shipan-grid">' + "".join(cards) + "</div>"

def render_course_cards(chart):
    cards = []
    for key in ["四課", "三課", "二課", "一課"]:
        values = chart.get("四課", {}).get(key, ["", ""])
        cards.append(
            f"""
            <div class="shipan-course-card">
                <div class="shipan-course-label">{html.escape(key)}</div>
                <div class="shipan-course-value">{html.escape(str(values[0]))}</div>
                <div class="shipan-course-subtle">{html.escape(str(values[1]))}</div>
            </div>
            """
        )
    return '<div class="shipan-course-grid">' + "".join(cards) + "</div>"

def render_shipan(day_chart, active_mansion, south_sky_text, center_content="", extra_overlays=""):
    rotation_step = 360 / len(MANSION_RING_DISPLAY)
    rotation_offset = 0
    if active_mansion in MANSION_RING_DISPLAY:
        rotation_offset = ZI_TARGET_ANGLE - MANSION_RING_DISPLAY.index(active_mansion) * rotation_step
    palaces = []
    for branch, (left, top) in PALACE_POSITIONS.items():
        palaces.append(
            f"""
            <div class="shipan-cell" style="left:{left}%; top:{top}%;">
                <div class="shipan-cell-general">{html.escape(str(day_chart.get("地轉天將", {}).get(branch, "")))}</div>
                <div class="shipan-cell-sky">{html.escape(str(day_chart.get("地轉天盤", {}).get(branch, "")))}</div>
            </div>
            """
        )

    # 28宿方盤外框：固定正方形（四四正正，不旋轉），只讓文字隨活盤旋轉
    # 位置在十二宮外圍的四邊，文字會沿方框移動
    frac_shift = rotation_offset * 28 / 360.0

    mansions = []
    for i in range(28):
        pos_t = (i + frac_shift) % 28
        side = int(pos_t // 7)
        frac = (pos_t % 7) / 7.0
        if side == 0:  # top
            left = frac * 100
            top = 4
        elif side == 1:  # right
            left = 96
            top = frac * 100
        elif side == 2:  # bottom
            left = (1 - frac) * 100
            top = 96
        else:  # left
            left = 4
            top = (1 - frac) * 100

        mansion = MANSION_RING_DISPLAY[i]

        # 文字方向：top/bottom 水平，左右側 垂直 (90deg)
        if side == 0 or side == 2:
            rot = 0
        else:
            rot = 90 if side == 1 else -90

        mansions.append(
            f"""
            <div class="shipan-mansion"
                 style="left:{left}%; top:{top}%; transform: rotate({rot}deg);">
                {html.escape(mansion)}
            </div>
            """
        )

    return f"""
    <div class="shipan-section">
        <div class="shipan-board-shell">
            <!-- 28宿方盤外框：固定正方形，四四正正，只文字隨活盤轉 -->
            <div class="shipan-outer-ring">
                {''.join(mansions)}
            </div>
            <!-- 方型式盤主體 (十二宮) -->
            <div class="shipan-board">
                {''.join(palaces)}
                <!-- 三傳四課放在式盤中間 -->
                <div class="shipan-center-large">
                    {center_content}
                </div>
            </div>
            {extra_overlays}
        </div>
    </div>
    """

def render_ai_analysis(chart_text, ltext, ltext1, ltext2, selected_model, button_key):
    if st.button("🔍 使用AI分析排盤結果", key=button_key):
        with st.spinner("AI正在分析六壬排盤結果..."):
            try:
                if st.session_state.get("use_custom_ai"):
                    custom_key = st.session_state.get("custom_api_key", "")
                    custom_url = st.session_state.get("custom_server_url", "")
                    custom_model = st.session_state.get("custom_model_name", "")
                    if not custom_key or not custom_url or not custom_model:
                        st.error("請填寫自定義AI的 API Key、Server URL 及模型名稱。")
                    else:
                        client = CustomAIClient(api_key=custom_key, base_url=custom_url)
                        ai_model = custom_model
                        liuren_prompt = format_liuren_results_for_prompt(chart_text, ltext, ltext1, ltext2)
                        messages = [
                            {"role": "system", "content": st.session_state.system_prompt},
                            {"role": "user", "content": liuren_prompt}
                        ]
                        api_params = {
                            "messages": messages,
                            "model": ai_model,
                            "max_tokens": st.session_state.get("ai_max_tokens", AI_MAX_MAX_TOKENS),
                            "temperature": st.session_state.get("ai_temperature", 0.7)
                        }
                        response = client.get_chat_completion(**api_params)
                        raw_response = response.choices[0].message.content
                        with st.expander("AI分析結果", expanded=True):
                            st.markdown(raw_response)
                else:
                    cerebras_api_key = st.secrets.get("CEREBRAS_API_KEY") or os.getenv("CEREBRAS_API_KEY")
                    if not cerebras_api_key:
                        st.error("CEREBRAS_API_KEY 未設置，請先在 .streamlit/secrets.toml 設置，或設置環境變量 CEREBRAS_API_KEY。")
                    else:
                        client = CerebrasClient(api_key=cerebras_api_key)
                        liuren_prompt = format_liuren_results_for_prompt(chart_text, ltext, ltext1, ltext2)
                        messages = [
                            {"role": "system", "content": st.session_state.system_prompt},
                            {"role": "user", "content": liuren_prompt}
                        ]
                        api_params = {
                            "messages": messages,
                            "model": selected_model,
                            "max_tokens": st.session_state.get("ai_max_tokens", AI_MAX_MAX_TOKENS),
                            "temperature": st.session_state.get("ai_temperature", 0.7)
                        }
                        response = client.get_chat_completion(**api_params)
                        raw_response = response.choices[0].message.content
                        with st.expander("AI分析結果", expanded=True):
                            st.markdown(raw_response)
            except Exception as e:
                st.error(f"調用AI時發生錯誤：{e}")

# Cerebras Model Options
CEREBRAS_MODEL_OPTIONS = [
    "gpt-oss-120b",
    "zai-glm-4.7",
]
CEREBRAS_MODEL_DESCRIPTIONS = {
    "gpt-oss-120b": "Cerebras: GPT-OSS 120B，高效能大型語言模型。",
    "zai-glm-4.7": "Cerebras: ZAI-GLM 4.7，優化中文推理能力。",
}

SYSTEM_PROMPTS_FILE = "system_prompts.json"
AI_MIN_MAX_TOKENS = 40000
AI_MAX_MAX_TOKENS = 200000

# --- System Prompt Management (加強版邏輯) ---

PROMPTS_KEY = "prompts"
SELECTED_KEY = "selected"

DEFAULT_SYSTEM_PROMPT = (
    "你是一位大六壬大師，熟悉《大六壬大全》、《六壬粹言》、《壬學瑣記》等經典古籍及歷史案例。請根據提供的六壬排盤數據，進行以下操作：\n"
    "1. 解釋盤局的關鍵要素（四課、三傳、天將、天盤地盤等）。\n"
    "2. 結合六壬經典理論，分析盤局的吉凶和潛在影響。\n"
    "3. 根據日課、月課、時課的格局及三傳、四課，詳細評估當前運勢趨勢。\n"
    "4. 提供實用的建議或應對策略。\n"
    "請以清晰的結構（分段、標題）呈現，語言專業且易懂，適當引用歷史案例或經典理論。"
)

def _get_default_prompts_data():
    """回傳乾淨的預設提示資料結構。"""
    return {
        PROMPTS_KEY: [{"name": "六壬大師", "content": DEFAULT_SYSTEM_PROMPT}],
        SELECTED_KEY: "六壬大師"
    }

def _backup_corrupted_prompts_file(filepath):
    """嘗試備份損壞的設定檔（加上時間戳）。"""
    if not os.path.exists(filepath):
        return None
    try:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.bak.{ts}"
        with open(filepath, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())
        return backup_path
    except Exception:
        return None

def _atomic_write_json(filepath, data):
    """原子寫入 JSON（先寫 .tmp 再 replace，避免寫入中斷造成損壞）。"""
    tmp_path = filepath + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, filepath)

def _sanitize_prompts_data(data):
    """
    驗證並修復提示資料結構。
    保證：
    - 回傳的永遠是 dict
    - prompts 是非空 list，每個項目都有 name(str) 與 content(str)
    - selected 是有效的字串，且存在於 prompts 名單中
    - 如果全部無效，會自動塞入預設提示
    """
    if not isinstance(data, dict):
        data = {}

    # 取出並清理 prompts
    raw_prompts = data.get(PROMPTS_KEY, [])
    if not isinstance(raw_prompts, list):
        raw_prompts = []

    cleaned_prompts = []
    seen_names = set()
    for p in raw_prompts:
        if not isinstance(p, dict):
            continue
        name = str(p.get("name", "")).strip()
        content = p.get("content", "")
        if not name or not isinstance(content, str):
            continue
        if name in seen_names:
            continue  # 重複名稱跳過
        seen_names.add(name)
        cleaned_prompts.append({"name": name, "content": content})

    # 如果沒有任何有效提示，塞入預設
    if not cleaned_prompts:
        cleaned_prompts = _get_default_prompts_data()[PROMPTS_KEY][:]

    # 處理 selected
    selected = data.get(SELECTED_KEY)
    prompt_names = [p["name"] for p in cleaned_prompts]
    if not isinstance(selected, str) or selected not in prompt_names:
        selected = prompt_names[0]

    return {
        PROMPTS_KEY: cleaned_prompts,
        SELECTED_KEY: selected
    }

def load_system_prompts():
    """載入系統提示，具備容錯、備份、自動修復與結構驗證。"""
    try:
        with open(SYSTEM_PROMPTS_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        # 即使 JSON 合法，也要做結構清理
        sanitized = _sanitize_prompts_data(raw_data)

        # 如果原本的資料被清理過（結構不完整），我們可以選擇寫回一次
        # 這裡為了簡單，只在必要時寫回
        if raw_data != sanitized:
            try:
                _atomic_write_json(SYSTEM_PROMPTS_FILE, sanitized)
            except Exception:
                pass  # 寫回失敗不影響本次載入

        return sanitized

    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
        # 載入失敗 → 備份舊檔 + 產生新預設
        backup_path = _backup_corrupted_prompts_file(SYSTEM_PROMPTS_FILE)
        default_data = _get_default_prompts_data()

        try:
            _atomic_write_json(SYSTEM_PROMPTS_FILE, default_data)
            if backup_path:
                st.warning(f"⚠️ 系統提示檔損壞或無法讀取，已自動備份為 {os.path.basename(backup_path)} 並重新產生預設設定。")
            else:
                st.info("ℹ️ 系統提示檔不存在或無法讀取，已自動建立預設設定。")
        except Exception as write_err:
            st.error(f"無法寫入系統提示檔：{write_err}")

        return default_data

def save_system_prompts(prompts_data):
    """儲存系統提示，使用原子寫入 + 事前結構清理。"""
    try:
        sanitized = _sanitize_prompts_data(prompts_data)
        _atomic_write_json(SYSTEM_PROMPTS_FILE, sanitized)
        return True
    except Exception as e:
        st.error(f"錯誤儲存提示：{e}")
        return False


def format_liuren_results_for_prompt(chart_text, ltext, ltext1, ltext2):
    """Format Liuren calculation results into a prompt for the AI model."""
    prompt_lines = [
        "以下是大六壬排盤的計算結果，請根據這些數據提供詳細的分析和解釋：",
        "",
        chart_text,
        "",
        "【月課詳細數據】",
        f"格局: {ltext.get('格局', '')}",
        f"三傳: 初傳{''.join(ltext.get('三傳', {}).get('初傳', []))} | 中傳{''.join(ltext.get('三傳', {}).get('中傳', []))} | 末傳{''.join(ltext.get('三傳', {}).get('末傳', []))}",
        f"四課: {ltext.get('四課', '')}",
        f"天將: {ltext.get('地轉天將', '')}",
        f"天盤: {ltext.get('地轉天盤', '')}",
        f"日馬: {ltext.get('日馬', '')}",
        "",
        "【日課詳細數據】",
        f"格局: {ltext1.get('格局', '')}",
        f"三傳: 初傳{''.join(ltext1.get('三傳', {}).get('初傳', []))} | 中傳{''.join(ltext1.get('三傳', {}).get('中傳', []))} | 末傳{''.join(ltext1.get('三傳', {}).get('末傳', []))}",
        f"四課: {ltext1.get('四課', '')}",
        f"天將: {ltext1.get('地轉天將', '')}",
        f"天盤: {ltext1.get('地轉天盤', '')}",
        f"日馬: {ltext1.get('日馬', '')}",
        "",
        "【時課詳細數據】",
        f"格局: {ltext2.get('格局', '')}",
        f"三傳: 初傳{''.join(ltext2.get('三傳', {}).get('初傳', []))} | 中傳{''.join(ltext2.get('三傳', {}).get('中傳', []))} | 末傳{''.join(ltext2.get('三傳', {}).get('末傳', []))}",
        f"四課: {ltext2.get('四課', '')}",
        f"天將: {ltext2.get('地轉天將', '')}",
        f"天盤: {ltext2.get('地轉天盤', '')}",
        f"日馬: {ltext2.get('日馬', '')}",
    ]
    return "\n".join(prompt_lines)

st.set_page_config(
    layout="wide",
    page_title="堅六壬 · 六壬排盤",
    page_icon="icon.jpg"
)

# ============================================================
# 整體 UI 美學調整（美學主義者 + 玄學軟件開發者視角）
# 色調：深墨黑 + 暖羊皮紙 + 古金 + 朱砂紅
# 氛圍：古雅、神秘、靜謐、尊重傳統卻不失現代可用性
# ============================================================
GLOBAL_AESTHETIC_CSS = """
<style>
/* 根色調變數 - 朱砂金碧風格 */
:root {
    --bg-deep: #0C0A08;
    --bg-card: #1F1B16;
    --bg-elevated: #25211B;
    --text-primary: #F4E9D8;
    --text-secondary: #B8A78A;
    --accent-gold: #D4AF37;       /* 更豐富的古金 */
    --accent-gold-bright: #E8C872; /* 金碧輝煌高光 */
    --accent-vermilion: #B8332E;  /* 朱砂紅，更鮮明有力 */
    --border-subtle: #3C352C;
}

/* 強制修正黑色文字為白色/淺色 (避免在暗背景看不見) */
.stApp, .stApp * {
    color: var(--text-primary) !important;
}
.stMarkdown p, .stMarkdown span, .stText, .stCaption, label {
    color: var(--text-primary) !important;
}

/* 全局背景與文字 */
.stApp {
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

/* 標題與文字層級 */
h1, h2, h3, h4 {
    color: var(--text-primary) !important;
    font-family: "Noto Serif SC", "Songti SC", "STSong", "KaiTi", "Microsoft YaHei", serif !important;
    letter-spacing: 0.02em;
}

h1 { font-size: 1.85rem !important; }
h2 { font-size: 1.45rem !important; color: var(--accent-vermilion) !important; }
h3 { font-size: 1.15rem !important; color: var(--accent-gold) !important; }

p, .stMarkdown, .stCaption {
    color: var(--text-secondary) !important;
    line-height: 1.65;
}

/* Sidebar 古風控制面板 */
[data-testid="stSidebar"] {
    background-color: #15120E !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] .stHeader {
    color: var(--accent-gold) !important;
}

/* Tabs 像古書簽或印章 */
.stTabs [data-baseweb="tab-list"] {
    background-color: #15120E !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    background-color: transparent !important;
    border-radius: 4px 4px 0 0;
    padding: 8px 18px !important;
    font-family: "Noto Serif SC", serif;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-vermilion) !important;
    border-bottom: 2px solid var(--accent-vermilion) !important;
    background-color: rgba(184, 51, 46, 0.08) !important;
}

/* 卡片與區塊（三傳、四課、meta 等） */
.shipan-meta-card,
.shipan-card,
.shipan-course-card,
.shipan-note {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.shipan-meta-card:hover,
.shipan-card:hover,
.shipan-course-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.45);
    border-color: var(--accent-vermilion);
}

/* 強調色 */
.shipan-meta-value,
.shipan-card-value,
.shipan-course-value,
.shipan-center-value {
    color: var(--text-primary) !important;
}

.shipan-cell-sky {
    color: var(--accent-gold) !important;
}

/* 按鈕 - 古雅風格 */
.stButton button {
    background-color: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--accent-gold) !important;
    border-radius: 6px !important;
    font-family: "Noto Serif SC", serif;
    transition: all 0.2s ease;
}

.stButton button:hover {
    background-color: var(--accent-vermilion) !important;
    color: #F4E9D8 !important;
    border-color: var(--accent-vermilion);
    box-shadow: 0 0 0 1px var(--accent-gold);
}

/* 輸入框 */
.stTextInput input, .stTextArea textarea, .stDateInput input, .stTimeInput input {
    background-color: #15120E !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px;
}

/* 底部 AI 問答區塊 */
[data-testid="stChatMessage"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle);
}

/* 整體更寬鬆的呼吸感 */
.block-container {
    padding-top: 2.5rem !important;  /* 增加頂部空間，讓 st.tabs 不會太頂，完整可見 */
    padding-bottom: 2rem !important;
}

/* 專門讓 tabs 往下一些，避免被頂部切到或看不完整 */
.stTabs {
    margin-top: 0.3rem !important;
}
.stTabs [data-baseweb="tab-list"] {
    margin-top: 0.4rem !important;
    padding-top: 0.2rem !important;
}

/* 讓經典排盤的 code 區塊也更優雅 */
.stCodeBlock {
    background-color: #15120E !important;
    border: 1px solid var(--border-subtle) !important;
}
</style>
"""
st.markdown(GLOBAL_AESTHETIC_CSS, unsafe_allow_html=True)

pan, classic_pan, guji, links, update = st.tabs([' 🧮排盤 ', ' 🧭經典排盤 ', ' 📚古籍 ',' 🔗連結 ',' 🆕更新 ' ])

with st.sidebar:
    st.header("日期與時間選擇")

    # Set default datetime to current time in Asia/Hong_Kong (HKT)
    default_datetime = pdlm.now(tz='Asia/Hong_Kong')

    # Quick-select button for current time
    if st.button("📍 現在"):
        now = pdlm.now(tz='Asia/Hong_Kong')
        st.session_state['dt_date'] = now.date()
        st.session_state['dt_time'] = now.time()
        st.rerun()

    # Native date picker with calendar popup
    selected_date = st.date_input(
        "日期",
        value=default_datetime.date(),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(2100, 12, 31),
        key='dt_date',
        help="點擊選擇日期"
    )

    # Native time picker with hour/minute selection
    selected_time = st.time_input(
        "時間",
        value=default_datetime.time(),
        step=datetime.timedelta(minutes=1),
        key='dt_time',
        help="點擊選擇時間"
    )

    y = selected_date.year
    m = selected_date.month
    d = selected_date.day
    h = selected_time.hour
    mi = selected_time.minute

    # Display selected datetime
    st.write(f"已選擇: {y}年{m}月{d}日 {h:02d}:{mi:02d}")

    # Timezone info
    st.caption("時區: Asia/Hong_Kong")

    st.markdown("---")
    st.header("AI設置")

    selected_model = st.selectbox(
        "AI 模型",
        options=CEREBRAS_MODEL_OPTIONS,
        index=0,
        key="cerebras_model_selector",
        help="\n".join(f"• {k}: {v}" for k, v in CEREBRAS_MODEL_DESCRIPTIONS.items())
    )

    st.markdown("---")
    st.subheader("🔌 自定義AI設置")
    use_custom_ai = st.toggle("使用自定義AI", key="use_custom_ai", help="啟用後可輸入任意OpenAI相容API的Key及Server設定")
    if use_custom_ai:
        st.text_input(
            "自定義 API Key",
            type="password",
            key="custom_api_key",
            placeholder="sk-...",
            help="輸入您的AI服務API Key"
        )
        st.text_input(
            "Server URL",
            key="custom_server_url",
            placeholder="https://api.openai.com/v1",
            help="輸入OpenAI相容API的Server地址，例如 https://api.openai.com/v1"
        )
        st.text_input(
            "模型名稱",
            key="custom_model_name",
            placeholder="gpt-4o, claude-3-5-sonnet, glm-4...",
            help="輸入您要使用的模型名稱"
        )

    system_prompts_data = load_system_prompts()
    # 載入後再做一次保險清理（雖然 load 內部已處理）
    system_prompts_data = _sanitize_prompts_data(system_prompts_data)
    prompts_list = system_prompts_data.get("prompts", [])
    prompt_names = [prompt["name"] for prompt in prompts_list]
    selected_prompt = system_prompts_data.get("selected")

    if prompt_names:
        selected_index = 0
        if selected_prompt in prompt_names:
            selected_index = prompt_names.index(selected_prompt)

        selected_name = st.selectbox(
            "選擇系統提示",
            options=prompt_names,
            index=selected_index,
            key="system_prompt_selector",
            help="選擇用於AI模型的系統提示，指導其分析六壬排盤結果"
        )

        system_prompts_data["selected"] = selected_name

        selected_content = ""
        for prompt in prompts_list:
            if prompt["name"] == selected_name:
                selected_content = prompt["content"]
                break

        if 'system_prompt' not in st.session_state:
            st.session_state.system_prompt = selected_content
        elif selected_name != st.session_state.get("last_selected_prompt"):
            st.session_state.system_prompt = selected_content

        st.session_state.last_selected_prompt = selected_name

        new_content = st.text_area(
            "編輯系統提示",
            value=st.session_state.system_prompt,
            height=150,
            placeholder="範例：你是一位大六壬專家，根據排盤數據提供詳細分析...",
            key="system_prompt_editor"
        )

        st.session_state.system_prompt = new_content

        col_u, col_d = st.columns(2)
        with col_u:
            if st.button("💾 更新提示", key="update_prompt_button"):
                for prompt in prompts_list:
                    if prompt["name"] == selected_name:
                        prompt["content"] = new_content
                        break
                if save_system_prompts(system_prompts_data):
                    st.toast(f"✅ 已更新系統提示 '{selected_name}'！")

        with col_d:
            if st.button("❌ 刪除提示", key="delete_prompt_button",
                        disabled=len(prompts_list) <= 1):
                prompts_list = [p for p in prompts_list if p["name"] != selected_name]
                system_prompts_data["prompts"] = prompts_list
                if selected_name == selected_prompt and prompts_list:
                    system_prompts_data["selected"] = prompts_list[0]["name"]
                if save_system_prompts(system_prompts_data):
                    st.toast(f"✅ 已刪除系統提示 '{selected_name}'！")
                    st.rerun()

    if "form_key_suffix" not in st.session_state:
        st.session_state.form_key_suffix = 0

    name_key = f"new_prompt_name_{st.session_state.form_key_suffix}"
    content_key = f"new_prompt_content_{st.session_state.form_key_suffix}"

    with st.expander("➕ 新增提示", expanded=False):
        new_prompt_name = st.text_input("新提示名稱", key=name_key)
        new_prompt_content = st.text_area(
            "新提示內容",
            height=100,
            placeholder="輸入AI分析指令...",
            key=content_key
        )
        if st.button("➕ 新增提示", key="add_prompt_button",
                    disabled=not new_prompt_name or not new_prompt_content):
            if new_prompt_name in prompt_names:
                st.error(f"提示名稱 '{new_prompt_name}' 已存在。")
            else:
                prompts_list.append({
                    "name": new_prompt_name,
                    "content": new_prompt_content
                })
                system_prompts_data["prompts"] = prompts_list
                if save_system_prompts(system_prompts_data):
                    st.session_state.form_key_suffix += 1
                    st.toast(f"✅ 已新增系統提示 '{new_prompt_name}'！")
                    st.rerun()

    if st.toggle("🔧 高級設置", key="advanced_settings_toggle"):
        st.session_state.ai_max_tokens = st.slider(
            "最大生成 Tokens",
            AI_MIN_MAX_TOKENS, AI_MAX_MAX_TOKENS,
            st.session_state.get("ai_max_tokens", AI_MAX_MAX_TOKENS),
            key="ai_max_tokens_slider",
            help="控制AI回應的最大長度"
        )
        st.session_state.ai_temperature = st.slider(
            "溫度 (專注 vs. 創意)",
            0.0, 1.5,
            st.session_state.get("ai_temperature", 0.7),
            step=0.05,
            key="ai_temperature_slider",
            help="較低值 (如 0.2) 更確定性；較高值 (如 0.8) 更隨機"
        )

cm =  jieqi.lunar_date_d(y, m, d).get("農曆月")
qgz = gangzhi(y, m, d, h, mi)
jq = jq(y, m, d, h, mi)
liuren_month = kinliuren.Liuren(jq, cm, qgz[1], qgz[2]).result_d(0)
liuren_day =  kinliuren.Liuren(jq, cm, qgz[2], qgz[3]).result(0)
liuren_hour =  kinliuren.Liuren(jq, cm, qgz[3], qgz[4]).result_m(0)
dhorse1 = liuren_month.get("日馬")
dhorse2 = liuren_day.get("日馬")
dhorse3 = liuren_hour.get("日馬")
ltext = liuren_month
ltext1 = liuren_day
ltext2 = liuren_hour
dchin = day_chin(qgz[2][1], weekday(y, m, d))
day_south = "".join([ltext1.get("地轉天盤").get(i) for i in list("巳午未申")])
date_line = "日期︰{}年{}月{}日{}時{}分\n".format(y, m, d, h, mi)
ju_line = "格局︰{}\n".format(ltext.get("格局")[0])
term_line = "節氣︰{}\n".format(jq)
ganzhi_line = "干支︰{}年 {}月 {}日 {}時 {}分\n".format(qgz[0], qgz[1], qgz[2], qgz[3], qgz[4])
horse_line = "日馬︰{}(月) {}(日) {}(時)\n\n".format(dhorse1, dhorse2, dhorse3)
header_line = "　　月課　　　　　　　日課　　　　　　　時課\n\n"
initial_line = "　{}　　　　　{}　　　　　{}\n".format("".join(ltext.get("三傳").get("初傳")), "".join(ltext1.get("三傳").get("初傳")), "".join(ltext2.get("三傳").get("初傳")))
middle_line = "　{}　　　　　{}　　　　　{}\n".format("".join(ltext.get("三傳").get("中傳")), "".join(ltext1.get("三傳").get("中傳")), "".join(ltext2.get("三傳").get("中傳")))
final_line = "　{}　　　　　{}　　　　　{}\n\n".format("".join(ltext.get("三傳").get("末傳")), "".join(ltext1.get("三傳").get("末傳")), "".join(ltext2.get("三傳").get("末傳")))
course_upper_line = "　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']]), "".join([ltext1.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']]), "".join([ltext2.get("四課").get(i)[0][0] for i in ['四課','三課','二課','一課']]))
course_lower_line = "　{}　　　　　{}　　　　　{}\n\n".format("".join([ltext.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']]), "".join([ltext1.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']]), "".join([ltext2.get("四課").get(i)[0][1] for i in ['四課','三課','二課','一課']]))
south_general_line = "　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("地轉天將").get(i) for i in list("巳午未申")]), "".join([ltext1.get("地轉天將").get(i) for i in list("巳午未申")]), "".join([ltext2.get("地轉天將").get(i) for i in list("巳午未申")]))
south_sky_line = "　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("地轉天盤").get(i) for i in list("巳午未申")]), "".join([ltext1.get("地轉天盤").get(i) for i in list("巳午未申")]), "".join([ltext2.get("地轉天盤").get(i) for i in list("巳午未申")]))
middle_upper_line = "{}{}　　{}{}　　　{}{}　　{}{}　　　{}{}　　{}{}\n".format(ltext.get("地轉天將").get("辰"), ltext.get("地轉天盤").get("辰"), ltext.get("地轉天盤").get("酉"), ltext.get("地轉天將").get("酉"), ltext1.get("地轉天將").get("辰"), ltext1.get("地轉天盤").get("辰"), ltext1.get("地轉天盤").get("酉"), ltext1.get("地轉天將").get("酉"), ltext2.get("地轉天將").get("辰"), ltext2.get("地轉天盤").get("辰"), ltext2.get("地轉天盤").get("酉"), ltext2.get("地轉天將").get("酉"))
middle_lower_line = "{}{}　　{}{}　　　{}{}　　{}{}　　　{}{}　　{}{}\n".format(ltext.get("地轉天將").get("卯"), ltext.get("地轉天盤").get("卯"), ltext.get("地轉天盤").get("戌"), ltext.get("地轉天將").get("戌"), ltext1.get("地轉天將").get("卯"), ltext1.get("地轉天盤").get("卯"), ltext1.get("地轉天盤").get("戌"), ltext1.get("地轉天將").get("戌"), ltext2.get("地轉天將").get("卯"), ltext2.get("地轉天盤").get("卯"), ltext2.get("地轉天盤").get("戌"), ltext2.get("地轉天將").get("戌"))
north_sky_line = "　{}　　　　　{}　　　　　{}\n".format("".join([ltext.get("地轉天盤").get(i) for i in list("寅丑子亥")]), "".join([ltext1.get("地轉天盤").get(i) for i in list("寅丑子亥")]), "".join([ltext2.get("地轉天盤").get(i) for i in list("寅丑子亥")]))
north_general_line = "　{}　　　　　{}　　　　　{}\n\n\n".format("".join([ltext.get("地轉天將").get(i) for i in list("寅丑子亥")]), "".join([ltext1.get("地轉天將").get(i) for i in list("寅丑子亥")]), "".join([ltext2.get("地轉天將").get(i) for i in list("寅丑子亥")]))
chart_text = (
    date_line + ju_line + term_line + ganzhi_line + horse_line + header_line +
    initial_line + middle_line + final_line + course_upper_line + course_lower_line +
    south_general_line + south_sky_line + middle_upper_line + middle_lower_line +
    north_sky_line + north_general_line
)
st.session_state.chart_text = chart_text
st.session_state.chart_ltext = ltext
st.session_state.chart_ltext1 = ltext1
st.session_state.chart_ltext2 = ltext2

with pan:
    st.markdown(
        '<h2 style="margin-bottom:0.1rem; color:#B8332E; letter-spacing:0.06em;">堅六壬</h2>',
        unsafe_allow_html=True
    )

    # 日期、節氣/格局、干支、日馬 改為純文字顯示，像經典排盤一樣（不使用表格卡片）
    meta_text = f"""日期︰{y}年{m}月{d}日{h:02d}時{mi:02d}分
格局︰{" / ".join(ltext1.get("格局", []))}
節氣︰{jq}
干支︰{qgz[0]}年 {qgz[1]}月 {qgz[2]}日 {qgz[3]}時 {qgz[4]}分
日馬︰{dhorse1}(月) {dhorse2}(日) {dhorse3}(時)"""
    st.text(meta_text)

    # --- 加入文字到盤式（類似 kinqimen），會與盤式一起被下載成圖片 ---
    if "board_annotations" not in st.session_state:
        st.session_state.board_annotations = []

    # 準備額外覆蓋文字的 HTML（會放在 shell 內，與盤式一起被 html2canvas 捕捉）
    extra_overlays = ""
    for ann in st.session_state.board_annotations:
        txt = html.escape(ann["text"])
        pos = ann["pos"]
        style = ("position:absolute; font-size:0.78rem; color:#F4E9D8; "
                 "background:rgba(15,13,10,0.92); padding:2px 5px; border-radius:3px; "
                 "white-space:nowrap; z-index:10; border:1px solid #D4AF37;")
        if pos == "center":
            style += " left:50%; top:50%; transform:translate(-50%,-50%);"
        elif pos == "top":
            style += " left:50%; top:4%; transform:translate(-50%,0);"
        elif pos == "bottom":
            style += " left:50%; bottom:4%; transform:translate(-50%,0);"
        elif pos == "left":
            style += " left:2%; top:50%; transform:translate(0,-50%) rotate(-90deg); transform-origin:left center;"
        elif pos == "right":
            style += " right:2%; top:50%; transform:translate(0,-50%) rotate(90deg); transform-origin:right center;"
        extra_overlays += f'<div style="{style}">{txt}</div>'

    added_texts = [ann["text"] for ann in st.session_state.get("board_annotations", [])]

    # 三傳四課 直接像經典排盤的"日課"那樣純文字顯示（6列格式），放在式盤中間
    chuan = ltext1.get("三傳", {})
    ke = ltext1.get("四課", {})
    chuan_lines = [
        ''.join(chuan.get('初傳', [])),
        ''.join(chuan.get('中傳', [])),
        ''.join(chuan.get('末傳', [])),
    ]
    # 四課兩行精確匹配經典排盤「日課」欄的 course_upper_line / course_lower_line (日課欄)
    # 例如 2026-6-10 0時13分： "未亥申子" / "亥卯子乙"
    # 與 chart_text 內 course_*_line 的日課部分使用相同取字邏輯
    ke_line1 = "".join([str(ke.get(i, ["", ""])[0])[0] for i in ['四課','三課','二課','一課']])
    ke_line2 = "".join([str(ke.get(i, ["", ""])[0])[1] for i in ['四課','三課','二課','一課']])
    center_text = (
        f"{chuan_lines[0]}\n"
        f"{chuan_lines[1]}\n"
        f"{chuan_lines[2]}\n"
        "\n"
        f"{ke_line1}\n"
        f"{ke_line2}"
    )
    center_content = f'<pre style="font-size: clamp(0.85rem, 1.7vw, 1.1rem); line-height: 1.15; margin:0; padding: 2px 4px; white-space:pre; color:#F4E9D8; text-align: center; font-family: monospace; letter-spacing: 0.05em;">{html.escape(center_text)}</pre>'

    board_html = render_shipan(ltext1, dchin, day_south, center_content=center_content, extra_overlays=extra_overlays)

    trigger_download = st.session_state.get("trigger_download", False)
    if trigger_download:
        st.session_state["trigger_download"] = False

    # 只顯示式盤的 component（無內部下載按鈕），支援 trigger 自動下載
    # 準備給 JS 的摘要與加入文字（按用戶指定：左標題 + 式盤摘要單行 | 分隔 + 文字按鈕文字 + 完整式盤圖）
    pat = " / ".join(ltext1.get("格局", []))
    gz = f"{qgz[0]}年 {qgz[1]}月 {qgz[2]}日 {qgz[3]}時 {qgz[4]}分"
    ma = f"{dhorse1}(月) {dhorse2}(日) {dhorse3}(時)"
    summary_line = f"日期: {y}年{m}月{d}日{h:02d}時{mi:02d}分 | 格局: {pat} | 節氣: {jq} | 干支: {gz} | 日馬: {ma}"
    component_html = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
{SHIPAN_STYLE}
<h3>式盤</h3>
{board_html}
<script>
const AUTO_DOWNLOAD = {str(trigger_download).lower()};
const EXPORT_TITLE = "堅六壬排盤";
const SUMMARY_LINE = {json.dumps(summary_line)};
const ADDED_TEXTS = {json.dumps(added_texts)};

function doDownload() {{
  const board = document.querySelector('.shipan-board-shell');
  if (!board) {{
    alert('無法找到式盤區域');
    return;
  }}
  html2canvas(board, {{
    scale: 2,
    backgroundColor: '#0C0A08'
  }}).then(function(boardCanvas) {{
    const size = 900;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#0C0A08';
    ctx.fillRect(0, 0, size, size);

    // 靠左標題
    ctx.fillStyle = '#B8332E';
    ctx.font = 'bold 24px "Noto Serif SC", "Songti SC", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(EXPORT_TITLE, 28, 36);

    // 式盤摘要單行（使用 | 分隔，依用戶指定格式）
    ctx.fillStyle = '#F4E9D8';
    ctx.font = '13px monospace';
    ctx.fillText("式盤摘要 " + SUMMARY_LINE, 28, 58);

    // 顯示「文字按鈕」所產生的文字（列表）
    let y = 78;
    if (ADDED_TEXTS && ADDED_TEXTS.length > 0) {{
      ctx.font = '12px monospace';
      for (let t of ADDED_TEXTS) {{
        ctx.fillText(t, 28, y);
        y += 16;
      }}
    }}

    // 繪製完整式盤圖案（包含外圍28宿方框 + 十二宮 + 中間三傳四課 + 任何overlay加入文字）
    const bw = boardCanvas.width;
    const bh = boardCanvas.height;
    const maxBoard = size - y - 20;
    const sc = Math.min(maxBoard / bw, maxBoard / bh);
    const dw = bw * sc;
    const dh = bh * sc;
    const dx = (size - dw) / 2;
    const dy = y + 10;
    ctx.drawImage(boardCanvas, dx, dy, dw, dh);

    const a = document.createElement('a');
    a.download = '堅六壬式盤.png';
    a.href = canvas.toDataURL('image/png');
    a.click();
  }}).catch(function(err) {{
    console.error(err);
    alert('下載失敗');
  }});
}}

if (AUTO_DOWNLOAD) {{
  setTimeout(doDownload, 150);
}}
</script>
"""
    components.html(component_html, height=1020, scrolling=True)

    # 加入文字 UI 和 下載按鈕 放在式盤之後
    # 點擊「加入文字」才顯示輸入框，確認後才加入
    if st.button("加入文字", key="add_text_trigger"):
        st.session_state.show_add_text_form = True
        st.rerun()

    if st.session_state.get("show_add_text_form", False):
        ann_text = st.text_input("", key="ann_text_input", placeholder="輸入要加入的文字", label_visibility="collapsed")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("確定", key="confirm_add_text"):
                if ann_text.strip():
                    st.session_state.board_annotations.append({
                        "text": ann_text.strip(),
                        "pos": "center"
                    })
                st.session_state.show_add_text_form = False
                st.rerun()
        with col_cancel:
            if st.button("取消", key="cancel_add_text"):
                st.session_state.show_add_text_form = False
                st.rerun()

    if st.session_state.get("board_annotations"):
        if st.button("清除所有加入的文字", key="clear_ann_btn"):
            st.session_state.board_annotations = []
            st.rerun()
        for i, a in enumerate(st.session_state.board_annotations):
            st.caption(f"[{i+1}] {a['pos']}: {a['text']}")

    if st.button("📥 下載盤式", key="download_btn_after"):
        st.session_state["trigger_download"] = True
        st.rerun()

    render_ai_analysis(chart_text, ltext, ltext1, ltext2, selected_model, "analyze_with_ai")

with classic_pan:
    with st.expander("📜 經典排盤（文字版）", expanded=False):
        st.caption("月課 / 日課 / 時課 三欄並列 · 傳統文字呈現")
        st.code(chart_text)
        expander = st.expander("原始碼")
        expander.write(str(ltext))

with guji:
    st.header('古籍')
    st.markdown(get_file_content_as_string("docs/guji.md"))

with links:
    st.header('連結')
    st.markdown(get_file_content_as_string("docs/contact.md"), unsafe_allow_html=True)

with update:
    st.header('更新')
    st.markdown(get_file_content_as_string("docs/changelog.md"))

# --- Fixed LLM Chat Section at Bottom ---
st.markdown("---")
st.markdown(
    '<div style="margin: 0.6rem 0 0.3rem; font-size:1.05rem; color:#B8332E; font-family: Noto Serif SC, serif;">💬 玄問 · AI 六壬問答</div>',
    unsafe_allow_html=True
)

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Display chat history
chat_container = st.container(height=400)
with chat_container:
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input (fixed at bottom by Streamlit)
if user_input := st.chat_input("輸入您的六壬問題...", key="chat_input"):
    # Append user message to history
    st.session_state.chat_messages.append({"role": "user", "content": user_input})

    # Display user message immediately
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_input)

    # Build context-aware messages for the AI
    # Build system prompt with chart context
    chart_context = ""
    if "chart_text" in st.session_state:
        liuren_prompt = format_liuren_results_for_prompt(
            st.session_state.chart_text,
            st.session_state.chart_ltext,
            st.session_state.chart_ltext1,
            st.session_state.chart_ltext2
        )
        chart_context = f"\n\n以下是當前的六壬排盤數據供參考：\n{liuren_prompt}"

    system_content = st.session_state.get("system_prompt", "") + chart_context

    # Build conversation messages (system + full chat history)
    api_messages = [{"role": "system", "content": system_content}]
    for msg in st.session_state.chat_messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        if st.session_state.get("use_custom_ai"):
            custom_key = st.session_state.get("custom_api_key", "")
            custom_url = st.session_state.get("custom_server_url", "")
            custom_model = st.session_state.get("custom_model_name", "")
            if not custom_key or not custom_url or not custom_model:
                raise ValueError("請填寫自定義AI的 API Key、Server URL 及模型名稱。")
            client = CustomAIClient(api_key=custom_key, base_url=custom_url)
            ai_model = custom_model
        else:
            cerebras_api_key = st.secrets.get("CEREBRAS_API_KEY") or os.getenv("CEREBRAS_API_KEY")
            if not cerebras_api_key:
                raise ValueError("CEREBRAS_API_KEY 未設置，請先在 .streamlit/secrets.toml 設置，或設置環境變量 CEREBRAS_API_KEY。")
            client = CerebrasClient(api_key=cerebras_api_key)
            ai_model = st.session_state.get("cerebras_model_selector", CEREBRAS_MODEL_OPTIONS[0])

        api_params = {
            "messages": api_messages,
            "model": ai_model,
            "max_tokens": st.session_state.get("ai_max_tokens", AI_MAX_MAX_TOKENS),
            "temperature": st.session_state.get("ai_temperature", 0.7)
        }
        response = client.get_chat_completion(**api_params)
        assistant_reply = response.choices[0].message.content

        # Append assistant reply to history
        st.session_state.chat_messages.append({"role": "assistant", "content": assistant_reply})

        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)
    except Exception as e:
        err_msg = f"調用AI時發生錯誤：{e}"
        st.session_state.chat_messages.append({"role": "assistant", "content": err_msg})
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(err_msg)

# Clear chat button
if st.session_state.chat_messages:
    if st.button("🗑️ 清除對話記錄", key="clear_chat"):
        st.session_state.chat_messages = []
        st.rerun()
