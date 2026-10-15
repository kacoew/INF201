# Bruker funksjonen fra oppgave 1
df_temp = frost_request(
    client_id=client_id,
    sources="SN17850",
    elements="mean(air_temperature P1D)",
    referencetime="2025-01-01/2025-12-31"
)

df_rain = frost_request(
    client_id=client_id,
    sources="SN17850",
    elements="sum(precipitation_amount P1D)",
    referencetime="2025-01-01/2025-12-31"
)

fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Temperatur
ax[0].plot(df_temp['date'], df_temp['value'], color='red')
ax[0].set_title('Daglig gjennomsnittstemperatur i Ås 2025')
ax[0].set_ylabel('Temperatur i celsius')
ax[0].grid(True)

# Nedbør
ax[1].bar(df_rain['date'], df_rain['value'], color='blue')
ax[1].set_title('Daglig nedbør i Ås 2025')
ax[1].set_ylabel('Nedbør (mm)')
ax[1].grid(True)

plt.xlabel('Dato')
plt.show()