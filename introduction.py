import streamlit as st
import requests

def fetch_motivational_quote():
    """
    Fetches a random motivational quote from ZenQuotes API.
    Returns a string in the format "Quote" - Author.
    """
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                quote = data[0]["q"]
                author = data[0]["a"]
                return f'"{quote}" - {author}'
    except Exception as e:
        return "Stay motivated and healthy!"
    return "Stay motivated and healthy!"

def run():
    st.markdown(
        """
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px;">
            <h1 style="color:#2c3e50;">Welcome to My Health & Nutrition App</h1>
            <p style="font-size:18px; color:#34495e;">
                This interactive web app helps you track your weight goals and calorie intake.
                Explore the <strong>Weight Calculator</strong> for personalized calorie estimates and the
                <strong>Calorie Intake</strong> tracker to log your daily meals.
            </p>
            <h3 style="color:#16a085;">Features:</h3>
            <ul style="font-size:16px; color:#34495e;">
                <li><strong>Weight Calculator:</strong> Estimate your Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and the time needed to reach your weight goal.</li>
                <li><strong>Calorie Intake Tracker:</strong> Log your meals, view nutrient breakdowns, and compare your intake with recommended targets.</li>
                <li><strong>Interactive Charts:</strong> Visualize your progress with engaging graphs and insights.</li>
                <li><strong>Motivational Boost:</strong> Enjoy a daily motivational quote fetched via a free API.</li>
            </ul>
            <p style="font-size:16px; color:#34495e;">
                Use the sidebar on the left to navigate through the app. Enjoy your journey to better health!
            </p>
        </div>
        """, unsafe_allow_html=True
    )

    # Fetch and display a motivational quote using a free API
    quote = fetch_motivational_quote()
    st.markdown(
        f"""
        <div style="background-color:#e8f8f5; padding:15px; border-radius:10px; margin-top:20px;">
            <h2 style="color:#27ae60;">Daily Motivation</h2>
            <p style="font-size:20px; color:#2c3e50;">{quote}</p>
        </div>
        """, unsafe_allow_html=True
    )

if __name__ == "__main__":
    run()
