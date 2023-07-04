import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """Asks user to specify a city, month, and day to analyze bikeshare data.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*40)
    print('\nHello! Let\'s explore some US bikeshare data!\n')
	
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    question = 'Please choose a city to explore the data from the following choices:\n [chicago, new york city, washington]\nChoice = '
    checkdata = CITY_DATA
    addtext = 'Excellent choice!'
    city = user_prompt(question, checkdata, addtext)
    	
    # get user input for month (all, january, february, ... , june)
    question = 'Please choose a month to explore the data from the following choices:\n [all, january, february, march, april, may, june]\nChoice = '
    checkdata = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    addtext = 'I can work with that!'
    month = user_prompt(question, checkdata, addtext)
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    question = 'Please choose a day to explore the data from the following choices:\n [all, monday, tuesday, wednesday, thursday, friday, saturday, sunday]\nChoice = '
    checkdata = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    addtext = 'As you wish!'
    day = user_prompt(question, checkdata, addtext)
    
    print('Your choices were: City ({}), Month ({}), Day ({})'.format(city.title(),month.title(),day.title()))
    print('-'*40)
    return city, month, day
    
def user_prompt(question, checkdata, addtext =' That\'s an acceptable entry.'):
    notvalid = True
    while notvalid:
        # Prompt user for input
        response = input(question).lower()
        # check if it's a valid entry 
        if type(checkdata) is dict:
            check = checkdata.get(response)
        else:
            check = response in checkdata
        
        if check:
            # if it's valid, let the user know and exit the loop
            print('{}.'.format(response.title()), addtext)
            notvalid = False
        else:
            # if it's not valid, let the user know and ask again
            print('Invalid entry, please try again')
        print('\n')
    return response


def load_data(city, month, day):
    """Loads bikeshare data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city bikeshare data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
	
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
	
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
	
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
        day = day.title()
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city df data is from
        (str) month - name of the month df was filtered by, or "all"
        (str) day - name of the day of week df was filtered by, or "all"
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        #you can determine the most common month
        mcmonthIdx = df['month'].mode()[0]
        # create a list to get the month name
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        print('The most common month of travel in {} was {}.\n'.format(city.title(), months[mcmonthIdx].title()))
    else:
        #only one month's data is displayed so it's not correct
        print('Cannot display the most common month because data was filtered to only include {}\'s data.\n'.format(month.title()))
    

    # display the most common day of week
    if day == 'all':
        #you can determine the most common day
        mcday = df['day_of_week'].mode()[0]
        print('The most common day of travel in {} was {}.\n'.format(city.title(),mcday.title()))
    else:
        #only one day's data is displayed so it's not correct
        print('Cannot display the most common day of week because data was filtered to only include {}\'s data.\n'.format(day.title()))


    # display the most common start hour
    # extract hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour
    # determine the most common hour
    mchour = df['hour'].mode()[0]
    print('The most common hour of travel in {} was {}.\n'.format(city.title(),mchour))
    #remove the hour column before continuing
    df.pop('hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    ss = df['Start Station'].mode()[0]
    print('The most commonly used start station was {}.\n'.format(ss))
	
    # display most commonly used end station
    es = df['End Station'].mode()[0]
    print('The most commonly used end station was {}.\n'.format(es))

    # display most frequent combination of start station and end station trip
    df['Stations'] = df['Start Station'] + ' / ' + df['End Station']
    sses = df['Stations'].mode()[0]
    print('The most frequent combination of start station and end station trip was {}.\n'.format(sses))
    df.pop('Stations')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was {} seconds.\n'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time was {} seconds.\n'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.keys():
        tempUtype = df['User Type'].dropna(axis = 0).value_counts()
        print('Here are the counts of each user type:')
        for i in range(tempUtype.size):
            print('{} - {}'.format(tempUtype.index[i],tempUtype.values[i]))
        print('\n')
    else:
        print('User type data is not available in this dataset.')
    
    # Display counts of gender
    if 'Gender' in df.keys():
        tempGender = df['Gender'].dropna(axis = 0).value_counts()
        print('Here are the counts of each gender:')
        for i in range(tempGender.size):
            print('{} - {}'.format(tempGender.index[i],tempGender.values[i]))
        print('\n')
    else:
        print('Gender data is not available in this dataset.\n')
		
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.keys():
        print('The earliest year of birth is {}.\n'.format(int(df['Birth Year'].min())),'\n')
        print('The most recent year of birth is {}.\n'.format(int(df['Birth Year'].max())),'\n')
        print('The most common year of birth is {}.\n'.format(int(df['Birth Year'].mode()[0])),'\n')	
    else:
        print('Birth year data is not available in this dataset.\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def raw_data_view(df):
    """Displays raw bikeshare data, 5 lines at a time, on bikeshare users if the user wants."""
    print('\nRaw Data Viewing...\n')
    
    # Prompt user to view raw data
    viewraw = input('Would you like to view the raw data 5 lines at a time? Enter yes/y or no/n.\n').lower()
    if viewraw == 'yes' or viewraw == 'y':
        # If yes, view 1st 5 rows of raw data
        viewindex = 0
        numrows = df.shape[0]
        print(df[0:viewindex + 5])
        while True:
            # Prompt user to continue viewing raw data
            viewraw = input('\nWould you like to view the next 5 lines? Enter yes/y or no/n.\n').lower()
            if viewraw == 'yes' or viewraw == 'y':
                # If yes, view next 5 rows of raw data
                viewindex += 5
                print(df[viewindex:viewindex + 5])
            else:
                # If no, exit and move on
                break
                
            if viewindex + 5 >= numrows:
                print('\nYou\'ve reached the end of the dataset.\n')
                break
    else:
        # If no, exit and move on
        return
        
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters() # this one is complete, could make better with subfunction
        
        df = load_data(city, month, day) # this one is complete
        
        time_stats(df, city, month, day)
        
        station_stats(df) # this one is complete
        
        trip_duration_stats(df) # this one is complete
        
        user_stats(df) # this one is complete
        
        raw_data_view(df) # this one is complete

        restart = input('\nWould you like to restart? Enter yes/y or no/n.\n')
        if restart.lower() == 'yes' or restart.lower() == 'y':
            continue
        else:
            break


if __name__ == "__main__":
	main()
