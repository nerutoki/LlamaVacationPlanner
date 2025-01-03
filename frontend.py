# Standard Libraries
import time 
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st

# Imported Libraries
from backend import analyze_text

#functions goes here 

############################################################

# SET UP PAGE SHENANIGANS 
############################################################

st.set_page_config(page_title="Vacation Planner", layout = "wide")
st.title(body=":red[Vacation Planner]")
st.divider()
progress_done = False
show_content = False

###########################################################

##LLM CODE ACTUALLY HERE
###########################################################
#CURSE THE  MAIN #########


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
            {
            "Barks Bakery": 
            {
            "name": "Barks Bakery",
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
            
            raw_data = analyze_text(HF_api_key = HF_api_key, prompt = prompt)
        
        #     print(raw_data)

            result_data = json.loads(raw_data)


            show_content = True
        else:
            st.error("Please check again if the fields are filled correctly.")
    else:
        st.empty()


st.markdown("##")

st.subheader(f'''
            Nearby Places to :red-background[:red[{user_place}]]
            ''')
st.divider()

if show_content == True:

    df = pd.DataFrame(json.loads(raw_data))

    df = df.transpose()

    coordinates_df = df[['latitude', 'longitude']]

    st.map(coordinates_df, size = 1000, color = '#ffaa00')

    st.divider()

    left_text_box, right_text_box = st.columns(2)

    with left_text_box:

        st.subheader(f'''
                :blue-background[{df["name"].iloc[0]}]
                ''')

        st.markdown(f'''
                {df["description"].iloc[0]}
                ''')

        st.subheader(f''' 
                :green-background[{df["name"].iloc[1]}]
                ''')

        st.markdown(f'''
                {df["description"].iloc[1]}
                ''')

        st.subheader(f'''
                :red-background[{df["name"].iloc[2]}]
                ''')

        st.markdown(f'''
                {df["description"].iloc[2]}
                ''')


        with right_text_box:
            st.subheader(f'''
                    :violet-background[{df["name"].iloc[3]}]
                    ''')

            st.markdown(f'''
                    {df["description"].iloc[3]}
                    ''')

            st.subheader(f''' 
                    :orange-background[{df["name"].iloc[4]}]
                    ''')

            st.markdown(f'''
                    {df["description"].iloc[4]}
                    ''')