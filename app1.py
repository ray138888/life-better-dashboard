import streamlit as st
import pandas as pd
import json
import os

# -----------------------------------------------------------------------------
# 1. 資料儲存與讀取設定 (使用本地 JSON 檔案作為資料庫)
# -----------------------------------------------------------------------------
DATA_FILE = "identity_data.json"

DEFAULT_DATA = {
    "old_identity": "",
    "new_identity": "我是那種會將火災預測模型推進到精準的「空間危害排序」的人；也是那種為了拍下極致畫面，願意籌劃長途自駕遠行的實踐者。",
    "vision_mvp": "",
    "year_goal": "",
    "month_goal": "",
    "habits": [
        {"領域": "學術", "具體行動 (作為新身份的證據)": "調整 GCN-TCAN 模型，精化住宅多房間佈局的危險度分級", "目標量化": "120 分鐘", "今日實際": "", "完成": False},
        {"領域": "專案", "具體行動 (作為新身份的證據)": "覆核市政採購公文與預算 (確保工程管理費率 1.0% 等規範達標)", "目標量化": "1 份", "今日實際": "", "完成": False},
        {"領域": "探索", "具體行動 (作為新身份的證據)": "推進絲路自駕細節 (氣候、路線與攝影器材清單)", "目標量化": "1 節點", "今日實際": "", "完成": False}
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

# 載入當前資料
data = load_data()

# -----------------------------------------------------------------------------
# 2. 網頁介面設定 (自動響應式 RWD)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Identity Architect", page_icon="🏗️", layout="wide")

st.title("Identity :blue[Architect]")
st.markdown("基於「行為塑造身份」的逆向工程儀表板")
st.divider()

# 使用 columns 建立並排佈局 (在手機上會自動轉為上下堆疊，達成 RWD)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 身份認同 (Identity Definition)")
    new_old_id = st.text_area("必須放棄的舊身份 (社會代價是什麼？)", 
                              value=data.get("old_identity", ""), height=100)
    new_new_id = st.text_area("核心身份宣告 (我是那種會...的人)", 
                              value=data.get("new_identity", ""), height=120)

with col2:
    st.subheader("2. 願景與里程碑 (Vision & Milestones)")
    new_vision = st.text_area("Vision MVP (三年後理想的週二，細節是什麼？)", 
                              value=data.get("vision_mvp", ""), height=100)
    
    # 內部再切分欄位
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        new_year = st.text_area("一年視角 (破局事實)", value=data.get("year_goal", ""), height=120)
    with sub_col2:
        new_month = st.text_area("一月視角 (關鍵條件)", value=data.get("month_goal", ""), height=120)

st.divider()

# -----------------------------------------------------------------------------
# 3. 每日量化紀錄表 (使用互動式 Data Editor)
# -----------------------------------------------------------------------------
st.subheader("3. 每日量化證明 (Daily Quantifiable Tracker)")
st.markdown("用客觀的數字來證明「你是誰」。點擊表格直接編輯、打勾，或點擊最下方新增/刪除列。")

# 將 JSON 中的習慣資料轉為 Pandas DataFrame，方便在 Streamlit 呈現
df_habits = pd.DataFrame(data["habits"])

# 使用 data_editor，設定 num_rows="dynamic" 允許使用者自由新增、刪除資料列
edited_df = st.data_editor(
    df_habits,
    use_container_width=True, # 自動適應螢幕寬度
    num_rows="dynamic",
    column_config={
        "領域": st.column_config.TextColumn("領域", width="small"),
        "具體行動 (作為新身份的證據)": st.column_config.TextColumn("具體行動 (作為新身份的證據)", width="large"),
        "目標量化": st.column_config.TextColumn("目標量化", width="small"),
        "今日實際": st.column_config.TextColumn("今日實際", width="small"),
        "完成": st.column_config.CheckboxColumn("完成", default=False)
    },
    hide_index=True
)

# -----------------------------------------------------------------------------
# 4. 資料更新與儲存
# -----------------------------------------------------------------------------
# 將編輯後的 DataFrame 轉回 JSON 格式的字典
updated_habits = edited_df.to_dict(orient="records")

# 檢查資料是否有變動，如果有變動就自動儲存回 JSON 檔案
if (new_old_id != data.get("old_identity") or
    new_new_id != data.get("new_identity") or
    new_vision != data.get("vision_mvp") or
    new_year != data.get("year_goal") or
    new_month != data.get("month_goal") or
    updated_habits != data.get("habits")):
    
    data["old_identity"] = new_old_id
    data["new_identity"] = new_new_id
    data["vision_mvp"] = new_vision
    data["year_goal"] = new_year
    data["month_goal"] = new_month
    data["habits"] = updated_habits
    
    save_data(data)