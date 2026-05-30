import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# -----------------------------------------------------------------------------
# 1. 系統設定與資料庫初始化 (本地 JSON 存檔)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="My Life OS", page_icon="🌌", layout="wide")

DATA_FILE = "life_os_data.json"
TODAY = str(date.today())

# 預設資料 (包含你的具體執行任務)
DEFAULT_DATA = {
    "vision": "我是那種會將火災預測模型推進到精準的「空間危害排序」的人；也是那種願意籌劃長途自駕遠行的實踐者。",
    "habits": [
        {"領域": "學術", "具體行動": "調整 GCN-TCAN 模型，精化「住宅」多房間佈局的危險度分級", "目標": "120 分鐘", "今日實際": "", "完成": False},
        {"領域": "專案", "具體行動": "覆核市政採購公文 (確認工程管理費率套用 1.0% 標準)", "目標": "1 份", "今日實際": "", "完成": False},
        {"領域": "探索", "具體行動": "推進 10 月絲路自駕 (西安至烏魯木齊) 準備：確認 eHi 租車與秋季路況", "目標": "1 項", "今日實際": "", "完成": False}
    ],
    "journals": {} # 儲存每日日記的字典
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

# 確保今天的日記欄位存在
if TODAY not in data["journals"]:
    data["journals"][TODAY] = {"morning": "", "evening": ""}

# -----------------------------------------------------------------------------
# 2. 介面設計：Notion 風格的多頁籤系統
# -----------------------------------------------------------------------------
st.title("🌌 系統化個人作業系統 (Life OS)")
st.markdown("將大腦的混亂外包給系統，把精力留給執行。")
st.divider()

# 建立三個分頁
tab1, tab2, tab3 = st.tabs(["✅ 每日量化打卡", "📔 晨晚間復盤", "🎯 核心願景設定"])

# ==========================================
# 分頁 1：每日量化打卡 (Habit Tracker)
# ==========================================
with tab1:
    st.subheader("今日執行矩陣")
    df_habits = pd.DataFrame(data["habits"])
    
    edited_df = st.data_editor(
        df_habits,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "完成": st.column_config.CheckboxColumn("完成", default=False)
        },
        hide_index=True
    )
    
    # 檢查並儲存變更
    updated_habits = edited_df.to_dict(orient="records")
    if updated_habits != data["habits"]:
        data["habits"] = updated_habits
        save_data(data)

# ==========================================
# 分頁 2：晨晚間復盤 (Daily Journal)
# ==========================================
with tab2:
    st.subheader(f"📅 今日復盤 ({TODAY})")
    
    st.markdown("#### 🌅 晨間意圖 (Morning Intention)")
    morning_text = st.text_area("今天最重要的一件事是什麼？我今天要避開什麼干擾？", 
                                value=data["journals"][TODAY]["morning"], height=100)
    
    st.markdown("#### 🌙 晚間反思 (Evening Review)")
    evening_text = st.text_area("今天學到了什麼？有哪些進度？明天可以如何優化？", 
                                value=data["journals"][TODAY]["evening"], height=150)
    
    # 檢查並儲存日記
    if morning_text != data["journals"][TODAY]["morning"] or evening_text != data["journals"][TODAY]["evening"]:
        data["journals"][TODAY]["morning"] = morning_text
        data["journals"][TODAY]["evening"] = evening_text
        save_data(data)

# ==========================================
# 分頁 3：核心願景設定 (Vision Board)
# ==========================================
with tab3:
    st.subheader("身份重塑與一年目標")
    new_vision = st.text_area("宣告你的新身份與願景", value=data["vision"], height=150)
    
    if new_vision != data["vision"]:
        data["vision"] = new_vision
        save_data(data)

st.caption("所有變更皆會自動儲存。")
