import streamlit as st
import introduction
import app
import calrie

# Customize page config
st.set_page_config(
    page_title="My Health & Nutrition App",
    page_icon="✨",
    layout="wide"
)

# Sidebar customization with new labels
st.sidebar.markdown("<h2 style='text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "",
    ["Introduction", "Weight Calculator 🏋️", "Calorie Intake 🍎"],
    index=0
)

# Render the selected page
if page == "Introduction":
    introduction.run()
elif page == "Weight Calculator 🏋️":
    app.run()
elif page == "Calorie Intake 🍎":
    calrie.run()
