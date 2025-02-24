import streamlit as st

def run():
    st.title("Welcome to My Health App")
    st.write("""
        This app helps you track your weight goals and calorie intake.
        
        **Introduction Page:**
        - Learn more about how to use the app.
        - Get an overview of the available features.
        
        Use the sidebar to navigate between the Weight Goal Calculator and the Calorie Intake Tracker.
    """)

if __name__ == "__main__":
    run()
