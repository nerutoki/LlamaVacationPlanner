# Standard Libraries
import datetime
import json
import pandas as pd

# Third-Parties Libraries
import streamlit as st

def remove_indentation(input_string):
        # Split the input string by lines
        lines = input_string.splitlines()
        
        # Strip leading spaces or tabs from each line
        stripped_lines = [line.lstrip() for line in lines]
        
        # Join the lines back into a single string
        return '\n'.join(stripped_lines)


dict_season_images = {"Spring": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhZiXccJCRBsFFFYCqxja3YZn0YIy7H989_Hwh5zWcngkOt2wffgc8IffMhtAB8VGMQxKkgyQMN6YWBlzD3HoHUcZFWgB_r6tf8MppVIt01ihq-df_MM0dQtrPskJLshi7XULxDywx8OA4/s1000/clover_bug.png",
                     "Autumn": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhH_mDQur6KTPeBTH8aAESkoJv8XKZfkco1JtBpEGT51tA88uOtUAum9TbynkiVSrtJO2Z9H7KFpmsQK2V-jQcza6GM3Yiak43we1mGyXrJOJqFtkVWgpYKo6D8sIfuQUY-pQtjwsgqSj3R/s800/line_autumn2.png",
                     "Summer": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjgbSi4DUUmdjS4XuAEBSUEo6ItNW_zEx-ZqJ81o1cDr2Lsj09US__Pna98aiG-BpjunEg59IEMIgOIWGyH9AptcuMcvu312ugCqPBVhd2fzzFpjzIPxqYWuEH4J5qBQQ8132VAw6bzLpee/s800/line_summer4.png",
                     "Winter": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgzsvv1UCkKUfHCsQCpxkRMNUOq5OCVmbYd96hxTIPlfdPPZz3bKxAkI5fssZ3iGoIiFy0x-IHXiWYt9L0rjnxXqM_brs4ONFuV_uQxIVUBYcwJksPBmwG-1xE75ZzlSyZC3w5hyeMZl2ST/s800/line_winter_crystal.png"
                     }

dict_weather_images = {"Cloudy":"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhaVU8_bPnnrsJWJZrZOXpsmYfwy9xRhRCdO2zseln57YdUOE_-ClZOIDzUZ-pzanSYiEIgiUc7jauImyXPkE0v5c4XP4Fr8BwkDvseWpThBgZ8iMZtV2VYkyBB4UJ11bwc_AvyJz13ohk/s800/tenki_mark05_kumori.png",
                       "Rain":"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjPBJCAPE0omJcc8fcYTcinsNp84_qYXXkXdg6GyUCWZUspWjyssI1dq6Q9HUJXMvRO1gLvZIWDXHOEQDOp0mdsCe2f0YRzfRcZjjt9CGxaRsuwop7I14lZ1-8FE1QjXjigmPzL3FZa5uI/s800/tenki_mark03_gouu.png",
                       "Snow": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhdtPHKDJKDxU7UlEeaFSwZJzCknRAIFTB1Xh8aEXQieNvPjGVRvqtw-GBnMuaC-74lh64KkKbSn1lpBSyr5NxXvi99W5BA51oo01-tJZ-95JkqhASLIv1D0WZmuq0BDLjZkRwQy-cJQnY/s800/tenki_mark08_yuki.png",
                       "Sunny":"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhwVQRBNp37wD368AZxWKFb07IPj1ibEwy5PAF6TD7DtfDWH6a0KBDOZGf45YIlNcyeqvrJmR08i4lKrKqOROxv-BSnoBdhGDbWzPm0A3YUV4SSzP9Z38hANQ_DUaKfQSErvfSrJtFi5QI/s800/tenki_mark01_hare.png",
                       "Thunderstorm":"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgdAQcf8-VGdXk0iyoPGGLJJ9pM5jEZ2pivapvaNMjxigZnpDjxohcNYatoZuaZ2uHJbTVPrqgxwPpzNecuWa8SMVSSaMRnWuHOHBMRSi6hbH-9H_0YHi89JfC-RmLC8dnBsWJQwSlBkAU/s800/tenki_mark07_kaminari.png"
                       }