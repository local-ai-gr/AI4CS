import numpy as np
import pandas as pd
from prophet import Prophet
import warnings
warnings.filterwarnings("ignore")
import psycopg2
import os

def expand_data(dataframe, name):
    dataframe_copy = dataframe.copy()
    dataframe_copy['Time'] = pd.to_datetime(dataframe_copy['charging_hour'], format='%Y-%m-%d %H:%M:%S').dt.tz_localize(None)
    start_index = dataframe_copy.iloc[0, -1].date()
    end_index = dataframe_copy.iloc[-1, -1].date()
    indices = pd.date_range(start_index, end_index, freq='1H')
    dataframe_copy.set_index('Time', inplace=True)
    new_dataframe = pd.DataFrame(index=indices, data=dataframe_copy)
    new_dataframe['utilization'] = new_dataframe['utilization'].fillna(0.0)
    return new_dataframe


conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()
query = "SELECT distinct(location_id) FROM ht_cpn_station_data_hour"
cursor.execute(query)
location_ids = [r[0] for r in cursor.fetchall()]
cursor.close()

for location_id in location_ids:

    cursor = conn.cursor()
    query = "SELECT * FROM ht_cpn_station_data_hour WHERE location_id = " + str(location_id)
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    cursor.close()

    expanded_data = expand_data(df, "name1")
    data = expanded_data['utilization']
    data = data.to_frame()
    data.index.name = "Datetime"
    data_train = data.copy()

    data_train_prophet = data_train.reset_index() \
        .rename(columns={'Datetime':'ds',
                        'utilization':'y'})
    try:
        model = Prophet()
        model.fit(data_train_prophet)
        future = model.make_future_dataframe(periods=96, freq='h', include_history=False)
        forecast = model.predict(future)
        forecast['location_id']=str(location_id)
        forecast_values = forecast[['location_id','ds','yhat']]
        forecast_values.columns = ['location_id','ds','forecasted_utilization']
        from sqlalchemy import create_engine
        engine = create_engine('postgresql://'+os.getenv("POSTGRES_USER")+':'+os.getenv("POSTGRES_PASSWORD")+'@'+os.getenv("POSTGRES_HOST")+':5432/'+os.getenv("POSTGRES_DB"))
        forecast_values.to_sql('utilization_forecast', engine, if_exists='append', index=False)
    except:
        pass

conn.close()