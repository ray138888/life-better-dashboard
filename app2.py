import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date

# -----------------------------------------------------------------------------
# 1. 系統設定與 Google Sheets 雲端資料庫連線
# -----------------------------------------------------------------------------
st.set_page_config(page_title="1天重塑人生計畫", page_icon="✨", layout="wide")

# 初始化 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 📢 【已綁定：你的專屬 Google 試算表網址】
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1vSL_FxL42qZv4bl_TqELWZ6Gyi17u1yEvV3uKdcwUPA/edit?usp=sharing"

# 取得精確的時間點與今日日期
NOW_STR = datetime.now().strftime("%Y-%m-%d %H:%M")
TODAY_STR = str(date.today())

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
# 2. 利用 Session State 鎖定資料，防止重新渲染時文字消失
# -----------------------------------------------------------------------------
if "load_database" not in st.session_state:
    with st.spinner("正在從雲端安全載入您的全套重塑人生作業系統..."):
        # 讀取文字區塊
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
            
        # 讀取全時歷史大框架紀錄流
        try:
            df_history = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="history_log", ttl=0)
            if df_history.empty or "儲存時間點" not in df_history.columns:
                st.session_state["df_history"] = pd.DataFrame(columns=["儲存時間點", "❤️ 核心信念", "🛑 反向願景", "🌅 理想願景", "1️⃣ 一年目標", "🚧 一個月專案"])
            else:
                st.session_state["df_history"] = df_history
        except Exception:
            st.session_state["df_history"] = pd.DataFrame(columns=["儲存時間點", "❤️ 核心信念", "🛑 反向願景", "🌅 理想願景", "1️⃣ 一年目標", "🚧 一個月專案"])

        # 讀取 Notion 每日復盤日誌流
        try:
            df_daily_log = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="daily_review_log", ttl=0)
            if df_daily_log.empty or "日期" not in df_daily_log.columns:
                st.session_state["df_daily_log"] = pd.DataFrame(columns=["日期", "⏰ 昨晚是否早睡", "👁️ 是否正視他人/敢與女生說話", "⚡ 是否推進核心學習/工作", "🥗 是否控制飲食/運動", "📊 當日情緒穩定分數 (1-5)", "📝 一句話核心反思"])
            else:
                st.session_state["df_daily_log"] = df_daily_log
        except Exception:
            st.session_state["df_daily_log"] = pd.DataFrame(columns=["開期", "⏰ 昨晚是否早睡", "👁️ 是否正視他人/敢與女生說話", "⚡ 是否推進核心學習/工作", "🥗 是否控制飲食/運動", "📊 當日情緒穩定分數 (1-5)", "📝 一句話核心反思"])

        # 讀取週計畫看盤
        try:
            df_weekly = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="weekly_blueprint", ttl=0)
            if df_weekly.empty or "時間分配" not in df_weekly.columns:
                st.session_state["df_weekly"] = pd.DataFrame([
                    {"時間分配": "星期一 (Mon)", "🔥 深度核心工作 / 學習計畫": "跑 GCN-TCAN 住宅模型空間特徵萃取數據", "💼 淺度工作 / 局內庶務": "覆核防災中心電梯汰換工程公文及預算表", "⏳ 自由支配 / 探索充電": "閱讀美股 AI 相關電力與能源建設基礎報告"},
                    {"時間分配": "星期二 (Tue)", "🔥 深度核心工作 / 學習計畫": "優化多房間 Layout 危險度分級演算法", "💼 淺度工作 / 局內庶務": "處理工程採購管理費率 1.0% 計算書", "⏳ 自由支配 / 探索充電": "慢跑 3 公里、徹底戒奶茶"},
                    {"時間分配": "星期三 (Wed)", "🔥 深度核心工作 / 學習計畫": "撰寫論文核心章節與指導教授開會準備", "💼 淺度工作 / 局內庶務": "局內日常公文核稿、聯繫外包廠商", "⏳ 自由支配 / 探索充電": "練習社交對談、嘗試正視他人眼睛 2 秒"},
                    {"時間分配": "星期四 (Thu)", "🔥 深度核心工作 / 學習計畫": "驗證 5-fold 交叉驗證數據的穩定性", "💼 淺度工作 / 局內庶務": "召開防災中心汰換專案內部進度會議", "⏳ 自由支配 / 探索充電": "追蹤美股高增長標的趨勢、早睡"},
                    {"時間分配": "星期五 (Fri)", "🔥 深度核心工作 / 學習計畫": "統整火災模擬 FDS/CFAST 數據集", "💼 淺度工作 / 局內庶務": "清理本週未完的局內行政公文", "⏳ 自由支配 / 探索充電": "規劃 10 月絲路 16 天自駕（西安到烏魯木齊）行程細節"},
                    {"時間分配": "星期六 (Sat)", "🔥 深度核心工作 / 學習計畫": "補足本週落後的硬核論文代碼與學術閱讀", "💼 淺度工作 / 局內庶務": "完全斷開公務、不收發局內訊息", "⏳ 自由支配 / 探索充電": "出門進行戶外攝影或無壓力放空"},
                    {"時間分配": "星期日 (Sun)", "🔥 深度核心工作 / 學習計畫": "利用本網頁回顧這一週的所有每日復盤日誌", "💼 淺度工作 / 局內庶務": "進行一週抱怨審計與思想存檔點確認", "⏳ 自由支配 / 探索充電": "定錨下一週的 Weekly Blueprint 行程"}
                ])
            else:
                st.session_state["df_weekly"] = df_weekly
        except Exception:
            st.session_state["df_weekly"] = pd.DataFrame([{"時間分配": "星期一", "🔥 深度核心工作 / 學習計畫": "", "💼 淺度工作 / 局內庶務": "", "⏳ 自由支配 / 探索充電": ""}])
            
        # 讀取 KISS 每日復盤流水帳
        try:
            df_kiss_log = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="kiss_review_log", ttl=0)
            if df_kiss_log.empty or "日期" not in df_kiss_log.columns:
                st.session_state["df_kiss_log"] = pd.DataFrame(columns=["日期", "🟢 Keep (繼續保持)", "🟡 Improve (亟需改進)", "🚀 Start (馬上啟動)", "🛑 Stop (立刻停止)"])
            else:
                st.session_state["df_kiss_log"] = df_kiss_log
        except Exception:
            st.session_state["df_kiss_log"] = pd.DataFrame(columns=["日期", "🟢 Keep (繼續保持)", "🟡 Improve (亟需改進)", "🚀 Start (馬上啟動)", "🛑 Stop (立刻停止)"])
            
        st.session_state["load_database"] = True

