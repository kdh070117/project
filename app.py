import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv("data/사망재해 성별 분석.csv", encoding="cp949")
    return df

df = load_data()

st.title("📊 Deaths by Industry & Gender (2021–2023)")

# 컬럼명 실제 파일에 맞게 수정 필요 (예: 'industry', 'gender')
st.write("데이터 컬럼명:", df.columns)  # 컬럼명 확인용

# 여기서 컬럼명을 실제 파일에 맞게 지정하세요.
# 예시로 industry, gender로 가정
df_long = df.melt(
    id_vars=['industry', 'gender'],  # 실제 컬럼명 확인 후 수정
    var_name='year',
    value_name='deaths'
)

df_long['year'] = df_long['year'].astype(int)
df_long['deaths'] = pd.to_numeric(df_long['deaths'], errors='coerce')

industries = df_long['industry'].unique()
genders = df_long['gender'].unique()

selected_industry = st.selectbox("Select Industry", industries)
selected_gender = st.selectbox("Select Gender", genders)

filtered = df_long[
    (df_long['industry'] == selected_industry) &
    (df_long['gender'] == selected_gender)
]

st.subheader(f"📈 Trend: {selected_industry} - {selected_gender}")

sns.set(style="whitegrid")
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='year', y='deaths', marker='o', ax=ax)
ax.set_title(f"{selected_industry} - {selected_gender} Deaths")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Deaths")

st.pyplot(fig)
