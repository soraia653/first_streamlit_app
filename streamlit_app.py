# troubleshooting - dont run anything
# streamlit.stop()

# required libraries
import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
  
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  
  return fruityvice_normalized

# display Fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?", "Kiwi")
  
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    output_from_func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(output_from_func)
    
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

# query fruit_load_list table from snowflake
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

# add a button to load the fruit data
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# allow user to add a fruit to the list
add_fruit = streamlit.text_input("Add a new fruit")

if add_fruit:
  my_cur.execute(f"INSERT INTO fruit_load_list VALUES ('{add_fruit}')")
  streamlit.write(f"Thanks for adding {add_fruit}.")
