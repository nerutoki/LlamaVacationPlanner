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
from utils import remove_indentation, weather_image, season_image

weather_choice = ["Cloudy", "Rain", "Snow", "Sunny", "Thunderstorm"]
season_choice = ["Spring", "Summer", "Autumn", "Winter"]
    
################################################################################
# SET UP PAGE 
################################################################################
st.set_page_config(page_title="Vacation Planner", layout = "centered")

# making center alignment titles
st.markdown("""
            <style>
            .center-title 
            {
            text-align: center;
            font-size: 10px;
            font-weight: bold;
            margin: 0;   
            padding: 0;
            }
            </style>""", 
            unsafe_allow_html=True)

################################################################################
# TITLE TO PLATFORM
################################################################################
st.title(body=":red[Vacation Planner]")
st.divider()

################################################################################
# VARIABLES
################################################################################
## control layout if LLM or Weather API is sucessful.
show_content = False
show_weather = False

## multiselect button for categories of interest
list_of_categories = ["Landmark", "Museums", "Film & Cinema", "Space", 
                      "Computer Science",  "Gaming", "Entertainment", 
                      "Restaurants", "Wildlife", "Local Festivities", 
                      "Cultural Performances", "Nightlife", "Botanical Gardens", 
                      "Art", "History", "Nature", "Sports"]

##weather variables for layout
weather_choice = ["Cloudy", "Rain", "Snow", "Sunny", "Thunderstorm"]
season_choice = ["Spring", "Summer", "Autumn", "Winter"]

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

 


################################################################################
# INTRODUCTION TO PLATFORM
################################################################################
st.markdown('''
                A Vacation Planning Platform. By inputting the following:
                1) Your destination name, 
                2) The day you land and leave the destination
                3) The type of experience you desire
                4) The season 
                
                It will give the following:
                1) An **introduction** to the location
                2) **Weather data** of the first week (Limited to latitude and 
                    longitudes less than 90 and doesn't not exceed -90)
                3) **Recommended interest-related places** near and in your destination
                4) **Map** data of the nearby places for visualization
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

        
    temp = '''    This website uses the Large Language Model, **meta-llama's 
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
                in the {user_season}.
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

                show_weather = True

            ############################################################ 
            # SEASONAL EVENTS LLM
            ############################################################
            format_seasonal_event = '''
            ### Van Gogh Art Gallery
            \n*A famous art gallery where many works of Van Gogh are showcased 
            within the museum. It houses the most Van Gogh pieces of artwork. 
            It has seasonal events across the whole range of seasons. It is 
            recommended to go there with a friend or two.*
            \n**Location:** It is located in Waikiki district, on the 
            south side of Oahu. 
            \n**Time Duration:** It is normally held during the spring. 
            The museum is opened until 10:00 pm.
            \n**Routes:** The best possible route is by car, but walking 
            from the bus stop is also an option.
            \n**Cost:** It is free to enter.
            '''

            prompt_seasonal_event = f'''
                Look up 3 seasonal popular event or activities in {user_place} 
                during {user_season}.
                I need the name as the subheader, and in-depth basic 
                information,location of event, time duration, routes, and 
                cost as body text as a string.
                I need them formatted like this: {format_seasonal_event} in 
                a string. It must follow the format.
                Do not output anything else. 
                I need 3 events.
                '''
            
            ## Store data from LLM Results if Exists for Seasonal Events
            raw_data_seasonal_event = remove_indentation(analyze_text(HF_api_key = HF_api_key, 
                                                   prompt = prompt_seasonal_event))


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

          ############################################################ 
          #ABOUT THE PLACE LLM
          ############################################################ 
            about_prompt = f'''Tell me about {user_place} in five sentences and the 
            famous things about that place in a string.'''

            response_info = remove_indentation(analyze_text(HF_api_key, prompt = about_prompt))
            ## if all LLMs and API successfully is stored, give permission to 
            # show the rest of the page.
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

#if LLM successfully was stored in a var.
if show_content == True:

    ############################################################################
    # MAIN TITLE 
    ############################################################################

    ##reformat date into MM/DD/YYYY
    start_date = datetime.datetime.strftime(user_start_date, "%m-%d-%Y")
    end_date = datetime.datetime.strftime(user_end_date, "%m-%d-%Y")

    #seasonal divider
    season_image(user_season[0])

    ## title
    st.header(f'{user_season[0]} Vacation At {user_place}')
    st.header(f'{start_date} to {end_date}')

    #seasonal divider
    season_image(user_season[0])

    ############################################################################
    # WEATHER SECTION
    ############################################################################

    st.header("First Week Weather Forecast")

    #seasonal divider
    season_image(user_season[0])

    if (show_weather == True):

        weather_columns = st.columns(7, border = True)

        for i, column in enumerate(weather_columns):
                print("Data in Pandas", df_weather_data.iloc[i,1])
                print("Name in Dictionary for Weathers", weather_code_dict.get(str(df_weather_data.iloc[i,1])))
                print(type(weather_code_dict.get(str(df_weather_data.iloc[i,1]))))


                # column.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhaVU8_bPnnrsJWJZrZOXpsmYfwy9xRhRCdO2zseln57YdUOE_-ClZOIDzUZ-pzanSYiEIgiUc7jauImyXPkE0v5c4XP4Fr8BwkDvseWpThBgZ8iMZtV2VYkyBB4UJ11bwc_AvyJz13ohk/s800/tenki_mark05_kumori.png")
                column.image(weather_image(weather_code_dict.get(str(df_weather_data.iloc[i,1]))))

                column.markdown(f" *{str(int(df_weather_data.iloc[i,0])*1.8+32)}\n°F* ")
                column.write(datetime.datetime.strptime(df_weather_data.index[i],"%Y-%m-%d").strftime("%m-%d-%Y"))
    else:
        st.write("Weather Data cannot be shown for current location.")

    #seasonal divider
    season_image(user_season[0])

    ############################################################################
    # BASIC INFORMATION SECTION
    ############################################################################
    
    # main header
    st.header("Comprehensive Information Board")
    # st.markdown(f"""<h2 class="center-title">Comprehensive Information Board</h2> """, 
    #             unsafe_allow_html=True)

    #seasonal divider
    season_image(user_season[0])

    # title
    st.subheader(f":red-background[:red[About {user_place}]]")

    st.write(response_info)

    season_image(user_season[0])

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
    
    #seasonal divider
    season_image(user_season[0])

    ############################################################################
    # Seasonal Food 
    ############################################################################
    
    st.subheader(f" :red-background[:red[{user_season[0]} Seasonal Food]]")

    st.write(raw_data_seasonal_food)

    season_image(user_season[0])

    ############################################################################
    # Seasonal Event
    ############################################################################
    st.subheader(f" :red-background[:red[{user_season[0]} Seasonal Event]]")

    st.write(raw_data_seasonal_event)

    season_image(user_season[0])