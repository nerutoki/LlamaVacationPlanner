# Standard Libraries
import datetime
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st
from openmeteopy import OpenMeteo
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions

# Imported Libraries
from backend import analyze_text
from utils import remove_indentation, dict_weather_images, dict_season_images
from components.weather_section import weather_section_widget
from components.seasonal_event_section import seasonal_event_widget
from components.seasonal_food_section import seasonal_food_widget
from components.about_place_section import about_place_widget

################################################################################
# SET UP PAGE 
################################################################################
st.set_page_config(page_title="Vacation Planner", layout = "centered")

################################################################################
# TITLE TO PLATFORM
################################################################################
st.title(body=":red[Vacation Planner]")
st.divider()

################################################################################
# VARIABLES
################################################################################
show_content = False
## multiselect button for categories of interest
list_of_categories = ["Landmark", "Museums", "Film & Cinema", "Space", 
                      "Computer Science",  "Gaming", "Entertainment", 
                      "Restaurants", "Wildlife", "Local Festivities", 
                      "Cultural Performances", "Nightlife", "Botanical Gardens", 
                      "Art", "History", "Nature", "Sports"]

##weather variables for layout
season_choice = ["Spring", "Summer", "Autumn", "Winter"]


################################################################################
# INTRODUCTION TO PLATFORM
################################################################################
st.markdown('''
                A Vacation Planning Platform. By inputting the following:
                1) Your destination's name
                2) The date of arrival and departure 
                3) The interests you may have 
                4) The Season of Arrival
                
                It will give the following:
                1) An **introduction** to the location
                2) **Weather Data** of the first week (Limited to latitude and 
                    longitudes less than 90 and doesn't not exceed -90)
                3) **Recommended interest-related places** near and in your destination
                4) **Map** data of nearby places near your destination for visualization
                5) **Seasonal Events and Food** according to the season 
                ''')
## source code button
st.link_button(label="Source Code Can Be Found Here", 
                   url="https://github.com/nerutoki/LlamaVacationPlanner", 
                   type = "primary")
st.divider()

##bi-columns for user fill-in fields and intro to platform
intro_column, user_fields_column = st.columns(2)

################################################################################
# FIRST COLUMN WITH USER RIGHTS
################################################################################
with intro_column:
    ##usage rights text

        
    temp = '''This website uses the Large Language Model, **meta-llama's 
                Llama-3.2-11B-Vision-Instruct** from **Hugging Face** to determine results. 
                
                The weather data is collected by using the Open-Source Weather 
                API Open-Meteo. 
                
                 **Hugging Face API Token is required.**
                Permission for usage of **meta-llama Llama-3.2-11B-Vision-Instruct** model is required.
                
            Downloading the API found on their Github or making a request

                to **Open-Meteo API** is required.'''
    
    st.markdown(remove_indentation(temp))
    
    ##three buttons for usage rights
    st.link_button(label="Llama-3.2-11B-Vision-Instruct Model", 
                   url="https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct",
                   type = "primary")
    
    st.link_button(label = "Create Hugging Face API Token", 
                   url="https://huggingface.co/docs/hub/en/security-tokens",
                   type = "primary")
    
    st.link_button(label= "Open-Meteo Website", 
                   url="https://open-meteo.com/", 
                   type = 'primary')


