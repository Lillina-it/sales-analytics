import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Аналитический дешборд")

@st.cache_data
def load_data():
    orders = pd.read_csv('data/orders.csv')
    users = pd.read_csv('data/users.csv')
    items = pd.read_csv('data/items.csv')
    df = orders.merge(users, on='user_id').merge(items, on='item_id')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['total_price'] = df['quantity'] * df['price_per_unit']
    return df

df = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Сырые данные", "Ключевые показатели", "Визуализация", "Аналитические выводы"])

with tab1:
    st.subheader("Сырые данные")
    cat_filter = st.multiselect("Фильтр по категории:", df['category'].unique())
    df_filtered = df[df['category'].isin(cat_filter)] if cat_filter else df
    st.dataframe(df_filtered)

with tab2:
    st.subheader("Ключевые показатели")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Всего заказов", len(df))
    c2.metric("Общая выручка", f"{df['total_price'].sum():,.0f} ₽")
    c3.metric("Уникальные пользователи", df['user_id'].nunique())
    c4.metric("Средний чек", f"{df['total_price'].sum() / len(df):,.0f} ₽")

with tab3:
    st.subheader("Визуализация")
    top_10 = df.groupby('item_name')['total_price'].sum().nlargest(10)
    fig1, ax1 = plt.subplots()
    top_10.plot(kind='barh', ax=ax1, color='skyblue')
    ax1.set_title("Топ-10 товаров по выручке")
    st.pyplot(fig1)

    cat_sales = df.groupby('category')['total_price'].sum()
    fig2, ax2 = plt.subplots()
    cat_sales.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
    ax2.set_title("Доля категорий в выручке")
    st.pyplot(fig2)

    df['day'] = df['order_date'].dt.day_name()
    day_sales = df.groupby('day')['total_price'].sum()
    fig3, ax3 = plt.subplots()
    day_sales.plot(kind='bar', ax=ax3, color='salmon')
    ax3.set_title("Продажи по дням недели")
    st.pyplot(fig3)

with tab4:
    st.subheader("Аналитические выводы")
    st.write(f"- Основная выручка приходится на категорию: {df.groupby('category')['total_price'].sum().idxmax()}")
    st.write("- Пик заказов наблюдается в: " + df.groupby('day')['order_id'].count().idxmax())
    st.write(f"- Лидер продаж: {df.groupby('item_name')['quantity'].sum().idxmax()}")