# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests 
# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your customs Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)


if ingredients_list:
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(each_fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        fv_dv = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

        #st.write(ingredients_string)

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

        #st.write(my_insert_stmt)

        time_to_insert = st.button('Submit Orders')

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, ',icon="✅")
           

