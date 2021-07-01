import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please choose one of the cities - chicago, new york city, washington: ')
        if city not in ['chicago','new york city','washington']:
            print ('This is not a valid input. Please try again.')
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
            month = input('Please select a month to filter e.g. january, february... Enter all if you don\'t want to filter by month: ')
            if month not in ['january','february','march','april', 'may','june', 'all']:
                print ('This is not a valid input. Please try again.')
            else:
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please select a day of week to filter e.g. monday, tuesday... Enter all if you don\'t want to filter by day of week: ')
        if day not in ['monday','tuesday','wednesday','thursday', 'friday','saturday', 'sunday', 'all']:
            print ('This is not a valid input. Please try again.')
        else:
            break

    print('-'*40)
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
 # load data file into a dataframe
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name



     # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # convert the Start Time column to datetime
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    print('Most common month: ', months[popular_month-1])

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print ('Most common day of week: ', popular_day)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_stn = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', popular_start_stn)

    # TO DO: display most commonly used end station
    popular_end_stn = df['End Station'].mode()[0]
    print('Most commonly used end station: ', popular_end_stn)

    # TO DO: display most frequent combination of start station and end station trip
    df['trip_stations'] = df['Start Station'].str.cat(df['End Station'],sep = " ")
    popular_trip = df['trip_stations'].mode()[0]
    print('Most frequent combination of start and end station trip: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print ('Total trip duration in seconds: ', tot_travel_time)
    # TO DO: display mean travel time
    av_travel_time = df['Trip Duration'].mean()
    print ('Average trip duration in seconds: ', av_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df.groupby('User Type')['User Type'].count(),"\n")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print(df.groupby('Gender')['Gender'].count(),"\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print ('\nEarliest year of birth: ',df['Birth Year'].min())
        print ('Most recent year of birth: ',df['Birth Year'].max())
        print ('Most common year of birth: ',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    view = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view == 'yes' or view.lower() =='y':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
