import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
import openpyxl
from openpyxl import load_workbook, Workbook
import seaborn 
import matplotlib.pyplot as plt

st.set_page_config(page_title="Assignment", page_icon=":bar_chart:",layout="wide")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

years = [18, 19, 20, 21, 22, 23]


fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)

    # Check file extension to use appropriate read function
    if filename.endswith('.csv') or filename.endswith('.txt'):
        df = pd.read_csv(fl, encoding="ISO-8859-1", skiprows=6)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        xls = pd.ExcelFile(fl)
        sheet_names = xls.sheet_names
       
        df = pd.read_excel(fl, sheet_name=sheet_names[2], skiprows=6)
        st.write(df)

    col1, col2 = st.columns((2))

    st.subheader("Time Series Analysis")
    selected_year = st.selectbox("Select year", years)
    st.write("Transaction Value (USD$ Millions) for the year 20", selected_year)
    
    category_df = df.groupby(by = ["Categories"], as_index=False)["Transaction Value (USD$ Millions)"].sum()

    

    with col1:
        st.subheader("Category wise Transaction Value")
        fig = px.bar(category_df, x="Categories", y="Transaction Value (USD$ Millions)", color="Categories", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Category wise Transaction Value")
        fig = px.pie(category_df, values="Transaction Value (USD$ Millions)", names="Categories", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    tech_df = df.groupby(by = ["Tech"], as_index=False)["Transaction Value (USD$ Millions)"].sum()
    with col1:
        st.subheader("Tech wise Transaction Value")
        fig = px.bar(tech_df, x="Tech", y="Transaction Value (USD$ Millions)", color="Tech", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Tech wise Transaction Value")
        fig = px.pie(tech_df, values="Transaction Value (USD$ Millions)", names="Tech", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    region_df = df.groupby(by = ["Region"], as_index=False)["Transaction Value (USD$ Millions)"].sum()
    with col1:
        st.subheader("Region wise Transaction Value")
        fig = px.bar(region_df, x="Region", y="Transaction Value (USD$ Millions)", color="Region", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Region wise Transaction Value")
        fig = px.pie(region_df, values="Transaction Value (USD$ Millions)", names="Region", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    firm_type_df = df.groupby(by = ["Firm Type"], as_index=False)["Transaction Value (USD$ Millions)"].sum()    
    with col1:
        st.subheader("Firm Type wise Transaction Value")
        fig = px.bar(firm_type_df, x="Firm Type", y="Transaction Value (USD$ Millions)", color="Firm Type", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Firm Type wise Transaction Value")
        fig = px.pie(firm_type_df, values="Transaction Value (USD$ Millions)", names="Firm Type", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)


    year_df = df.groupby(df['Date'].dt.year, as_index=False)["Transaction Value (USD$ Millions)"].sum()
    with col1:
        st.subheader("Year wise Transaction Value")
        df['Date'] = pd.to_datetime(df['Date'])

        # Group data by Year
        df['Year'] = df['Date'].dt.year
        year_df = df.groupby('Year', as_index=False)["Transaction Value (USD$ Millions)"].sum()
        fig_bar = px.bar(year_df, x="Year", y="Transaction Value (USD$ Millions)",color="Year", template="seaborn")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Year wise Transaction Value")
        fig = px.pie(year_df, values="Transaction Value (USD$ Millions)", names="Year", template="seaborn")
        st.plotly_chart(fig, use_container_width=True)


    

    # Filter data for the selected year
    df_time_series = df[df["Date"].dt.strftime('%y') == str(selected_year)]

    # Group data by month in chronological order
    df_time_series['Month'] = pd.Categorical(df_time_series['Date'].dt.strftime('%b'), categories=months, ordered=True)
    time_series_df = df_time_series.groupby(by="Month", as_index=False)["Transaction Value (USD$ Millions)"].sum()

    # Plot the line graph
    fig_line = px.line(time_series_df, x="Month", y="Transaction Value (USD$ Millions)", markers=True, template="seaborn")
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("Category wise Transaction Value for the year 20", selected_year)
    categories = st.multiselect("Select Category", df["Categories"].unique())
    if categories:
        df_time_series = df_time_series[df_time_series["Categories"].isin(categories)]
    # Group data by month in chronological order
    df_time_series['Month'] = pd.Categorical(df_time_series['Date'].dt.strftime('%b'), categories=months, ordered=True)
    time_series_df = df_time_series.groupby(by=["Categories", "Month"], as_index=False)["Transaction Value (USD$ Millions)"].sum()

    # Plot the line graph
    fig_line = px.line(time_series_df, x="Month", y="Transaction Value (USD$ Millions)", color="Categories", markers=True, template="seaborn")
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("Tech wise Transaction Value for the year 20", selected_year)
    tech = st.multiselect("Select Tech", df["Tech"].unique())
    if tech:
        df_time_series = df_time_series[df_time_series["Tech"].isin(tech)]
    # Group data by month in chronological order
    df_time_series['Month'] = pd.Categorical(df_time_series['Date'].dt.strftime('%b'), categories=months, ordered=True)
    time_series_df = df_time_series.groupby(by=["Tech", "Month"], as_index=False)["Transaction Value (USD$ Millions)"].sum()

    # Plot the line graph
    fig_line = px.line(time_series_df, x="Month", y="Transaction Value (USD$ Millions)", color="Tech", markers=True, template="seaborn")
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("Region wise Transaction Value for the year 20", selected_year)
    regions = st.multiselect("Select region", df["Region"].unique())
    if regions:
        df_time_series = df_time_series[df_time_series["Region"].isin(regions)]
    # Group data by month in chronological order
    df_time_series['Month'] = pd.Categorical(df_time_series['Date'].dt.strftime('%b'), categories=months, ordered=True)
    time_series_df = df_time_series.groupby(by=["Region", "Month"], as_index=False)["Transaction Value (USD$ Millions)"].sum()

    # Plot the line graph
    fig_line = px.line(time_series_df, x="Month", y="Transaction Value (USD$ Millions)", color="Region", markers=True, template="seaborn")
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("Firm Type wise Transaction Value for the year 20", selected_year)
    firm_type = st.multiselect("Select Firm type", df["Firm Type"].unique())
    if firm_type:
        df_time_series = df_time_series[df_time_series["Firm Type"].isin(firm_type)]
    # Group data by month in chronological order
    df_time_series['Month'] = pd.Categorical(df_time_series['Date'].dt.strftime('%b'), categories=months, ordered=True)
    time_series_df = df_time_series.groupby(by=["Firm Type", "Month"], as_index=False)["Transaction Value (USD$ Millions)"].sum()

    # Plot the line graph
    fig_line = px.line(time_series_df, x="Month", y="Transaction Value (USD$ Millions)", color="Firm Type", markers=True, template="seaborn")
    st.plotly_chart(fig_line, use_container_width=True)


    #hierarchical clustering
    st.subheader("Hierarchical view of Transaction Value")
    fig3 = px.treemap(df, path=['Tech', 'Categories', 'Region'], values='Transaction Value (USD$ Millions)', color='Transaction Value (USD$ Millions)', hover_data=['Transaction Value (USD$ Millions)'])
    fig3.update_layout(width=1000, height=800)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Month wise Transaction Value for the categories")
    df_time_series['Month'] = pd.Categorical(df_time_series['Date'].dt.strftime('%b'), categories=months, ordered=True)
    time_series_df = df_time_series.groupby(by=["Categories", "Month"], as_index=False)["Transaction Value (USD$ Millions)"].sum()
    sub_category = pd.pivot_table(time_series_df, index='Categories', columns='Month', values='Transaction Value (USD$ Millions)', aggfunc='sum')
    st.write(sub_category.style.background_gradient(cmap='Blues'))

    data = {
    'Date': ['Aug-22', 'Sep-22', 'Oct-22', 'Nov-22', 'Dec-22', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'May-23', 'Jun-23', 'Jul-23', 'Aug-23'],
    'Allocations into': [125, 5727, 32240, 89686, 5088, 12691, 1764, 12772, 860, 2463, 8983, 9450, 10964],
    'Investments from': [2054, 3775, 8972, 22890, 10705, 16650, 5871, 9779, 3823, 3606, 9905, 5090, 7020]
    }
    
    st.subheader('Private Capital Energy Transition Funds Analysis')
    private_df = pd.DataFrame(data)
    df_melted = private_df.melt(id_vars='Date', value_vars=['Allocations into', 'Investments from'], var_name='Type', value_name='Value')
    fig = px.bar(df_melted, x='Date', y='Value', color='Type', barmode='group', 
             title='Private Capital Energy Transition Funds (USD mns)',
             category_orders={"Date": data['Date']})
    st.plotly_chart(fig, use_container_width=True, width=1000, height=600)

    data = {
    'Month': ['Aug-22', 'Sep-22', 'Oct-22', 'Nov-22', 'Dec-22', 'Jan-23', 'Feb-23', 
              'Mar-23', 'Apr-23', 'May-23', 'Jun-23', 'Jul-23', 'Aug-23'],
    'Private Capital': [125, 5727, 32240, 89686, 5088, 12691, 1764, 
                        12772, 860, 2463, 8983, 9450, 10964],
    'Energy Transition Funds': [2054, 3775, 8972, 22890, 10705, 16650, 5871, 
                                9779, 3823, 3606, 9905, 5090, 7020]
    }
    pripie_df = pd.DataFrame(data)

    
    fig_private = px.pie(values=pripie_df['Private Capital'], names=pripie_df['Month'],
                     title='Allocations into Private Capital',
                     template='seaborn')
    st.plotly_chart(fig_private, use_container_width=True)

    fig_energy = px.pie(values=pripie_df['Energy Transition Funds'], names=pripie_df['Month'],
                    title='Investments into Energy Transition Funds',
                    template='seaborn')
    st.plotly_chart(fig_energy, use_container_width=True)

    pripie_df['Cumulative Private Capital'] = pripie_df['Private Capital'].cumsum()
    pripie_df['Cumulative Energy Transition Funds'] = pripie_df['Energy Transition Funds'].cumsum()

    fig_progress = px.bar(pripie_df, x='Month', y=['Cumulative Private Capital', 'Cumulative Energy Transition Funds'],
                        title='Cumulative Allocations Progress',
                        labels={'value': 'Allocations', 'variable': 'Type', 'Month': 'Month'},
                        template='seaborn')

    st.plotly_chart(fig_progress, use_container_width=True)

    
