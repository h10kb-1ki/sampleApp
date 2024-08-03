import streamlit as st
import pandas as pd
import altair as alt

# ファイルの読み込み
df = pd.read_csv('newly_confirmed_cases_per_100_thousand_population_daily.csv')
# データフレームの整形
df['Date'] = pd.to_datetime(df['Date'])
df = df[['Date', 'Hokkaido', 'Tokyo', 'Osaka', 'Okinawa']]
df.rename(columns={'Date': '年月日', 
                   'Hokkaido': '北海道', 
                   'Tokyo': '東京', 
                   'Osaka': '大阪', 
                   'Okinawa': '沖縄'}, 
          inplace=True
          )
# Altair用にmelt
df_melt = pd.melt(df, id_vars='年月日', var_name='都道府県', value_name='陽性者数')

# 表示する都道府県を選択
options = df_melt['都道府県'].unique().tolist()
prefs = st.multiselect('都道府県を選択', options)

btn = st.button('表示')
if btn:
    df_q = df_melt.query('都道府県 in @prefs')
    chart = alt.Chart(df_q).mark_area().encode(
                    x="年月日:T",
                    y="陽性者数:Q",
                    color="都道府県:N",
                    row=alt.Row("都道府県:N"),
                ).properties(height=200, width=400
            )
    st.altair_chart(chart)
    # 表示用にdfを加工（選択された都道府県のみに）
    df.set_index('年月日', inplace=True)
    df_select = df[prefs]
    st.dataframe(df_select.style.highlight_max(axis=0), 
                 width=150*len(options), height=300)