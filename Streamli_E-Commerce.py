import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
customer_summary = pd.read_csv('https://raw.githubusercontent.com/Chagiyaa/IDCamp2023/main/customer_summary.csv')
product_summary = pd.read_csv('https://raw.githubusercontent.com/Chagiyaa/IDCamp2023/main/products_summary.csv')
payment_summary = pd.read_csv('https://raw.githubusercontent.com/Chagiyaa/IDCamp2023/payment_summary.csv')

# First Page
def first_page():
    
    st.header('Top 3 Products with Most Orders and Their Categories')

    # Short
    sorted_product_summary = product_summary.sort_values(by='jumlah_order', ascending=False)
    # Top 3
    top_3_products = sorted_product_summary.head(3)

    fig1, ax1 = plt.subplots(figsize=(12, 8))
    sns.barplot(x='product_id', y='jumlah_order', hue='product_category_name_english', data=top_3_products, ax=ax1)
    plt.title('Top 3 Products with Most Orders and Their Categories')
    plt.xticks(rotation=45)
    plt.tick_params(axis='x', which='both', bottom=False, length=0)
    plt.legend(title='Category', bbox_to_anchor=(1.09, 0.9), loc='lower center', fontsize=10)
    plt.xlabel('')
    plt.ylabel('Number of Orders')

    st.pyplot(fig1)

    st.header('Count of Product ID by Average Review Score')
    # Count of Product ID by Average Review Score
    product_summary['review_category'] = pd.cut(
        product_summary['avg_review_score'],
        bins=[-float('inf'), 3, float('inf')],
        labels=['Less than 3', 'More than 3'],
        right=False
    )

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2 = sns.countplot(x='review_category', data=product_summary, palette='viridis')
    for p in ax2.patches:
        ax2.annotate(
            f'{p.get_height()}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='center',
            xytext=(0, 6),
            textcoords='offset points',
            fontsize=10
        )
    plt.title('Count of Product ID by Average Review Score')
    plt.xlabel('Average Review Score Category')
    plt.ylabel('Number of Product')

    st.pyplot(fig2)

# Second Page
def second_page():
    
    st.header('Count and Percentage of Customers based on Jumlah Order')

    # create category of jumlah order item (lebih dari 1 dan 1 kali)
    customer_summary['order_category'] = customer_summary['jumlah_order_item'].apply(lambda x: '>1' if x > 1 else '1')
    customer_counts = customer_summary.groupby('order_category')['customer_id'].count()
    # value baru untuk perhitungan persentase
    total_customers = len(customer_summary['customer_id'])
    customer_percentage = customer_counts / total_customers * 100

    # Plot the bar chart
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(customer_counts.index, customer_counts.values, color=['skyblue', '#90EE90'])

    # Add count and percentage values on top of each bar
    for bar, count, percentage in zip(bars, customer_counts.values, customer_percentage.values):
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.1,
            f'{count} ({percentage:.2f}%)',
            ha='center',
            va='bottom'
        )

    plt.ylabel('Number of Customers')
    plt.title('Count and Percentage of Customers based on Jumlah Order')

    st.pyplot(fig2)

    # Top 3 Customers with the Most Jumlah Order Item
    st.subheader('Top 3 Customers with the Most Jumlah Order Item')

    df_sorted = customer_summary.sort_values(by='jumlah_order_item', ascending=False)
    top_3_customers_item = df_sorted.head(3)

    fig3, ax3 = plt.subplots()
    plt.bar(top_3_customers_item['customer_id'], top_3_customers_item['jumlah_order_item'])
    plt.ylabel('Jumlah Order Item')
    plt.xticks(rotation=90)
    plt.title('Top 3 Customers with the Most Jumlah Order Item')

    st.pyplot(fig3)

    # Top 3 Customers with the Most Total Spend
    st.subheader('Top 3 Customers with the Most Total Spend')

    df_sorted_spend = customer_summary.sort_values(by='total_price', ascending=False)
    top_3_customers_spend = df_sorted_spend.head(3)

    fig4, ax4 = plt.subplots()
    plt.bar(top_3_customers_spend['customer_id'], top_3_customers_spend['total_price'])
    plt.ylabel('Total Spend')
    plt.xticks(rotation=90)
    plt.title('Top 3 Customers with the Most Total Spend')

    st.pyplot(fig4)

# Third Page
def third_page():
    
    st.header('Payment Summary')

    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.barplot(x='payment_type', y='jumlah_order', data=payment_summary, palette='viridis', ax=ax5)

    for i, v in enumerate(payment_summary['jumlah_order']):
        plt.text(i, v + 1, str(v), ha='center', va='bottom')

    plt.title('Payment Summary')
    plt.xlabel('Payment Type')
    plt.ylabel('Number of Orders')

    st.pyplot(fig5)

# Main Streamlit App
st.title('Dashboard E-Commerce Public Dataset')

# Add tabs to the sidebar
tabs = ['Products', 'Customers', 'Payments']
selected_tab = st.sidebar.radio('Select Section', tabs)

# Display the selected tab
if selected_tab == 'Products':
    first_page()
elif selected_tab == 'Customers':
    second_page()
elif selected_tab == 'Payments':
    third_page()
