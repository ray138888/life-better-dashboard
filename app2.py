import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Identity Architect", page_icon="🏗️", layout="wide")

# 1. 建立與 Google Sheets 的連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 填入你剛剛建立的 Google 試算表網址 (URL)
# 請將下方的網址替換成你自己的試算表網址
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/你的試算表ID/edit"

st.title("Identity :blue[Architect] (Cloud Sync ☁️)")
st.markdown("資料已與 Google 試算表雙向綁定")
st.divider()

# 2. 從 Google Sheets 讀取資料
# 假設我們將資料存在名為 'habits' 的工作表中
try:
    df_habits = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="habits")
    # 如果是空表，初始化欄位
    if df_habits.empty:
        df_habits = pd.DataFrame(columns=["領域", "具體行動", "目標量化", "今日實際", "完成"])
except Exception as e:
    st.warning("尚未偵測到工作表資料，將建立初始預設值。")
    df_habits = pd.DataFrame([
        {"領域": "學術", "具體行動": "調整 GCN-TCAN 模型", "目標量化": "120 分鐘", "今日實際": "", "完成": False}
    ])

st.subheader("每日量化證明 (Daily Quantifiable Tracker)")

# 3. 使用 data_editor 讓使用者編輯
edited_df = st.data_editor(
    df_habits,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "完成": st.column_config.CheckboxColumn("完成", default=False)
    },
    hide_index=True
)

# 4. 檢查是否有變動，若有變動則寫回 Google Sheets
# 比較兩個 DataFrame 是否相等，若不相等則觸發更新
if not df_habits.equals(edited_df):
    conn.update(
        spreadsheet=SPREADSHEET_URL,
        worksheet="habits",
        data=edited_df
    )
    st.success("✅ 資料已自動同步至 Google 試算表！")