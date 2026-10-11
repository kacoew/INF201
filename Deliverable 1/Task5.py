def moving_average(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    '''
    Beregner en glidende gjennomsnittstemperatur over et gitt antall dager

    Parametere:
        df (pd.DataFrame): En DataFrame som inneholder kolonner med dato 
        og verdier for den observasjonen man jobber med
        window (int): Antall dager som skal inngå i det glidende gjennomsnittet

    Returnerer:
        pd.DataFrame: En kopi av DataFrame-en med en ekstra kolonn
    '''
    df_ma = df.copy()
    df_ma['moving_avg'] = df_ma['value'].rolling(window=window).mean()
    return df_ma


df_temp_ma = moving_average(df_temp, window=7)


# Daglig temperatur som punkter
plt.scatter(df_temp_ma['date'], df_temp_ma['value'], color='red', s=10, label='Daglig temperatur')

# Moving average som linje
plt.plot(df_temp_ma['date'], df_temp_ma['moving_avg'], color='blue', linewidth=2, label='7-dagers moving average')

plt.title('Daglig temperatur og 7-dagers glidende gjennomsnitt (Ås 2025)')
plt.xlabel('Dato')
plt.ylabel('Temperatur i celsius')
plt.legend()
plt.grid(True)
plt.show()