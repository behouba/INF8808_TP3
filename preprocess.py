'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    dataframe['Date_Plantation'] = pd.to_datetime(dataframe['Date_Plantation'])
    return dataframe


def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    dataframe = dataframe[(dataframe['Date_Plantation'].dt.year >= start) & 
                          (dataframe['Date_Plantation'].dt.year <= end)]
    return dataframe


def summarize_yearly_counts(dataframe):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    dataframe['Year'] = dataframe['Date_Plantation'].dt.year
    yearly_df = dataframe.groupby(['Arrond_Nom', 'Year']).size().reset_index(name='Counts')
    return yearly_df


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    restructured = yearly_df.pivot(index='Arrond_Nom', columns='Year', values='Counts')
    restructured = restructured.fillna(0)
    return restructured


def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    filtered = dataframe[(dataframe['Arrond_Nom'] == arrond) &
                         (dataframe['Date_Plantation'].dt.year == year)]
    daily_counts = filtered.groupby('Date_Plantation').size().reset_index(name='Counts')

    if not daily_counts.empty:
        full_range = pd.date_range(
            start=daily_counts['Date_Plantation'].min(),
            end=daily_counts['Date_Plantation'].max()
        )
        daily_counts = daily_counts.set_index('Date_Plantation').reindex(full_range, fill_value=0).rename_axis('Date_Plantation').reset_index()

    return daily_counts
