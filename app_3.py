# app_3.py
import streamlit as st
print("Streamlit está instalado correctamente.")
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trained model, scaler, and features
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
features = joblib.load('features.pkl')

# Load the dataset
data_final = pd.read_csv('data_final.csv')  

# Convert 'time spent' to total seconds if it's in timedelta format
if data_final['time_spent'].dtype == 'object':
    data_final['time_spent'] = pd.to_timedelta(data_final['time_spent']).dt.total_seconds()

# Get unique categories
unique_genders = data_final['gender'].unique().tolist()
unique_workout_types = data_final['workout_type'].unique().tolist()
unique_gym_types = data_final['gym_type'].unique().tolist()
unique_user_locations = data_final['user_location'].unique().tolist()

# Sidebar menu with image
st.sidebar.image('Imagen_menu.png', use_column_width=True)
menu = st.sidebar.radio('Menu', ['Project Description', 'Visualizations', 'Active User Prediction', 'New User Prediction'])

# Main image and title
st.title('CatFitAI')
st.image('CatFit.png', use_column_width=True)


if menu == 'Project Description':
    st.title('Project Description 📚')
    st.write("""
    This project aims to predict user retention in a gym. 
    It uses historical user data, including demographic information, types of activities performed, 
    and subscription data to train a machine learning model that can predict whether a user will be retained or not.
    
    ### Objectives:
    - **Predict User Retention**: Use historical data to predict if a user will continue using the gym services.
    - **Provide Insights**: Offer insights into user behavior and preferences.
    - **Improve Retention Strategies**: Suggest activities to users who are at risk of leaving to improve retention rates.
    """)

elif menu == 'Visualizations':
    st.title('Visualizations 📊')
    st.write("""
    In this section, we provide various visualizations to help understand the data better. 
    These visualizations can offer insights into user behavior, preferences, and trends.
    """)

    # Select visualizations to display
    visualizations = st.multiselect(
        'Select visualizations to display',
        ['Gender Distribution', 'Age Distribution', 'User Location', 'Gym Type', 'Time Spent in Gym', 'Subscription Type']
    )

    if 'Gender Distribution' in visualizations:
        st.subheader('Gender Distribution')
        gender_counts = data_final['gender'].value_counts()
        plt.figure(figsize=(8, 6))
        plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        st.pyplot(plt)

    if 'Age Distribution' in visualizations:
        st.subheader('Age Distribution')
        age_bins = [18, 30, 45, 60, 100]
        age_labels = ['18-30', '30-45', '45-60', '60+']
        data_final['age_group'] = pd.cut(data_final['age'], bins=age_bins, labels=age_labels, right=False)
        plt.figure(figsize=(10, 6))
        sns.countplot(data=data_final, x='age_group', palette='viridis')
        plt.title('Age Distribution')
        plt.xlabel('Age Group')
        plt.ylabel('Count')
        st.pyplot(plt)

    if 'User Location' in visualizations:
        st.subheader('User Location')
        plt.figure(figsize=(10, 6))
        sns.countplot(data=data_final, x='user_location', palette='viridis')
        plt.title('User Location Distribution')
        plt.xlabel('User Location')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    if 'Gym Type' in visualizations:
        st.subheader('Gym Type')
        plt.figure(figsize=(10, 6))
        sns.countplot(data=data_final, x='gym_type', palette='viridis')
        plt.title('Gym Type Distribution')
        plt.xlabel('Gym Type')
        plt.ylabel('Count')
        st.pyplot(plt)

    if 'Time Spent in Gym' in visualizations:
        st.subheader('Time Spent in Gym')
        time_bins = [0, 1800, 3600, 5400, 7200, 9000]
        time_labels = ['0-30 min', '30-60 min', '60-90 min', '90-120 min', '120-150 min']
        data_final['time_spent_bins'] = pd.cut(data_final['time_spent'], bins=time_bins, labels=time_labels)
        plt.figure(figsize=(10, 6))
        sns.countplot(data=data_final, x='time_spent_bins', palette='viridis')
        plt.title('Time Spent in Gym')
        plt.xlabel('Time Spent (minutes)')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    if 'Subscription Type' in visualizations:
        st.subheader('Subscription Type')
        plt.figure(figsize=(10, 6))
        sns.countplot(data=data_final, x='subscription_plan', palette='viridis')
        plt.title('Subscription Plan Distribution')
        plt.xlabel('Subscription Plan')
        plt.ylabel('Count')
        st.pyplot(plt)

