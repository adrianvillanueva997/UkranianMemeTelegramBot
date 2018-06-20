from sqlalchemy import create_engine

username = ''
password = ''
client_id = ''
client_secret = ''
engine = create_engine("mysql+mysqldb://" + '' + "@?charset=utf8mb4",
                       encoding='utf-8')
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_MAPS_API_KEY = ''
OPbase_url = 'http://api.openweathermap.org/data/2.5/weather'
OPapi_key = ''  # << Get your API key (APPID) here: http://openweathermap.org/appid
updater = ":"
dotaApi = ''
TIMEZONEDB_URL = r'http://api.timezonedb.com/v2/get-time-zone'
timezonekey = ''
joke_url = r'https://icanhazdadjoke.com/slack'
simpsons_url = r'https://frinkiac.com/api/random'
