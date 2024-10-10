import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='12345678',database = "github")

st.title("GITHUB DATA DRIVE")
query = """ Select * from github; """
df = pd.read_sql_query(query,myconnection)
col_name = "star_count"
tab1, tab2 = st.tabs(["HOME", "VISUALIZATION"])


with tab1:
    st.write("## About the Project")
    st.write("A project that revolutionizes GITHUB analysis through the ingenious fusion of GITHUB API, and MySQL. \nImmerse yourself in the data exploration experience through an interactive and intuitive Streamlit dashboard.\nEffortlessly input Repositories, fetch dynamic repository data, and perform seamless data migration operations all in one place. \nThis project serves as a testament to my expertise in API utilization, database management, data migration, and crafting intuitive dashboards.")
    st.write("Developed by: Mohamed Ismayil")

with tab2:
    st.write("## Data VISUALIZATION")

    st.write("Here is the data visualization of the Github Repositories")

    st.write("## Repository Name")
    top_languages = df["pro_language"].value_counts().nlargest(10)
    fig = px.bar(
        x=top_languages.index,
        y=top_languages.values,
        labels={'x': 'Programming Language', 'y': 'Total Count'},
        title='Top 10 Programming Languages',
        color=top_languages.index, 
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        width=800,
        height=500
    )
    st.plotly_chart(fig)

    df['creation_date'] = df['creation_date'].dt.year

    creation_trend = df['creation_date'].value_counts().sort_index()

    fig = px.line(
        x=creation_trend.index,
        y=creation_trend.values,
        labels={'x': 'Year', 'y': 'Number of Repositories Created'},
        title='Number of Repositories Created Per Year',
        markers=True 
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        width=800,
        height=500
    )

    st.plotly_chart(fig)

    repos_per_topic = df.groupby(['creation_date', 'topic']).size().reset_index(name='Count')

    fig = px.line(
        repos_per_topic,
        x='creation_date',
        y='Count',
        color='topic',
        labels={'Creation Year': 'Year', 'Count': 'Number of Repositories Created'},
        title='Number of Repositories Created Per Topic Over Years',
        markers=True )

    fig.update_layout(
        width=800,
        height=500,
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig)


    metric = st.selectbox(
        "Select Metric to Display",
        options=["Star Count", "Fork Count", "Issue Count"]
        )

    if metric == "Star Count":
        col_name = "star_count"
    elif metric == "Fork Count":
        col_name = "fork_count"
    elif metric == "Issue Count":
        col_name = "issue_count"

    popular_languages_by_option = df.groupby('pro_language')[col_name].sum().sort_values(ascending=False).head(10)

    fig = px.bar(
        x=popular_languages_by_option.index,
        y=popular_languages_by_option.values,
        labels={'x': 'Programming Language', 'y': f'Total {metric}'},
        title=f"Top 10 Programming Languages by {metric}",
        color=popular_languages_by_option.index,
        color_discrete_sequence=px.colors.sequential.Plasma 
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        width=800,
        height=500
    )
    st.plotly_chart(fig)

    topic = df.groupby('topic')[col_name].sum().sort_values(ascending=False).head(10)


    fig = px.bar(
        x=topic.index,
        y=topic.values,
        labels={'x': 'Topic', 'y': metric},
        title=f'Top 10 Topics by {metric}',
        color=topic.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        width=800,
        height=500
    )

    st.plotly_chart(fig)

    top_starred_repos = df.nlargest(5, col_name)

    top_starred_repos = top_starred_repos.sort_values(by=col_name)

    fig = px.bar(
        top_starred_repos,
        x= col_name,
        y='r_name',
        color=col_name,
        labels={col_name: metric , 'r_name': 'Repository'},
        title=f'Top 5 Repositories with most {metric}',
        orientation='h'
    )

    fig.update_layout(
        width=800,
        height=500
    )

    st.plotly_chart(fig)