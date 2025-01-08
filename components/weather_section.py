# Standard Libraries
import datetime
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st
from openmeteopy import OpenMeteo
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions

# Import 
from utils import dict_season_images, dict_weather_images

#Variables
weather_choice = ["Cloudy", "Rain", "Snow", "Sunny", "Thunderstorm"]

weather_code_dict = {'0': weather_choice[3], ##Sunny
                      '1': weather_choice[3],  ##Sunny
                      '2': weather_choice[0],  ##Cloudy
                      '3': weather_choice[0],  ##Cloudy
                      '45': weather_choice[0],  ##Cloudy
                      '48': weather_choice[0],  ##Cloudy
                      '51': weather_choice[1],  ##Rain
                      '53': weather_choice[1],  ##Rain
                      '55': weather_choice[1],  ##Rain
                      '56': weather_choice[1],  ##Rain
                      '57': weather_choice[1],  ##Rain
                      '61': weather_choice[1],  ##Rain
                      '63': weather_choice[1],  ##Rain
                      '65': weather_choice[1],  ##Rain
                      '66': weather_choice[1],  ##Rain
                      '67': weather_choice[1],  ##Rain
                      '71': weather_choice[2],  ##Snow
                      '73': weather_choice[2],  ##Snow
                      '75': weather_choice[2],  ##Snow
                      '77': weather_choice[2],  ##Snow
                      '80': weather_choice[1],  ##Rain
                      '81': weather_choice[1],  ##Rain
                      '82': weather_choice[1],  ##Rain
                      '85': weather_choice[2],  ##Snow
                      '86': weather_choice[2],  ##Snow 
                      '95': weather_choice[4],  ##Thunderstorm
                      '96': weather_choice[4],  ##Thunderstorm
                      '99': weather_choice[4],  ##Thunderstorm 
                      }

show_weather = False

def weather_section_widget(latitude, longitude, user_season):
    """ Take in the latitude and longitude to produce the first week's weather
    of the place's coordinates.
        
    Args:
        latitude (str): Latitude coordinates of the place
        longitude (str): Longitude coordinates of the place
        user_season (str): the season when the user comes in for 
                            dynamically creating dividers
        
    Return: 
        response (str): Answer from LLM

    """
   
    st.header("First Week Weather Forecast")
    #seasonal divider
    st.divider()

    ##api cannot accept under -90 or above 90
    if (longitude < 90 and longitude > -90) and (latitude < 90 and latitude > -90):
        daily = DailyForecast()
        options = ForecastOptions(latitude,longitude)

        raw_data_open_meteo_weather = OpenMeteo(options=options, 
                                            hourly = None, 
                                            daily = daily.apparent_temperature_max()) 
        raw_data_open_meteo_weather = OpenMeteo(options=options, 
                                        hourly = None, 
                                        daily = daily.weathercode())

        # Download data
        df_weather_data = raw_data_open_meteo_weather.get_pandas()


        weather_columns = st.columns(7, border = True)

        for i, column in enumerate(weather_columns):
                column.image(dict_weather_images.get(weather_code_dict.get(str(df_weather_data.iloc[i,1]))))
                column.markdown(f" *{str(int((df_weather_data.iloc[i,0]*1.8+32)))} \n°F*")
                column.write(datetime.datetime.strptime(df_weather_data.index[i],"%Y-%m-%d").strftime("%m-%d-%Y"))
    else:
        st.write("Weather Data cannot be shown for current location.")

