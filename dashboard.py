import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency

sns.set(style="dark")


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="M", on="shipping_limit_date").agg(
        {"order_id": "nunique", "total_price": "sum"}
    )

    # Mengatur indeks ulang dengan format bulan dan tahun
    daily_orders_df.index = daily_orders_df.index.strftime("%B %Y")

    # Mengatur nama kolom
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(
        columns={"order_id": "order_count", "total_price": "revenue"}, inplace=True
    )

    daily_orders_df = daily_orders_df[
        (daily_orders_df["order_count"] != 0) & (daily_orders_df["revenue"] != 0)
    ]
    return daily_orders_df


def create_sum_payment_order_df(df):
    sum_payment_order_df = (
        df.groupby(by="payment_type")
        .order_id.nunique()
        .sort_values(ascending=False)
        .reset_index()
    )
    return sum_payment_order_df


all_df = pd.read_csv("dicoding_project.csv")

datetime_columns = ["shipping_limit_date", "shipping_limit_date"]
all_df.sort_values(by="shipping_limit_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["shipping_limit_date"].min()
max_date = all_df["shipping_limit_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan

    local_image_path = "logo_image.png"
    st.image(local_image_path, use_column_width=True)

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

    main_df = all_df[
        (all_df["shipping_limit_date"] >= str(start_date))
        & (all_df["shipping_limit_date"] <= str(end_date))
    ]

daily_orders_df = create_daily_orders_df(main_df)
sum_payment_order_df = create_sum_payment_order_df(main_df)


st.header("E-Commerce Public Dataset :sparkles:")

st.subheader(
    "Bagaimana performa penjualan dan revenue perusahaan dalam beberapa bulan terakhir?"
)
st.subheader("Data Order Dalam Per Bulan ")

col1, col2 = st.columns(2)

with col1:
    total_orders = (
        daily_orders_df.order_count.sum()
    )  # Mengganti dengan kolom yang sesuai
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(
        daily_orders_df.revenue.sum(), "EUR", locale="es_ES"
    )  # Mengganti dengan kolom yang sesuai
    st.metric("Total Revenue", value=total_revenue)

st.subheader("Total revenue")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["shipping_limit_date"],  # Mengganti dengan kolom yang sesuai
    daily_orders_df["order_count"],  # Mengganti dengan kolom yang sesuai
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15, rotation=45)

st.pyplot(fig)

st.subheader(
    "Sistem pembayaran apa yang banyak digunakan pelanggan untuk melakukan transaksi?"
)
st.subheader("Sistem pembayaran")

payment_counts = (
    sum_payment_order_df.groupby("payment_type")
    .order_id.sum()
    .sort_values(ascending=False)
    .head(10)
)


# Visualisasi data dengan diagram batang menggunakan seaborn
plt.figure(figsize=(10, 5))
plt.bar(
    sum_payment_order_df["payment_type"],
    sum_payment_order_df["order_id"],
    color="#72BCD4",
)
plt.title("Sistem Pembayaran yang Paling Banyak Digunakan", fontsize=15)
plt.xlabel("Sistem Pembayaran")
plt.ylabel("Jumlah Penggunaan")
plt.xticks(rotation=45)
st.pyplot(plt)

# payment_data = sum_payment_order_df.groupby("payment_type").order_id.sum().reset_index()

# # Mengurutkan data berdasarkan jumlah 'order_id' secara menurun
# payment_data = payment_data.sort_values(by="order_id", ascending=False)

# # Mengatur ulang indeks baris dan menggantinya dengan indeks berurutan yang dimulai dari 1
# payment_data.reset_index(drop=True, inplace=True)

# payment_data = payment_data.rename(
#     columns={"payment_type": "Tipe Pembayaran", "order_id": "Jumlah Pembeli"}
# )

# # Menampilkan data dalam bentuk tabel di Streamlit
# st.subheader("Sistem Pembayaran Yang digunakan : ")
# st.table(payment_data.head(10))
