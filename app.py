import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calculate_bmr(weight_kg, height_cm, age, gender):
    # Using Mifflin-St Jeor Equation
    if gender == "Male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def calculate_tdee(bmr, activity_level):
    # Activity level multipliers
    activity_multipliers = {
        "Sedentary: Little to no exercise (desk job)": 1.2,
        "Lightly Active: Light exercise 1-3 days/week": 1.375,
        "Moderately Active: Moderate exercise 3-5 days/week": 1.55,
        "Very Active: Hard exercise 6-7 days/week": 1.725,
        "Extra Active: Very hard exercise or physical job": 1.9
    }
    return bmr * activity_multipliers[activity_level]

def calculate_time_to_goal(current_weight_kg, desired_weight_kg, deficit_surplus):
    weight_diff_kg = abs(current_weight_kg - desired_weight_kg)
    calories_per_kg = 7700  # Approximate calories per kg of body weight
    total_calories = weight_diff_kg * calories_per_kg
    days = total_calories / abs(deficit_surplus)
    return days / 7  # Convert to weeks

def recommended_water_intake(age, gender):
    if 9 <= age <= 13:
        return 2.4 if gender == "Male" else 2.1
    elif 14 <= age <= 18:
        return 3.3 if gender == "Male" else 2.2
    elif 19 <= age <= 70:
        return 3.7 if gender == "Male" else 2.7
    else:
        return "Age out of range for recommendation"

def run():
    st.title("Weight Goal Calculator")
    
    # User inputs
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
        ["Sedentary: Little to no exercise (desk job)",
         "Lightly Active: Light exercise 1-3 days/week",
         "Moderately Active: Moderate exercise 3-5 days/week",
         "Very Active: Hard exercise 6-7 days/week",
         "Extra Active: Very hard exercise or physical job"]
    )

    # Calculations
    bmr = calculate_bmr(current_weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    weight_diff = current_weight_kg - desired_weight_kg
    if weight_diff > 0:
        deficit = 500
        target_calories = tdee - deficit
        goal_type = "deficit"
    else:
        surplus = 250
        target_calories = tdee + surplus
        goal_type = "surplus"

    # Range of time to goal (min: 250 cal, avg: 500 cal, max: 1000 cal for loss; reverse for gain)
    if goal_type == "deficit":
        min_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 250)
        max_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 1000)
    else:
        min_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 500)
        max_time = calculate_time_to_goal(current_weight_kg, desired_weight_kg, 125)
    
    weeks_to_goal = calculate_time_to_goal(current_weight_kg, desired_weight_kg, deficit if goal_type == "deficit" else surplus)
    recommended_water = recommended_water_intake(age,gender)

    # Display results
    st.header("Results")
    st.write(f"Your maintenance calories (TDEE): {tdee:.0f} calories/day")
    st.write(f"Recommended daily calories for {goal_type}: {target_calories:.0f} calories/day")
    st.write(f"Estimated time to reach goal: {weeks_to_goal:.1f} weeks")

    # Statistical Insights
    st.subheader("Statistical Insights")
    st.write("Time to goal range:")
    st.write(f"- Slow pace: {max_time:.1f} weeks")
    st.write(f"- Recommended pace: {weeks_to_goal:.1f} weeks")
    st.write(f"- Fast pace: {min_time:.1f} weeks")

    # Water intake comparison
    st.subheader("Water Intake Comparison")
    fig, ax = plt.subplots()
    water_data = [water_intake, recommended_water]
    bars = ax.bar(['Your Intake', 'Recommended'], water_data)
    ax.set_ylabel('Liters')
    ax.set_title('Daily Water Intake Comparison')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}L',
                ha='center', va='bottom')
    st.pyplot(fig)

    # Recommendations
    st.subheader("Personalized Recommendations")
    if goal_type == "deficit":
        st.write(f"To lose weight safely, aim for a {deficit} calorie daily deficit.")
        st.write("This will result in approximately 0.5 kg of weight loss per week.")
    else:
        st.write(f"To gain weight safely, aim for a {surplus} calorie daily surplus.")
        st.write("This will result in approximately 0.25 kg of weight gain per week.")
    
    water_diff = water_intake - recommended_water
    if water_diff < -0.5:
        st.write(f"Consider increasing your water intake by about {abs(water_diff):.1f} liters to meet the recommended amount.")
    elif water_diff > 0.5:
        st.write(f"Your water intake is {water_diff:.1f} liters above the recommendation, which is great!")
    else:
        st.write("Your water intake is close to the recommended amount. Good job!")

    # TDEE Explanation
    st.subheader("What is TDEE?")
    st.write("""
        Total Daily Energy Expenditure (TDEE) is the total number of calories your body burns in a day. 
        It includes:
        
        1. **Basal Metabolic Rate (BMR)**: Calories burned at rest to maintain basic bodily functions.
        2. **Physical Activity**: Calories burned through exercise and daily movement.
        3. **Thermic Effect of Food**: Calories used to digest and process food.
        
        We calculate BMR using the Mifflin-St Jeor equation, considered one of the most accurate formulas.
        Then, we multiply it by an activity factor based on your lifestyle.
    """)

if __name__ == "__main__":
    run()
