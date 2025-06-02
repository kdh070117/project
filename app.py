import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

matplotlib.rcParams['font.family'] = 'NanumGothic'  # 또는 'Malgun Gothic'

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("사망재해_현황_및_분석성별_20250602121409.csv", encoding="cp949")
    return df

df = load_data()

st.title("📈 산업별·성별 사망자 수 라인 그래프")

# ✅ wide -> long 포맷으로 변환
df_long = df.melt(id_vars=['산업중분류별(1)', '성별(1)'], 
                  var_name='연도', 
                  value_name='사망자수')

# 연도는 문자열이므로 정수형으로 바꿔주자
df_long['연도'] = df_long['연도'].astype(int)

# 사용자 선택: 산업 분야와 성별 필터링
industries = df_long['산업중분류별(1)'].unique()
genders = df_long['성별(1)'].unique()

selected_industry = st.selectbox("산업을 선택하세요", industries)
selected_gender = st.selectbox("성별을 선택하세요", genders)

# 필터링
filtered = df_long[
    (df_long['산업중분류별(1)'] == selected_industry) &
    (df_long['성별(1)'] == selected_gender)
]

# 📈 라인 그래프
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='연도', y='사망자수', marker='o', ax=ax)
ax.set_title(f"{selected_industry} - {selected_gender} 사망자 수 추이")
ax.set_xlabel("연도")
ax.set_ylabel("사망자 수")

st.pyplot(fig)
