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
        city = input('What city interests you out of New York City, Chicago or Washington? ').lower() #converts all uppercase characters to lowercase. If no uppercase characters exist, it returns the original string.
        if city.lower() not in ('new york city', 'new york','chicago', 'washington'):
            print('We only have info on New York, Chicago or Washington at the moment \n Can you try one of them instead?')
        else:
             break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('What month?\n All, January, February, March, April, May, June: ').lower()
        if month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("We don't have that month. Please try one from the list as above")
        else:
             break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('And what day of the week?\n All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ')
        if day.lower() not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("Have you spelled it correctly?")
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]


    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.dayofweek.html
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    common_month = df['month'].value_counts().keys()[0]
    print(f'The most common travel month is: {common_month}')


    # TO DO: display the most common day of week
    common_day = df['day_of_week'].value_counts().keys()[0]
    print(f'The most common travel day is: {common_day}')



    # TO DO: display the most common start hour
    hours = df['Start Time'].dt.hour
    hour_mode = hours.mode()[0]
    print(f'Common hour: {hour_mode}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    # TO DO: display most commonly used start station
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('Stations\n\n')
    start_time = time.time()

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station:', Start_Station)


    # TO DO: display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('Most commonly used alighting point is :', End_Station)


    # TO DO: display most frequent combination of start station and end station trip
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
    Combo_Station = df.groupby(['Start Station','End Station']).count().idxmax()[0] #most frequent combination! Alternative of print((df["Start Station"] + " - " + df["End Station"]).value_counts().idxmax()) for same effect
    print('Most commonly used combination of start station and end station:', Start_Station, "and", End_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('Durations\n\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_travel_time = sum(df['Trip Duration'])
    print("Total travel time is: ", Total_travel_time/86400, " days.") #86400 seconds in a day, sum is seconds

    # TO DO: display mean travel time
    Average_travel_time = df['Trip Duration'].mean()
    print("Average travel time is: ", Average_travel_time/60 , " minutes.") #


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('User stats\n\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n\n', user_types)

    # TO DO: Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    # TO DO: Display earliest, most recent, and most common year of birth
    #https://docs.python.org/3/reference/compound_stmts.html#try

    try:
      Earliest_year = df['Birth Year'].min().astype(int)
      print('\nEarliest Year:', Earliest_year, 'woah!!')
    except KeyError:
      print("\nEarliest Year:\nNo personal data available for this month.")

    try:
      Most_recent_year = df['Birth Year'].max().astype(int)
      print('\nMost Recent Year:', Most_recent_year)
    except KeyError:
      print("\nMost Recent Year:\nNo personal data available for this month.")

    try:
      Most_common_year = df['Birth Year'].value_counts().idxmax().astype(int) #https://stackoverflow.com/questions/21291259/convert-floats-to-ints-in-pandas
      print('\nMost Common Year:', Most_common_year)
    except KeyError:
      print("\nMost Common Year:\nNo personal data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        lines = 0
        count = 0

        while True:

            datasource = input("Would you like to view 5 lines of raw data? Enter Y or N ").lower()

            if datasource == 'y':
                print(df.iloc[count:count+5])
                lines += 5
                count += 5
            elif datasource == 'n':
                break



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for visiting! See y'all next time")
            break


if __name__ == "__main__":
	main()
