import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

dash = '*'*40 #used in several functions to help delineate error messages.

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nPlease input a city to analyze, you may choose Chicago, New York City, or Washington: ').lower()            
        except:
            print('\nPlease type the name of the city exactly as displayed above.\n')
        else:
            #ensure that a vaild city was entered
            if city in ['chicago','new york city','washington']:
                break
            print('\n',dash,'\nThat is not a city on the list, please try again.  Type the name of the city exactly as displayed above.\n',dash,'\n')


    # get user input for month (all, January, February, ... , June)
    while True:
        try:
            month = input('\nPlesae input a month to analyze between January and June.  Type the whole month name (ex. january, february, etc...). If you would like to analyze the whole file, type "all" without quotes: ').lower()
        except:
            print('\nPlease type the name of the month or all.\n')
        else:
            if month in ['january','february','march','april','may','june','all','"all"']:
                break
            print('\n',dash,'\nThat is not a valid entry for month. Please type the full name of the month or type "all" to see all months.\n',dash,'\n')

    # get user input for day of week (all, Monday, Tuesday, ... Sunday)
    while True:
        try:
            day = input('\nPlesae input a day of the week to analyze.  Type the whole day name (ex. monday, tuesday, etc...). If you would like to analyze all days, type "all" without quotes: ').lower()
        except:
            print('\nPlease type the name of the day or all.\n')
        else:
            if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all','"all"']:
                break
            print('\n',dash,'\nThat is not a valid entry for day. Please type the full name of the day or type "all" to see all days.\n',dash,'\n')


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
    df = pd.read_csv(CITY_DATA.get(city))

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
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

  
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Print the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[df['month'].mode()[0]-1].title()
    print('\nThe most common month for travel is {}.\n'.format(month))

    # Print the most common day of week
    top_day_of_week = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week for travel is {}.\n'.format(top_day_of_week))

    # Print the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    top_hour = df['hour'].mode()[0]
    print('\nThe most common hour of the day for travel is {} o\'clock (24h time format).\n'.format(top_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is {}.\n'.format(top_start_station))

    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used ending station is {}.\n'.format(top_end_station))

    # display most frequent combination of start station and end station trip
    df['Start - Stop'] = df['Start Station'] + ' --> ' + df['End Station']
    top_start_stop = df['Start - Stop'].mode()[0].split(' --> ')
    print('\nThe most frequent combination of start station and end station consists of the trip starting at {} and ending at {}.\n'.format(top_start_stop[0],top_start_stop[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time   
    # time_stats series will store the total trip durations in different time increments (seconds, minutes, etc...)
    time_stats = pd.Series(data = [df['Trip Duration'].sum(),df['Trip Duration'].sum()/60,df['Trip Duration'].sum()/60/60,df['Trip Duration'].sum()/60/60/24,df['Trip Duration'].sum()/60/60/24/7,df['Trip Duration'].sum()/60/60/24/7/52],index = ['seconds','minutes','hours','days','weeks','years'])
    
    for index,value in time_stats.items():
        print('\nThe total travel time in {} was {} {}.\n'.format(index,value,index))
    
    # alt_time_series will store the total trip duration in a different manner such that to retrieve the total trip duration one must sum across all rows of the series to get the total years, weeks, days, hours, minutes and seconds of the trip.  
    alt_time_series = pd.Series(time_stats.copy(),dtype = 'int')
    alt_time_series['years'] = int(time_stats['years'])
    alt_time_series['weeks'] = int(time_stats['years'] % 1 * 52)
    alt_time_series['days'] =  int(time_stats['years'] % 1 * 52 % 1 * 7)
    alt_time_series['hours'] = int(time_stats['years'] % 1 * 52 % 1 * 7 % 1 * 24)
    alt_time_series['minutes'] = int(time_stats['years'] % 1 * 52 % 1 * 7 % 1 * 24 % 1 * 60)
    alt_time_series['seconds'] = int(time_stats['years'] % 1 * 52 % 1 * 7 % 1 * 24 % 1 * 60 % 1 * 60)
    
    print('\nAnother way to describe this would be to say that the total travel time was {} year(s),{} week(s),{} day(s),{} hour(s),{} minute(s), and {} second(s).\n'.format(alt_time_series['years'],alt_time_series['weeks'],alt_time_series['days'],alt_time_series['hours'],alt_time_series['minutes'],alt_time_series['seconds']))
    

    # display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print('\nThe average travel time for each trip was {} seconds which is roughly {} minutes.\n'.format(avg_travel,int(round(avg_travel/60))))
    
    #Calculate trip avg max distance start
    #calculate the trip whose absolute difference between the trip vs. that trip's reciprocal is the longest among all trips vs. reciprocal trips.
    #For example, the avg trip time from A to B was x minutes, but the avg trip time from B to A was y minutes, with y >>> x
    
    print('\nNow finding the trip whose average travel-time from A --> B has the largest absolute difference as compared to the reverse average travel-time from B --> A.\n')

    #get all the trip averages
    df_trip_avg = pd.DataFrame(df.groupby(['Start Station','End Station'])['Trip Duration'].mean()) 

    #create the framework for the dataframe of reverse trips from B-->A
    tuples = list(zip(df_trip_avg.index.get_level_values(1),df_trip_avg.index.get_level_values(0))) #gets the inverse indeces of the df_trip_avg data_frame
    index = pd.MultiIndex.from_tuples(tuples, names = ['Start Station', 'End Station'])
    df_reverse_trip_avg = pd.DataFrame(index = index) 

    #Add the average trip data to the reverse trip dataframe
    df_reverse_trip_avg['recip avg'] = df_reverse_trip_avg.join(df_trip_avg, on=['Start Station','End Station']) 

    #swap the indeces names and values so that the recip avg column now reflects a given trip's reciprocal trip average.
    df_reverse_trip_avg = df_reverse_trip_avg.rename({'Start Station': 'End Station', 'End Station': 'Start Station'}, axis = 'index')
    df_reverse_trip_avg = df_reverse_trip_avg.swaplevel(0,1)

    #join the avg dataframe with the reciprocal avg dataframe
    join_df = df_trip_avg.join(df_reverse_trip_avg,on=['Start Station','End Station']) 

    #Calculate the difference betwee the avg trip and that trip's reciprocal avg trip
    #Example: avg trip from A to B was x minutes, but avg trip from B to A was y minutes.  
    join_df['Difference'] = abs(join_df['Trip Duration'] - join_df['recip avg'])

    #get the max difference between A --> B vs. B --> A
    max_dif_df = join_df[join_df['Difference'] == join_df['Difference'].max()]
    A = max_dif_df.index[0][0]
    B = max_dif_df.index[0][1]
    A_to_B_avg = round(max_dif_df.loc[(A,B),'Trip Duration']/60,2) #get the avg travel times in minutes
    B_to_A_avg = round(max_dif_df.loc[(A,B),'recip avg']/60,2)
    max_difference = round(max_dif_df.loc[(A,B),'Difference']/60,2)

    print('\nThe average travel-time from "{}" to "{}" took {:,} minutes, but the inverse travel-time average from "{}" to "{}" took {:,} minutes for an absolute difference of {:,} minutes.  Among all the travel-time averages from A-->B as compared to their travel-time averages from B-->A, this trip had the largest absolute difference between the two.\n'.format(A,B,A_to_B_avg,B,A,B_to_A_avg,max_difference))
    #Calculate trip avg max distance end



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_series = df['User Type'].value_counts()    
    print('The count of trips by user type are as follows:\n')
    for index,value in user_type_series.items():
        print('The user type of {} had {:,} trip(s).\n'.format(index,value))

    # Display counts of gender
    if 'Gender' in df:
        gender_series = df['Gender'].value_counts()
        print('The count of trips by gender are as follows:\n')
        for index,value in gender_series.items():
            print('{:,} trips were completed by {}s.\n'.format(value,index.lower()))
    

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        mode_year = int(df['Birth Year'].mode()[0])
        print('The oldest person or persons completing a trip were born in {}.\n'.format(earliest_year))
        print('The youngest person or persons completing a trip were born in {}.\n'.format(most_recent_year))
        print('Most of the trips were completed by people born in {}.\n'.format(mode_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def print_raw_data(df):
    """Prints raw data 5 rows at a time until user enters no or the end of the dataframe is reached."""
    
    more_data = 'yes'
    i = 0    
    pd.set_option('display.max_columns',None) #use so that all columns will be displayed
    while i < len(df) and more_data == 'yes':
        print(df[i:i+5])
        i+=5
        while True:
            try:
                more_data = input('\nWould you like to continue seeing raw data 5 rows at a time? Enter yes or no.\n')
            except:
                print('\nThat is not a valid entry.\n')
            else:            
                if more_data.lower() in ['yes','no']:
                    break
                print('\n',dash,'\nThat is not a valid entry, please try again.  Would you like to continue seeing raw data 5 rows at a time? Enter yes or no.\n',dash,'\n')
        
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        while True:
            try:
                raw_data = input('\nWould you like to see the raw data 5 rows at a time? Enter yes or no.\n')
                if raw_data.lower() == 'yes':
                    print_raw_data(df)
                elif raw_data.lower() == 'no':
                    break
            except:
                print('\nThat is not a valid entry.\n')
            else:
                if raw_data.lower() in ['yes','no']:
                    break
                print('\n',dash,'\nThat is not a valid entry, please try again. Would you like to see the raw data 5 rows at a time? Enter yes or no.\n',dash,'\n')
                
                

        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() in ['yes','no']:
                    break
            except:
                print('\nThat is not a valid entry.\n')
            else:                
                print('\n',dash,'\nThat is not a valid entry, please try again. Would you like to restart? Enter yes or no.\n',dash,'\n')

        if restart.lower() == 'no':
            break

if __name__ == "__main__":
	main()
