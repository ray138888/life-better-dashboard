import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# -----------------------------------------------------------------------------
# 1. 系統設定與 Google Sheets 雲端資料庫連線
# -----------------------------------------------------------------------------
st.set_page_config(page_title="1天重塑人生計畫", page_icon="✨", layout="wide")

# 初始化 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 📢 【已綁定：你的專屬 Google 試算表完整網址】
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1vSL_FxL42qZv4bl_TqELWZ6Gyi17u1yEvV3uKdcwUPA/edit?usp=sharing"

TODAY = str(date.today())

# -----------------------------------------------------------------------------
# 2. 雲端資料讀取與初始化邏輯
# -----------------------------------------------------------------------------
# 初始化文字資料的預設值
default_text_data = {
    "mantra": "", "tolerated_dissatisfaction": "", "unbearable_truth": "",
    "anti_vision_5y": "", "anti_vision_10y": "", "anti_vision_end": "", "anti_vision_ghost": "",
    "identity_give_up": "", "embarrang_truth": "", "self_protection": "",
    "vision_3y": "", "new_identity": "", "immediate_action": "",
    "alarm_1100": "", "alarm_1330": "", "alarm_1515": "", "alarm_1700": "", "alarm_1930": "", "alarm_2100": "",
    "bonus_1": "", "bonus_2": "", "bonus_3": "",
    "true_block": "", "actual_enemy": "", "anti_vision_compressed": "", "vision_compressed": "",
    "one_year_lens": "", "one_month_lens": "", "daily_lens": "", "constraints": ""
}

# 從 Google Sheets 讀取或初始化這三大區塊的資料
try:
    # 讀取文字區塊 (分頁: text_data)
    df_text = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="text_data")
    if df_text.empty or "key" not in df_text.columns:
        df_text = pd.DataFrame(list(default_text_data.items()), columns=["key", "value"])
except Exception:
    df_text = pd.DataFrame(list(default_text_data.items()), columns=["key", "value"])

text_dict = dict(zip(df_text["key"], df_text["value"]))

try:
    # 讀取抱怨審計表 (分頁: complaints)
    df_complaints = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="complaints")
    if df_complaints.empty:
        df_complaints = pd.DataFrame([{"🗣️ 抱怨 (前三名)": "", "🕵️‍♂️ 真實情況": ""}] * 3)
except Exception:
    df_complaints = pd.DataFrame([{"🗣️ 抱怨 (前三名)": "", "🕵️‍♂️ 真實情況": ""}] * 3)

try:
    # 讀取每日槓桿清單 (分頁: daily_levers)
    df_levers = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="daily_levers")
    if df_levers.empty:
        df_levers = pd.DataFrame([
            {"任務": "建立 3 個月後的進度追蹤器", "完成": False},
            {"任務": "建立財務追蹤表", "完成": False},
            {"任務": "停止喝奶茶 (戒除壞習慣)", "完成": False},
            {"任務": "早上 10 點前回覆所有訊息，不拖延", "完成": False},
            {"任務": "每天冥想", "完成": False}
        ])
except Exception:
    df_levers = pd.DataFrame([{"任務": "新任務範例", "完成": False}])

# -----------------------------------------------------------------------------
# 3. 響應式 RWD 介面渲染 (全繁體中文)
# -----------------------------------------------------------------------------
st.title("✨ 1 天重塑人生計畫 (The 1-Day Reset Protocol)")
st.markdown("基於 Dan Koe 經典框架 · 本系統已與你的 Google Sheets 實現實時雙向同步。")

# 信念與基礎宣告
st.markdown("❤️ **我的信念 (Mantra)**")
new_mantra = st.text_input("寫下一句激勵你改變生活、擁抱新身份的咒語：", value=text_dict.get("mantra", ""))
text_dict["mantra"] = new_mantra

st.divider()

# 四大核心頁籤
tab1, tab2, tab3, tab4 = st.tabs(["🌅 晨間：心理挖掘", "⏱️ 日間：中斷自動導航", "🌙 晚間：洞察總結", "🎯 終極儀表板"])

