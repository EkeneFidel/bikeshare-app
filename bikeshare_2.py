import time
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta



st.write("""
# BIKE SHARE PROJECT
""")

st.sidebar.header("User Input")
st.sidebar.write("Filter Data By Choosing Parameters")


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
cities = ["Chicago", "Washington", "New York City"]
days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','All']

    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    st.write('Hello! Let\'s explore some US bikeshare data!')

    

    city = st.sidebar.text_input("What city data would you like to see? (Chicago, Washington, New York City) ").lower().title()

    month = st.sidebar.text_input("What month do you want? (January - June or All)").lower().title()
    if month == "":
        month = "All"

    day = st.sidebar.text_input("What day do you want? (Sunday - Saturday or All)").lower().title()
    if day == "":
        day = "All"
    
    return city, month, day

    
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    
  

    # filter by month if applicable
    if month.title() != 'All':
        # use the index of the months list to get the corresponding int
        month_number = months.index(month) + 1
        
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
    
        
    # filter by day of week if applicable
    if day.title() != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    st.write(f'The Most Common Month: **{popular_month}**')


    # display the most common day of week
    
    popular_day = df['day_of_week'].mode()[0]
    st.write(f'The Most Common Day of the week: **{popular_day}**' )


    # extract hour from the Start Time column to create an hour column
    
    df['hour'] =  df['Start Time'].dt.strftime("%I %p")
    
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    st.write(f'The Most Common Start Hour: **{(popular_hour)}**')

    
    return df

    
    # print("\nThis took %s seconds." % (time.time() - start_time))
    


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    st.write(f'Most Start Station: **{popular_start_station}**')


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    st.write(f'Most End Station: **{popular_end_station}**')
   


    # display most frequent combination of start station and end station trip
    df['Start End Station'] = ' From ' + df['Start Station'] + ' to ' + df['End Station']
    popular_start_end = df['Start End Station'].mode()[0]
    st.write('Most Frequent Combination Of Start Station And End Station Trip is:', f'**{popular_start_end}**')
    



    # print("\nThis took %s seconds." % (time.time() - start_time))
    


def trip_duration_stats(df, month):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()

    # display total travel time
    total_travel_time = timedelta(seconds= int(df['Trip Duration'].sum()))
    totaltt = df['Trip Duration'].sum()
    t_days = total_travel_time.days
    t_seconds = total_travel_time.seconds
    t_hours = t_seconds//3600
    t_minutes = (t_seconds//60)%60
    t_seconds = t_seconds%60
    if month.title() != 'All':
        st.write(f'Total Travel Time for {month}: **{t_days} days {t_hours} hours {t_minutes} minutes {t_seconds} seconds**', )
        st.write(totaltt//360)
    else:
        st.write(f'Total Travel Time  for the months of January to June: **{t_days} days {t_hours} hours {t_minutes} minutes {t_seconds} seconds**', )
        st.write(totaltt//360)

    # display mean travel time
    mean_travel_time = timedelta(seconds=df['Trip Duration'].mean())
    meantt = df['Trip Duration'].mean()
    m_days = mean_travel_time.days
    m_seconds = mean_travel_time.seconds
    m_hours = m_seconds//3600
    m_minutes = (m_seconds//60)%60
    m_seconds = m_seconds%60
    if month.title() != 'All':
        st.write(f'Average Travel Time for {month}: **{m_days} days {m_hours} hours {m_minutes} minutes {m_seconds} seconds**', )
        st.write(meantt)
    else:
        st.write(f'Average Travel Time  for the months of January to June: **{m_days} days {m_hours} hours {m_minutes} minutes {m_seconds} seconds**', )
        st.write(f'**{np.ceil(meantt)}** in Hours')

    # print("\nThis took %s seconds." % (time.time() - start_time))
    


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    start_time = time.time()

    # Display counts of user types
    st.write('User Type Stats:')
    st.table(df['User Type'].value_counts())
    
    
    if "Gender" in df:
        # Display counts of gender
        st.write('\nGender Stats:')
        st.table(df['Gender'].value_counts())
    else:
        st.success("No Gender Data To Show")
        


        # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        st.write(f'Earliest Year Of Birth: **{earliest_year}**')
                

        recent_year = int(df['Birth Year'].max())
        st.write(f'Most recent Year Of Birth: **{recent_year}**')
        
        
        common_year = int(df['Birth Year'].mode()[0])
        st.write(f'Most Common Year Of Birth: **{common_year}**')
    
    else:
        st.success("No Birth Year Data To Show")

    
def produce_raw_data(df):
    num = st.sidebar.slider("How  many raw data do you want displayed? ", min_value=0, step=5)
    if num == 5:
        dataframe = df.head(num)
        st.subheader("Raw Data")
        st.write(dataframe)  
    elif num > 5:
        for i in range(5, num+1, 5):
            dataframe = df.head(i)  
            dataframe = dataframe.tail()  
            st.write(dataframe)  
    


    # print("\nThis took %s seconds." % (time.time() - start_time))
    


def main():
    
    city, month, day = get_filters()
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.text("0% Complete")
    st.write()
    

    try:
        
        df = load_data(city, month, day)
        
        df = time_stats(df)
        station_stats(df)
        trip_duration_stats(df, month)
        user_stats(df, city)
        produce_raw_data(df)

        for i in range(1, 11):
            status_text.text("%i%% Complete" % (i*10))
            progress_bar.progress(i*10)
            time.sleep(0.05)
        
        
                    
    except KeyError:
        st.warning("Input correct data")

    
    
        

        # restart = input('\nWould you like to restart? Enter yes or no.\n')
        # if restart.lower() != 'yes':
        #     break


if __name__ == "__main__":
	main()
