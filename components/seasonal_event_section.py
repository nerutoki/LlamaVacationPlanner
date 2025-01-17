# Standard Libraries

# Third-Parties Libraries
import streamlit as st

from utils import dict_season_images,remove_indentation
from backend import analyze_text       

def seasonal_event_widget(user_place, user_season, HF_api_key):
    """ Take in the user's response in order to dynamically edit 
    the prompt to send to the LLM.
        
    Args:
        HF_api_key (str): Hugging Face API Token
        user_place (str): the place the user's going to
        user_season (str): the season when the user comes in for 
                            dynamically creating dividers
        
    Return: 
        response (str): Answer from LLM

    """
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

    ############################################################################
    # Seasonal Event Section
    ############################################################################
    st.subheader(f" :red-background[:red[{user_season} Seasonal Event]]")

    st.write(raw_data_seasonal_event)

    dict_season_images.get(user_season)
