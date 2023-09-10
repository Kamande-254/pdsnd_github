import time
import pandas as pd
import numpy as np

# Dictionary employed for loading the appropriate CSV files.
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
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs  
    while True:
        try:
            city = input("Enter the city you want to view data for (Chicago, New York City, Washington): ").strip().lower()
            if city in CITY_DATA:
                break
            else:
                raise ValueError("Invalid city input. Please choose a valid city.")
        except ValueError as e:
            print(e)

    # Get user input for the month (all, January, February, ..., June)
    while True:
        try:
            month = input(
                "Specify a month for filtering (January, February, March, April, May, June, all): ").strip().lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                break
            else:
                raise ValueError("Invalid month input. Please choose a valid option.")
        except ValueError as e:
            print(e)

    # Get user input for the day of the week (all, Sunday, Monday, ..., Saturday)
    while True:
        try:
            day = input(
                "If you have a specific day in mind, please enter it (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, all): ").strip().lower()
            if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
                break
            else:
                raise ValueError("Invalid day input. Please choose a valid option.")
        except ValueError as e:
            print(e)

    print('-' * 40)

    # Check if the user has selected "all" for both month and day
    if month == 'all' and day == 'all':
        print('No filtering will be applied')
    else:
        return city, month, day

# Load the data for the specified city, month, and day
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
    # Load the data file into the DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Retrieve month and day of the week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if a specific month is provided
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        if month.capitalize() in months:
            month = months.index(month.capitalize()) + 1
            # Filter by month to create the new DataFrame
            df = df[df['month'] == month]
        else:
            print("Invalid month input. No month filter applied.")

    # Filter by day of the week if a specific day is provided
    if day != 'all':
        # Filter by day of the week to create new DataFrame
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('The Most Common Month is:', popular_month)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day of the Week is:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
        # Determine the most common hour
    print('Most Common Hour is:', popular_hour)
        # Print the most common hour

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    frequent_start_station = df['Start Station'].value_counts().idxmax()
    print("Most Frequently Used Starting Station is:", frequent_start_station)

    # Display most commonly used end station
    frequent_end_station =  df['End Station'].value_counts().idxmax()
    print("Most Frequently Used end Station is:", frequent_end_station)

    # Display most frequent combination of start station and end station trip
    df['common_trip'] = df['Start Station'] + " to " + df['End Station']
         # Create a new column 'common_trip' by combining 'Start Station' and 'End Station'

    # Find and display the most frequent route
    busiest_route = df['common_trip'].mode()[0]
    print("The Busiest Route is:", busiest_route)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = int(sum(df['Trip Duration'] / 60) / 60)
    print("Total Travel Time (in hours) for Your Selection is:", total_travel_time)

    # Display mean travel time
    average_travel_time = int(df['Trip Duration'].mean() % 60)
    print("Average Travel Time (in minutes):", average_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df.groupby(['User Type'])['User Type'].count()
    print("Count by User Type:\n", user_type_counts)


    # Display counts of gender
    try:
        # Group the DataFrame by 'Gender' and count the occurrences of each gender
        gender_counts = df.groupby(['Gender'])['Gender'].count()
        
        # Display the gender counts
        print("Usage by Gender:\n", gender_counts)
    # Handle any potential exceptions (e.g., if 'Gender' is not a valid input)
    except Exception as e:
        print(f"An error occurred: {e}")


    # Display earliest, most recent, and most common year of birth
    try:
        print("Subscriber Birth Year Statistics:\n")
        
        # Calculate and display the oldest subscriber's birth year
        oldest_birth_year = int(df['Birth Year'].min())
        print("Oldest Subscriber Birth Year:", oldest_birth_year)
        
        # Calculate and display the youngest subscriber's birth year
        youngest_birth_year = int(df['Birth Year'].max())
        print("Youngest Subscriber Birth Year:", youngest_birth_year)
    
        # Calculate and display the most common birth year
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("Most Common Birth Year:", most_common_birth_year)

    # Handle the KeyError exception for 'Birth Year' column not existing in the DataFrame
    except KeyError:
        print("No additional birth year information exists!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays rows of data based on user's request."""
    start_loc = 0
    while True:
        show_data = input("Do you want to see 5 rows of data? Enter 'yes' or 'no': ").lower()
        if show_data != 'yes':
            break
        else:
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)  # Add this line to display data to the main loop

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()