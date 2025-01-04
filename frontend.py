# Standard Libraries
import time 
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st

# Imported Libraries
from backend import analyze_text

## functions goes here

def get_df_from_LLM(prompt, HF_api_key):
        raw_data = analyze_text(HF_api_key = HF_api_key, prompt = prompt)

        df = pd.DataFrame(json.loads(raw_data))

        df = df.transpose()

        return df

############################################################

# SET UP PAGE SHENANIGANS 
############################################################

st.set_page_config(page_title="Vacation Planner", layout = "wide")
st.title(body=":red[Vacation Planner]")
st.divider()
progress_done = False
show_content = False

# ###########################################################

# ##LLM CODE ACTUALLY HERE
# ###########################################################
# #CURSE THE  MAIN #########


col1, col2 = st.columns(2)

with col1:
    
    st.markdown('''
                A Vacation Planning Website. By giving a place's name and 
                a category, it will return five places in the area that may align with your interest(s).

                This website uses the Large Language Model, meta-llama's Llama-3.2-11B-Vision-Instruct from Hugging Face to determine results. 

                Hugging Face API Token is required. Permission for
                usage of meta-llama's Llama-3.2-11B-Vision-Instruct model is required.
                ''')
    
    st.link_button(label="Source Code Found Here", url="https://github.com/nerutoki/LlamaVacationPlanner", type = "secondary")

    # col3, col4 = st.columns(2)
    
    # col3.link_button(label="Llama-3.2-11B-Vision-Instruct", url="https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct",
    #                  type = "secondary")
    # col4.link_button(label = "Create Hugging Face API Token", url="https://huggingface.co/docs/hub/en/security-tokens",
    #                  type = "secondary")

list_of_categories = ["Landmark", "Museums", "Film & Cinema", "Space", "Computer Science",  "Gaming", "Entertainment", "Restaurants", "Wildlife", "Local Festivities", "Cultural Performances", "Nightlife", "Botanical Gardens", "Art", "History", "Nature", "Sports"]
    
with col2:

    user_place = st.text_input(label= "Insert Place Here",
                type="default", placeholder="Insert City Here EX: Honolulu, Hawaii/Brooklyn", label_visibility="visible")

    user_preferred_categories = st.multiselect(label="Interests/Category", options=list_of_categories, placeholder="Choose Option(s)",disabled=False, label_visibility="visible")

    HF_api_key = st.text_input(label=''' # **Hugging Face Account required.**
                  ''', type="password", placeholder="Token Here")
    
    user_start_date = st.date_input(label="Start Date", value="today", min_value=None, max_value=None, key="start date", help=None, on_change=None, args=None, kwargs=None,  format="MM/DD/YYYY", disabled=False, label_visibility="visible")

    user_end_date = st.date_input(label="End Date", value="today", min_value=None, max_value=None, key="end date", help=None, on_change=None, args=None, kwargs=None,  format="MM/DD/YYYY", disabled=False, label_visibility="visible")

    user_preferred_season = st.multiselect(max_selections=1,label="Seasons", options=["Spring", "Summer", "Autumn", "Winter"], placeholder="Choose Option(s)",disabled=False, label_visibility="visible")
    

    if st.button("Start", type = 'primary'):

        if (user_place != None and user_place != "") and (user_preferred_categories != [] and user_preferred_categories != None) and (HF_api_key != None and HF_api_key != ""):
            
            format = '''
            {
            "Game Over": 
            {
            "name": "Game Over",
            "description": "A retro arcade and board game bar featuring consoles such as Nintendo and PlayStation.",
            "latitude": 21.2813146,
            "longitude": -157.8565834
             },
             "Boby's Bakery": 
                {
                "name": "Boby's Bakery",
                "description": "A retro arcade and board game bar featuring consoles such as Nintendo and PlayStation.",
                "latitude": 21.2813146,
                "longitude": -157.8565834
                }
                }
            '''

            prompt = f'''
                I need 5 or less real places nearby {user_place} that are related to 
                {user_preferred_categories} type(s) activities. It must be returned 
                with a name, a one sentence description, the latititude coordinate, and the 
                longitude coordinate as the keys, and the answers as values in a json object.
                Name, description, latitude coordinate, and longitude coordinate must be keys. 
                Only give me a one sentence description. 
                Only give me real places. 
                Do not use square brackets.
                Must be in the json string format {format} . 
                Return only a valid json string for output. Must be valid. Do not return anything else. 
                Do not use Google Maps API.
                    '''
            
            raw_data = format
            
        #     raw_data = analyze_text(HF_api_key = HF_api_key, prompt = prompt)
        
        #     print(raw_data)
            show_content = True
        else:
            st.error("Please check again if the fields are filled correctly.")
    else:
        st.empty()



