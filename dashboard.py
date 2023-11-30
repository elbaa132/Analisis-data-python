import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt

def create_monthly_rentals_df(df):
    df_daily['yr'] = df_daily['dteday'].dt.year
    df_daily['mnth'] = df_daily['dteday'].dt.month
    filtered = df_daily[(df_daily['yr'] >= 2011) & (df_daily['yr'] <= 2012)]
    monthly_rentals_df = filtered.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
    return monthly_rentals_df

def create_comparison_holiday_df(df):
    total_holiday = df_daily[df_daily['holiday'] == 1]['cnt'].sum()
    total_weekdays = df_daily[df_daily['holiday'] == 0]['cnt'].sum()
    percentage = ((total_holiday - total_weekdays) / total_weekdays) * 100
    return total_holiday, total_weekdays

def create_daily_paterns_df(df):
    df_hour['weekday'] = pd.to_datetime(df_hour['dteday']).dt.day
    daily_hourly_rentals = df_hour.groupby(['weekday', 'hr'])['cnt'].sum().reset_index()
    pivot_data = daily_hourly_rentals.pivot(index='weekday', columns='hr', values='cnt')
    return pivot_data

def create_seasonal_rentals_df(df):
    df_hour['season'] = df_hour['season'].map({
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
})
    seasonal_rentals = df_hour.groupby(['season', 'mnth'])['cnt'].sum().reset_index()
    return seasonal_rentals

def create_paterns_per_hour_df(df):
    hourly_rentals = df_hour.groupby('hr')['cnt'].sum()
    return hourly_rentals


# membaca dan menampilkan dataset harian
df_daily = pd.read_csv('dashboard/day.csv')
df_daily.head()

# membaca dan menampilkan dataset per jam
df_hour = pd.read_csv('dashboard/hour.csv')
df_hour.head()

# memperbaiki tipe data pada masing-masing dataset
df_daily['dteday'] = pd.to_datetime(df_daily['dteday'])

df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

min_date = df_hour["dteday"].min()
max_date = df_hour["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/elbaa132/Analisis-data-python/main/CapitalBikeshare-main.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#dataframe
monthly_rentals_df = create_monthly_rentals_df(df_daily)
total_holiday, total_weekdays = create_comparison_holiday_df(df_daily)
pivot_data = create_daily_paterns_df(df_hour)
seasonal_rentals = create_seasonal_rentals_df(df_hour)
hourly_rentals = create_paterns_per_hour_df(df_hour)

st.header('Capital Bike Share :sparkles:')
st.subheader('Tren Peminjaman Sepeda per Bulan (2011-2012)')

fig, ax = plt.subplots(figsize=(8, 4))

for year in monthly_rentals_df['yr'].unique():
    data_year = monthly_rentals_df[monthly_rentals_df['yr'] == year]
    plt.plot(data_year['mnth'], data_year['cnt'], marker='o', label=year)

ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.legend(title='Tahun', loc='upper left')
ax.grid()
st.pyplot(fig)

st.subheader('Perbandingan Jumlah Peminjaman Sepeda (Hari Libur vs Weekdays)')
labels = ['Hari Libur', 'Hari Biasa']
sizes = [total_holiday, total_weekdays]
fig, ax = plt.subplots(figsize=(6, 4))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['orange', 'lightgreen'])
st.pyplot(fig)

st.subheader('Pola Peminjaman Harian')
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(pivot_data, cmap='YlGnBu', ax=ax)
ax.set_title(None)
ax.set_xlabel('Jam')
ax.set_ylabel('Hari dalam Bulan')
st.pyplot(fig)

st.subheader('Pengaruh musim terhadap jumlah rental')
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(data=seasonal_rentals, x='mnth', y='cnt', hue='season', marker='o')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
ax.legend(title='Musim')
ax.grid()
st.pyplot(fig)

st.subheader('Pola Peminjaman Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(6, 4))
hourly_rentals.plot(kind='line', color='green')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Peminjaman')
ax.set_xticks(range(24))
ax.grid()
st.pyplot(fig)

st.caption('Copyright (c) Marella Elba Nafisa 2023')