import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. 系統設定與 Google Sheets 雲端資料庫連線
# -----------------------------------------------------------------------------
st.set_page_config(page_title="1天重塑人生計畫", page_icon="✨", layout="wide")

# 初始化 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 📢 【已綁定：你的專屬 Google 試算表網址】
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1vSL_FxL42qZv4bl_TqELWZ6Gyi17u1yEvV3uKdcwUPA/edit?usp=sharing"

# 取得精確的儲存時間點（包含日期與時間）
NOW_STR = datetime.now().strftime("%Y-%m-%d %H:%M")

# 預設文字區塊架構
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

# -----------------------------------------------------------------------------
# 2. 利用 Session State 鎖定資料，防止重整或重新渲染時文字消失
# -----------------------------------------------------------------------------
if "load_database" not in st.session_state:
    with st.spinner("正在從雲端安全載入您的個人作業系統與歷史檔案..."):
        # 讀取文字區塊 (ttl=0 徹底關閉快取)
        try:
            df_text = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="text_data", ttl=0)
            if df_text.empty or "key" not in df_text.columns:
                st.session_state["text_dict"] = default_text_data.copy()
            else:
                st.session_state["text_dict"] = dict(zip(df_text["key"], df_text["value"]))
        except Exception:
            st.session_state["text_dict"] = default_text_data.copy()

        # 讀取抱怨審計表
        try:
            df_complaints = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="complaints", ttl=0)
            if df_complaints.empty:
                st.session_state["df_complaints"] = pd.DataFrame([{"🗣️ 抱怨 (前三名)": "", "🕵️‍♂️ 真實情況": ""}] * 3)
            else:
                st.session_state["df_complaints"] = df_complaints
        except Exception:
            st.session_state["df_complaints"] = pd.DataFrame([{"🗣️ 抱怨 (前三名)": "", "🕵️‍♂️ 真實情況": ""}] * 3)

        # 讀取每日槓桿清單
        try:
            df_levers = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="daily_levers", ttl=0)
            if df_levers.empty:
                st.session_state["df_levers"] = pd.DataFrame([
                    {"任務": "建立 GCN-TCAN 住宅模型特徵數據", "完成": False},
                    {"任務": "覆核局內電梯汰換公文預算 (管理費率 1.0%)", "完成": False},
                    {"任務": "確認 10 月絲路自駕 eHi 異地還車細節", "完成": False},
                    {"任務": "檢視美股 AI 電力基礎建設標的財報", "完成": False},
                    {"任務": "不喝奶茶，晚上進行深度冥想", "完成": False}
                ])
            else:
                st.session_state["df_levers"] = df_levers
        except Exception:
            st.session_state["df_levers"] = pd.DataFrame([{"任務": "新任務範例", "完成": False}])
            
        # 🔔 新增：讀取全時歷史紀錄流
        try:
            df_history = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="history_log", ttl=0)
            if df_history.empty or "儲存時間點" not in df_history.columns:
                st.session_state["df_history"] = pd.DataFrame(columns=["儲存時間點", "❤️ 核心信念", "🛑 反向願景", "🌅 理想願景", "1️⃣ 一年目標", "🚧 一個月專案"])
            else:
                st.session_state["df_history"] = df_history
        except Exception:
            st.session_state["df_history"] = pd.DataFrame(columns=["儲存時間點", "❤️ 核心信念", "🛑 反向願景", "🌅 理想願景", "1️⃣ 一年目標", "🚧 一個月專案"])
            
        st.session_state["load_database"] = True

