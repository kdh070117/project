import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv("/mnt/data/사망재해 성별 분석.csv", encoding="cp949")
    return df

# 데이터 로딩
df = load_data()

# 페이지 제목
st.title("📊 Deaths by Industry & Gender (2021–2023)")

# 데이터 변형: wide → long
df_long = df.melt(
    id_vars=['industy', 'gender(1)'],
    var_name='year',
    value_name='deaths'
)

# 타입 변환
df_long['year'] = df_long['year'].astype(int)
df_long['deaths'] = pd.to_numeric(df_long['deaths'], errors='coerce')

# 사용자 선택 필터
industries = df_long['industy'].unique()
genders = df_long['gender(1)'].unique()

selected_industry = st.selectbox("Select Industry", industries)
selected_gender = st.selectbox("Select Gender", genders)

# 선택 필터링
filtered = df_long[
    (df_long['industy'] == selected_industry) &
    (df_long['gender(1)'] == selected_gender)
]

# 그래프 출력
st.subheader(f"📈 Trend: {selected_industry} - {selected_gender}")

sns.set(style="whitegrid")
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='year', y='deaths', marker='o', ax=ax)
ax.set_title(f"{selected_industry} - {selected_gender} Deaths")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Deaths")

# ✅ x축 레이블 회전 및 글꼴 크기 조정
ax.tick_params(axis='x', labelsize=10)
plt.xticks(rotation=45)

st.pyplot(fig)