# ==========================================
# 頁籤 1：晨間 - 心理挖掘
# ==========================================
with tab1:
    st.header("🌅 晨間 – 心理挖掘 (Vision & Anti-Vision)")
    
    st.subheader("● ● 區塊 A：你痛苦的現實 ● ●")
    text_dict["tolerated_dissatisfaction"] = st.text_area("1. 容忍的不滿：你已經學會與什麼樣沉悶且持續的不滿共存？", value=text_dict.get("tolerated_dissatisfaction", ""))
    
    st.markdown("2. 抱怨審計表：你反覆抱怨但卻從未去改變的事情是什麼？")
    edited_complaints = st.data_editor(df_complaints, use_container_width=True, hide_index=True, key="ed_comp")
    
    text_dict["unbearable_truth"] = st.text_area("3. 無法承受的真相：關於你目前的生活，什麼真相是讓你覺得如果告訴你深愛/尊敬的人，會感到無法承受的？", value=text_dict.get("unbearable_truth", ""))

    st.divider()
    st.subheader("● ● 區塊 B：反向願景 (The Anti-Vision) ● ●")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        text_dict["anti_vision_5y"] = st.text_area("1) 5 年地獄：如果未來 5 年什麼都沒改變，描述一個平凡的週二。在哪醒來？身體感覺如何？做什麼工作？", value=text_dict.get("anti_vision_5y", ""), height=150)
        text_dict["anti_vision_end"] = st.text_area("3) 生命終點：你到了生命盡頭。你活了最安全的版本，從未打破模式。代價是什麼？", value=text_dict.get("anti_vision_end", ""), height=150)
    with col1_2:
        text_dict["anti_vision_10y"] = st.text_area("2) 10 年地獄：現在想像 10 年後。你錯過了什麼？誰放棄了你？當你不在場時，別人怎麼說你？", value=text_dict.get("anti_vision_10y", ""), height=150)
        text_dict["anti_vision_ghost"] = st.text_area("4) 未來的幽靈：你生活中誰已經活成了你剛才描述的未來？想到變成他們，你有什麼感覺？", value=text_dict.get("anti_vision_ghost", ""), height=150)

    st.divider()
    st.subheader("● ● 區塊 C：阻力與身份 ● ●")
    text_dict["identity_give_up"] = st.text_area("5. 必須放棄的身份：要真正改變，你必須放棄什麼身份？(「我是那種...的人」) 不再做那個人，你會付出什麼社會代價？", value=text_dict.get("identity_give_up", ""))
    text_dict["embarrang_truth"] = st.text_area("6. 令人尷尬的真相：你沒有改變的最尷尬原因是什麼？", value=text_dict.get("embarrang_truth", ""))
    text_dict["self_protection"] = st.text_area("7. 自我保護：如果你現在的行為是一種自我保護，你到底在保護什麼？", value=text_dict.get("self_protection", ""))

    st.divider()
    st.subheader("● ● 區塊 D：願景 MVP (The Vision MVP) ● ●")
    text_dict["vision_3y"] = st.text_area("1. 3 年天堂：如果 3 年後你活出完全不同的人生，一個平凡的週二長什麼樣？", value=text_dict.get("vision_3y", ""))
    text_dict["new_identity"] = st.text_area("2. 新的身份：(寫下：「我是那種會...的人」)", value=text_dict.get("new_identity", ""))
    text_dict["immediate_action"] = st.text_input("3. 立即行動：如果你已經是那個人，這禮拜你會做的「一件事」是什麼？", value=text_dict.get("immediate_action", ""))

# ==========================================
# 頁籤 2：日間 - 中斷自動導航
# ==========================================
with tab2:
    st.header("⏱️ 日間 – 中斷自動導航 (The Alarm Protocol)")
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        text_dict["alarm_1100"] = st.text_area("11:00 am：我現在正在做的事，是為了逃避什麼？", value=text_dict.get("alarm_1100", ""))
        text_dict["alarm_1515"] = st.text_area("3:15 pm：我現在是正朝著我討厭的生活前進，還是我想要的生活？", value=text_dict.get("alarm_1515", ""))
        text_dict["alarm_1930"] = st.text_area("7:30 pm：今天我做了哪些事是出於「保護舊身份」而不是「真正的渴望」？", value=text_dict.get("alarm_1930", ""))
    with col2_2:
        text_dict["alarm_1330"] = st.text_area("1:30 pm：如果有人錄下我過去兩小時的行為，他們會認為我想從生活中得到什麼？", value=text_dict.get("alarm_1330", ""))
        text_dict["alarm_1700"] = st.text_area("5:00 pm：什麼是最重要的事情，但我卻假裝它不重要？", value=text_dict.get("alarm_1700", ""))
        text_dict["alarm_2100"] = st.text_area("9:00 pm：今天什麼時候我感覺最充滿活力？", value=text_dict.get("alarm_2100", ""))

    st.divider()
    text_dict["bonus_1"] = st.text_input("如果我不再需要別人視我為 [舊身份]，什麼會改變？", value=text_dict.get("bonus_1", ""))
    text_dict["bonus_2"] = st.text_input("在生活中的哪個部分，我正在用「活力」換取「安全感」？", value=text_dict.get("bonus_2", ""))
    text_dict["bonus_3"] = st.text_input("明天，我可以成為我渴望變成的那個人，最小的具體版本是什麼？", value=text_dict.get("bonus_3", ""))

