import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# -----------------------------------------------------------------------------
# 1. 系統設定與資料庫初始化 (自動儲存至本地端 JSON 檔案)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="一年重塑計畫", page_icon="🎯", layout="wide")

DATA_FILE = "dan_koe_life_data.json"

# 初始化繁體中文的預設資料架構
DEFAULT_DATA = {
    "anti_vision": "每天渾渾噩噩、專業技能停滯不前；在 5 年後還拿著差不多的薪水，身體肥胖、缺乏精力，每天醒來都感到焦慮與後悔。",
    "week_focus": "本週核心：攻克論文關鍵數據，同時精準覆核局內重要工程預算。",
    "top_priorities": [
        "調整 GCN-TCAN 空間特徵萃取模型，精化住宅佈局的危險度分級",
        "覆核防災中心電梯汰換工程公文 (確認工程管理費率套用 1.0%)",
        "推進 10 月絲路 16 天自駕自駕與行程細節 (確認 eHi 租車與秋季路況)"
    ],
    "time_blocks": [
        {"時間區塊": "07:00 - 09:00", "核心領域": "🔥 深度工作", "具體任務 / 預期產出": "執行火災模擬與 GCN-TCAN 數據跑組", "狀態": "未開始"},
        {"時間區塊": "09:00 - 10:00", "核心領域": "☕ 緩衝時間", "具體任務 / 預期產出": "盥洗、早餐、切換思維狀態", "狀態": "未開始"},
        {"時間區塊": "10:00 - 12:00", "核心領域": "💼 淺度工作", "具體任務 / 預期產出": "處理局內防災中心公文與行政庶備", "狀態": "未開始"},
        {"時間區塊": "13:00 - 14:00", "核心領域": "🗺️ 探索規劃", "具體任務 / 預期產出": "確認絲路自駕（西安到烏魯木齊）路況與還車方案", "狀態": "未開始"},
        {"時間區塊": "14:00 以後", "核心領域": "⏳ 自由支配", "具體任務 / 預期產出": "維持日常規律、健身、閱讀、檢視美股 AI 電力基礎建設走勢", "狀態": "未開始"}
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
# 2. 網頁視覺與響應式介面設計 (RWD 繁體中文版)
# -----------------------------------------------------------------------------
st.title("🎯 1 年人生重塑系統 (Life Architect)")
st.markdown(f"基於 Dan Koe 經典框架 · 今天是 `{date.today()}`")
st.divider()

# RWD 兩欄佈局：左邊是願景引導，右邊是今日行動
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🛑 階段一：反向願景 (Anti-Vision)")
    st.caption("提醒自己：如果今天偷懶，一年後絕對不想過上什麼樣的痛苦生活？")
    new_anti_vision = st.text_area("寫下你最討厭的現狀與盲點：", value=data["anti_vision"], height=140, key="av_input")
    
    st.divider()
    
    st.subheader("📅 本週核心焦點")
    new_week_focus = st.text_input("這一週的破局關鍵事實：", value=data["week_focus"], key="wf_input")
    
    st.markdown("#### 🚀 今日最重要的 3 件高槓桿任務")
    p1 = st.text_input("1. 最高優先 (學術/核心技能)", value=data["top_priorities"][0])
    p2 = st.text_input("2. 次要優先 (專案/當前業務)", value=data["top_priorities"][1])
    p3 = st.text_input("3. 維護優先 (自我實現/探索)", value=data["top_priorities"][2])
    
    new_priorities = [p1, p2, p3]

with col2:
    st.subheader("⚡ 階段二：時間區塊防守矩陣 (Time-Blocking)")
    st.markdown("不用填滿每一分鐘，而是確保神聖的 **深度工作時間** 不被任何人打擾。")
    st.caption("💡 技巧：您可以直接點擊下方表格內的任何格子進行「修改任務」或「切換狀態」。")
    
    # 轉換成 DataFrame 供 Data Editor 編輯
    df_blocks = pd.DataFrame(data["time_blocks"])
    
    edited_df = st.data_editor(
        df_blocks,
        use_container_width=True,
        num_rows="dynamic", # 允許自由增減時間區塊
        column_config={
            "時間區塊": st.column_config.TextColumn("⏰ 時間範圍", width="small", help="例如：07:00 - 09:00"),
            "核心領域": st.column_config.SelectboxColumn(
                "🎯 領域類別",
                options=["🔥 深度工作", "💼 淺度工作", "☕ 緩衝時間", "🗺️ 探索規劃", "⏳ 自由支配"],
                width="small"
            ),
            "具體任務 / 預期產出": st.column_config.TextColumn("📝 具體任務 / 預期產出", width="large"),
            "狀態": st.column_config.SelectboxColumn(
                "📌 狀態",
                options=["未開始", "執行中 ⚡", "已完成 ✅", "已順延 ☕"],
                width="small"
            )
        },
        hide_index=True
    )

# -----------------------------------------------------------------------------
# 3. 自動偵測變更與儲存機制
# -----------------------------------------------------------------------------
updated_blocks = edited_df.to_dict(orient="records")

if (new_anti_vision != data["anti_vision"] or 
    new_week_focus != data["week_focus"] or 
    new_priorities != data["top_priorities"] or 
    updated_blocks != data["time_blocks"]):
    
    data["anti_vision"] = new_anti_vision
    data["week_focus"] = new_week_focus
    data["top_priorities"] = new_priorities
    data["time_blocks"] = updated_blocks
    
    save_data(data)
    st.toast("系統已自動同步變更！", icon="💾")
