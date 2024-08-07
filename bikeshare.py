import time
import pandas as pd
import numpy as np

"""Purpose: Use Python, Pandas, NumPy, to explore US bikeshare data for three cities (Chicago, New York, and Washington) 
    
    by Tran Hoang An Binh
    Project: Explore US Bikeshare Data
    Due Date: 07/11/2024
"""
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in ["chicago", "new york city", "washington"]:
            break
        else:
            print('Invalid input. Please choose from Chicago, New York City, or Washington.')

    # Get user input for month (all, january, february, ... , june).
    while True:
        month = input('Which month? January, February, March, April, May, June, or all?\n').lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print('Invalid input. Please enter a valid month or "all".')

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    while True:
        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n').lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print('Invalid input. Please enter a valid day or "all".')

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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # Convert 'Start Time' column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns.
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Define months.
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    # Filter by month if applicable.
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    # Filter by day of week if applicable.
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Define month names.
    month_names = ['January', 'February', 'March', 'April', 'May', 'June']

    # Display the most common month.
    common_month_num = df['Month'].mode()[0]
    common_month_name = month_names[common_month_num - 1]
    print(f'Most Common Month: {common_month_name}')

    # Display the most common day of week.
    common_day = df['Day of Week'].mode()[0]
    print(f'Most Common Day of Week: {common_day}')

    # Display the most common start hour.
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f'Most Common Start Hour: {common_hour}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start_station = df['Start Station'].value_counts().idxmax()
    print(f'Most Common Start Station: {common_start_station}')

    # Display most commonly used end station.
    common_end_station = df['End Station'].value_counts().idxmax()
    print(f'Most Common End Station: {common_end_station}')

    # Display most frequent combination of start station and end station trip.
    common_trip = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
    print(f'Most Common Trip: from {common_trip[0]} to {common_trip[1]}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is: ", total)

    # Display mean travel time.
    mean = df['Trip Duration'].mean() / 3600.0
    print("mean travel time in hours is: ", mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_types = df['User Type'].value_counts()
    print('User Types:')
    print(user_types)

    # Display counts of gender.
    if 'Gender' in df.columns:
        print('\nGender:')
        user_gender = df['Gender'].value_counts()
        [print(f'{gender}: {count}') for gender, count in user_gender.items()]
    else:
        print('\nGender data not available.')

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        print('\nBirth Year:')
        birth_years = df['Birth Year'].dropna().astype(int)
        print(f'Earliest: {birth_years.min()}')
        print(f'Most Recent: {birth_years.max()}')
        print(f'Most Common: {birth_years.mode()[0]}')
    else:
        print('\nBirth Year data not available.')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def individual_data(df):
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n").lower()
        if raw_data == 'yes':
            print("\nDisplaying 5 rows of data.\n")
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
            if end_data > df_length:
                end_data = df_length
        elif raw_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))
        
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n").lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
