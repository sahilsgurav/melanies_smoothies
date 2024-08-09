# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie ! :cup_with_straw: ")
st.write(
 """Choose the **fruits** you want in your **smooothie** !"""
)




#option=st.selectbox("What is your favorite fruit ?",("Banana","Strawberries","Peaches"),)

#st.write("Your favourite fruit is  - ",option)



name_on_order=st.text_input("Name on Smoothie : ")
#if name_on_order:
    #st.write("name on smoothie is : ",name_on_order)


#session=get_active_session()
cnx= st.connection("snowflake")
session= cnx.session()

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#st.dataframe(data=my_dataframe,use_container_width=True)
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect('Choose upto 5 ingredients',my_dataframe, max_selections = 5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        #st.text(fruityvice_response.json())
        fv_df = st.dataframe(data = fruityvice_response.json(),use_container_width = True)
     
    st.write(ingredients_string)

    my_insert_stmt= "insert into SMOOTHIES.PUBLIC.ORDERS (ingredients,name_on_order) values ('"+ingredients_string+"','"+name_on_order+"')"
    #st.write(my_insert_stmt)
    
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothie is ordered !",icon="✅")



    

