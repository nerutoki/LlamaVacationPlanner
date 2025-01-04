#Standard Libraries
import os
import json
import re

# Third-Party Libraries
from huggingface_hub import InferenceClient

## functions here delete this comment later

def analyze_text(HF_api_key, prompt):
    """ Take in a prompt that is updated based on the user's answer.
        
    Args:
        HF_api_key (str): Hugging Face API Token
        prompt (str): Prompt the LLM
        
    Return: 
        response (str): Answer from LLM

    """

    api_key = HF_api_key

    client = InferenceClient(api_key = api_key)

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct", 
        messages=messages, 
        max_tokens=500,
        stream=True
    )

    result = ""

    for chunk in stream:
        result = result + chunk.choices[0].delta.content

    return result


if __name__ == "__main__":

    # hf_api_key = os.environ.get('hf_api_key')

    user_place_city = ["Honolulu"]
    user_preferred_category = ["Gaming"]

    format = '''
  "Game Over": {
    "name": "Game Over",
    "description": "A retro arcade and board game bar featuring consoles such as Nintendo and PlayStation.",
    "latitude": 21.2813146,
    "longitude": -157.8565834
  }
    '''

    prompt = f'''
        I need 5 or less real places nearby {user_place_city} that are related to 
          {user_preferred_category}-type activities. It must be returned 
          with a name, a one sentence description, the latititude coordinate, and the 
          longitude coordinate as the keys, and the answers as values in a json object.
           Name, description, latitude coordinate, and longitude coordinate must be keys. 
          Only give me a one sentence description. Only give me real places. Do not use square brackets.

          Must be in the format {format} and add a comma after each json object.

          The whole json string should be wrapped with curly brackets at the beginning and end.
          Return only a valid json string for output. Must be valid. Do not return anything else. 
          Do not use Google Maps API.
            '''
    
    # raw_data = analyze_text(HF_api_key = hf_api_key, prompt = prompt)
    # print(result)

  ## this is as test case variable to prevent api spam
    raw_data = '''{
  "Game Over": {
    "name": "Game Over",
    "description": "A retro arcade and board game bar featuring consoles such as Nintendo and PlayStation.",
    "latitude": 21.2813146,
    "longitude": -157.8565834
  },
  "Honolulu Gaming Center": {
    "name": "Honolulu Gaming Center",
    "description": "A PC gaming center offering a variety of games including CS:GO, Dota 2, and League of Legends.",
    "latitude": 21.3063779,
    "longitude": -157.8587604
  },
  "Sky Zone Trampoline Park": {
    "name": "Sky Zone Trampoline Park",
    "description": "An indoor trampoline park featuring arcade games, bounce houses, and dodgeball.",
    "latitude": 21.3479163,
    "longitude": -157.8579785
  },
  "Escape Room Hawaii": {
    "name": "Escape Room Hawaii",
    "description": "A challenge to solve puzzles and mysteries to escape within 60 minutes, similar to escape room games.",
    "latitude": 21.2814851,
    "longitude": -157.8578445
  },
  "Sky Zone Trampoline Park in Pearl City": {
    "name": "Sky Zone Trampoline Park in Pearl City",
    "description": "An indoor trampoline park featuring arcade games, bounce houses, and dodgeball.",
    "latitude": 21.4598049,
    "longitude": -157.9562369
  }
}'''

    result_data = json.loads(raw_data)

    objects_keys = [attribute for attribute in result_data.keys()]

    ## not necessary tbh
    name_value_data = []
    description_value_data = []
    latitude_value_data = []
    longitude_value_data = []

    for attribute in objects_keys:
        name_value_data.append(result_data[attribute]["name"])
        description_value_data.append(result_data[attribute]["description"])
        latitude_value_data.append(result_data[attribute]["latitude"])
        longitude_value_data.append(result_data[attribute]["longitude"])

    print("names", name_value_data)
    print("description", description_value_data)
    print("Latitude", latitude_value_data)
    print("Longitude", longitude_value_data)