elif menu == 'Active User Prediction':
    st.title('Active User Prediction 🔍')
    st.write("""
    In this section, you can select an existing user from the gym and predict whether they will be retained or not. 
    If the prediction is that the user will not be retained, we will suggest alternative activities they might enjoy.
    """)

    # Select user
    user_id = st.selectbox('Select User ID', data_final['user_id'].unique())

    # Get user data
    user_data = data_final[data_final['user_id'] == user_id].copy()

    # Display user statistics
    st.subheader('User Statistics')
    st.write(user_data)

    # Prepare input data for prediction
    # Ensure all columns are present
    for col in features:
        if col not in user_data.columns:
            user_data.loc[:, col] = 0

    # Ensure the columns are in the correct order
    input_data = user_data[features]

    # Scale the input data
    input_scaled = scaler.transform(input_data)

    # Make predictions
    if st.button('Predict'):
        prediction = model.predict(input_scaled)
        prediction_proba = model.predict_proba(input_scaled)
        
        if prediction[0]:
            st.write("Prediction: Retained ✅")
            st.write("The model predicts that the user will be retained. This means that the user is likely to continue using the gym services based on the provided data.")
        else:
            st.write("Prediction: Not Retained ❌")
            st.write("The model predicts that the user will not be retained. This means that the user is likely to stop using the gym services based on the provided data.")
            
            # Recommend alternative activities
            current_workout = user_data['workout_type'].values[0]
            similar_users = data_final[(data_final['age'] == user_data['age'].values[0]) &
                                       (data_final['gender'] == user_data['gender'].values[0]) &
                                       (data_final['gym_type'] == user_data['gym_type'].values[0]) &
                                       (data_final['user_location'] == user_data['user_location'].values[0])]
            alternative_workouts = similar_users['workout_type'].value_counts().index.tolist()
            alternative_workouts = [wt for wt in alternative_workouts if wt != current_workout][:3]
            
            st.write("To improve retention, consider suggesting the following activities:")
            st.write(", ".join(alternative_workouts))
            
            # Recommend loyalty bonus if the user is old
            sign_up_date = pd.to_datetime(user_data['sign_up_date'].values[0])
            if (pd.Timestamp.now() - sign_up_date).days > 365:
                st.write("As a loyal customer, we would like to offer you a special discount on your next subscription renewal!")


elif menu == 'New User Prediction':
    st.title('New User Prediction 🆕')
    st.write("""
    In this section, you can input the details of a new user and predict whether they will be retained or not. 
    This can help in understanding the likelihood of retention for new users based on their profile.
    """)

    # Input fields
    age = st.number_input('Age', min_value=0, max_value=100, value=30)
    calories_burned = st.number_input('Calories Burned', min_value=0, value=500)
    price_per_month = st.number_input('Price per Month', min_value=0.0, value=49.99)
    time_spent_minutes = st.number_input('Time Spent (minutes)', min_value=0, value=60)

    # Convert time spent from minutes to seconds
    time_spent = time_spent_minutes * 60

    # Categorical inputs
    gender = st.selectbox('Gender', unique_genders)
    workout_type = st.selectbox('Workout Type', unique_workout_types)
    gym_type = st.selectbox('Gym Type', unique_gym_types)
    user_location = st.selectbox('User Location', unique_user_locations)

    # Create a dictionary for the input data
    input_data = {
        'age': [age],
        'calories_burned': [calories_burned],
        'price_per_month': [price_per_month],
        'time spent': [time_spent],
        f'gender_{gender}': [1],
        f'workout_type_{workout_type}': [1],
        f'gym_type_{gym_type}': [1],
        f'user_location_{user_location}': [1]
    }

    # Ensure all columns are present
    for col in features:
        if col not in input_data:
            input_data[col] = [0]

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame(input_data)

    # Ensure the columns are in the correct order
    input_df = input_df[features]

    # Scale the input data
    input_scaled = scaler.transform(input_df)

    # Make predictions
    if st.button('Predict'):
        prediction = model.predict(input_scaled)
        prediction_proba = model.predict_proba(input_scaled)
        
        if prediction[0]:
            st.write("Prediction: Retained ✅")
            st.write("The model predicts that the user will be retained. This means that the user is likely to continue using the gym services based on the provided data.")
        else:
            st.write("Prediction: Not Retained ❌")
            st.write("The model predicts that the user will not be retained. This means that the user is likely to stop using the gym services based on the provided data.")
        
        