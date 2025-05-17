import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt

# Load data
df = pd.read_csv("dashboard/hoursClean_df.csv")
df['date'] = pd.to_datetime(df['date'])

st.set_page_config(page_title="Bike-sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")


def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='date').agg({
        "unregistered": "sum",
        "registered": "sum",
        "count": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
        "count": "count",
        "unregistered": "unregistered",
        "registered": "registered"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "unregistered": "sum",
        "registered": "sum",
        "count": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "count": "count",
        "unregistered": "unregistered",
        "registered": "registered"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['unregistered', 'registered'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "unregistered": "sum",
        "registered": "sum",
        "count": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "count": "count",
        "unregistered": "unregistered",
        "registered": "registered"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['unregistered', 'registered'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hour").agg({
        "unregistered": "sum",
        "registered": "sum",
        "count": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "count": "count",
        "unregistered": "unregistered",
        "registered": "registered"
    }, inplace=True)
    
    return hourly_users_df

# make filter components (komponen filter)

min_date = df["date"].min()
max_date = df["date"].max()

# ----- SIDEBAR -----
with st.sidebar:
    # add logo
    st.image("assets/Sepeda.png")

    st.markdown("<h1 style='text-align: center;'>Date Filter</h1>", unsafe_allow_html=True)

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Select Date Range:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.markdown("<h1 style='text-align: center; font-size:20px;'>Let's Connect With Me</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.sidebar.columns([1,1,1])

with col1:
    st.markdown("[![LinkedIn](https://skillicons.dev/icons?i=linkedin)](https://www.linkedin.com/in/andrysyvamldni/)")
with col2:
    st.markdown("[![Instagram](https://skillicons.dev/icons?i=instagram)](https://www.instagram.com/andrymldni/)")
with col3:
    st.markdown("[![Github](https://skillicons.dev/icons?i=github)](https://github.com/andrymldni)")

# hubungkan filter dengan main_df
main_df = df[
    (df["date"] >= str(start_date)) &
    (df["date"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)

# ----- MAINPAGE -----
st.title(":bar_chart: Dicoding Bike-Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['count'].sum()
    st.metric("Total user", value=total_all_rides)
with col2:
    total_unregistered = main_df['unregistered'].sum()
    st.metric("Total unregistered User", value=total_unregistered)
with col3:
    total_registered = main_df['registered'].sum()
    st.metric("Total registered User", value=total_registered)

st.markdown("---")

# ----- CHART -----

# Tren pengguna sepeda
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_users_df, x='yearmonth', y='count', label='Total Users', marker='o')
sns.lineplot(data=monthly_users_df, x='yearmonth', y='unregistered', label='Unregistered Users', marker='o')
sns.lineplot(data=monthly_users_df, x='yearmonth', y='registered', label='Registered Users', marker='o')

ax.set(title="Tren pengguna sepeda", xlabel='Bulan-Tahun', ylabel='Total user')
ax.legend()
# Display the plot
st.pyplot(fig)

# Visualization in the first column
st.header("Visualizations")

st.write("<div style='font-size: 24px;'>Musim apa yang menjadi favorit pengguna untuk bersepeda?</div>", unsafe_allow_html=True)
with st.expander("Lihat Visualisasi"):
        color_list = ['#1565c0', '#bbdefb', '#bbdefb', '#bbdefb']
        season_plot = df.groupby('season')['count'].sum().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=season_plot, x='season', y='count', palette=color_list, ax=ax)
        plt.title("Most Favourite Season to Ride a Bike")
        plt.xlabel('Season')
        plt.ylabel('Total Users')
        st.pyplot(fig)
        st.write("Dari visualisasi di atas, terlihat bahwa musim favorit pengguna sepeda adalah musim fall.")

st.write("<div style='font-size: 24px;'>Apakah pengguna sepeda lebih cenderung keluar saat cuaca cerah atau saat cuaca buruk?</div>", unsafe_allow_html=True)
with st.expander("Lihat Visualisasi"):
        weather_plot = df[['weather_condition', 'count']]
        weather_plot.replace({
            'weather_condition': {
                1: 'Clear',
                2: 'Mist',
                3: 'Light Snow, Light Rain',
                4: 'Heavy Rain, Snow, Fog'
            }
        }, inplace=True)
        weather_plot = weather_plot.groupby('weather_condition')['count'].sum().reset_index()
        weather_plot = weather_plot.sort_values('count', ascending=False)
        color_list = ['#1565c0', '#bbdefb', '#bbdefb', '#bbdefb']
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
        sns.barplot(data=weather_plot, x='count', y='weather_condition', palette=color_list)
        plt.title("Total Bike Users in Different Weather Conditions")
        plt.ylabel("Weather Condition")
        plt.xlabel("Total Users")
        for p in ax.patches:
            width = p.get_width()
            plt.text(width, p.get_y() + p.get_height() / 2, f"{width:,.0f}", ha='left', va='center')
        st.pyplot(fig)
        st.write("Dari visualisasi di atas, terlihat bahwa pengguna sepeda lebih cenderung keluar saat cuaca cerah.")

st.write("<div style='font-size: 24px;'>Bagaimana tren jumlah pengguna sepeda sewaan per jam pada hari kerja?</div>", unsafe_allow_html=True)
with st.expander("Lihat Visualisasi"):
        grouped_hour = df.groupby(['workingday', 'hour'])['count'].mean().reset_index(name='counts')
        for workingday, group in grouped_hour.groupby('workingday'):
            chart = alt.Chart(group).mark_line().encode(
                x='hour',
                y='counts',
                color=alt.value('blue') if workingday else alt.value('orange'),
            ).properties(
                title=f'Workingday: {workingday}',
                width=600,
                height=400
            )
            st.altair_chart(chart, use_container_width=True)
            st.write("Dari visualisasi di atas, terlihat bahwa tren jumlah pengguna sepeda sewaan per jam pada hari kerja lebih tinggi pada jam 7-9 pagi dan 4-7 sore.")

# Menambahkan informasi kredit
st.markdown(
    "<div style='text-align: center;'><h5 style='color: #888;'>Copyright ©, created by Andry Syva Maldini</h5></div>",
    unsafe_allow_html=True
)
