from re import search
import streamlit as st
from sentence_similarity_service import format_response, semantic_search, analytics_service

st.write("""
# Semantic search based on metadata

This project has the intuition to recommend a book based on a search query 
inserted by the user. The data used to build this model can be found at [Amazon Review Data]
(https://nijianmo.github.io/amazon/index.html), and all the code is available on [Github](https://github.com/Adilsitos/Semantic-Search-Amazon-Data)

""")

#num_recommendations = st.number_input('Number of recommendations:', min_value=1, max_value=20, value=5)

user_input = st.text_input('Book Search')

search_button =  st.button('Search')

if (search_button or user_input) and user_input != '':
   
    recommendations = semantic_search(user_input, '10')
    df = format_response(recommendations)

    st.write("Did the recommendations match your expectations?")

    feedback_cols = st.beta_columns(2)
    with feedback_cols[0]:
        positive_btn = st.button("Yes")
    with feedback_cols[1]:
        negative_btn = st.button("No")

    if positive_btn:
        st.write("Thank you for your feedback! "
        "We appreciate your interest in improve our system 🙌")
        analytics_service(df, user_input, 1)
        

    if negative_btn:
        st.write("Thank you for your feedback! "
        "We appreciate your interest in improve our system 🙌")
        analytics_service(df, user_input, 0)
        

    for title, description, score in zip(df['title'], df['description'], df['scores'] ):
        
        st.write(f'#  {str(title).capitalize()}')
    
        title_rm_spaces = str(title).replace(" ", "+")

        amazon_url = f'(https://www.amazon.com/s?k={title_rm_spaces})'
        good_reads_url = f'(https://www.goodreads.com/search?utf8=✓&query={title_rm_spaces}&search_type=books)'
        
        st.write('[Search on Amazon]'+amazon_url)
        st.write('[Search on Goodreads]'+good_reads_url)
    
        st.write(f'Recommendation score: {score}')
    
  
    