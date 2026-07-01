import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Retail EDA", layout="wide")
st.title("📊 Online Retail EDA Dashboard")

@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    data = {
        'invoiceno': np.random.choice(range(50000, 60000), 5000),
        'description': np.random.choice([
            'WHITE HANGING HEART T-LIGHT HOLDER', 'REGENCY CAKESTAND 3 TIER',
            'JUMBO BAG RED RETROSPOT', 'PARTY BUNTING', 'LUNCH BAG RED RETROSPOT',
            'ASSORTED COLOUR BIRD ORNAMENT', 'POPPY\'S PLAYHOUSE BEDROOM',
            'POPPY\'S PLAYHOUSE KITCHEN', 'FELTCRAFT PRINCESS CHARLOTTE DOLL',
            'IVORY KNITTED MUG COSY'], 5000),
        'quantity': np.random.randint(1, 50, 5000),
        'invoicedate': np.random.choice(dates, 5000),
        'unitprice': np.round(np.random.uniform(0.5, 50, 5000), 2),
        'customerid': np.random.choice(range(12000, 15000), 5000),
        'country': np.random.choice(['United Kingdom', 'Germany', 'France', 'Spain', 
                                     'Netherlands', 'Australia', 'USA'], 5000, 
                                    p=[0.7, 0.08, 0.06, 0.05, 0.04, 0.04, 0.03])
    }
    df = pd.DataFrame(data)
    df['totalprice'] = df['quantity'] * df['unitprice']
    df['month'] = df['invoicedate'].dt.to_period('M').astype(str)
    df['date'] = df['invoicedate'].dt.date
    return df

df = load_data()

# --- KPIs ---
st.subheader("Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${df['totalprice'].sum():,.0f}")
c2.metric("Total Orders", f"{df['invoiceno'].nunique():,}")
c3.metric("Total Customers", f"{df['customerid'].nunique():,}")
c4.metric("Avg Order Value", f"${df['totalprice'].sum()/df['invoiceno'].nunique():.2f}")

st.markdown("---")

# --- Dashboard Tabs ---
t1, t2, t3, t4 = st.tabs(["📈 Sales Trend", "🏆 Top Products", "🌍 Country Analysis", "📋 Data Overview"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monthly Revenue")
        monthly = df.groupby('month')['totalprice'].sum().reset_index()
        fig = px.line(monthly, x='month', y='totalprice', markers=True)
        fig.update_layout(xaxis_tickangle=-45, yaxis_title='Revenue ($)', xaxis_title='Month')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Daily Orders")
        daily = df.groupby('date')['invoiceno'].nunique().reset_index()
        fig2 = px.bar(daily, x='date', y='invoiceno')
        fig2.update_layout(yaxis_title='Order Count', xaxis_title='Date')
        st.plotly_chart(fig2, use_container_width=True)

with t2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Products by Revenue")
        top_rev = df.groupby('description')['totalprice'].sum().nlargest(10).reset_index()
        fig = px.bar(top_rev, x='totalprice', y='description', orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title='Revenue ($)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Products by Quantity")
        top_qty = df.groupby('description')['quantity'].sum().nlargest(10).reset_index()
        fig = px.bar(top_qty, x='quantity', y='description', orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

with t3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 7 Countries by Revenue")
        country_rev = df.groupby('country')['totalprice'].sum().nlargest(7).reset_index()
        fig = px.bar(country_rev, x='country', y='totalprice')
        fig.update_layout(xaxis_tickangle=-45, yaxis_title='Revenue ($)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Customer Distribution")
        country_cust = df.groupby('country')['customerid'].nunique().nlargest(7).reset_index()
        fig2 = px.pie(country_cust, values='customerid', names='country', hole=0.3)
        st.plotly_chart(fig2, use_container_width=True)

with t4:
    st.subheader("Data Preview - First 50 Rows")
    st.dataframe(df.head(50), use_container_width=True)
    
    st.subheader("Summary Statistics")
    st.write(df[['quantity','unitprice','totalprice']].describe())