# -----------------------------------------------------------------------------
# 3. 側邊欄控制台：獨立儲存按鈕
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 系統控制台")
    st.markdown("為了防止瀏覽器重新整理導致數據丟失，請在填寫完一個階段後，點擊下方按鈕同步至雲端：")
    save_button = st.button("💾 點我同步儲存至雲端", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. 響應式 RWD 介面渲染
# -----------------------------------------------------------------------------
st.title("⚡ 1 天重塑人生計畫 (The 1-Day Reset Protocol)")
st.markdown("基於 Dan Koe 經典框架 · 本系統已具備記憶體防丟失、全自動歷史流與雲端同步機制。")

# 信念與基礎宣告
st.markdown("❤️ **我的信念 (Mantra)**")
st.session_state["text_dict"]["mantra"] = st.text_input(
    "寫下一句激勵你改變生活、擁抱新身份的咒語：", 
    value=st.session_state["text_dict"].get("mantra", "")
)

st.divider()

# 四大核心頁籤
tab1, tab2, tab3, tab4 = st.tabs(["🌅 晨間：心理挖掘", "⏱️ 日間：中斷自動導航", "🌙 晚間：洞察總結", "🎯 終極儀表板"])

# ==========================================
# 頁籤 1：晨間 - 心理挖掘
# ==========================================
with tab1:
    st.header("🌅 晨間 – 心理挖掘 (Vision & Anti-Vision)")
    
    st.subheader("● ● 區塊 A：你痛苦的現實 ● ●")
    st.session_state["text_dict"]["tolerated_dissatisfaction"] = st.text_area("1. 容忍的不滿：你已經學會與什麼樣沉悶且持續的不滿共存？", value=st.session_state["text_dict"].get("tolerated_dissatisfaction", ""))
    
    st.markdown("2. 抱怨審計表：你反覆抱怨但卻從未去改變的事情是什麼？")
    st.session_state["df_complaints"] = st.data_editor(st.session_state["df_complaints"], use_container_width=True, hide_index=True, key="ed_comp")
    
    st.session_state["text_dict"]["unbearable_truth"] = st.text_area("3. 無法承受的真相：關於你目前的生活，什麼真相是讓你覺得如果告訴你深愛/尊敬的人，會感到無法承受的？", value=st.session_state["text_dict"].get("unbearable_truth", ""))

    st.divider()
    st.subheader("● ● 區塊 B：反向願景 (The Anti-Vision) ● ●")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.session_state["text_dict"]["anti_vision_5y"] = st.text_area("1) 5 年地獄：如果未來 5 年什麼都沒改變，描述一個平凡的週二。", value=st.session_state["text_dict"].get("anti_vision_5y", ""), height=150)
        st.session_state["text_dict"]["anti_vision_end"] = st.text_area("3) 生命終點：你到了生命盡頭。你活了最安全的版本，代價是什麼？", value=st.session_state["text_dict"].get("anti_vision_end", ""), height=150)
    with col1_2:
        st.session_state["text_dict"]["anti_vision_10y"] = st.text_area("2) 10 年地獄：現在想像 10 年後。你錯過了什麼？誰放棄了你？", value=st.session_state["text_dict"].get("anti_vision_10y", ""), height=150)
        st.session_state["text_dict"]["anti_vision_ghost"] = st.text_area("4) 未來的幽靈：你生活中誰已經活成了你剛才描述的未來？", value=st.session_state["text_dict"].get("anti_vision_ghost", ""), height=150)

    st.divider()
    st.subheader("● ● 區塊 C：阻力與身份 ● ●")
    st.session_state["text_dict"]["identity_give_up"] = st.text_area("5. 必須放棄的身份：要真正改變，你必須放棄什麼身份？", value=st.session_state["text_dict"].get("identity_give_up", ""))
    st.session_state["text_dict"]["embarrang_truth"] = st.text_area("6. 令人尷跨的真相：你沒有改變的最尷尬原因是什麼？", value=st.session_state["text_dict"].get("embarrang_truth", ""))
    st.session_state["text_dict"]["self_protection"] = st.text_area("7. 自我保護：如果你現在的行為是一種自我保護，你到底在保護什麼？", value=st.session_state["text_dict"].get("self_protection", ""))

    st.divider()
    st.subheader("● ● 區塊 D：願景 MVP (The Vision MVP) ● ●")
    st.session_state["text_dict"]["vision_3y"] = st.text_area("1. 3 年天堂：如果 3 年後你活出完全不同的人生，一個平凡的週二長什麼樣？", value=st.session_state["text_dict"].get("vision_3y", ""))
    st.session_state["text_dict"]["new_identity"] = st.text_area("2. 新的身份：(寫下：「我是那種會...的人」)", value=st.session_state["text_dict"].get("new_identity", ""))
    st.session_state["text_dict"]["immediate_action"] = st.text_input("3. 立即行動：如果你已經是那個人，這禮拜你會做的「一件事」是什麼？", value=st.session_state["text_dict"].get("immediate_action", ""))

# ==========================================
# 頁籤 2：日間 - 中斷自動導航
# ==========================================
with tab2:
    st.header("⏱️ 日間 – 中斷自動導航 (The Alarm Protocol)")
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.session_state["text_dict"]["alarm_1100"] = st.text_area("11:00 am：我現在正在做的事，是為了逃避什麼？", value=st.session_state["text_dict"].get("alarm_1100", ""))
        st.session_state["text_dict"]["alarm_1515"] = st.text_area("3:15 pm：我現在是正朝著我討厭的生活前進，還是我想要的生活？", value=st.session_state["text_dict"].get("alarm_1515", ""))
        st.session_state["text_dict"]["alarm_1930"] = st.text_area("7:30 pm：今天我做了哪些事是出於「保護舊身份」而不是「真正的渴望」？", value=st.session_state["text_dict"].get("alarm_1930", ""))
    with col2_2:
        st.session_state["text_dict"]["alarm_1330"] = st.text_area("1:30 pm：如果有人錄下我過去兩小時的行為，他們會認為我想從生活中得到什麼？", value=st.session_state["text_dict"].get("alarm_1330", ""))
        st.session_state["text_dict"]["alarm_1700"] = st.text_area("5:00 pm：什麼是最重要的事情，但我卻假裝它不重要？", value=st.session_state["text_dict"].get("alarm_1700", ""))
        st.session_state["text_dict"]["alarm_2100"] = st.text_area("9:00 pm：今天什麼時候我感覺最充滿活力？", value=st.session_state["text_dict"].get("alarm_2100", ""))

    st.divider()
    st.session_state["text_dict"]["bonus_1"] = st.text_input("如果我不再需要別人視我為 [舊身份]，什麼會改變？", value=st.session_state["text_dict"].get("bonus_1", ""))
    st.session_state["text_dict"]["bonus_2"] = st.text_input("在生活中的哪個部分，我正在用「活力」換取「安全感」？", value=st.session_state["text_dict"].get("bonus_2", ""))
    st.session_state["text_dict"]["bonus_3"] = st.text_input("明天，我可以成為我渴望變成的那個人，最小的具體版本是什麼？", value=st.session_state["text_dict"].get("bonus_3", ""))

# ==========================================
# 頁籤 3：晚間 - 洞察總結
# ==========================================
with tab3:
    st.header("🌙 晚間 – 洞察總結 (Synthesizing Insight)")
    col3_1, col3_2 = st.columns(2)
    with col3_1:
        st.session_state["text_dict"]["true_block"] = st.text_area("真正的阻礙：為什麼你一直停滯不前？", value=st.session_state["text_dict"].get("true_block", ""))
        st.session_state["text_dict"]["anti_vision_compressed"] = st.text_area("反向願景 (壓縮版)：用一句話寫下你過夠了、絕不接受的糟糕未來。", value=st.session_state["text_dict"].get("anti_vision_compressed", ""))
        st.session_state["text_dict"]["one_year_lens"] = st.text_area("一年視角：一年後必須發生什麼具體事實，證明你打破了舊模式？", value=st.session_state["text_dict"].get("one_year_lens", ""))
    with col3_2:
        st.session_state["text_dict"]["actual_enemy"] = st.text_area("真正的敵人：操控你的內在慣性或限制性信念是什麼？", value=st.session_state["text_dict"].get("actual_enemy", ""))
        st.session_state["text_dict"]["vision_compressed"] = st.text_area("願景 MVP (壓縮版)：用一句話寫下你正在建設的全新人生。", value=st.session_state["text_dict"].get("vision_compressed", ""))
        st.session_state["text_dict"]["one_month_lens"] = st.text_area("一月視角：一個月後必須完成什麼，一年的目標才有可能實現？", value=st.session_state["text_dict"].get("one_month_lens", ""))

    st.session_state["text_dict"]["daily_lens"] = st.text_area("每日視角：明天你可以把哪 2-3 個行動排進時間區塊？", value=st.session_state["text_dict"].get("daily_lens", ""))

# ==========================================
# 頁籤 4：終極儀表板 (Master Dashboard)
# ==========================================
with tab4:
    st.header("🕹️ 終極儀表板 (Master Dashboard)")
    st.markdown("下方欄位會即時同步你在「晚間」分頁寫下的精煉總結。")
    
    dash_col1, dash_col2 = st.columns(2)
    with dash_col1:
        st.markdown("#### 🛑 1. 反向願景 (The Anti-Vision)")
        st.info(st.session_state["text_dict"]["anti_vision_compressed"] if st.session_state["text_dict"].get("anti_vision_compressed") else "（請先至「晚間」分頁填寫反向願景壓縮版）")
        
        st.markdown("#### 1️⃣ 3. 一年目標 (The 1-Year Goal)")
        st.info(st.session_state["text_dict"]["one_year_lens"] if st.session_state["text_dict"].get("one_year_lens") else "（請先至「晚間」分頁填寫一年視角）")
        
        st.markdown("#### ⚡ 5. 每日槓桿行動 (Daily Levers)")
        st.session_state["df_levers"] = st.data_editor(st.session_state["df_levers"], use_container_width=True, num_rows="dynamic", hide_index=True, key="ed_lev")

    with dash_col2:
        st.markdown("#### 🌅 2. 理想願景 (The Vision)")
        st.success(st.session_state["text_dict"]["vision_compressed"] if st.session_state["text_dict"].get("vision_compressed") else "（請先至「晚間」分頁填寫願景壓縮版）")
        
        st.markdown("#### 🚧 4. 一個月專案 (The 1-Month Project)")
        st.success(st.session_state["text_dict"]["one_month_lens"] if st.session_state["text_dict"].get("one_month_lens") else "（請先至「晚間」分頁填寫一月視角）")
        
        st.markdown("#### 🛡️ 6. 限制與底線 (Constraints)")
        st.session_state["text_dict"]["constraints"] = st.text_area("為了實現願景，我絕對不願意犧牲什麼？", value=st.session_state["text_dict"].get("constraints", ""), height=100)

    # 🔔 新增：歷史累積紀錄流渲染區塊
    st.divider()
    st.subheader("📜 歷史全時紀錄流 (截至目前填寫軌跡)")
    st.caption("只要點擊左側的「同步儲存」，系統就會把那一刻的思考結晶追加到下方，形成你的思想進化史。")
    st.dataframe(st.session_state["df_history"], use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# 5. 手動觸發雲端儲存與歷史追加機制
# -----------------------------------------------------------------------------
if save_button:
    with st.spinner("雲端試算表同步中，正在為當前意志留下歷史存檔點..."):
        try:
            # 1. 建立當前的歷史新切片
            new_entry = pd.DataFrame([{
                "儲存時間點": NOW_STR,
                "❤️ 核心信念": st.session_state["text_dict"]["mantra"],
                "🛑 反向願景": st.session_state["text_dict"]["anti_vision_compressed"],
                "🌅 理想願景": st.session_state["text_dict"]["vision_compressed"],
                "1️⃣ 一年目標": st.session_state["text_dict"]["one_year_lens"],
                "🚧 一個月專案": st.session_state["text_dict"]["one_month_lens"]
            }])
            
            # 2. 追加至歷史 DataFrame 中
            st.session_state["df_history"] = pd.concat([st.session_state["df_history"], new_entry], ignore_index=True)
            
            # 3. 轉換文字字典為 DataFrame 格式
            df_text_save = pd.DataFrame(list(st.session_state["text_dict"].items()), columns=["key", "value"])
            
            # 4. 強制全面寫入 Google Sheets 四個分頁
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="text_data", data=df_text_save)
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="complaints", data=st.session_state["df_complaints"])
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="daily_levers", data=st.session_state["df_levers"])
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="history_log", data=st.session_state["df_history"])
            
            st.success("✅ 雲端同步成功！已為你當下的意志留下歷史存檔點！")
            st.balloons()
            st.rerun() # 重新整理由後端載入最新排列
        except Exception as e:
            st.error(f"儲存失敗，請檢查 Google 試算表的分頁名稱是否拼寫正確。錯誤訊息: {e}")