################################################################################
# SECOND COLUMN: USER FILL-IN INTERFACE 
################################################################################
with user_fields_column:

    user_place = st.text_input(label= "Which Place Are You Going?",
                               type="default", 
                               placeholder="EX: Honolulu, Hawaii", 
                               label_visibility="visible")

    user_categories = st.multiselect(label="What Is Your Interest(s)?", 
                                     options=list_of_categories, 
                                     placeholder="Choose Option(s)",
                                     disabled=False, 
                                     label_visibility="visible")
    
    user_start_date = st.date_input(label="What Is Your Start Date?", 
                                    value="today", 
                                    min_value="today", 
                                    max_value=None, 
                                    key="start date", 
                                    help=None,  
                                    format="MM/DD/YYYY", 
                                    disabled=False, 
                                    label_visibility="visible")

    user_end_date = st.date_input(label="What Is Your End Date?", 
                                  value="today", 
                                  min_value="today", 
                                  max_value=None, 
                                  key="end date", 
                                  help=None, 
                                  format="MM/DD/YYYY", 
                                  disabled=False, 
                                  label_visibility="visible")

    user_season = st.multiselect(max_selections=1,
                                label= "Which Season?", 
                                options= season_choice, 
                                placeholder="Choose A Season", 
                                disabled=False, 
                                label_visibility="visible")
    
    HF_api_key = st.text_input(label='''Fill In Your Hugging Face API Key 
                               Below.''', 
                               type="password", 
                               placeholder="Hugging Face API Key Here")
    
    st.markdown("**Hugging Face Account required.**")


    ################################################################################ 
    # LLM CONTENT HERE
    ################################################################################
    if st.button("Start", type = 'primary'):

        ## all user fields must be filled in
        if (user_place != None and user_place != "") and (user_categories != [] and user_categories != None) and HF_api_key != None and HF_api_key != "" and user_season != None and user_season != []:

            ############################################################ 
            # LLM/API CONTENT HERE
            ############################################################ 

            ############################################################ 
            # RECOMMENDED NEARBY PLACES LLM
            ############################################################ 

            ## LLM's Output Format for Nearby Places
            format_nearby_places = '''
            {
            "Game Over": 
            {
            "name": "Game Over",
            "description": "A retro arcade and board game bar featuring consoles 
            such as Nintendo and PlayStation.",
            "latitude": 21.2813146,
            "longitude": -157.8565834
                },
                "Boby's Bakery": 
            {
            "name": "Boby's Bakery",
            "description": "A retro arcade and board game bar featuring consoles 
            such as Nintendo and PlayStation.",
            "latitude": 21.2813146,
            "longitude": -157.8565834
            }
            }
            '''

            ## LLM Prompt for Nearby Places
            prompt_nearby_places = f'''
                I need 5 or less real places nearby {user_place} that are 
                related to {user_categories} type(s) activities 
                in the {user_season[0]}.
                It must be returned with a name, a one sentence description, 
                the latititude coordinate, and the longitude coordinate 
                as the keys, and the answers as values in a json object.
                Name, description, latitude coordinate, and longitude coordinate 
                must be keys. 
                Only give me a one sentence description. 
                Only give me real places. 
                Do not use square brackets.
                Must be in the json string format {format_nearby_places} . 
                Return only a valid json string for output. Must be valid. 
                Do not return anything else. 
                Do not use Google Maps API.
                I need a proper json file that can be loaded.
                '''
            
            ## Store data from LLM Results if Exists for Nearby Places
            raw_data_nearby_places = analyze_text(HF_api_key = HF_api_key, 
                                                    prompt = prompt_nearby_places)
            
            df_nearby_places = pd.DataFrame(json.loads(raw_data_nearby_places))
            df_nearby_places = df_nearby_places.transpose()

            ## save coordinates for Weather and Map Sections.
            df_coordinates = df_nearby_places[['latitude', 'longitude']]

            ############################################################ 
            # WEATHER API
            ############################################################ 

            # Latitude, Longitude 
            longitude = df_coordinates['longitude'].iloc[0]
            latitude =  df_coordinates['latitude'].iloc[0]

            show_content = True
        else:
            # if fields were not completed fully
            st.error("Please check again if the fields are filled correctly.")
    else:
        ## remove all data from bottom from previous session
        st.empty()

################################################################################
# SHOWING BOTTOM CONTENTS
################################################################################

############################################################################
# MAIN TITLE 
############################################################################

if show_content == True:
        ##reformat date into MM/DD/YYYY
        start_date = datetime.datetime.strftime(user_start_date, "%m-%d-%Y")
        end_date = datetime.datetime.strftime(user_end_date, "%m-%d-%Y")

        #seasonal divider
        st.image(dict_season_images.get(user_season[0]))

        ## title
        st.header(f'{user_season[0]} Vacation At {user_place}')
        st.header(f'{start_date} to {end_date}')

        #seasonal divider
        st.image(dict_season_images.get(user_season[0]))

        ############################################################################
        # WEATHER SECTION
        ############################################################################
        weather_section_widget(latitude = latitude, longitude = longitude, user_season=user_season[0])

        #seasonal divider
        st.divider()

        ############################################################################
        # BASIC INFORMATION SECTION
        ############################################################################

        # main header
        st.header("Comprehensive Information Board")

        #seasonal divider
        st.divider()

        # title
        st.subheader(f":red-background[:red[About {user_place}]]")

        about_place_widget(user_place = user_place, HF_api_key=HF_api_key)

        st.image(dict_season_images.get(user_season[0]))

        ############################################################################
        # Places of Interest (Nearby Places)
        ############################################################################

        st.subheader(f''' :red-background[:red[Places of Interest in {user_place}]]''')

        ## show map data
        st.divider()
        st.map(df_coordinates, size = 1000, color = '#ffaa00')
        st.divider()

        ## show places of interest with 3 on left and 2 on right
        left_text_box, right_text_box = st.columns(2)

        with left_text_box:
            st.subheader(f'''
            :blue-background[{df_nearby_places["name"].iloc[0]}]
            ''')

            st.markdown(f'''
            {df_nearby_places["description"].iloc[0]}
            ''')

            st.subheader(f''' 
                            :green-background[{df_nearby_places["name"].iloc[1]}]
                            ''')

            st.markdown(f'''
                            {df_nearby_places["description"].iloc[1]}
                            ''')

            st.subheader(f'''
                            :red-background[{df_nearby_places["name"].iloc[2]}]
                            ''')

            st.markdown(f'''
                            {df_nearby_places["description"].iloc[2]}
                            ''')


        with right_text_box:
            st.subheader(f'''
                            :violet-background[{df_nearby_places["name"].iloc[3]}]
                            ''')

            st.markdown(f'''
                            {df_nearby_places["description"].iloc[3]}
                            ''')

            st.subheader(f''' 
                            :orange-background[{df_nearby_places["name"].iloc[4]}]
                            ''')

            st.markdown(f'''
                            {df_nearby_places["description"].iloc[4]}
                            ''')

        st.image(dict_season_images.get(user_season[0]))

        seasonal_food_widget(user_place = user_place, user_season=user_season[0], HF_api_key=HF_api_key)
        st.image(dict_season_images.get(user_season[0]))
        seasonal_event_widget(user_place = user_place, user_season=user_season[0], HF_api_key=HF_api_key)
        st.image(dict_season_images.get(user_season[0]))