import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Load the data
bycategory_combined_df = pd.read_csv('bycategory_combined_data.csv')
byproduct_combined_df = pd.read_csv('byproduct_combined_data.csv')

# Set up the Streamlit page configuration
st.set_page_config(page_title="Product Sales and Reviews Dashboard", layout="wide")

# Sidebar with selection options
st.sidebar.title("Navigation")
st.sidebar.markdown("Select the visualizations you want to explore:")

# Page Title
st.title("📊 Product Sales and Reviews Dashboard")

# Option to choose which visualization to show
page = st.sidebar.selectbox("Choose a page", ["Overview", "Review vs Sales", "Sales by Category", "Price and Sales Analysis", "Conclusion"])

# Overview Page
# Overview Page
if page == "Overview":
    st.header("📝 Overview of the Data")
    
    # Pilih dataset untuk ditampilkan
    dataset_choice = st.selectbox("Pilih dataset untuk ditampilkan", ["bycategory_combined_df", "byproduct_combined_df"])
    
    if dataset_choice == "bycategory_combined_df":
        st.write(bycategory_combined_df.head())
        st.write("### Summary Statistics:")
        st.write(bycategory_combined_df.describe())
    else:
        st.write(byproduct_combined_df.head())
        st.write("### Summary Statistics:")
        st.write(byproduct_combined_df.describe())


# Review vs Sales Page
if page == "Review vs Sales":
    st.header("📈 Review Count vs Average Review Score by Category")
    
    # Scatter plot: Review count vs Average review score
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x="review_count", y="average_review_score", size="total_sales", hue="review_count",
        data=bycategory_combined_df, sizes=(50, 300), alpha=0.7, palette="coolwarm"
    )
    plt.title("Review Count vs Average Review Score by Category", fontsize=14)
    plt.xlabel("Number of Reviews")
    plt.ylabel("Average Review Score")
    plt.legend(title="Category", loc="upper right")
    st.pyplot(plt)

# Sales by Category Page
if page == "Sales by Category":
    st.header("📊 Top Product Categories by Total Sales")
    
    # Show top categories by total sales
    top_sales_categories = bycategory_combined_df.sort_values(by='total_sales', ascending=False).head(10)
    
    # Create the bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="total_sales", y="product_category_name", data=top_sales_categories,
        palette="Greens_r"
    )
    
    # Set the title and labels
    plt.title("Top 10 Product Categories by Total Sales", fontsize=14)
    plt.xlabel("Total Sales (in millions)")  # Label with 'millions' for better understanding
    plt.ylabel(None)
    
    # Format the x-axis to display in millions (optional adjustment)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x/1e6:.2f}M'))  # Format as millions
    
    # Show the plot
    st.pyplot(plt)


# Price and Sales Analysis Page
if page == "Price and Sales Analysis":
    st.header("💸 Price vs Total Sales")
    
    # Pilih dataset untuk analisis harga dan penjualan
    dataset_choice = st.selectbox("Pilih dataset untuk analisis", ["bycategory_combined_df", "byproduct_combined_df"])
    
    if dataset_choice == "bycategory_combined_df":
        # Convert total_sales to numeric, and handle non-numeric values
        bycategory_combined_df['total_sales'] = pd.to_numeric(bycategory_combined_df['total_sales'], errors='coerce')

        # Check for the maximum value of total_sales after conversion
        max_sales = bycategory_combined_df['total_sales'].max()
        st.write(f"Maximum Total Sales: {max_sales}")

        # Scatter plot Price vs Total Sales (in millions)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x="item_price", y=bycategory_combined_df["total_sales"] / 1_000_000,  # Total sales in millions
            size="review_count", hue="average_review_score",
            data=bycategory_combined_df, sizes=(50, 300), alpha=0.7, palette="coolwarm"
        )

        # Add a title and labels
        plt.title("Price vs Total Sales (in millions)", fontsize=14)
        plt.xlabel("Item Price")
        plt.ylabel("Total Sales (in millions)")

        # Show legend and plot
        plt.legend(title="Average Rating", loc="upper right")
        st.pyplot(plt)


    else:
        # Convert total_sales to numeric for byproduct_combined_df
        byproduct_combined_df['total_sales'] = pd.to_numeric(byproduct_combined_df['total_sales'], errors='coerce')

        # Scatter plot Price vs Total Sales for byproduct_combined_df
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x="item_price", y=byproduct_combined_df["total_sales"] / 1_000_000, 
            size="review_count", hue="average_review_score",
            data=byproduct_combined_df, sizes=(50, 300), alpha=0.7, palette="coolwarm"
        )
        plt.title("Price vs Total Sales (in millions)", fontsize=14)
        plt.xlabel("Item Price")
        plt.ylabel("Total Sales (in millions)")
        plt.legend(title="Average Rating", loc="upper right")
        st.pyplot(plt)


# Conclusion Page
if page == "Conclusion":
    st.header("📚 Conclusion")
    st.write("""
    ### Q1: Bagaimana hubungan antara rating produk dan kategori produk dalam hal jumlah ulasan dan rating rata-rata?
    - Kategori produk dengan jumlah ulasan lebih dari 2000 cenderung membentuk pola horizontal, dengan variasi rating yang cukup luas.
    - Kategori produk dengan ulasan kurang dari 2000 cenderung memiliki rating lebih tinggi dan konsisten.

    ### Q2: Apa faktor-faktor yang paling berpengaruh terhadap total penjualan produk?
    - Harga produk, jumlah ulasan, dan kategori produk memiliki pengaruh signifikan terhadap total penjualan.
    - Kategori tertentu seperti "cool_stuff" menunjukkan perbedaan signifikan dalam penjualan meskipun harga produk tidak terlalu tinggi.

    ### Q3: Apakah kategori produk tertentu memiliki rating lebih tinggi daripada yang lain?
    - Kategori dengan lebih sedikit ulasan cenderung memiliki rating lebih tinggi, sementara kategori dengan ulasan lebih banyak memiliki variasi rating yang lebih besar.

    #### Note:
    - Data di atas memberikan wawasan yang berguna untuk memanfaatkan faktor-faktor seperti harga, ulasan, dan kategori dalam strategi penjualan dan pemasaran.
    """)
    st.write("📈 **Further Exploration**: Consider exploring correlations between other variables and sales for a deeper insight.")
