# Imported libraries
import requests # HTTP library for making requests to the Frost API
import pandas as pd # Organizes and analyzes the weather data
import yaml # Structures data into a .yml file for easy reading and sharing

# Reads client ID from a file outside the repository
with open('/Users/kachinaaschenberg/Documents/NMBU/INF201/Frost_API.txt', 'r') as infile:
    client_id = infile.read().strip()

def frost_request(client_id: str, sources: str, elements: str, referencetime: str) -> pd.DataFrame: 
    '''
    Gets data from the Frost API and returns a pandas DataFrame in YAML format
    (same function as in Task 1, based on MET's Python example)
    Args:
        client_id (str): Client ID for the Frost API.
        sources (str): Station ID, e.g., 'SN17850'.
        elements (str): Element, e.g., 'mean(air_temperature P1D)'
        referencetime (str): Time range, e.g., '2025-01-01/2025-12-31'.
    Returns:
        pd.DataFrame: DataFrame containing the requested data from the Frost API.
    '''

    # Define the endpoint and parameters for the API request
    endpoint = 'https://frost.met.no/observations/v0.jsonld' 
    parameters = {
        'sources': sources,
        'elements': elements,
        'referencetime': referencetime,
        'timeoffsets': 'default',
    }

    # HTTP GET request to Frost API with authentication using the client ID
    r = requests.get(endpoint, params=parameters, auth=(client_id, ''))

    # Check if the request was successful (status code 200)
    if r.status_code != 200:
        print(f'Feil {r.status_code}: {r.json()}')
        return None

    # Check if the response contains data
    records = [] # List to store the records from the API response
    for item in r.json()['data']: # Iterate through each item in the 'data' field of the JSON response
        records.append((item['referenceTime'], item['observations'][0]['value'])) # Append a tuple of (date, value) to the records list

    df = pd.DataFrame(records, columns=['date', 'value']) # Create a pandas df from the records list
    df['date'] = pd.to_datetime(df['date']) # Convert the 'date' column to datetime format for an easier analysis
    return df

def find_heatwaves(df: pd.DataFrame, threshold: float = 27.0, min_days: int = 5) -> list:
    '''
    Finds periods where the maximum temperature is >= threshold for at least min_days consecutive days
    Args:
        df (pd.DataFrame): DataFrame containing the temperature data with 'date' and 'value' columns.
        threshold (float): Temperature threshold to define a heatwave (default is 27.0 degrees).
        min_days (int): Minimum number of consecutive days to define a heatwave (default is 5 days).
    Returns:
        list: List of (start_date, end_date) for each heatwave
    '''

    # Filter the df to only include days temperature is above the threshold
    hot = df[df['value'] >= threshold].sort_values('date')

    # Hot days get put into periods of consecutive days (group 1, group 2, etc.)
    new_period = hot['date'].diff() != pd.Timedelta(days=1) # New period starts when its more than one day since the previous hot day 
    period_id = new_period.cumsum() # assigns group numbers to each period of consecutive hot days


    # Create a list of heatwaves that are at least 5 days long
    heatwaves = []
    for _, period in hot.groupby(period_id): # Iterate through each group of consecutive hot days
        if len(period) >= min_days: # If the period is at least 5 days long, add it to the heatwaves list
            heatwaves.append((period['date'].iloc[0], period['date'].iloc[-1])) # Append a tuple of (start_date, end_date) to the heatwaves list
    return heatwaves

def count_heatwaves(client_id: str, station_id: str, station_name: str, year: int, filename: str = None) -> int: 
    '''
    Counts the number of heatwaves for a station in a given year and writes a summary to a YAML file
    Args:
        client_id (str): Client ID for the Frost API.
        station_id (str): Station ID, e.g., 'SN17850'.
        station_name (str): Name of the station, e.g., 'Ås'.
        year (int): Year for which to count heatwaves, e.g., 2025
        filename (str): Optional filename for the YAML summary file. If None, a default name
    Returns:
        int: Number of heatwaves found for the specified station and year.
    '''

    # Get the maximum temperature data for the specified station and year
    df_max = frost_request(client_id, station_id, 'max(air_temperature P1D)', 
                           f'{year}-01-01/{year}-12-31') 
    if df_max is None:
        return 0

    # Find heatwaves in the data
    heatwaves = find_heatwaves(df_max)

    # Write a summary of the heatwaves to a YAML file, including set parameters and the number of heatwaves found
    summary = {
        'dates': [f'{start:%Y-%m-%d} - {end:%Y-%m-%d}' for start, end in heatwaves],
        'station_id': station_id,
        'station_name': station_name,
        'year': year,
    }
    # Creates a default filename based on the station ID and year if no name is provided
    if filename is None:
        filename = f'heatwaves_{station_id}_{year}.yml'

    # Write the summary to a YAML file
    with open(filename, 'w') as outfile:
        yaml.dump(summary, outfile)

    # Return the number of heatwaves found
    return len(heatwaves)

# Example usage of the count_heatwaves function
n = count_heatwaves(client_id, 'SN17850', 'Ås', 2025)
print(f'Antall hetebølger i Ås i 2025: {n}')
