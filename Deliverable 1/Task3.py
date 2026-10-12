# Libraries needed (pandas is not standard and must be installed in Python)
import requests
import pandas as pd

# Leser client-ID`en min fra en fil utenfor repoet
with open('/Users/kachinaaschenberg/Documents/NMBU/INF201/Frost_API.txt', 'r') as infile:
    client_id = infile.read().strip()

# Function to get daily mean temperature from Frost API
def get_temperature(year):

    endpoint = "https://frost.met.no/observations/v0.jsonld"

    parameters = {
        "sources": "SN17850",
        "elements": "mean(air_temperature P1D)",
        "referencetime": f"{year}-01-01/{year}-12-31"
    }

    response = requests.get(
        endpoint,
        params=parameters,
        auth=(client_id, ""),
        timeout=30
    )

    response.raise_for_status()

    return response.json()

data_1925 = get_temperature(1925)
data_2025 = get_temperature(2025)


if __name__ == "__main__":

    data_1925 = get_temperature(1925)

    print("Status: Data hentet fra Frost API")
    print("Antall dataposter:", len(data_1925["data"]))






    # pip freeze ?
    # git clone? ghost
    # use english
     # type hints and docstrings
     # make branches and merge in git afterwards
     # commit push and pull often