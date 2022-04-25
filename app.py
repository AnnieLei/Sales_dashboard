# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:47:25 2022

@author: Doudou
https://www.youtube.com/watch?v=Sb0A9i6d320&t=466s
https://github.com/Sven-Bo/streamlit-sales-dashboard
"""

import pandas as pd
import plotly.express as px
import streamlit as st

#emojis:https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title=('Sales Dashboard'),
                   page_icon=':bar_chart:',
                   layout='wide'
)

@st.cache
def get_data_from_excle():
    #df=pd.read_excel('supermarkt_sales1.xlsx',header=0,sheet_name='Sales')
    df=pd.read_csv('sales.csv')
    df["hour"]=df["Time"].str.split(":")
    df["hour"]=df["Time"].str.split(":", expand=True)

    #df["hour"]=pd.to_datetime(df["Time"],format="%H:%M:").dt.hour
    return df

df=get_data_from_excle()


#----SIDEBAR---
st.sidebar.header("Please Filter here:")
city=st.sidebar.multiselect(
    "Select the City",
    options=df["City"].unique(),
    default=(df["City"].unique())
    )

customer_type=st.sidebar.multiselect(
    "Select the Customer Type",
    options=df["Customer_type"].unique(),
    default=(df["Customer_type"].unique())
    )

gender=st.sidebar.multiselect(
    "Select the Gender",
    options=df["Gender"].unique(),
    default=(df["Gender"].unique())
    )

df_selection=df.query(
    "City==@city & Customer_type==@customer_type & Gender==@gender")


#----MAINPAGE-------
#st.title(":bar_chart:Sales Dashboard")
#st.markdown("##")


new_title = '<p style="font-family:Cooper Black; color:#FF9633; font-size: 30px;">Sales Dashboard</p>'
st.markdown(new_title, unsafe_allow_html=True)

#TOP KPI's
total_sales=int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),1)
star_rating=":star:"*int(round(average_rating,0))
average_sale_by_transaction=round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column=st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")
    
st.markdown("---")


#SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line=(
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    )

fig_product_sales=px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line </b>",
    color_discrete_sequence=["#008388"]*len(sales_by_product_line),
    template="plotly_white",
    )

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
    )

#st.plotly_chart(fig_product_sales)


#Sales by hour(Bar chart)
sales_by_hour=(
    df_selection.groupby(by=["hour"]).sum()[["Total"]]
    )
df_selection.info()
fig_hourly_sales=px.bar(
    sales_by_hour,
    y="Total",
    x=sales_by_hour.index,
    title="<b>Sales by hour </b>",
    color_discrete_sequence=["#008388"]*len(sales_by_hour),
    template="plotly_white",
    )
fig_hourly_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(tickmode="linear")),
    yaxis=(dict(showgrid=False)),
    )

#st.plotly_chart(fig_hourly_sales)

left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales,use_container_width=True)


#-----HIDE STREAMILIT STYLE ---
hide_st_style="""
             <style>
             #MainMenu {visibility:hidden;}
             footer {visibility:hidden;}
             header  {visibility:hidden;}
             </style>
             """

st.markdown(hide_st_style, unsafe_allow_html=True)

dfdsc=df_selection.describe()
st.markdown(""" <style> .font {
font-size:30px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Give me a glance</p>', unsafe_allow_html=True)


st.dataframe(dfdsc)

#https://python.plainenglish.io/three-tips-to-improve-your-streamlit-app-a4c94b4d2b30
st.markdown(""" <style> .font {
font-size:30px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Wonder what the data looks like?</p>', unsafe_allow_html=True)


st.dataframe(df_selection)

def convert_df(dfx):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return dfx.to_csv().encode('utf-8')

csv = convert_df(df_selection)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='salesx.csv',
     mime='text/csv',
 )

