import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📌 영어만 사용 – 폰트 문제 없음
@st.cache_data
def load_data():
    return pd.read_csv("사망재해_현황_및_분석성별_20250602121409.csv", encoding="cp949")

df = load_data()

st.title("📈 Deaths by Industry and Gender Over Years")

# Wide -> Long format
df_long = df.melt(id_vars=['산업중분류별(1)', '성별(1)'], 
                  var_name='Year', 
                  value_name='Deaths')

# Change column names to English for chart titles
df_long.rename(columns={
    '산업중분류별(1)': 'Industry',
    '성별(1)': 'Gender'
}, inplace=True)

df_long['Year'] = df_long['Year'].astype(int)

# User selection
industries = df_long['Industry'].unique()
genders = df_long['Gender'].unique()

selected_industry = st.selectbox("Select an industry", industries)
selected_gender = st.selectbox("Select a gender", genders)

filtered = df_long[
    (df_long['Industry'] == selected_industry) &
    (df_long['Gender'] == selected_gender)
]

# Plot
fig, ax = plt.subplots()
sns.lineplot(data=filtered, x='Year', y='Deaths', marker='o', ax=ax)
ax.set_title(f"{selected_industry} - {selected_gender} Death Trend")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Deaths")

st.pyplot(fig)
