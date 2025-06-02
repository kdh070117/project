import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# ✅ 한글 폰트 수동 설정 (Streamlit Cloud 포함)
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

@st.cache_data
def load_data():
    return pd.read_csv("사망재해_현황_및_분석성별_20250602121409.csv", encoding="cp949")

df = load_data()

st.title("📈 산업별·성별 사망자 수 라인 그래프")

df_long = df.melt(id_vars=['산업중분류별(1)', '성별(1)'],
                  var_name='연도',
                  value_name='사망자수')
df_long['연도'] = df_long['연도'].astype(int)

# 사용자 선택
산업목록 = df_long['산업중분류별(1)'].unique()
성별목록 = df_long['성별(1)'].unique()

선택산업 = st.selectbox("산업을 선택하세요", 산업목록)
선택성별 = st.selectbox("성별을 선택하세요", 성별목록)

# 필터링
filtered = df_long[
    (df_long['산업중분류별(1)'] == 선택산업) &
    (df_long['성별(1)'] == 선택성별)
]

# 그래프
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='연도', y='사망자수', marker='o', ax=ax)
ax.set_title(f"{선택산업} - {선택성별} 사망자 수 추이")
ax.set_xlabel("연도")
ax.set_ylabel("사망자 수")

st.pyplot(fig)
