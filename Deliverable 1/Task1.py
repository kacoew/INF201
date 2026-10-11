import requests
import pandas as pd
import matplotlib.pyplot as plt

# Henter client_id som er lagret utenfor REPO
with open('C:/Users/Selin/OneDrive/NMBU/2.år/INF201/Frost_API.txt', 'r') as infile:
    client_id = infile.read().strip()


def frost_request(client_id: str, sources: str, elements: str, referencetime: str) -> pd.DataFrame:
    '''
    Henter data fra Frost API og returnerer en pandas DataFrame

    Parameters:
        client_id (str): API-nøkkelen din fra frost.met.no
        sources (str): Stasjons-ID, f.eks. 'SN17850'
        elements (str): Element, f.eks. 'mean(air_temperature P1D)'
        referencetime (str): Tidsrom, f.eks. '2025-01-01/2025-12-31'
    '''

    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
    'sources': sources,
    'elements': elements,
    'referencetime': referencetime,
    }
    # Henter data fra Frost API
    r = requests.get(endpoint, params=parameters, auth=(client_id, ''))

    # Sjekk statuskode
    if r.status_code != 200:
        print(f"Feil {r.status_code}: {r.json()}")
        return None

    data = r.json()

    # Sjekk om data finnes
    if "data" not in data:
        print("Ingen data mottatt.")
        return None

    # Plukke ut alle observasjoner
    records = []
    for item in data["data"]:
        date = item["referenceTime"]
        temp = item["observations"][0]["value"]
        records.append((date, temp))

    df = pd.DataFrame(records, columns=["date", "temperature"])

    # Konverter dato til datetime
    df["date"] = pd.to_datetime(df["date"])

    return df


# Kaller funksjonen
df = frost_request(
    client_id=client_id,
    sources="SN17850",
    elements="mean(air_temperature P1D)",
    referencetime="2025-01-01/2025-12-31"
)

# plotter grafen
plt.plot(df['date'], df['temperature'], color='blue')
plt.title('Daglig gjennomsnittstemperatur i Ås 2025')
plt.xlabel('Dato')
plt.ylabel('Temperatur i celsius')
plt.grid(True)
plt.show()

# Lager en oversiktlig tabell
summary = {
    "Mean": df["temperature"].mean(),
    "Median": df["temperature"].median(),
    "Min": df["temperature"].min(),
    "Max": df["temperature"].max(),
}

summary_df = pd.DataFrame(summary, index=[0])
print(summary_df)

# Husk å referer til met for måten man henter infoen på, kildereferering
