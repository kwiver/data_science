# import libraries
import pandas as pd
import plotly.express as px
import streamlit as st

def streamlit_app():
    # page config
    st.set_page_config(
        page_title="Bank Churn Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    #load datast

    df = pd.read_csv("cleaned_bank_cusomer_churn.csv")
    
    # header
    st.title("📉 Business Churn Customer")
    st.caption("A stragetic overview churn pattern customer segment, demographics and finance")
    st.markdown("---")
    
    # sidebar filter
    st.sidebar.header("Dashboard Filters")
    
    geo_filter = st.sidebar.multiselect(
        label="Geography",
        options=df["Geography"].unique(),
        default=df["Geography"].unique()
    )
    
    gender_filter = st.sidebar.multiselect(
        label="Gender",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    
    # apply filter
    filtered_df = df[
        (df["Geography"].isin(geo_filter)) &
        (df["Gender"].isin(gender_filter))
    ]
    # kpi summary
    total_count = len(filtered_df)
    churn_customer = filtered_df["Exited"].sum()
    churn_rate = round(churn_customer / total_count * 100, 2)
    
    avg_credit_score = round(filtered_df["CreditScore"].mean(), 1)
    avg_salary = round(filtered_df["EstimatedSalary"].mean(), 1)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Customer", total_count)
    col2.metric("Churn Customer", churn_customer)
    col3.metric("Churn Rate", f"{churn_rate}%")
    col4.metric("Avg Credit Score", avg_credit_score)
    col5.metric("Avg Estimated Salary", f"${avg_salary:,.0f}")
    
    # row 1 - Geography & Gender
    left, right = st.columns(2)
    with left:
        st.subheader("Customer Churn Distribtion by Geography")
        fig_geo = px.histogram(
            filtered_df,
            x="Geography",
            color="Exited",
            barmode="group",
            title="Churn rate accross countries"
        )
    
        st.plotly_chart(fig_geo, use_container_width=True)

    with right:
        st.subheader("Customer Churn Distribtion by Gender")
        fig_gender = px.histogram(
            filtered_df,
            x="Gender",
            color="Exited",
            barmode="group",
            title="Churn rate by Gender"
        )
    
        st.plotly_chart(fig_gender, use_container_width=True)
        
    
    # row 2 - Age and Credit score
    left, right = st.columns(2)
    with left:
        st.subheader("Age: Customer churn vs Non-Churn")
        fig_age = px.box(
            filtered_df,
            x="Exited",
            y="Age",
            color="Exited",
            points="all",
            title="Age Distributin by Churn"
        )
    
        st.plotly_chart(fig_age, use_container_width=True)

    with right:
        st.subheader("Customer Churn Distribtion by CreditScore")
        fig_credit_score = px.histogram(
            filtered_df,
            x="CreditScore",
            color="Exited",
            title="Churn rate by Credit Score"
        )
    
        st.plotly_chart(fig_credit_score, use_container_width=True)

    # row 3 - NumberOfProduct and Tenure
    left, right = st.columns(2)
    with left:
        st.subheader("Number of Products: Customer churn vs Non-Churn")
        fig_product = px.histogram(
            filtered_df,
            x="NumOfProducts",
            barmode="group",
            color="Exited",
            title="How Products Influence churn"
        )
    
        st.plotly_chart(fig_product, use_container_width=True)

    with right:
        st.subheader("Tenure: Customer loyalty Indicator")
        fig_tenure = px.histogram(
            filtered_df,
            x="Tenure",
            color="Exited",
            title="Tenure Comparison Between churn & Active customer"
        )
    
        st.plotly_chart(fig_tenure, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head(20))

streamlit_app()