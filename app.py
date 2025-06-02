import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (mac/linux 환경에 따라 다를 수 있음)
import matplotlib
matplotlib.rcParams['font.family'] = 'NanumGothic'  # or 'Malgun Gothic' (Windows)

# CSV 불러오기 (인코딩 문제 해결)
@st.cache_data
def load_data():
    return pd.read_csv("사망재해_현황_및_분석성별_20250602121409.csv", encoding='cp949')

# 데이터 로딩
df = load_data()

st.title("📈 사망재해 연도별 추이 분석")

# 데이터 확인
st.subheader("🔍 원본 데이터 미리보기")
st.dataframe(df)

# 라인 그래프 - 연도별 사망자 수
if '연도' in df.columns and '사망자수' in df.columns:
    st.subheader("🧩 연도별 사망자 수 변화")

    # 연도별 사망자 수 합계
    df_grouped = df.groupby('연도')['사망자수'].sum().reset_index()

    # 그래프 그리기
    fig, ax = plt.subplots()
    sns.lineplot(data=df_grouped, x='연도', y='사망자수', marker='o', ax=ax)
    ax.set_title("연도별 사망자 수 추이")
    ax.set_xlabel("연도")
    ax.set_ylabel("사망자 수")
    st.pyplot(fig)
else:
    st.warning("⚠️ '연도' 또는 '사망자수' 컬럼이 존재하지 않습니다.")
