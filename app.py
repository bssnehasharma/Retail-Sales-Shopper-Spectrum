import streamlit as st
import pandas as pd
import numpy as np # <- add this line
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Cleaner + EDA", layout="wide")
st.title("📊 Quick Data Cleaner & EDA App")

uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(df.head())

    # 2. Cleaning options
    st.sidebar.header("Cleaning Options")
    if st.sidebar.checkbox("Drop Duplicates"):
        df = df.drop_duplicates()
    if st.sidebar.checkbox("Fill Missing Values"):
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("Unknown")
                
    st.subheader("Cleaned Data")
    st.write(f"Shape: {df.shape}")
    st.dataframe(df.head())

    # 3. EDA Section
    st.subheader("EDA")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Summary Stats**")
        st.dataframe(df.describe())

    with col2:
        st.write("**Missing Values**")
        st.dataframe(df.isnull().sum())

    # 4. Plots
    st.subheader("Visualizations")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    plot_type = st.selectbox("Choose Plot", ["Histogram", "Correlation Heatmap", "Bar Plot"])

    if plot_type == "Histogram":
        col = st.selectbox("Select Numeric Column", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        st.pyplot(fig)

    elif plot_type == "Correlation Heatmap":
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    elif plot_type == "Bar Plot" and cat_cols:
        col = st.selectbox("Select Categorical Column", cat_cols)
        fig, ax = plt.subplots()
        df[col].value_counts()[:10].plot(kind='bar', ax=ax)
        st.pyplot(fig)

    # 5. Download cleaned data
    st.download_button(
        "Download Cleaned CSV",
        df.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv")
