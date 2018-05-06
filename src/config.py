from sqlalchemy import create_engine

username = ''
password = ''
client_id = ''
client_secret = ''
engine = create_engine("mysql+mysqldb://:" + '' + "@?charset=utf8mb4",
                       encoding='utf-8')
GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_MAPS_API_KEY = ''
OPbase_url = 'http://api.openweathermap.org/data/2.5/weather'
OPapi_key = ''  # << Get your API key (APPID) here: http://openweathermap.org/appid
updater = "368625073:"
dotaApi = ''

timezonekey = ''
