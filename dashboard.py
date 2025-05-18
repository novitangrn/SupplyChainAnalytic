import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e8df5;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📊 Supply Chain Analytics Dashboard")
st.markdown("Visualisasi data supply chain untuk melihat tren penjualan, profitabilitas, dan performa pengiriman.")

# Function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('incom2024_delay_example_dataset.csv')
        
        # Convert date columns to datetime
        date_columns = ['order_date', 'shipping_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data()

# Check if data is loaded
if df is None:
    st.error("Tidak dapat memuat data. Silakan periksa file data Anda.")
    st.stop()

# Sidebar for filters
st.sidebar.header("Filter Data")

# Date range filter
if 'order_date' in df.columns:
    min_date = df['order_date'].min().date()
    max_date = df['order_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Periode Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[(df['order_date'].dt.date >= start_date) & 
                        (df['order_date'].dt.date <= end_date)]
    else:
        filtered_df = df
else:
    filtered_df = df

# Market filter
if 'market' in df.columns:
    all_markets = ['All'] + sorted(filtered_df['market'].unique().tolist())
    selected_market = st.sidebar.selectbox("Market", all_markets)
    
    if selected_market != 'All':
        filtered_df = filtered_df[filtered_df['market'] == selected_market]

# Region filter
if 'order_region' in df.columns:
    all_regions = ['All'] + sorted(filtered_df['order_region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", all_regions)
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['order_region'] == selected_region]

# Customer segment filter
if 'customer_segment' in df.columns:
    all_segments = ['All'] + sorted(filtered_df['customer_segment'].unique().tolist())
    selected_segment = st.sidebar.selectbox("Customer Segment", all_segments)
    
    if selected_segment != 'All':
        filtered_df = filtered_df[filtered_df['customer_segment'] == selected_segment]

# Product category filter
if 'category_name' in df.columns:
    all_categories = ['All'] + sorted(filtered_df['category_name'].unique().tolist())
    selected_category = st.sidebar.selectbox("Product Category", all_categories)
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category_name'] == selected_category]

# Create tabs for different dashboard sections
tab1, tab2, tab3, tab4 = st.tabs(["Performa Penjualan", "Analisis Pelanggan", "Performa Pengiriman", "Detail Data"])

# Tab 1: Sales Performance
with tab1:
    st.header("Performa Penjualan")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'sales' in df.columns:
            total_sales = filtered_df['sales'].sum()
            st.metric("Total Penjualan", f"${total_sales:,.2f}")
        else:
            st.metric("Total Penjualan", "Data tidak tersedia")
    
    with col2:
        if 'order_profit_per_order' in df.columns:
            total_profit = filtered_df['order_profit_per_order'].sum()
            st.metric("Total Profit", f"${total_profit:,.2f}")
        else:
            st.metric("Total Profit", "Data tidak tersedia")
    
    with col3:
        if 'order_id' in df.columns:
            total_orders = filtered_df['order_id'].nunique()
            st.metric("Jumlah Pesanan", f"{total_orders:,}")
        else:
            st.metric("Jumlah Pesanan", "Data tidak tersedia")
    
    with col4:
        if 'order_item_quantity' in df.columns:
            total_items = filtered_df['order_item_quantity'].sum()
            st.metric("Total Items Terjual", f"{total_items:,}")
        else:
            st.metric("Total Items Terjual", "Data tidak tersedia")
    
    st.subheader("Tren Penjualan")
    
    # Sales trend over time
    if 'order_date' in df.columns and 'sales' in df.columns:
        sales_over_time = filtered_df.groupby(filtered_df['order_date'].dt.date)['sales'].sum().reset_index()
        sales_over_time.columns = ['Date', 'Sales']
        
        fig_sales = px.line(
            sales_over_time, 
            x='Date', 
            y='Sales',
            title='Penjualan Harian',
            labels={'Sales': 'Penjualan ($)', 'Date': 'Tanggal'},
        )
        fig_sales.update_layout(height=400)
        st.plotly_chart(fig_sales, use_container_width=True)
    else:
        st.warning("Data yang diperlukan untuk tren penjualan tidak tersedia.")
    
    # Sales by category and region
    col1, col2 = st.columns(2)
    
    with col1:
        if 'category_name' in df.columns and 'sales' in df.columns:
            sales_by_category = filtered_df.groupby('category_name')['sales'].sum().reset_index()
            sales_by_category = sales_by_category.sort_values('sales', ascending=False)
            
            fig_category = px.bar(
                sales_by_category,
                x='category_name',
                y='sales',
                title='Penjualan berdasarkan Kategori Produk',
                labels={'sales': 'Penjualan ($)', 'category_name': 'Kategori Produk'},
                color='sales',
                color_continuous_scale=px.colors.sequential.Blues,
            )
            fig_category.update_layout(height=400)
            st.plotly_chart(fig_category, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk penjualan berdasarkan kategori tidak tersedia.")
    
    with col2:
        if 'order_region' in df.columns and 'sales' in df.columns:
            sales_by_region = filtered_df.groupby('order_region')['sales'].sum().reset_index()
            sales_by_region = sales_by_region.sort_values('sales', ascending=False).head(10)
            
            fig_region = px.bar(
                sales_by_region,
                x='sales',
                y='order_region',
                title='Top 10 Region berdasarkan Penjualan',
                labels={'sales': 'Penjualan ($)', 'order_region': 'Region'},
                orientation='h',
                color='sales',
                color_continuous_scale=px.colors.sequential.Blues,
            )
            fig_region.update_layout(height=400)
            st.plotly_chart(fig_region, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk penjualan berdasarkan region tidak tersedia.")
    
    # Profit analysis
    st.subheader("Analisis Profitabilitas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'order_profit_per_order' in df.columns and 'order_date' in df.columns:
            profit_over_time = filtered_df.groupby(filtered_df['order_date'].dt.date)['order_profit_per_order'].sum().reset_index()
            profit_over_time.columns = ['Date', 'Profit']
            
            fig_profit = px.line(
                profit_over_time, 
                x='Date', 
                y='Profit',
                title='Tren Profit Harian',
                labels={'Profit': 'Profit ($)', 'Date': 'Tanggal'},
            )
            fig_profit.update_layout(height=400)
            st.plotly_chart(fig_profit, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk tren profit tidak tersedia.")
    
    with col2:
        if 'shipping_mode' in df.columns and 'order_profit_per_order' in df.columns:
            profit_by_shipping = filtered_df.groupby('shipping_mode')['order_profit_per_order'].sum().reset_index()
            profit_by_shipping = profit_by_shipping.sort_values('order_profit_per_order', ascending=False)
            
            fig_shipping_profit = px.pie(
                profit_by_shipping,
                values='order_profit_per_order',
                names='shipping_mode',
                title='Profit berdasarkan Mode Pengiriman',
                hole=0.4,
                labels={'order_profit_per_order': 'Profit ($)', 'shipping_mode': 'Mode Pengiriman'},
            )
            fig_shipping_profit.update_layout(height=400)
            st.plotly_chart(fig_shipping_profit, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk profit berdasarkan mode pengiriman tidak tersedia.")

# Tab 2: Customer Analysis
with tab2:
    st.header("Analisis Pelanggan")
    
    # Customer segmentation
    col1, col2 = st.columns(2)
    
    with col1:
        if 'customer_segment' in df.columns and 'sales' in df.columns:
            sales_by_segment = filtered_df.groupby('customer_segment')['sales'].sum().reset_index()
            
            fig_segment = px.pie(
                sales_by_segment,
                values='sales',
                names='customer_segment',
                title='Penjualan berdasarkan Segmen Pelanggan',
                hole=0.4,
                labels={'sales': 'Penjualan ($)', 'customer_segment': 'Segmen Pelanggan'},
            )
            fig_segment.update_layout(height=400)
            st.plotly_chart(fig_segment, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk analisis segmen pelanggan tidak tersedia.")
    
    with col2:
        if 'sales_per_customer' in df.columns and 'customer_segment' in df.columns:
            avg_sales_by_segment = filtered_df.groupby('customer_segment')['sales_per_customer'].mean().reset_index()
            
            fig_avg_sales = px.bar(
                avg_sales_by_segment,
                x='customer_segment',
                y='sales_per_customer',
                title='Rata-rata Penjualan per Segmen Pelanggan',
                labels={'sales_per_customer': 'Rata-rata Penjualan ($)', 'customer_segment': 'Segmen Pelanggan'},
                color='sales_per_customer',
                color_continuous_scale=px.colors.sequential.Viridis,
            )
            fig_avg_sales.update_layout(height=400)
            st.plotly_chart(fig_avg_sales, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk rata-rata penjualan per segmen tidak tersedia.")
    
    # Geographic analysis
    st.subheader("Analisis Geografis")
    
    if 'customer_country' in df.columns and 'sales' in df.columns:
        sales_by_country = filtered_df.groupby('customer_country')['sales'].sum().reset_index()
        sales_by_country = sales_by_country.sort_values('sales', ascending=False)
        
        fig_country = px.choropleth(
            sales_by_country,
            locations='customer_country',
            locationmode='country names',
            color='sales',
            hover_name='customer_country',
            title='Penjualan berdasarkan Negara',
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig_country.update_layout(height=500)
        st.plotly_chart(fig_country, use_container_width=True)
    else:
        st.warning("Data yang diperlukan untuk analisis geografis tidak tersedia.")
    
    # Top customers
    if 'customer_id' in df.columns and 'sales' in df.columns:
        top_customers = filtered_df.groupby('customer_id')['sales'].sum().reset_index()
        top_customers = top_customers.sort_values('sales', ascending=False).head(10)
        top_customers['customer_id'] = top_customers['customer_id'].astype(str)
        
        fig_top_customers = px.bar(
            top_customers,
            x='customer_id',
            y='sales',
            title='Top 10 Pelanggan berdasarkan Penjualan',
            labels={'sales': 'Penjualan ($)', 'customer_id': 'ID Pelanggan'},
            color='sales',
            color_continuous_scale=px.colors.sequential.Greens,
        )
        fig_top_customers.update_layout(height=400)
        st.plotly_chart(fig_top_customers, use_container_width=True)
    else:
        st.warning("Data yang diperlukan untuk analisis top pelanggan tidak tersedia.")

# Tab 3: Shipping Performance
with tab3:
    st.header("Performa Pengiriman")
    
    # Delivery status analysis
    col1, col2 = st.columns(2)
    
    with col1:
        if 'label' in df.columns:
            # Convert label values to descriptive text
            delivery_status = filtered_df['label'].map({-1: 'Early Arrival', 0: 'On Time', 1: 'Delayed'}).value_counts().reset_index()
            delivery_status.columns = ['Status', 'Count']
            
            fig_delivery = px.pie(
                delivery_status,
                values='Count',
                names='Status',
                title='Status Pengiriman',
                hole=0.4,
                color_discrete_map={'Early Arrival': '#28a745', 'On Time': '#17a2b8', 'Delayed': '#dc3545'},
            )
            fig_delivery.update_layout(height=400)
            st.plotly_chart(fig_delivery, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk status pengiriman tidak tersedia.")
    
    with col2:
        if 'shipping_mode' in df.columns:
            shipping_mode_counts = filtered_df['shipping_mode'].value_counts().reset_index()
            shipping_mode_counts.columns = ['Shipping Mode', 'Count']
            
            fig_shipping_mode = px.bar(
                shipping_mode_counts,
                x='Shipping Mode',
                y='Count',
                title='Jumlah Pesanan berdasarkan Mode Pengiriman',
                labels={'Count': 'Jumlah Pesanan', 'Shipping Mode': 'Mode Pengiriman'},
                color='Count',
                color_continuous_scale=px.colors.sequential.Oranges,
            )
            fig_shipping_mode.update_layout(height=400)
            st.plotly_chart(fig_shipping_mode, use_container_width=True)
        else:
            st.warning("Data yang diperlukan untuk mode pengiriman tidak tersedia.")
    
    # Shipping time analysis
    if 'order_date' in df.columns and 'shipping_date' in df.columns:
        filtered_df['shipping_time'] = (filtered_df['shipping_date'] - filtered_df['order_date']).dt.days
        
        st.subheader("Analisis Waktu Pengiriman")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_shipping_time = filtered_df.groupby('shipping_mode')['shipping_time'].mean().reset_index()
            avg_shipping_time = avg_shipping_time.sort_values('shipping_time')
            
            fig_shipping_time = px.bar(
                avg_shipping_time,
                x='shipping_mode',
                y='shipping_time',
                title='Rata-rata Waktu Pengiriman berdasarkan Mode',
                labels={'shipping_time': 'Rata-rata Waktu (hari)', 'shipping_mode': 'Mode Pengiriman'},
                color='shipping_time',
                color_continuous_scale=px.colors.sequential.Purples,
            )
            fig_shipping_time.update_layout(height=400)
            st.plotly_chart(fig_shipping_time, use_container_width=True)
        
        with col2:
            if 'market' in df.columns:
                avg_shipping_by_market = filtered_df.groupby('market')['shipping_time'].mean().reset_index()
                avg_shipping_by_market = avg_shipping_by_market.sort_values('shipping_time', ascending=False)
                
                fig_market_time = px.bar(
                    avg_shipping_by_market,
                    x='market',
                    y='shipping_time',
                    title='Rata-rata Waktu Pengiriman berdasarkan Market',
                    labels={'shipping_time': 'Rata-rata Waktu (hari)', 'market': 'Market'},
                    color='shipping_time',
                    color_continuous_scale=px.colors.sequential.Purples,
                )
                fig_market_time.update_layout(height=400)
                st.plotly_chart(fig_market_time, use_container_width=True)
            else:
                st.warning("Data yang diperlukan untuk analisis waktu pengiriman berdasarkan market tidak tersedia.")
        
        # Distribution of shipping times
        fig_hist = px.histogram(
            filtered_df,
            x='shipping_time',
            nbins=30,
            title='Distribusi Waktu Pengiriman',
            labels={'shipping_time': 'Waktu Pengiriman (hari)', 'count': 'Jumlah Pesanan'},
            color_discrete_sequence=['#6c5ce7'],
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Data yang diperlukan untuk analisis waktu pengiriman tidak tersedia.")
    
    # Delivery performance by region
    if 'label' in df.columns and 'order_region' in df.columns:
        st.subheader("Performa Pengiriman berdasarkan Region")
        
        # Create a pivot table for delivery status by region
        delivery_by_region = pd.crosstab(
            filtered_df['order_region'], 
            filtered_df['label'].map({-1: 'Early Arrival', 0: 'On Time', 1: 'Delayed'})
        ).reset_index()
        
        # Melt the dataframe for plotting
        delivery_by_region_melted = pd.melt(
            delivery_by_region, 
            id_vars=['order_region'], 
            var_name='Status', 
            value_name='Count'
        )
        
        # Calculate the total orders per region for percentage calculation
        region_totals = delivery_by_region_melted.groupby('order_region')['Count'].sum().reset_index()
        region_totals.columns = ['order_region', 'Total']
        
        # Merge the total back into the melted dataframe
        delivery_by_region_melted = pd.merge(delivery_by_region_melted, region_totals, on='order_region')
        
        # Calculate percentage
        delivery_by_region_melted['Percentage'] = delivery_by_region_melted['Count'] / delivery_by_region_melted['Total'] * 100
        
        # Sort by delayed percentage
        top_regions = delivery_by_region_melted[delivery_by_region_melted['Status'] == 'Delayed'].sort_values('Percentage', ascending=False).head(10)
        regions_to_plot = top_regions['order_region'].unique()
        
        plot_data = delivery_by_region_melted[delivery_by_region_melted['order_region'].isin(regions_to_plot)]
        
        fig_region_delivery = px.bar(
            plot_data,
            x='order_region',
            y='Percentage',
            color='Status',
            title='Top 10 Region dengan Persentase Keterlambatan Tertinggi',
            labels={'Percentage': 'Persentase (%)', 'order_region': 'Region', 'Status': 'Status Pengiriman'},
            color_discrete_map={'Early Arrival': '#28a745', 'On Time': '#17a2b8', 'Delayed': '#dc3545'},
            barmode='group',
        )
        fig_region_delivery.update_layout(height=500)
        st.plotly_chart(fig_region_delivery, use_container_width=True)
    else:
        st.warning("Data yang diperlukan untuk analisis performa pengiriman berdasarkan region tidak tersedia.")

# Tab 4: Data Detail
with tab4:
    st.header("Detail Data")
    
    # Show data statistics
    st.subheader("Statistik Data")
    
    # Select columns for statistics based on data types
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        stats_df = filtered_df[numeric_cols].describe().T
        stats_df = stats_df.reset_index()
        stats_df.columns = ['Metric'] + list(stats_df.columns[1:])
        st.dataframe(stats_df, use_container_width=True)
    else:
        st.warning("Tidak ada kolom numerik untuk ditampilkan statistiknya.")
    
    # Raw data viewer with pagination
    st.subheader("Data Mentah")
    
    # Select columns to display
    all_columns = filtered_df.columns.tolist()
    selected_columns = st.multiselect("Pilih Kolom untuk Ditampilkan", all_columns, default=all_columns[:10])
    
    # Pagination
    page_size = st.slider("Jumlah Baris per Halaman", min_value=5, max_value=100, value=20, step=5)
    total_pages = (len(filtered_df) - 1) // page_size + 1
    
    if total_pages > 0:
        page_num = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1, step=1)
        start_idx = (page_num - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_df))
        
        st.dataframe(filtered_df[selected_columns].iloc[start_idx:end_idx], use_container_width=True)
        st.write(f"Menampilkan {start_idx+1} hingga {end_idx} dari {len(filtered_df)} baris")
    else:
        st.write("Tidak ada data untuk ditampilkan.")

# Footer
st.markdown("---")
st.markdown("### 📈 Supply Chain Analytics Dashboard | Created with Streamlit")
st.markdown("Dashboard ini menampilkan analisis penjualan, pelanggan, dan performa pengiriman dari data e-commerce.")
