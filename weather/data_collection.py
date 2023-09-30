import requests
import datetime
from weather.db import get_db

forecast_url = 'https://api.open-meteo.com/v1/forecast?latitude=40.015&longitude=-105.2706&start_date={start}&end_date={end}&hourly=temperature_2m&timezone=America%2FDenver'
def get_monthly_forecast():
    db = get_db()
    end = datetime.date.today()
    delta = datetime.timedelta(weeks=4)
    start = end - delta
    
    response = requests.get(forecast_url.format(start=start,end=end))
    data = response.json()
    times = data['hourly']['time']
    temps = data['hourly']['temperature_2m']

    for z in zip(times, temps):
        db.execute('INSERT OR REPLACE INTO forecast (time, temp) VALUES (?,?)', z) 

    db.commit()

history_url = 'https://archive-api.open-meteo.com/v1/archive?latitude=40.015&longitude=-105.2706&start_date={start}&end_date={end}&hourly=temperature_2m&timezone=America%2FDenver'
def get_monthly_history():
    db = get_db()
    end = datetime.date.today()
    delta = datetime.timedelta(weeks=4)
    start = end - delta
    
    response = requests.get(history_url.format(start=start,end=end))
    data = response.json()
    times = data['hourly']['time']
    temps = data['hourly']['temperature_2m']

    for z in zip(times, temps):
        db.execute('INSERT OR REPLACE INTO history (time, temp) VALUES (?,?)', z) 

    db.commit()

def init_app(app):
    with app.app_context():
        get_monthly_forecast()
        get_monthly_history()