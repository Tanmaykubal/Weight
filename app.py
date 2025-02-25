import streamlit as st

import matplotlib.pyplot as plt

import requests



def calculate_bmr(weight_kg, height_cm, age, gender):

    if gender == "Male":

        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5

    else:

        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161



def calculate_tdee(bmr, activity_level):

    activity_multipliers = {

        "Sedentary (little/no exercise)": 1.2,

        "Lightly Active (1-3 days/week)": 1.375,

        "Moderately Active (3-5 days/week)": 1.55,

        "Very Active (6-7 days/week)": 1.725,

        "Extra Active (physical job/exercise)": 1.9

    }

    return bmr * activity_multipliers[activity_level]



def calculate_time_to_goal(current_weight_kg, desired_weight_kg, deficit_surplus):

    weight_diff_kg = abs(current_weight_kg - desired_weight_kg)

    calories_per_kg = 7700  

    total_calories = weight_diff_kg * calories_per_kg

    days = total_calories / abs(deficit_surplus)

    return days / 7



def recommended_water_intake(age, gender):
    if 9 <= age <= 13:
        return 2.4 if gender == "Male" else 2.1
    elif 14 <= age <= 18:
        return 3.3 if gender == "Male" else 2.2
    elif 19 <= age <= 70:
        return 3.7 if gender == "Male" else 2.7
    else:
        return "Age out of range for recommendation"

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)
    
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"



def fetch_advice():

    """Fetch a random advice from Advice Slip API."""

    try:

        response = requests.get("https://api.adviceslip.com/advice")

        if response.status_code == 200:

            data = response.json()

            advice = data["slip"]["advice"]

            return advice

    except Exception as e:

        return "Remember to stay consistent and focused on your goals!"

    return "Remember to stay consistent and focused on your goals!"



def run():

    st.markdown("<h1 style='color:#2980b9;'>Weight Goal Calculator</h1>", unsafe_allow_html=True)

    

    with st.container():

        st.markdown("<h3 style='color:#27ae60;'>Enter Your Details</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            current_weight_kg = st.number_input("Current Weight (kg)", min_value=20.0, max_value=250.0, value=70.0)

            height_cm = st.number_input("Height (cm)", min_value=90.0, max_value=250.0, value=170.0)

            age = st.number_input("Age", min_value=1, max_value=120, value=30)

        with col2:

            desired_weight_kg = st.number_input("Desired Weight (kg)", min_value=20.0, max_value=250.0, value=65.0)

            water_intake = st.number_input("Daily Water Intake (liters)", min_value=0.0, max_value=20.0, value=2.0)

            gender = st.selectbox("Gender", ["Male", "Female"])

    

    activity_level = st.selectbox(

        "Activity Level",

        ["Sedentary (little/no exercise)",

         "Lightly Active (1-3 days/week)",

         "Moderately Active (3-5 days/week)",

         "Very Active (6-7 days/week)",

         "Extra Active (physical job/exercise)"]

    )

    

    bmr = calculate_bmr(current_weight_kg, height_cm, age, gender)

    tdee = calculate_tdee(bmr, activity_level)

    weight_diff = current_weight_kg - desired_weight_kg
    bmi = calculate_bmi(current_weight_kg, height_cm)

    

    if weight_diff > 0:

        deficit = 500

        target_calories = tdee - deficit

        goal_type = "deficit"

    else:

        surplus = 250

        target_calories = tdee + surplus

        goal_type = "surplus"

    

    if goal_type == "deficit":

        min_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 250)

        max_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 1000)

        weeks_to_goal = calculate_time_to_goal(current_weight_kg, desired_weight_kg, deficit)

    else:

        min_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 500)

        max_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 125)

        weeks_to_goal = calculate_time_to_goal(current_weight_kg, desired_weight_kg, surplus)

    

    recommended_water = recommended_water_intake(age,gender)
    bmi_cat = bmi_category(bmi)
   

    

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#8e44ad;'>Results</h2>", unsafe_allow_html=True)

    st.write(f"**Maintenance Calories (TDEE):** {tdee:.0f} calories/day")

    st.write(f"**Recommended Daily Calories ({goal_type}):** {target_calories:.0f} calories/day")

    st.write(f"**Estimated Time to Reach Goal:** {weeks_to_goal:.1f} weeks")
    st.write(f"**Your BMI:** {bmi:.1f} ({bmi_cat})")


    

    st.markdown("<h3 style='color:#d35400;'>Time to Goal Range (min: 250 cal, avg: 500 cal, max: 1000 cal for loss; reverse for gain)</h3>", unsafe_allow_html=True)

    st.write(f"- Slow pace: {max_time:.1f} weeks")

    st.write(f"- Recommended pace: {weeks_to_goal:.1f} weeks")

    st.write(f"- Fast pace: {min_time:.1f} weeks")

    

    st.markdown("<h3 style='color:#c0392b;'>Water Intake Comparison</h3>", unsafe_allow_html=True)

    fig, ax = plt.subplots()

    water_data = [water_intake, recommended_water]

    bars = ax.bar(['Your Intake', 'Recommended'], water_data, color=['#3498db', '#2ecc71'])

    ax.set_ylabel('Liters')

    ax.set_title('Daily Water Intake Comparison')

    for bar in bars:

        height = bar.get_height()

        ax.text(bar.get_x() + bar.get_width()/2., height,

                f'{height:.1f}L',

                ha='center', va='bottom')

    st.pyplot(fig)

    

    st.markdown("<h3 style='color:#16a085;'>Personalized Recommendations</h3>", unsafe_allow_html=True)

    if goal_type == "deficit":

        st.write("To lose weight safely, aim for a **500 calorie daily deficit**.")

        st.write("This typically results in about 0.5 kg weight loss per week.")

    else:

        st.write("To gain weight safely, aim for a **250 calorie daily surplus**.")

        st.write("This typically results in about **0.25 kg** weight gain per week.")

    

    water_diff = water_intake - recommended_water

    if water_diff < -0.5:

        st.write(f"Consider increasing your water intake by about **{abs(water_diff):.1f} liters**.")

    elif water_diff > 0.5:

        st.write(f"Great! Your water intake is **{water_diff:.1f} liters** above the recommendation.")

    else:

        st.write("Your water intake is close to the recommended amount. Good job!")

    

    st.markdown("<h3 style='color:#34495e;'>What is TDEE?</h3>", unsafe_allow_html=True)

    st.write("""

    **Total Daily Energy Expenditure (TDEE)** is the number of calories your body burns in a day.

    It includes:

    - **Basal Metabolic Rate (BMR):** Calories burned at rest.

    - **Physical Activity:** Calories burned during exercise and daily movement.

    - **Thermic Effect of Food:** Calories used in digesting food.

    

    We use the Mifflin-St Jeor equation for BMR and multiply by an activity factor.

    """)

    

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#27ae60;'>Advice Based on Your Inputs</h2>", unsafe_allow_html=True)

    advice = fetch_advice()

    st.write(f"**Advice:** {advice}")




    

if __name__ == "__main__":

    run()
