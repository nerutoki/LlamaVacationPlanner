 # Standard Libraries

# Third-Parties Libraries
import streamlit as st

from utils import remove_indentation
from backend import analyze_text       

def about_place_widget(user_place, HF_api_key):
    """ Take in the user's response in order to dynamically edit 
    the prompt to send to the LLM.
        
    Args:
        HF_api_key (str): Hugging Face API Token
        user_place (str): the main text needed for prompt
        
    Return: 
        response (str): Answer from LLM

    """
    about_prompt = f'''Tell me about {user_place} in five sentences and the 
    famous things about that place in a string.'''

    response_info = remove_indentation(analyze_text(HF_api_key, prompt = about_prompt))

    st.write(response_info)