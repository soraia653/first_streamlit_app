import streamlit
import requests
import pandas as pd

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# read CSV file from S3 bucket and display as a df table
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# create pick list so that user can pick the fruits they want to include
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# display Fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

# accept user input
fruit_choice = streamlit.text_input("What fruit would you like information about?", "Kiwi")
streamlit.write('The user entered', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# normalize json data
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output it as a table
streamlit.dataframe(fruityvice_normalized)
