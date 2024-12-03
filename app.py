import streamlit as st
import pandas as pd
from recommendation_engine import RecommendationEngine

# Initialize the recommendation engine
rec_engine = RecommendationEngine('dataset.csv')

# Streamlit app layout
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo2.png", width=100)
with col2:
    st.title("Analytics Vidhya")

st.header("Free Courses")

# User input for searching
query = st.text_input("Search for a course:")

if query:
    recommendations = rec_engine.get_recommendations(query)
    
    if not recommendations.empty:
        for i in range(0, len(recommendations), 3):
            row_data = recommendations.iloc[i:i+3]
            cols = st.columns(3)

            for col, (_, row) in zip(cols, row_data.iterrows()):
                with col:
                    st.image(row['Image_URL'], caption=row['Course_name'], width=250)
                    st.markdown(f"### [{row['Course_name']}]({row['Course']})")
                    st.write(row['Description'])
    else:
        st.write("No courses found for the search term.")
else:
    st.write("Enter a course name to search for relevant courses.")
