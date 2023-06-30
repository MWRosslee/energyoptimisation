import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Load data from CSV files
inverter_data = pd.read_csv('inverter.csv')
weather_data = pd.read_csv('weather.csv')
forecast_data = pd.read_csv('forecast.csv')

# Combine inverter and weather data based on a common column (e.g., date)
combined_data = pd.merge(inverter_data, weather_data, on='date')

# Check if 'grid_connected' column exists in the combined_data DataFrame
if 'grid_connected' not in combined_data.columns:
    print("Error: 'grid_connected' column does not exist in the combined data.")
    exit()

# Extract the relevant features for training the model
features = combined_data[['power_generation', 'battery_level', 'cloud_cover', 'rainfall']]

# Extract the target variable for training the model
target = combined_data['grid_connected']

# Check if there are enough samples for training
if len(features) < 10 or len(target) < 10:
    print("Error: Insufficient data for training the model.")
    exit()

# Sample a smaller dataset for training
sample_size = 100  # Adjust this value to specify the desired sample size
sampled_data = combined_data.sample(n=sample_size, random_state=42)

# Split the sampled data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    sampled_data[['power_generation', 'battery_level', 'cloud_cover', 'rainfall']],
    sampled_data['grid_connected'],
    test_size=0.2,
    random_state=42
)

# Initialize the models
models = {
    'Random Forest': RandomForestClassifier(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Support Vector Machines': SVC()
}

# Train and evaluate different models
for model_name, model in models.items():
    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"{model_name} accuracy: {accuracy}")

    # Use the trained model to make predictions on the forecast data
    forecast_features = forecast_data[['power_generation', 'battery_level', 'cloud_cover', 'rainfall']]
    predictions = model.predict(forecast_features)

    # Generate recommendations based on the predictions
    for index, prediction in enumerate(predictions):
        if prediction == 1:
            print(f"For date {forecast_data['date'][index]}: It is recommended to charge from the grid.")
        else:
            print(f"For date {forecast_data['date'][index]}: It is recommended to run off battery power or solely run from the grid.")
    print("-" * 50)