# -----------------------------------------------------------------------------
# 3. 側邊欄控制台
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 系統控制台")
    st.markdown("當你填寫完心理挖掘、修改了週計畫看板或調整藍圖後，點擊下方按鈕一鍵同步：")
    save_button = st.button("💾 一鍵同步儲存至雲端", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. 響應式 RWD 介面渲染
# -----------------------------------------------------------------------------
st.title("⚡ 1 天重塑人生計畫 (The 1-Day Reset Protocol)")
st.markdown("❤️ **我的信念 (Mantra)**")
st.session_state["text_dict"]["mantra"] = st.text_input("寫下一句激勵你改變生活、擁抱新身份的咒語：", value=st.session_state["text_dict"].get("mantra", ""))

st.divider()

# 四大核心頁籤
tab1, tab2, tab3, tab4 = st.tabs(["🌅 晨間：心理挖掘", "⏱️ 日間：中斷自動導航", "🌙 晚間：洞察總結", "🎯 終極戰略儀表板"])

# ==========================================
# 頁籤 1 ~ 3：Dan Koe 核心拷問
# ==========================================
with tab1:
    st.header("🌅 晨間 – 心理挖掘")
    st.subheader("● ● 區塊 A：你痛苦的現實 ● ●")
    st.session_state["text_dict"]["tolerated_dissatisfaction"] = st.text_area("1. 容忍的不滿：你已經學會與什麼樣沉悶且持續的不滿共存？", value=st.session_state["text_dict"].get("tolerated_dissatisfaction", ""))
    st.markdown("2. 抱怨審計表：")
    st.session_state["df_complaints"] = st.data_editor(st.session_state["df_complaints"], use_container_width=True, hide_index=True, key="ed_comp")
    st.session_state["text_dict"]["unbearable_truth"] = st.text_area("3. 無法承受的真相：關於你目前的生活，什麼真相是讓你覺得無法承受的？", value=st.session_state["text_dict"].get("unbearable_truth", ""))
    st.divider()
    st.subheader("● ● 區塊 B：反向願景 (The Anti-Vision) ● ●")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.session_state["text_dict"]["anti_vision_5y"] = st.text_area("1) 5 年地獄：", value=st.session_state["text_dict"].get("anti_vision_5y", ""), height=150)
        st.session_state["text_dict"]["anti_vision_end"] = st.text_area("3) 生命終點：", value=st.session_state["text_dict"].get("anti_vision_end", ""), height=150)
    with col1_2:
        st.session_state["text_dict"]["anti_vision_10y"] = st.text_area("2) 10 年地獄：", value=st.session_state["text_dict"].get("anti_vision_10y", ""), height=150)
        st.session_state["text_dict"]["anti_vision_ghost"] = st.text_area("4) 未來的幽靈：", value=st.session_state["text_dict"].get("anti_vision_ghost", ""), height=150)
    st.divider()
    st.subheader("● ● 區塊 C：阻力與身份 ● ●")
    st.session_state["text_dict"]["identity_give_up"] = st.text_area("5. 必須放棄的身份：", value=st.session_state["text_dict"].get("identity_give_up", ""))
    st.session_state["text_dict"]["embarrang_truth"] = st.text_area("6. 令人尷跨的真相：", value=st.session_state["text_dict"].get("embarrang_truth", ""))
    st.session_state["text_dict"]["self_protection"] = st.text_area("7. 自我保護：", value=st.session_state["text_dict"].get("self_protection", ""))
    st.divider()
    st.subheader("● ● 區塊 D：願景 MVP ● ●")
    st.session_state["text_dict"]["vision_3y"] = st.text_area("1. 3 年天堂：", value=st.session_state["text_dict"].get("vision_3y", ""))
    st.session_state["text_dict"]["new_identity"] = st.text_area("2. 新的身份：", value=st.session_state["text_dict"].get("new_identity", ""))
    st.session_state["text_dict"]["immediate_action"] = st.text_input("3. 立即行動：", value=st.session_state["text_dict"].get("immediate_action", ""))

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

with tab3:
    st.header("🌙 晚間 – 洞察總結")
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
# 頁籤 4：終極儀表板 (Master Dashboard) 完美整合版
# ==========================================
with tab4:
    st.header("🎯 終極戰略控制中心 (Master Dashboard)")
    
    dash_col1, dash_col2 = st.columns(2)
    with dash_col1:
        st.markdown("#### 🛑 1. 反向願景 (The Anti-Vision)")
        st.info(st.session_state["text_dict"]["anti_vision_compressed"] if st.session_state["text_dict"].get("anti_vision_compressed") else "（請先至「晚間」分頁填寫）")
        st.markdown("#### 1️⃣ 3. 一年目標 (The 1-Year Goal)")
        st.info(st.session_state["text_dict"]["one_year_lens"] if st.session_state["text_dict"].get("one_year_lens") else "（請先至「晚間」分頁填寫）")
        st.markdown("#### ⚡ 5. 每日槓桿行動 (Daily Levers)")
        st.session_state["df_levers"] = st.data_editor(st.session_state["df_levers"], use_container_width=True, num_rows="dynamic", hide_index=True, key="ed_lev")
    with dash_col2:
        st.markdown("#### 🌅 2. 理想願景 (The Vision)")
        st.success(st.session_state["text_dict"]["vision_compressed"] if st.session_state["text_dict"].get("vision_compressed") else "（請先至「晚間」分頁填寫）")
        st.markdown("#### 🚧 4. 一個月專案 (The 1-Month Project)")
        st.success(st.session_state["text_dict"]["one_month_lens"] if st.session_state["text_dict"].get("one_month_lens") else "（請先至「晚間」分頁填寫）")
        st.markdown("#### 🛡️ 6. 限制與底線 (Constraints)")
        st.session_state["text_dict"]["constraints"] = st.text_area("為了實現願景，我絕對不願意犧牲什麼？", value=st.session_state["text_dict"].get("constraints", ""), height=100)

    # 週計畫戰術看板
    st.divider()
    st.subheader("📅 一週戰略計畫藍圖 (Weekly Blueprint)")
    st.session_state["df_weekly"] = st.data_editor(
        st.session_state["df_weekly"], use_container_width=True, hide_index=True, key="ed_weekly",
        column_config={
            "時間分配": st.column_config.TextColumn("📅 時間範圍", disabled=True, width="small"),
            "🔥 深度核心工作 / 學習計畫": st.column_config.TextColumn("🔥 深度核心工作 / 核心技能學習計畫", width="large"),
            "💼 淺度工作 / 局內庶務": st.column_config.TextColumn("💼 淺度工作 / 行政庶務核稿", width="medium"),
            "⏳ 自由支配 / 探索充電": st.column_config.TextColumn("⏳ 自由支配 / 投資探索與生活充電", width="medium")
        }
    )

    # KISS 每日滾動高能復盤
    st.divider()
    st.subheader("💋 KISS 每日敏捷進化復盤 (Keep / Improve / Start / Stop)")
    picked_date = st.date_input("📆 請選擇 KISS 復盤日期：", value=date.today(), key="kiss_date_picker")
    KISS_DATE_STR = picked_date.strftime("%B %d, %Y")
    
    st.info(f"✍️ 您正在填寫 **{KISS_DATE_STR}** 的 KISS 戰術進化報告：")
    kiss_col1, kiss_col2 = st.columns(2)
    with kiss_col1:
        kiss_keep = st.text_area("🟢 Keep (今天做得很好，未來要繼續保持的習慣/心態？)", placeholder="例如：對談時有直視眼睛2秒、堅持沒點奶茶。", key="k_input")
        kiss_improve = st.text_area("🟡 Improve (今天有哪些地方做得不夠好，亟需改進與調整？)", placeholder="例如：晚上11點後又忍不住開始滑美股，導致大腦過度興奮。", key="i_input")
    with kiss_col2:
        kiss_start = st.text_area("🚀 Start (為了擊敗舊身份，明天有哪些行動必須馬上啟動？)", placeholder="例如：明天上班前先去買無糖豆漿，中斷對含糖飲料的依賴。", key="s_input")
        kiss_stop = st.text_area("🛑 Stop (有哪些消耗精力、引發情緒化的壞習慣必須立刻停止？)", placeholder="例如：立刻停止半途而廢的心態，代碼卡住時不准立刻關掉視窗。", key="st_input")

    submit_kiss = st.button("🚀 提交今日 KISS 進化報告", type="primary")
    if submit_kiss:
        with st.spinner("正在將 KISS 數據寫入雲端..."):
            try:
                new_kiss_row = pd.DataFrame([{"日期": KISS_DATE_STR, "🟢 Keep (繼續保持)": kiss_keep, "🟡 Improve (亟需改進)": kiss_improve, "🚀 Start (馬上啟動)": kiss_start, "🛑 Stop (立刻停止)": kiss_stop}])
                st.session_state["df_kiss_log"] = st.session_state["df_kiss_log"][st.session_state["df_kiss_log"]["日期"] != KISS_DATE_STR]
                st.session_state["df_kiss_log"] = pd.concat([st.session_state["df_kiss_log"], new_kiss_row], ignore_index=True)
                conn.update(spreadsheet=SPREADSHEET_URL, worksheet="kiss_review_log", data=st.session_state["df_kiss_log"])
                st.success(f"🎉 {KISS_DATE_STR} 的 KISS 戰術進化報告已成功安全同步！")
                st.balloons()
            except Exception as e: st.error(f"KISS 儲存失敗: {e}")

    st.markdown("#### 📜 我的歷史 KISS 進化軌跡")
    st.dataframe(st.session_state["df_kiss_log"], use_container_width=True, hide_index=True)

    # 🔥 【完美修復：具備每日更新、滾動重置功能的基礎指標打勾追蹤】
    st.divider()
    st.subheader("📊 每日基礎指標打勾 (習慣與狀態追蹤)")
    st.markdown("此區塊已全面升級為**「動態滾動重置」**。切換新日期時，打勾方塊與滑桿會自動清空，方便您依照實際情況填寫。")
    
    # 🔔 指標打勾區塊的專屬日期定錨器
    picked_review_date = st.date_input("📆 請選擇指標追蹤日期：", value=date.today(), key="review_date_picker")
    REVIEW_DATE_STR = str(picked_review_date) # 儲存標準格式如 "2026-05-31"
    
    st.info(f"✍️ 正在填寫 **{REVIEW_DATE_STR}** 的實際行為指標：")
    
    rev_col1, rev_col2, rev_col3 = st.columns([1, 1, 1.5])
    with rev_col1:
        rev_sleep = st.checkbox("⏰ 昨晚是否在 12 點前早睡？ (拿回理性大腦主導權)", value=False, key=f"chk_sleep_{REVIEW_DATE_STR}")
        rev_social = st.checkbox("👁️ 今天對談是否有直視他人眼睛/敢跟女生正常說話？", value=False, key=f"chk_social_{REVIEW_DATE_STR}")
    with rev_col2:
        rev_study = st.checkbox("⚡ 今天是否有推進高槓桿學習/工作？ (研究論文/預算審查)", value=False, key=f"chk_study_{REVIEW_DATE_STR}")
        rev_diet = st.checkbox("🥗 今天是否有控制飲食與運動習慣？ (管住嘴、拒絕奶茶)", value=False, key=f"chk_diet_{REVIEW_DATE_STR}")
    with rev_col3:
        # 加上動態 Key，只要切換日期，滑桿與文字框就會立刻重置為預設值
        rev_emotion = st.slider("📊 今日情緒穩定與克制衝動分數 (1:極度情緒化, 5:冷靜理性掌控者)", 1, 5, 3, key=f"sld_emo_{REVIEW_DATE_STR}")
        rev_note = st.text_input("📝 一句話核心反思：", placeholder="今天你在什麼地方差點向舊習慣妥協？", key=f"txt_note_{REVIEW_DATE_STR}")

    submit_daily_review = st.button("🚀 提交該日指標日誌並寫入雲端", type="primary", key="btn_review_submit")
    if submit_daily_review:
        with st.spinner("正在將指標戰果同步至雲端試算表..."):
            try:
                # 建立新紀錄
                new_review_row = pd.DataFrame([{
                    "日期": REVIEW_DATE_STR,
                    "⏰ 昨晚是否早睡": "✅ 是" if rev_sleep else "❌ 否",
                    "👁️ 是否正視他人/敢與女生說話": "✅ 是" if rev_social else "❌ 否",
                    "⚡ 是否推進核心學習/工作": "✅ 是" if rev_study else "❌ 否",
                    "🥗 是否控制飲食/運動": "✅ 是" if rev_diet else "❌ 否",
                    "📊 當日情緒穩定分數 (1-5)": rev_emotion,
                    "📝 一句話核心反思": rev_note
                }])
                
                # 自動去重覆蓋
                st.session_state["df_daily_log"] = st.session_state["df_daily_log"][st.session_state["df_daily_log"]["日期"] != REVIEW_DATE_STR]
                st.session_state["df_daily_log"] = pd.concat([st.session_state["df_daily_log"], new_review_row], ignore_index=True)
                
                # 寫入工作表 daily_review_log
                conn.update(spreadsheet=SPREADSHEET_URL, worksheet="daily_review_log", data=st.session_state["df_daily_log"])
                st.success(f"🎉 {REVIEW_DATE_STR} 的基礎指標已成功寫入雲端！")
                st.balloons()
            except Exception as e:
                st.error(f"指標儲存失敗，請確保試算表內有名為 daily_review_log 的分頁。錯誤: {e}")

    st.markdown("#### 📊 我的重塑歷史數據流水帳 (全天候累積軌跡)")
    st.dataframe(st.session_state["df_daily_log"], use_container_width=True, hide_index=True)

    # 歷史計畫存檔流
    st.divider()
    st.subheader("📜 戰略藍圖進化軌跡 (計畫變更存檔點)")
    st.dataframe(st.session_state["df_history"], use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# 5. 手動觸發雲端儲存與歷史大框架追加機制
# -----------------------------------------------------------------------------
if save_button:
    with st.spinner("雲端試算表全面寫入同步中..."):
        try:
            new_entry = pd.DataFrame([{"儲存時間點": NOW_STR, "❤️ 核心信念": st.session_state["text_dict"]["mantra"], "🛑 反向願景": st.session_state["text_dict"]["anti_vision_compressed"], "🌅 理想願景": st.session_state["text_dict"]["vision_compressed"], "1️⃣ 一年目標": st.session_state["text_dict"]["one_year_lens"], "🚧 一個月專案": st.session_state["text_dict"]["one_month_lens"]}])
            st.session_state["df_history"] = pd.concat([st.session_state["df_history"], new_entry], ignore_index=True)
            df_text_save = pd.DataFrame(list(st.session_state["text_dict"].items()), columns=["key", "value"])
            
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="text_data", data=df_text_save)
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="complaints", data=st.session_state["df_complaints"])
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="daily_levers", data=st.session_state["df_levers"])
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="history_log", data=st.session_state["df_history"])
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="weekly_blueprint", data=st.session_state["df_weekly"])
            
            st.success("✅ 雲端大框架同步成功！")
            st.rerun() 
        except Exception as e: st.error(f"大框架儲存失敗: {e}")
