from re import search
import streamlit as st
from sentence_similarity_service import format_response, semantic_search

st.write("""
# Recommendation system using NLP

This project has the intuition to recommend a book based on a search query 
inserted by the user. The data used to build this model can be found at [Amazon Review Data]
(https://nijianmo.github.io/amazon/index.html), and all the code is available on [Github](https://github.com/Adilsitos/Semantic-Search-Amazon-Data)

""")

#num_recommendations = st.number_input('Number of recommendations:', min_value=1, max_value=20, value=5)

user_input = st.text_input('Book Search', 'A book about machine learning with focus on NLP')

if st.button('Search'):
   
    recommendations = semantic_search(user_input, '10')
    df = format_response(recommendations)

    for title, description, score in zip(df['title'], df['description'], df['scores'] ):
        

        st.write(f'#  {str(title).capitalize()}')
    
        title_rm_spaces = str(title).replace(" ", "+")

        amazon_url = f'(https://www.amazon.com/s?k={title_rm_spaces})'
        good_reads_url = f'(https://www.goodreads.com/search?utf8=✓&query={title_rm_spaces}&search_type=books)'
        
        st.write('[Search on amazon]'+amazon_url)
        st.write('[Search on goodreads]'+good_reads_url)
       
        st.write(f'Recommendation score: {score}')
 
  
    