# ==========================================
# 頁籤 3：晚間 - 洞察總結
# ==========================================
with tab3:
    st.header("🌙 晚間 – 洞察總結 (Synthesizing Insight)")
    col3_1, col3_2 = st.columns(2)
    with col3_1:
        text_dict["true_block"] = st.text_area("真正的阻礙：為什麼你一直停滯不前？", value=text_dict.get("true_block", ""))
        text_dict["anti_vision_compressed"] = st.text_area("反向願景 (壓縮版)：用一句話寫下你過夠了、絕不接受的糟糕未來。", value=text_dict.get("anti_vision_compressed", ""))
        text_dict["one_year_lens"] = st.text_area("一年視角：一年後必須發生什麼具體事實，證明你打破了舊模式？", value=text_dict.get("one_year_lens", ""))
    with col3_2:
        text_dict["actual_enemy"] = st.text_area("真正的敵人：操控你的內在慣性或限制性信念是什麼？", value=text_dict.get("actual_enemy", ""))
        text_dict["vision_compressed"] = st.text_area("願景 MVP (壓縮版)：用一句話寫下你正在建設的全新人生。", value=text_dict.get("vision_compressed", ""))
        text_dict["one_month_lens"] = st.text_area("一月視角：一個月後必須完成什麼，一年的目標才有可能實現？", value=text_dict.get("one_month_lens", ""))

    text_dict["daily_lens"] = st.text_area("每日視角：明天你可以把哪 2-3 個行動排進時間區塊？", value=text_dict.get("daily_lens", ""))

# ==========================================
# 頁籤 4：終極儀表板 (Master Dashboard)
# ==========================================
with tab4:
    st.header("🕹️ 終極儀表板 (Master Dashboard)")
    st.markdown("下方欄位會即時同步你在「晚間」寫下的高精煉總結。")
    
    dash_col1, dash_col2 = st.columns(2)
    with dash_col1:
        st.markdown("#### 🛑 1. 反向願景 (The Anti-Vision)")
        st.info(text_dict["anti_vision_compressed"] if text_dict.get("anti_vision_compressed") else "（請先至「晚間」分頁填寫反向願景壓縮版）")
        
        st.markdown("#### 1️⃣ 3. 一年目標 (The 1-Year Goal)")
        st.info(text_dict["one_year_lens"] if text_dict.get("one_year_lens") else "（請先至「晚間」分頁填寫一年視角）")
        
        st.markdown("#### ⚡ 5. 每日槓桿行動 (Daily Levers)")
        edited_levers = st.data_editor(df_levers, use_container_width=True, num_rows="dynamic", hide_index=True, key="ed_lev")

    with dash_col2:
        st.markdown("#### 🌅 2. 理想願景 (The Vision)")
        st.success(text_dict["vision_compressed"] if text_dict.get("vision_compressed") else "（請先至「晚間」分頁填寫願景壓縮版）")
        
        st.markdown("#### 🚧 4. 一個月專案 (The 1-Month Project)")
        st.success(text_dict["one_month_lens"] if text_dict.get("one_month_lens") else "（請先至「晚間」分頁填寫一月視角）")
        
        st.markdown("#### 🛡️ 6. 限制與底線 (Constraints)")
        text_dict["constraints"] = st.text_area("為了實現願景，我絕對不願意犧牲什麼？", value=text_dict.get("constraints", ""), height=100)

# -----------------------------------------------------------------------------
# 4. 實時檢查變動並寫回 Google Sheets
# -----------------------------------------------------------------------------
# 轉換當前文字狀態為 DataFrame 格式
df_text_current = pd.DataFrame(list(text_dict.items()), columns=["key", "value"])

# 偵測是否需要同步
if (not df_text_current.equals(df_text) or 
    not edited_complaints.equals(df_complaints) or 
    not edited_levers.equals(df_levers)):
    
    # 全面更新 Google Sheets 中的三個工作表 (Worksheets)
    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="text_data", data=df_text_current)
    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="complaints", data=edited_complaints)
    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="daily_levers", data=edited_levers)
    
    st.toast("☁️ 進度已即時同步儲存至 Google 試算表！", icon="💾")
