import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (matplotlib 한글 깨짐 방지)
import matplotlib
matplotlib.rcParams['font.family'] = 'NanumGothic'

st.set_page_config(page_title="사망재해 분석 대시보드", layout="wide")

# 제목
st.title("📊 사망재해 현황 및 분석 대시보드")

# 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("사망재해_현황_및_분석성별_20250602121409.csv", encoding='utf-8')
    return df

df = load_data()

# 데이터 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 필터 설정
st.sidebar.header("🔍 필터")
if '성별' in df.columns:
    gender_options = st.sidebar.multiselect("성별 선택", options=df['성별'].unique(), default=df['성별'].unique())
    df = df[df['성별'].isin(gender_options)]

# 예시 시각화: 연도별 사망자 수 추이
if '연도' in df.columns and '사망자수' in df.columns:
    st.subheader("📈 연도별 사망자 수 추이")
    year_data = df.groupby('연도')['사망자수'].sum().reset_index()

    fig, ax = plt.subplots()
    sns.lineplot(data=year_data, x='연도', y='사망자수', marker='o', ax=ax)
    ax.set_title("연도별 사망자 수")
    st.pyplot(fig)