if show_content == True:

        ## insert new code here## insert new code here## insert new code here## insert new code here
        ## insert new code here## insert new code here## insert new code here## insert new code here## insert new code here
        ## insert new code here## insert new code here## insert new code here## insert new code here## insert new code here## insert new code here
        ## insert new code here## insert new code here## insert new code here## insert new code here## insert new code here
        ## insert new code here## insert new code here## insert new code here## insert new code here## insert new code here


        if user_preferred_season != None and user_preferred_season != []:

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
                </style>""", unsafe_allow_html=True)


                st.markdown(f"""<h2 class="center-title">{user_preferred_season[0]} AT {user_place}</h2> """ , unsafe_allow_html=True)
                st.markdown(f"""<h2 class="center-title">From {user_start_date} to {user_end_date}</h2> """ , unsafe_allow_html=True)
                st.divider()

                st.image(f"./irasutoya_images/{user_preferred_season[0].lower()}_season.png")
                st.header(f"{user_preferred_season[0]} Seasonal Food")

                # seasonal_food_format = '''
                # {
                # “May 3rd, 2024”
                # {
                # "Date": “May 3rd, 2024”,
                # “Day Temperature": “75°F”,
                # “Weather”: “Sunny",
                # },
                # {
                # “May 4th, 2024”
                # {
                # "Date": “May 3rd, 2024”,
                # “Day Temperature": “75°F”,
                # “Weather”: “Cloudy",
                # }
                # }
                # '''

                seasonal_food_prompt = f'''Look up 3 seasonal food in {user_place} during {user_preferred_season}.
                Give me the name of the food and a short description. The short description must have the preferred way to eat it and basic information about it.  Do not output anything else.
                I need 3 seasonal food.
                        '''

                # seasonal_food_raw_data = analyze_text(HF_api_key, prompt = seasonal_food_prompt)

                st.write(seasonal_food_raw_data)

                st.image(f"./irasutoya_images/{user_preferred_season[0].lower()}_season.png")

                st.header(f"{user_preferred_season[0]} Seasonal Event")

                seasonal_event_prompt = f'''
                Look up 3 seasonal popular event or activities in {user_place} during {user_preferred_season}.
                Give me the name of the event as a header and a short description as the body text.
                 The description must be shown as bullet points:
                 1) where it is located
                  2) the time duration
                  3) the common way(s) to get there
                  4) the overall cost
                  5) and basic information.
                Do not output anything else. 
                I need 3 events.
                '''

                # seasonal_event_raw_data = analyze_text(HF_api_key, prompt = seasonal_event_prompt)

                st.write(seasonal_event_raw_data)

                st.image(f"./irasutoya_images/{user_preferred_season[0].lower()}_season.png")


                # ########################################################################
                # ### do not touch weather but it is weather
                # ########################################################################
                st.header("Weather")
                st.divider()

                weather_choice = ["Cloudy", "Rain", "Snow", "Sunny", "Thunderstorm"]

                weather_format = '''
                {
                “May 3rd, 2024”
                {
                "Date": “May 3rd, 2024”,
                “Day Temperature": “75°F”,
                “Weather”: “Sunny",
                },
                {
                “May 4th, 2024”
                {
                "Date": “May 3rd, 2024”,
                “Day Temperature": “75°F”,
                “Weather”: “Cloudy",
                }
                }
                '''


                weather_prompt = f'''Do not output anything else and tell me the 7 days forecast starting from {user_start_date}.
                Give me for each day, the day temperature in Fahrenheit, and the type of weather among the choices here: {weather_choice} in the area of {user_place}. 
                Do not use square brackets like this [ ].
                Must be in a json string file format {weather_format} like this.
                The days must be in order with {user_start_date} as the first date.
                The beginning and end must be wrapped with double quotes.
                Do not output anything else other than json file. Must be valid json string file. Do not output any other text. Do not return anything else.
                '''

                # weather_raw_data = analyze_text(HF_api_key = hf_api_key, prompt = weather_prompt)
                # print(weather_raw_data)

                weather_raw_data = '''{
                "2025-01-03": {
                "Date": "January 3rd, 2025",
                "Day Temperature": "82°F",
                "Weather": "Sunny"
                },
                "2025-01-04": {
                "Date": "January 4th, 2025",
                "Day Temperature": "80°F",
                "Weather": "Cloudy"
                },
                "2025-01-05": {
                "Date": "January 5th, 2025",
                "Day Temperature": "78°F",
                "Weather": "Rain"
                },
                "2025-01-06": {
                "Date": "January 6th, 2025",
                "Day Temperature": "80°F",
                "Weather": "Sunny"
                },
                "2025-01-07": {
                "Date": "January 7th, 2025",
                "Day Temperature": "81°F",
                "Weather": "Cloudy"
                },
                "2025-01-08": {
                "Date": "January 8th, 2025",
                "Day Temperature": "79°F",
                "Weather": "Snow"
                },
                "2025-01-09": {
                "Date": "January 9th, 2025",
                "Day Temperature": "82°F",
                "Weather": "Sunny"
                }
                }
                '''

                weather_df = pd.DataFrame(json.loads(weather_raw_data))

                weather_df = weather_df.transpose()

                weather_columns = st.columns(7, border = True)

                for i, column in enumerate(weather_columns):
                        column.image(f"./irasutoya_images/{weather_df["Weather"].iloc[i].lower()}.png")
                        column.subheader(weather_df["Day Temperature"].iloc[i])
                        column.write(weather_df["Date"].iloc[i])

        
        st.markdown("##")

        st.subheader(f'''
        Nearby Places to :red-background[:red[{user_place}]]
        ''')
        st.divider()
        df = pd.DataFrame(json.loads(raw_data))

        df = df.transpose()

        coordinates_df = df[['latitude', 'longitude']]

        #     st.map(coordinates_df, size = 1000, color = '#ffaa00')

        st.divider()

        left_text_box, right_text_box = st.columns(2)

        with left_text_box:
                st.subheader(f'''
                :blue-background[{df["name"].iloc[0]}]
                ''')

                st.markdown(f'''
                {df["description"].iloc[0]}
                ''')

                        # st.subheader(f''' 
                        #         :green-background[{df["name"].iloc[1]}]
                        #         ''')

                        # st.markdown(f'''
                        #         {df["description"].iloc[1]}
                        #         ''')

                        # st.subheader(f'''
                        #         :red-background[{df["name"].iloc[2]}]
                        #         ''')

                        # st.markdown(f'''
                        #         {df["description"].iloc[2]}
                        #         ''')


        # with right_text_box:
        #         st.subheader(f'''
        #                         :violet-background[{df["name"].iloc[3]}]
        #                         ''')

        #         st.markdown(f'''
        #                         {df["description"].iloc[3]}
        #                         ''')

        #         st.subheader(f''' 
        #                         :orange-background[{df["name"].iloc[4]}]
        #                         ''')

        #         st.markdown(f'''
        #                         {df["description"].iloc[4]}
        #                         ''')