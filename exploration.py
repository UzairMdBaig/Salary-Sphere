import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("survey_results_public.csv")

def shorten_Categories(Series,cutoff):
    new_column_names = {}
    for i in range(len(Series)):
        if Series.values[i] >= cutoff:
            new_column_names[Series.index[i]] = Series.index[i]
        else:
            new_column_names[Series.index[i]] = 'Others'
    return new_column_names

def degree_type(x):
    if x == 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)':
        return 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)'
    elif x == 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':
        return 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)'
    elif x == 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':
        return 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)'
    else:
        return "Less than Batchelor's degree"
    
def years_convert(x):
    if x == 'Less than 1 year':
        return 0.5
    elif x == 'More than 50 years':
        return 50
    else:
        return float(x)
    
def data_transform(df):
    df = df.rename({'ConvertedCompYearly':'Salary'},axis=1)
    df = df[df['Employment'] == 'Employed, full-time']
    df = df[['Country','DevType','EdLevel','RemoteWork','YearsCodePro','Salary']]
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['DevType'] != 'Student']
    df = df[df['DevType'] != 'Marketing or sales professional']
    df = df[df['DevType'] != 'Senior Executive (C-Suite, VP, etc.)']
    df = df[df['DevType'] != 'Scientist']
    df = df[df['DevType'] != 'Hardware Engineer']
    df = df[df['DevType'] != 'Product manager']
    df = df[df['DevType'] != 'Academic researcher']
    df = df[df['DevType'] != 'Other (please specify):']
    df = df[df['DevType'] != 'Educator']
    df = df[df['DevType'] != 'Developer Experience']
    df = df[df['DevType'] != 'Project manager']
    df = df[df['DevType'] != 'Research & Development role']
    country_names = shorten_Categories(df['Country'].value_counts(),415)
    df['Country'] = df['Country'].map(country_names)
    df['Country'].value_counts()
    df['EdLevel'] = df['EdLevel'].apply(degree_type)
    df['YearsCodePro'] = df['YearsCodePro'].apply(years_convert)
    devtype_names = shorten_Categories(df['DevType'].value_counts(),375)
    df['DevType'] = df['DevType'].map(devtype_names)
    df = df[df['Country'] != 'Others']
    df = df[df['DevType'] != 'Others']
    return df

df = data_transform(df)

def show_exploration_page():
    st.title("Data Exploration")
    st.write("#### Based on Stackoverflow 2023 survey")
    st.write("##")
    st.write("##### Distribution of Survey Participants by Country ")
   
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=95)
    ax1.axis("equal")

    st.pyplot(fig1)

    st.write("---")

    us_data = df[df["Country"]=="United States of America"]
    india_data = df[df["Country"]=="India"]

    us_data = us_data.groupby("DevType")["Salary"].mean()
    india_data = india_data.groupby("DevType")["Salary"].mean()


    st.write("##### Mean salary as per devtype (US vs India) ")
    col1, col2 = st.columns(2)
    with col1:
        st.write("##### US ")
        st.bar_chart(us_data)
    with col2:
        st.write("##### India ")
        st.bar_chart(india_data)

    st.write("---")
    
    data = df.groupby("YearsCodePro")["Salary"].mean()
    st.write("##### Mean salary on progression of experience")
    st.line_chart(data)



    







