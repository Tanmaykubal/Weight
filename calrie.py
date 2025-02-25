import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

import os

from scipy import stats



def run():

    st.markdown("<h1 style='color:#e67e22;'>Calorie Intake Tracker</h1>", unsafe_allow_html=True)

    

    if not os.path.exists("food_data.xlsx"):

        st.error("Food data file missing! Please run 'create_food_data.py' first.")

        st.stop()

    

    food_df = pd.read_excel("food_data.xlsx")

    

    st.markdown(

        "<div style='background-color:#ecf0f1; padding:10px; border-radius:5px;'>"

        "<h3>Log your daily food consumption</h3></div>", unsafe_allow_html=True)

    

    target_calories = st.number_input("Enter Your Daily Target Calorie Intake", min_value=500, max_value=5000, value=2000)

    date = st.date_input("Select Date")

    

    if "calorie_data" not in st.session_state:

        st.session_state.calorie_data = []

    

    st.subheader("Select Foods Consumed")

    selected_food = st.multiselect("Select Food Items", food_df["Food Item"])

    quantities = {}

    

    for food in selected_food:

        quantities[food] = st.number_input(f"Quantity of {food} (grams)", min_value=0, value=100)

    

    if st.button("Add Foods"):

        for food, quantity in quantities.items():

            if quantity > 0:

                food_row = food_df.loc[food_df["Food Item"] == food].iloc[0]

                food_calories = food_row["Calories per 100g"]

                food_protein = food_row["Protein per 100g"]

                food_carbs = food_row["Carbs per 100g"]

                food_fat = food_row["Fat per 100g"]

                

                total_calories = (food_calories * quantity) / 100

                total_protein = (food_protein * quantity) / 100

                total_carbs = (food_carbs * quantity) / 100

                total_fat = (food_fat * quantity) / 100

                

                # Check if the food already exists for the selected date

            existing_entry = next(

                (entry for entry in st.session_state.calorie_data if entry["Date"] == date and entry["Food"] == food), None

            )



            if existing_entry:

                # Update the existing entry instead of adding a new one

                existing_entry["Calories"] = total_calories

                existing_entry["Protein"] = total_protein

                existing_entry["Carbs"] = total_carbs

                existing_entry["Fat"] = total_fat

            else:

                # Add a new entry if it doesn't exist

                st.session_state.calorie_data.append({

                    "Date": date, "Food": food, "Calories": total_calories,

                    "Protein": total_protein, "Carbs": total_carbs, "Fat": total_fat

                })



    

    df_log = pd.DataFrame(st.session_state.calorie_data)

    if not df_log.empty:

        st.markdown("<h3>Your Food Log</h3>", unsafe_allow_html=True)

        st.write(df_log)

        

        daily_total = df_log[df_log["Date"] == date]["Calories"].sum()

        daily_protein = df_log[df_log["Date"] == date]["Protein"].sum()

        daily_carbs = df_log[df_log["Date"] == date]["Carbs"].sum()

        daily_fat = df_log[df_log["Date"] == date]["Fat"].sum()

        

        st.write(f"**Total Calories for {date}:** {daily_total:.0f} kcal")

        st.write(f"**Total Protein for {date}:** {daily_protein:.1f} g")

        st.write(f"**Total Carbs for {date}:** {daily_carbs:.1f} g")

        st.write(f"**Total Fat for {date}:** {daily_fat:.1f} g")

        

        if "daily_summary" not in st.session_state:

            st.session_state.daily_summary = []

        if st.button("Save Day"):

            st.session_state.daily_summary.append({

                "Date": date, "Calories": daily_total, "Protein": daily_protein,

                "Carbs": daily_carbs, "Fat": daily_fat

            })

    

    df_summary = pd.DataFrame(st.session_state.get("daily_summary", []))

    if not df_summary.empty:

        st.markdown("<h3>Calories Consumption Over Time</h3>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(df_summary["Date"], df_summary["Calories"], marker="o", label="Calories Consumed")

        ax.axhline(y=target_calories, color="r", linestyle="--", label="Calorie Target")

        ax.set_xlabel("Date")

        ax.set_ylabel("Calories")

        ax.legend()

        st.pyplot(fig)

    

    if not df_log.empty:

        past_date = st.date_input("Select a past day for Nutrient Breakdown", min_value=df_log["Date"].min(), max_value=df_log["Date"].max())

        if not df_log[df_log["Date"] == past_date].empty:

            daily_protein = df_log[df_log["Date"] == past_date]["Protein"].sum()

            daily_carbs = df_log[df_log["Date"] == past_date]["Carbs"].sum()

            daily_fat = df_log[df_log["Date"] == past_date]["Fat"].sum()

            nutrient_df = pd.DataFrame({

                "Nutrient": ["Protein", "Carbs", "Fat"],

                "Amount (g)": [daily_protein, daily_carbs, daily_fat]

            })

            st.markdown(f"<h3>Nutrient Breakdown for {past_date}</h3>", unsafe_allow_html=True)

            st.dataframe(nutrient_df)

        else:

            st.warning(f"No data available for {past_date}")

    else:

        st.warning("The 'Date' column is missing from the food log.")

    # 7-Day Average Calculation

    if len(df_summary) >= 7:

       if st.button("Show 7-Day Average"):

        last_7_days = df_summary.tail(7)

        avg_calories = last_7_days["Calories"].mean()

        avg_protein = last_7_days["Protein"].mean()

        avg_carbs = last_7_days["Carbs"].mean()

        avg_fat = last_7_days["Fat"].mean()



        avg_df = pd.DataFrame({

            "Nutrient": ["Calories", "Protein", "Carbs", "Fat"],

            "7-Day Average": [avg_calories, avg_protein, avg_carbs, avg_fat]

        })



        st.write("### 7-Day Average Nutrient Intake")

        st.dataframe(avg_df)



    # Perform One-Sample t-test only if there are at least 7 data points

    if len(df_summary) >= 7:

        # Perform one-sample t-test

        t_stat, p_value = stats.ttest_1samp(df_summary["Calories"].tail(7), target_calories)



        if p_value < 0.05:

            # Statistically significant result

            st.write("### Result: You’re not eating the right amount of calories—you’re either consuming too much or too little compared to your goal.")

        else:

            # Not statistically significant

            st.write("### Result: You are on the right track. Your calorie intake is not significantly different from your target.")



    





if __name__ == "__main__":

    run()
