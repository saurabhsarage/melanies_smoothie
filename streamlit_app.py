# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("My Parents New Helthy Diner")
# st.title(f":cup_with_straw: Customize Your Smoothies!:cup_with_straw: ")
st.write(
  """
  Choose the fruits you want in your custom Smoothies
  """
)

title = st.text_input('Name on Smoothie')
st.write('''The name on Smoothie will be''', title)

cnx = st.connection("snowflake")
session = cnx.session() #get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


ingreadient_list = st.multiselect(
    'Choose upto 5 ingreadient:',
    my_dataframe,
    max_selections=5
)

ingreadient_String = ''

if ingreadient_list:
    
    for fruits in ingreadient_list:
        ingreadient_String = ingreadient_String + fruits + ' ' 
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits,' is ', search_on, '.')
        
        st.subheader(fruits + ' Nutrition  Information')
        smoothiefroot_response = requests.get(f"https://www.smoothiefroot.com/api/fruit/{search_on}")

        st.dataframe(smoothiefroot_response.json(), use_container_width=True)

# st.write(ingreadient_String)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingreadient_String + """', '"""+title+"""')"""

time_to_insert = st.button("Submit Order")

# st.stop()
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {title}!', icon="✅")


# smoothiefroot_response = requests.get("https://www.smoothiefroot.com/api/fruit/watermelon")

# st.dataframe(smoothiefroot_response.json(), use_container_width=True)
