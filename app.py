import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("사망재해 성별 분석.csv", encoding="cp949")
    return df

df = load_data()

st.title("📊 Deaths by Industry & Gender (2021–2023)")

# ✅ wide → long 포맷 변환
df_long = df.melt(id_vars=['industy', 'gender(1)'],
                  var_name='year',
                  value_name='deaths')

# 숫자형 변환
df_long['year'] = df_long['year'].astype(int)
df_long['deaths'] = pd.to_numeric(df_long['deaths'], errors='coerce')

# 사용자 선택
industries = df_long['industy'].unique()
genders = df_long['gender(1)'].unique()

selected_industry = st.selectbox("Select Industry", industries)
selected_gender = st.selectbox("Select Gender", genders)

# 필터링
filtered = df_long[
    (df_long['industy'] == selected_industry) &
    (df_long['gender(1)'] == selected_gender)
]

# 라인 그래프
st.subheader(f"📈 Trend: {selected_industry} - {selected_gender}")

sns.set(style="whitegrid")
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='year', y='deaths', marker='o', ax=ax)
ax.set_title(f"{selected_industry} - {selected_gender} Deaths")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Deaths")

st.pyplot(fig)
