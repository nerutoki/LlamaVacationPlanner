 # Standard Libraries
import datetime
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st

from utils import season_image,  weather_image, remove_indentation
from backend import analyze_text       

def about_place_widget(user_place, user_season, HF_api_key):
    about_prompt = f'''Tell me about {user_place} in five sentences and the 
    famous things about that place in a string.'''

    response_info = remove_indentation(analyze_text(HF_api_key, prompt = about_prompt))
    ## if all LLMs and API successfully is stored, give permission to 
    # show the rest of the page.
    show_content = True