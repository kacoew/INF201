# Imported libraries
import requests  # HTTP library for making requests to the Frost API
import pandas as pd  # Organizes and analyzes the weather data
import matplotlib.pyplot as plt  # Plots the temperature data
import matplotlib.dates as mdates  # Formats dates on the x-axis

# Reads client ID from a file outside the repository
with open('/Users/kachinaaschenberg/Documents/NMBU/INF201/Frost_API.txt', 'r') as infile:
    client_id = infile.read().strip()


def frost_request(client_id: str, sources: str, elements: str,
                  referencetime: str) -> pd.DataFrame | None:
    '''
    Gets observations from the Frost API and returns them as a pandas DataFrame.
    Based on MET's Python example: https://frost.met.no/python_example.html

    Args:
        client_id (str): Personal client ID for the Frost API.
        sources (str): Station ID, e.g. 'SN17850'.
        elements (str): Element to fetch, e.g. 'mean(air_temperature P1D)'.
        referencetime (str): Time range, e.g. '2025-01-01/2026-01-01'.
            The end date is not included.

    Returns:
        pd.DataFrame | None: DataFrame with the columns 'date' and 'value',
        or None if the request failed.
    '''
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': sources,
        'elements': elements,
        'referencetime': referencetime,
        'timeoffsets': 'default',  # only one (the official) value per day
    }

    r = requests.get(endpoint, params=parameters, auth=(client_id, ''))

    if r.status_code != 200:
        print(f'Error {r.status_code}: {r.json()}')
        return None

    records = []
    for item in r.json()['data']:
        records.append((item['referenceTime'], item['observations'][0]['value']))

    df = pd.DataFrame(records, columns=['date', 'value'])
    df['date'] = pd.to_datetime(df['date'])
    return df


def get_mean_temperature(client_id: str, station_id: str, year: int) -> pd.DataFrame | None:
    '''
    Helper function that calls frost_request with the right parameters.
    Gets the daily mean air temperature for one station a whole year.

    Args:
        client_id (str): Personal client ID for the Frost API.
        station_id (str): Station ID, e.g. 'SN17850'.
        year (int): Year to get data from, e.g. 1925.

    Returns:
        pd.DataFrame | None: DataFrame with the columns 'date' and 'value',
        or None if the request failed.
    '''
    return frost_request(client_id, station_id, 'mean(air_temperature P1D)',
                         f'{year}-01-01/{year + 1}-01-01')


def summary_table(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    '''
    Makes a summary table with mean, median, min and max temperature for each year in the dictionary.

    Args:
        data (dict[str, pd.DataFrame]): Maps a label like '1925' to a DataFrame
            with a 'value' column.

    Returns:
        pd.DataFrame: One row per label and one column per statistic,
        rounded to one decimal.
    '''

    # Create a dictionary to hold the summary statistics for each label
    rows = {}
    for label, df in data.items(): # Iterate through each label and its corresponding df in the dictionary
        rows[label] = {
            'Mean': df['value'].mean(),
            'Median': df['value'].median(),
            'Min': df['value'].min(),
            'Max': df['value'].max(),
        } 
    return pd.DataFrame(rows).T.round(1) 


# Get the data for both years
df_1925 = get_mean_temperature(client_id, 'SN17850', 1925)
df_2025 = get_mean_temperature(client_id, 'SN17850', 2025)

# Plot both years on the same calendar axis (month), so they can be compared 
fig, ax = plt.subplots(figsize=(12, 5)) # Gives a figure and axis for the plot with a set size
ax.plot(df_1925['date'].apply(lambda d: d.replace(year=2000)), df_1925['value'], color='tab:blue', label='1925', linewidth=1.2) # Plot the temperature values for each year with  color and label
ax.plot(df_2025['date'].apply(lambda d: d.replace(year=2000)), df_2025['value'], color='tab:red', label='2025', linewidth=1.2) # Plot the temperature values for each year with color and label


ax.xaxis.set_major_locator(mdates.MonthLocator()) # Set the x-axis to each month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%B')) # Format the x-axis labels to show the whole month name 
ax.axhline(0, color='grey', linewidth=0.8)  # line at 0 °C 
ax.set_title('Daily mean air temperature in Ås: 1925 vs 2025') # Set the title of the plot
ax.set_xlabel('Month') # Set the label for the x-axis
ax.set_ylabel('Temperature (°C)') # Set the label for the y-axis
ax.grid(True, alpha=0.3) # Enable grid lines on the plot with a specified transparency
ax.legend() # Add a legend to the plot to identify the lines for each year
plt.tight_layout() # Prevent overlapping elements
plt.show() # Display the plot

# Summary table for both years
print(summary_table({'1925': df_1925, '2025': df_2025}))




# pip freeze ?
# git clone? ghost
# use english
# type hints and docstrings
# make branches and merge in git afterwards
# commit push and pull often