 # Standard Libraries
import datetime
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st

from utils import season_image,  weather_image, remove_indentation
from backend import analyze_text          


def seasonal_food_widget(user_place, user_season, HF_api_key):
    ############################################################ 
    # SEASONAL FOOD LLM 
    ############################################################ 
    format_seasonal_food = '''
        ### Papaya
        \n *A fruit that is found in the tropical areas. It is grown 
        on a tree.*
        \n The best way to eat this fruit is raw or by using it in a 
        papaya salad.
        '''

    prompt_seasonal_food = f'''
        Look up 3 seasonal food in {user_place} during {user_season}.
        Give me the name of the food and a short description. It must 
        also have the preferred way to eat it and some more in-depth 
        information about it. 
        The format should look like this with more information: 
        {format_seasonal_food} 
        It must follow the format.
        Do not output anything else.
        I need 3 seasonal food.
        '''
    # Store data from LLM for Seasonal Food
    raw_data_seasonal_food = remove_indentation(analyze_text(HF_api_key, 
                                            prompt = prompt_seasonal_food))

    ############################################################################
    # Seasonal Food 
    ############################################################################

    st.subheader(f" :red-background[:red[{user_season[0]} Seasonal Food]]")

    st.write(raw_data_seasonal_food)

    season_image(user_season[0])