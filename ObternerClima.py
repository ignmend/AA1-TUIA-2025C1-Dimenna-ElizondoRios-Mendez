import requests
import pandas as pd

def obtener_clima_df(lat, lon, start_date, end_date):
    """
    Devuelve un DataFrame con datos horarios de clima (temperatura, humedad, lluvia)
    para la ubicación y fechas indicadas.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "America/New_York"  # cambia a la zona de NY
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    df = pd.DataFrame({
        "datetime": pd.to_datetime(data["hourly"]["time"]),
        "temperature": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
        "rain_bool": [True if r > 0 else False for r in data["hourly"]["precipitation"]]
    })
    return df

# Lista de años que querés
anios = [2015, 2009, 2014, 2011, 2012, 2010, 2013]

# Coordenadas de NYC
lat, lon = 40.7128, -74.0060

# Descargar y concatenar
dfs = []
for anio in anios:
    start_date = f"{anio}-01-01"
    end_date = f"{anio}-12-31"
    print(f"Descargando {anio}...")
    df_anio = obtener_clima_df(lat, lon, start_date, end_date)
    df_anio["year"] = anio
    dfs.append(df_anio)

df_ny = pd.concat(dfs, ignore_index=True)
print(df_ny.head())
df_ny.info()