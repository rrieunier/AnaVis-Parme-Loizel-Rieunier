from zipfile import ZipFile
import pandas as pd
import datetime

data = ZipFile('data/brut.zip', 'r')

stations = pd.read_csv(data.open('brut/bicincitta_parma_summary.csv'), sep=';')
status = pd.read_csv(data.open('brut/status_bicincitta_parma.csv'),
                     sep=';',
                     names="date;Station;Status;Nombre de vélos disponibles;Nombre d'emplacements disponibles".split(
                         ';'),
                     parse_dates=["date"]).head(
    n=10000)
weather = pd.read_csv(data.open('brut/weather_bicincitta_parma.csv'),
                      sep=';',
                      names="Timestamp;Status;Clouds;Humidity;Pressure;Rain;WindGust;WindVarEnd;WindVarBeg;WindDeg;WindSpeed;Snow;TemperatureMax;TemperatureMin;TemperatureTemp".split(
                          ';'),
                      parse_dates=["Timestamp"]).head(
    n=10000)

# Removes numbering in station names
stations['station'] = stations['station'].apply(lambda x: x[4:])

velos = []

weather = weather.set_index('Timestamp').resample('10Min', label='right', closed='right').last().dropna().reset_index()

for key, df in status.groupby("Station"):
    velos.append(df.set_index('date').resample('10min', label='right', closed='right').last().dropna().reset_index())
