import streamlit as st
import introduction
import app
import calrie

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Introduction", "App", "Calorie"])

if page == "Introduction":
    introduction.run()      # Loads the introduction page
elif page == "App":
    app.run()               # Loads the weight goal calculator from app.py
elif page == "Calorie":
    calrie.run()            # Loads the calorie tracker from calrie.py
