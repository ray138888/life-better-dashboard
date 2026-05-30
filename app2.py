import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# -----------------------------------------------------------------------------
# 1. 系統設定與資料庫初始化 (自動儲存至本地端 JSON 檔案)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="1天重塑人生計畫", page_icon="⚡", layout="wide")

DATA_FILE = "dan_koe_full_template.json"

# 萬全還原 Dan Koe Notion 模版的五大核心區塊
DEFAULT_DATA = {
    "anti_vision": "寫下你絕對不想成為的人...\n(例如：身體肥胖、毫無專業累積、每天醒來都在為預算與時間感到無力與焦虑。)",
    "ideal_vision": "寫下你渴望過上的生活...\n(例如：自由掌控清晨的 4 小時深度工作，將硬核技術轉化為個人槓桿，每年能安排一場極致的自駕探索。) ",
    "one_year_goals": [
        {"核心領域": "🚀 學術與技能", "目標描述": "完成 GCN-TCAN 模型優化與論文，聚焦住宅佈局危險度分級", "預計破局時程": "12 個月內"},
        {"核心領域": "💼 專案與事業", "目標描述": "精準控管局內工程進度與預算編列 (如防災中心汰換案)", "預計破局時程": "持續維持"},
        {"核心領域": "🌍 自由與探索", "目標描述": "解鎖 16 天絲路自駕與高難度alpine攝影計畫", "預計破局時程": "2026年10月"}
    ],
    "weekly_milestones": [
        {"本週關鍵任務": "跑出一組多房間配置的危險度分級數據", "對應一年目標": "學術與技能", "緊急程度": "🔥 緊急高價值", "確認完成": False},
        {"本週關鍵任務": "完成電梯汰換工程採購公文覆核 (費率 1.0%)", "對應一年目標": "專案與事業", "緊急程度": "⚡ 重要非緊急", "確認完成": False},
        {"本週關鍵任務": "確認 eHi 租車西安/烏魯木齊異地還車細節", "對應一年目標": "自由與探索", "緊急程度": "☕ 日常維護", "確認完成": False}
    ],
    "daily_time_blocks": [
        {"時間": "07:00 - 09:00", "核心焦點": "🔥 深度工作 (無干擾)", "具體產出 / 行動項目": "關閉手機，全力衝刺論文核心特徵萃取代碼與數據分析", "狀態": "未開始"},
        {"時間": "09:00 - 10:00", "核心焦點": "☕ 緩衝休息", "具體產出 / 行動項目": "放空、盥洗、早餐、高意圖思考今天避開什麼", "狀態": "未開始"},
        {"時間": "10:00 - 12:00", "核心焦點": "💼 淺度工作 (庶務)", "具體產出 / 行動項目": "處理局內公文、審核採購預算表、日常聯繫", "狀態": "未開始"},
        {"時間": "13:00 - 14:00", "核心焦點": "🗺️ 探索/投資管理", "具體產出 / 行動項目": "規劃絲路自駕路況或覆盤美股 AI 電力基礎建設標的", "狀態": "未開始"},
        {"時間": "14:00 以後", "核心焦點": "⏳ 自由支配 (斷開)", "具體產出 / 行動項目": "健身、閱讀、陪伴、或徹底放空放鬆", "狀態": "未開始"}
    ]
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# -----------------------------------------------------------------------------
# 2. 響應式 RWD 介面渲染 (全繁體中文)
# -----------------------------------------------------------------------------
st.title("⚡ 1 天人生重塑作業系統 (How to Fix Your Life in 1 Day)")
st.markdown("意識決定方向，系統決定結果。這套系統完美對應 Dan Koe 的核心日常架構。")
st.divider()

# ==========================================
# 頂部：願景指南（雙欄 RWD 佈局）
# ==========================================
st.subheader("📌 模版第一部分：身份與意識錨定 (Identity Alignment)")
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown("#### 🛑 反向願景 (The Anti-Vision)")
    st.caption("痛苦是最好的燃料。寫下你一年後死也不想過的生活：")
    updated_anti = st.text_area("我不允許自己變成這樣的人：", value=data["anti_vision"], height=120, key="anti_v_input")

with col_v2:
    st.markdown("#### 🏆 理想願景 (The Ideal Vision)")
    st.caption("北極星指標。寫下你三年後真正渴望且具備主導權的生活：")
    updated_ideal = st.text_area("這是我正在前往的終點：", value=data["ideal_vision"], height=120, key="ideal_v_input")

st.divider()

# ==========================================
# 中部：戰略拆解（雙欄 RWD 佈局）
# ==========================================
st.subheader("🎯 模版第二部分：目標逆向工程 (Goal Reverse Engineering)")
col_g1, col_g2 = st.columns([1, 1.2])

with col_g1:
    st.markdown("#### 🚀 一年視角破局目標 (1-Year Goals)")
    st.caption("在今年內，有哪三大具體事實能向世界證明你打破了舊循環？")
    
    df_year = pd.DataFrame(data["one_year_goals"])
    edited_year = st.data_editor(
        df_year, use_container_width=True, num_rows="dynamic", hide_index=True,
        column_config={
            "核心領域": st.column_config.SelectboxColumn("核心領域", options=["🚀 學術與技能", "💼 專案與事業", "🌍 自由與探索", "💰 財務與投資"], width="small"),
            "目標描述": st.column_config.TextColumn("目標描述", width="large"),
            "預計破局時程": st.column_config.TextColumn("時程", width="small")
        }
    )

with col_g2:
    st.markdown("#### 📅 一週視角核心里程碑 (Weekly Milestones)")
    st.caption("為了讓一年目標發生，這星期有哪三件重要大案是你必須死守的底線？")
    
    df_week = pd.DataFrame(data["weekly_milestones"])
    edited_week = st.data_editor(
        df_week, use_container_width=True, num_rows="dynamic", hide_index=True,
        column_config={
            "本週關鍵任務": st.column_config.TextColumn("本週關鍵任務", width="large"),
            "對應一年目標": st.column_config.TextColumn("對應領域", width="small"),
            "緊急程度": st.column_config.SelectboxColumn("分類", options=["🔥 緊急高價值", "⚡ 重要非緊急", "☕ 日常維護"]),
            "確認完成": st.column_config.CheckboxColumn("完成狀態", default=False)
        }
    )

st.divider()

# ==========================================
# 底部：每日執行（單欄完美適應手機端）
# ==========================================
st.subheader("⏰ 模版第三部分：每日時間區塊防守矩陣 (Daily Time-Blocking)")
st.markdown("不要填滿每一分鐘，而是保護你最神聖的 **4 小時深度工作**。")

df_daily = pd.DataFrame(data["daily_time_blocks"])
edited_daily = st.data_editor(
    df_daily, use_container_width=True, num_rows="dynamic", hide_index=True,
    column_config={
        "時間": st.column_config.TextColumn("⏰ 時間範圍", width="small"),
        "核心焦點": st.column_config.SelectboxColumn("🎯 核心焦點", options=["🔥 深度工作 (無干擾)", "💼 淺度工作 (庶務)", "☕ 緩衝休息", "🗺️ 探索/投資管理", "⏳ 自由支配 (斷開)"], width="medium"),
        "具體產出 / 行動項目": st.column_config.TextColumn("📝 具體產出 / 行動項目（不可模糊，要有檢核點）", width="large"),
        "狀態": st.column_config.SelectboxColumn("📌 狀態", options=["未開始", "執行中 ⚡", "已完成 ✅", "已順延 ☕"])
    }
)

# -----------------------------------------------------------------------------
# 3. 自動偵測變更與儲存機制
# -----------------------------------------------------------------------------
updated_year_list = edited_year.to_dict(orient="records")
updated_week_list = edited_week.to_dict(orient="records")
updated_daily_list = edited_daily.to_dict(orient="records")

if (updated_anti != data["anti_vision"] or 
    updated_ideal != data["ideal_vision"] or 
    updated_year_list != data["one_year_goals"] or 
    updated_week_list != data["weekly_milestones"] or 
    updated_daily_list != data["daily_time_blocks"]):
    
    data["anti_vision"] = updated_anti
    data["ideal_vision"] = updated_ideal
    data["one_year_goals"] = updated_year_list
    data["weekly_milestones"] = updated_week_list
    data["daily_time_blocks"] = updated_daily_list
    
    save_data(data)
    st.toast("💾 變更已自動同步儲存至系統！")
