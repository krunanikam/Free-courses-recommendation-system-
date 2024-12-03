import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load dataset
data = pd.read_csv('dataset.csv', encoding='ISO-8859-1')

# Preprocess 'Description' column to handle missing values
data['Description'] = data['Description'].fillna('').astype(str)

# Function to fetch an image URL using Bing Search
def fetch_image(course_name):
    search_query = course_name.replace(" ", "+")
    url = f"https://www.bing.com/images/search?q={search_query}+course+image"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the first image result
        img_tag = soup.find("img", {"class": "mimg"})
        if img_tag and img_tag.get("src"):
            return img_tag["src"]
    except Exception as e:
        st.error(f"Error fetching image: {e}")
    
    # Return a placeholder if image fetching fails
    return "https://via.placeholder.com/400x200?text=No+Image+Available"

# Streamlit app layout
st.set_page_config(page_title="Free Courses", page_icon="📚", layout="wide")

# Add custom CSS for consistent image alignment, spacing, and zoom effect
st.markdown(
    """
    <style>
    h4 a {
        text-decoration: none; /* Remove underline */
        color: black; /* Default text color */
    }
    h4 a:hover {
        color: #007BFF; /* Change color on hover */
    }
    .image-container {
        height: 150px; /* Set a fixed height */
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    img {
        max-height: 100%; /* Scale image within the container */
        max-width: 100%; /* Prevent image from overflowing */
    }
    img:hover {
        transform: scale(1.1); /* Zoom effect */
        transition: 0.3s; /* Smooth transition */
    }
    .row-spacing {
        margin-bottom: 30px; /* Space between rows */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display header with logo beside the title
col1, col2 = st.columns([1, 5])  # Adjust column widths
with col1:
    st.image("logo2.png", width=100)  # Replace with your logo file path
with col2:
    st.markdown("<h1 style='margin-top: 20px;'>Analytics Vidhya</h1>", unsafe_allow_html=True)

# App title and heading
st.markdown("<hr>", unsafe_allow_html=True)
st.header("Free Courses")
st.write("Explore our collection of free courses and enhance your skills!")

# User input for searching courses
query = st.text_input("Search for a course:", placeholder="Enter a course name")

# Filter and display courses
if query:
    filtered_data = data[data['Course_name'].str.contains(query, case=False, na=False)]
    
    if not filtered_data.empty:
        # Display courses in rows of 3
        for i in range(0, len(filtered_data), 3):  # Iterate in steps of 3
            row_data = filtered_data.iloc[i:i+3]  # Get 3 courses per row
            cols = st.columns(3)  # Create 3 columns for the row

            with st.container():  # Add container for row spacing
                st.markdown('<div class="row-spacing">', unsafe_allow_html=True)
                for col, (_, row) in zip(cols, row_data.iterrows()):
                    with col:
                        # Display course name as a clickable link
                        st.markdown(f"<h4 style='text-align: center;'><a href='{row['Course']}' target='_blank'>{row['Course_name']}</a></h4>", unsafe_allow_html=True)
                        
                        # Fetch and display the image in a fixed-height container
                        image_url = fetch_image(row['Course_name'])
                        st.markdown(
                            f"<div class='image-container'><img src='{image_url}' alt='{row['Course_name']}'></div>",
                            unsafe_allow_html=True
                        )
                st.markdown('</div>', unsafe_allow_html=True)  # Close row spacing container
    else:
        st.write("No courses found for the search term.")
else:
    st.write("Enter a course name to search for relevant courses.")
