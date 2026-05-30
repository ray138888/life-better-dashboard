import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# -----------------------------------------------------------------------------
# 1. 系統設定與資料庫初始化 (自動儲存至本地端 JSON 檔案)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="1天重塑人生計畫", page_icon="✨", layout="wide")

DATA_FILE = "dan_koe_1day_reset.json"

# 初始化完整的預設資料架構 (完全對應 Dan Koe 模版)
DEFAULT_DATA = {
    "mantra": "",
    "step0_checks": [False, False, False, False, False],
    # Part 1: Morning
    "tolerated_dissatisfaction": "",
    "complaints": [
        {"🗣️ 抱怨 (過去一年的前三名)": "", "🕵️‍♂️ 真實情況 (旁觀者會覺得你其實想要什麼？)": ""},
        {"🗣️ 抱怨 (過去一年的前三名)": "", "🕵️‍♂️ 真實情況 (旁觀者會覺得你其實想要什麼？)": ""},
        {"🗣️ 抱怨 (過去一年的前三名)": "", "🕵️‍♂️ 真實情況 (旁觀者會覺得你其實想要什麼？)": ""}
    ],
    "unbearable_truth": "",
    "anti_vision_5y": "",
    "anti_vision_10y": "",
    "anti_vision_end": "",
    "anti_vision_ghost": "",
    "identity_give_up": "",
    "embarrassing_truth": "",
    "self_protection": "",
    "vision_3y": "",
    "new_identity": "",
    "immediate_action": "",
    # Part 2: Throughout the Day
    "alarm_1100": "",
    "alarm_1330": "",
    "alarm_1515": "",
    "alarm_1700": "",
    "alarm_1930": "",
    "alarm_2100": "",
    "bonus_1": "",
    "bonus_2": "",
    "bonus_3": "",
    # Part 3: Evening
    "true_block": "",
    "actual_enemy": "",
    "anti_vision_compressed": "",
    "vision_compressed": "",
    "one_year_lens": "",
    "one_month_lens": "",
    "daily_lens": "",
    # Master Dashboard & Next Steps
    "constraints": "",
    "daily_levers": [
        {"任務": "建立 3 個月後的進度追蹤器", "完成": False},
        {"任務": "建立財務追蹤表", "完成": False},
        {"任務": "停止喝奶茶 (戒除壞習慣)", "完成": False},
        {"任務": "早上 10 點前回覆所有訊息，不拖延", "完成": False},
        {"任務": "每天冥想", "完成": False}
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
# 2. 標題與 Step 0 (環境設定)
# -----------------------------------------------------------------------------
st.title("✨ 1 天重塑人生計畫 (The 1-Day Reset Protocol)")
st.markdown("基於 Dan Koe 的重設協議。透過轉變身份來改變生活，打破自動導航模式，將人生變成一場可以破關的遊戲。")

with st.expander("🛑 Step 0: 環境設定 (開始前必讀)", expanded=True):
    st.markdown("撥出一整天的時間。尋求獨處，進行數位排毒，並對自己保持殘酷的誠實。")
    data["step0_checks"][0] = st.checkbox("理解：已閱讀過文章，了解核心概念。", value=data["step0_checks"][0])
    data["step0_checks"][1] = st.checkbox("獨處：不閒晃、不社交。只有你一個人。", value=data["step0_checks"][1])
    data["step0_checks"][2] = st.checkbox("時間：先撥出 30 分鐘到 1 小時來完成第一部分。", value=data["step0_checks"][2])
    data["step0_checks"][3] = st.checkbox("數位排毒：不滑社群媒體、不看 YouTube。只有你的鬧鐘和這個儀表板。", value=data["step0_checks"][3])
    data["step0_checks"][4] = st.checkbox("承諾：承諾用最殘酷、未經過濾的誠實來回答問題。", value=data["step0_checks"][4])
    
    st.markdown("❤️ **我的信念 (Mantra)**")
    data["mantra"] = st.text_input("寫下一句激勵你改變生活、擁抱新身份的咒語：", value=data["mantra"])

st.divider()

# -----------------------------------------------------------------------------
# 3. 四大核心頁籤 (Tab 系統)
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🌅 晨間：心理挖掘", "⏱️ 日間：中斷自動導航", "🌙 晚間：洞察總結", "🎯 終極儀表板"])

# ==========================================
# 頁籤 1：晨間 - 心理挖掘
# ==========================================
with tab1:
    st.header("🌅 晨間 – 心理挖掘 (Vision & Anti-Vision)")
    st.caption("為大腦建立新的認知框架。設定 15-30 分鐘。如果無法立刻回答，先留白，今天晚點再回來。")
    
    st.subheader("● ● 區塊 A：你痛苦的現實 ● ●")
    data["tolerated_dissatisfaction"] = st.text_area("1. 容忍的不滿：你已經學會與什麼樣沉悶且持續的不滿共存？", value=data["tolerated_dissatisfaction"])
    
    st.markdown("2. 抱怨審計表：你反覆抱怨但卻從未去改變的事情是什麼？")
    df_complaints = pd.DataFrame(data["complaints"])
    edited_complaints = st.data_editor(df_complaints, use_container_width=True, hide_index=True)
    data["complaints"] = edited_complaints.to_dict(orient="records")
    
    data["unbearable_truth"] = st.text_area("3. 無法承受的真相：關於你目前的生活，什麼真相是讓你覺得如果告訴你深愛/尊敬的人，會感到無法承受的？", value=data["unbearable_truth"])

    st.divider()
    st.subheader("● ● 區塊 B：反向願景 (The Anti-Vision) ● ●")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        data["anti_vision_5y"] = st.text_area("1) 5 年地獄：如果未來 5 年什麼都沒改變，描述一個平凡的週二。在哪醒來？身體感覺如何？做什麼工作？", value=data["anti_vision_5y"], height=150)
        data["anti_vision_end"] = st.text_area("3) 生命終點：你到了生命盡頭。你活了最安全的版本，從未打破模式。代價是什麼？", value=data["anti_vision_end"], height=150)
    with col1_2:
        data["anti_vision_10y"] = st.text_area("2) 10 年地獄：現在想像 10 年後。你錯過了什麼？誰放棄了你？當你不在場時，別人怎麼說你？", value=data["anti_vision_10y"], height=150)
        data["anti_vision_ghost"] = st.text_area("4) 未來的幽靈：你生活中誰已經活成了你剛才描述的未來？想到變成他們，你有什麼感覺？", value=data["anti_vision_ghost"], height=150)

    st.divider()
    st.subheader("● ● 區塊 C：阻力與身份 ● ●")
    data["identity_give_up"] = st.text_area("5. 必須放棄的身份：要真正改變，你必須放棄什麼身份？(「我是那種...的人」) 不再做那個人，你會付出什麼社會代價？", value=data["identity_give_up"])
    data["embarrassing_truth"] = st.text_area("6. 令人尷尬的真相：你沒有改變的最尷尬原因是什麼？那個聽起來讓你顯得軟弱、害怕或懶惰的真正原因？", value=data["embarrassing_truth"])
    data["self_protection"] = st.text_area("7. 自我保護：如果你現在的行為是一種自我保護，你到底在保護什麼？這層保護又讓你付出了什麼代價？", value=data["self_protection"])

    st.divider()
    st.subheader("● ● 區塊 D：願景 MVP (The Vision MVP) ● ●")
    data["vision_3y"] = st.text_area("1. 3 年天堂：如果 3 年後你活出完全不同的人生，一個平凡的週二長什麼樣？", value=data["vision_3y"])
    data["new_identity"] = st.text_area("2. 新的身份：(寫下：「我是那種會...的人」)", value=data["new_identity"])
    data["immediate_action"] = st.text_input("3. 立即行動：如果你已經是那個人，這禮拜你會做的「一件事」是什麼？", value=data["immediate_action"])

# ==========================================
# 頁籤 2：日間 - 中斷自動導航
# ==========================================
with tab2:
    st.header("⏱️ 日間 – 中斷自動導航 (The Alarm Protocol)")
    st.caption("🪄 把這些問題設定進你手機的鬧鐘標題。當鬧鐘響起時，立刻回答。你必須強制中斷大腦的慣性模式。")
    
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        data["alarm_1100"] = st.text_area("11:00 am：我現在正在做的事，是為了逃避什麼？", value=data["alarm_1100"])
        data["alarm_1515"] = st.text_area("3:15 pm：我現在是正朝著我討厭的生活前進，還是我想要的生活？", value=data["alarm_1515"])
        data["alarm_1930"] = st.text_area("7:30 pm：今天我做了哪些事是出於「保護舊身份」而不是「真正的渴望」？", value=data["alarm_1930"])
    with col2_2:
        data["alarm_1330"] = st.text_area("1:30 pm：如果有人錄下我過去兩小時的行為，他們會認為我想從生活中得到什麼？", value=data["alarm_1330"])
        data["alarm_1700"] = st.text_area("5:00 pm：什麼是最重要的事情，但我卻假裝它不重要？", value=data["alarm_1700"])
        data["alarm_2100"] = st.text_area("9:00 pm：今天什麼時候我感覺最充滿活力？什麼時候感覺最死氣沉沉？", value=data["alarm_2100"])

    st.divider()
    st.markdown("#### 🚶‍♂️ 額外反思 (通勤、散步或躺著時思考)")
    data["bonus_1"] = st.text_input("如果我不再需要別人視我為 [舊身份]，什麼會改變？", value=data["bonus_1"])
    data["bonus_2"] = st.text_input("在生活中的哪個部分，我正在用「活力」換取「安全感」？", value=data["bonus_2"])
    data["bonus_3"] = st.text_input("明天，我可以成為我渴望變成的那個人，最小的具體版本是什麼？", value=data["bonus_3"])

# ==========================================
# 頁籤 3：晚間 - 洞察總結
# ==========================================
with tab3:
    st.header("🌙 晚間 – 洞察總結 (Synthesizing Insight)")
    st.caption("🪄 經過這一天，我們需要將洞察提煉出來，開始邁向新的思維層級。")
    
    col3_1, col3_2 = st.columns(2)
    with col3_1:
        data["true_block"] = st.text_area("真正的阻礙：經過今天，關於你為何一直停滯不前，感覺最真實的原因是什麼？", value=data["true_block"], height=100)
        data["anti_vision_compressed"] = st.text_area("反向願景 (壓縮版)：用一句話寫下你拒絕讓生活變成的樣子。(讀起來要有痛感)", value=data["anti_vision_compressed"], height=100)
        data["one_year_lens"] = st.text_area("一年視角：一年後必須發生什麼具體事實，你才知道你已經打破了舊模式？", value=data["one_year_lens"], height=100)
    with col3_2:
        data["actual_enemy"] = st.text_area("真正的敵人：不是環境、不是別人。掌控你的內在模式或信念到底是什麼？", value=data["actual_enemy"], height=100)
        data["vision_compressed"] = st.text_area("願景 MVP (壓縮版)：用一句話寫下你正在建設的未來。", value=data["vision_compressed"], height=100)
        data["one_month_lens"] = st.text_area("一月視角：一個月後必須完成什麼，一年的目標才有可能實現？", value=data["one_month_lens"], height=100)

    data["daily_lens"] = st.text_area("每日視角：明天你可以把哪 2-3 個行動排進時間區塊，是那個「未來的你」自然會去做的？", value=data["daily_lens"])

# ==========================================
# 頁籤 4：終極儀表板
# ==========================================
with tab4:
    st.header("🕹️ 終極儀表板 (Master Dashboard)")
    st.markdown("將上述的所有情感包袱與洞察，濃縮成這個 1 頁的每日導航圖。**下方欄位已自動帶入你在「晚間」寫下的總結。**")
    
    dash_col1, dash_col2 = st.columns(2)
    
    with dash_col1:
        st.markdown("#### 🛑 1. 反向願景 (The Anti-Vision)")
        st.info(data["anti_vision_compressed"] if data["anti_vision_compressed"] else "（請先至「晚間」分頁填寫反向願景壓縮版）")
        
        st.markdown("#### 1️⃣ 3. 一年目標 (The 1-Year Goal)")
        st.info(data["one_year_lens"] if data["one_year_lens"] else "（請先至「晚間」分頁填寫一年視角）")
        
        st.markdown("#### ⚡ 5. 每日槓桿行動 (Daily Levers)")
        st.caption("將推進專案的核心任務寫在這裡：")
        df_levers = pd.DataFrame(data["daily_levers"])
        edited_levers = st.data_editor(df_levers, use_container_width=True, hide_index=True,
                                       column_config={"任務": st.column_config.TextColumn("具體任務", width="large"),
                                                      "完成": st.column_config.CheckboxColumn("完成", default=False)})
        data["daily_levers"] = edited_levers.to_dict(orient="records")

    with dash_col2:
        st.markdown("#### 🌅 2. 理想願景 (The Vision)")
        st.success(data["vision_compressed"] if data["vision_compressed"] else "（請先至「晚間」分頁填寫願景壓縮版）")
        
        st.markdown("#### 🚧 4. 一個月專案 (The 1-Month Project)")
        st.success(data["one_month_lens"] if data["one_month_lens"] else "（請先至「晚間」分頁填寫一月視角）")
        
        st.markdown("#### 🛡️ 6. 限制與底線 (Constraints)")
        data["constraints"] = st.text_area("為了實現願景，我絕對不願意犧牲什麼？(例如：睡眠、家庭時間、健康)", value=data["constraints"], height=100)

save_data(data)
