import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file (cp949 encoding for Korean)
@st.cache_data
def load_data():
    df = pd.read_csv("사망재해 성별 분석.csv", encoding="cp949")
    return df

# Load data
df = load_data()

st.title("📊 Deaths by Industry and Gender")

# Rename columns for consistency and English readability
df.columns = ['Industry', 'Gender', '2021', '2022', '2023']

# Convert to long format
df_long = df.melt(
    id_vars=['Industry', 'Gender'], 
    var_name='Year', 
    value_name='Deaths'
)

# Convert year to integer
df_long['Year'] = df_long['Year'].astype(int)

# Selection widgets
industries = df_long['Industry'].unique()
genders = df_long['Gender'].unique()

selected_industry = st.selectbox("Select Industry:", industries)
selected_gender = st.selectbox("Select Gender:", genders)

# Filter data
filtered_data = df_long[
    (df_long['Industry'] == selected_industry) &
    (df_long['Gender'] == selected_gender)
]

# Visualization
st.subheader(f"📈 Deaths Over Time: {selected_industry} - {selected_gender}")
sns.set(style="whitegrid")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='Year', y='Deaths', marker='o', ax=ax)
ax.set_title(f"Death Trend: {selected_industry} - {selected_gender}")
ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("Number of Deaths", fontsize=10)
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)

st.pyplot(fig)

# Option to view data table
if st.checkbox("Show Data Table"):
    st.dataframe(filtered_data.reset_index(drop=True))
