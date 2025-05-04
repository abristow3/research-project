import numpy as np
import pandas as pd
from random import choices
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os


class HealthModel:
    def __init__(self, num_records=1000, start_date=None, model_file='plant_health_xgb_model.pkl'):
        self.num_records = num_records
        self.model_file = model_file
        self.model = None  # Initialize model as None

        # Set start date if not provided
        if not start_date:
            start_date = datetime.now() - timedelta(days=self.num_records + 1)
        self.start_date = start_date

        # Check if model file exists, if not, generate data and train a new model
        if os.path.exists(self.model_file):
            self.setup()
        else:
            print(f"Model file {self.model_file} not found, generating data and training model...")
            data = self.generate_data()

            # Feature columns (excluding 'timestamp' and 'yellowing')
            X = data.drop(columns=['timestamp', 'yellowing'])
            y = data['yellowing']

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train the model
            self.train_model(X_train, y_train)

            # Evaluate the model
            self.evaluate_model(X_test, y_test)

    def setup(self):
        try:
            self.model = joblib.load(self.model_file)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")

    def train_model(self, X_train, y_train):
        xgb_model = XGBClassifier(
            colsample_bytree=0.8,
            learning_rate=0.01,
            max_depth=5,
            min_child_weight=1,
            n_estimators=200,
            subsample=0.8,
            scale_pos_weight=3  # Adjust for class imbalance
        )
        # Train the model
        xgb_model.fit(X_train, y_train)
        # Save the trained model
        joblib.dump(xgb_model, self.model_file)
        print(f"Model trained and saved as {self.model_file}.")
        self.model = xgb_model

    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model."""
        y_pred = self.model.predict(X_test)

        # Print evaluation results
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def generate_seasonal_trends(self, days_from_start):
        season = (days_from_start // 30) % 4  # Rough seasonal cycle based on 30-day months
        time_of_day = np.sin(2 * np.pi * (days_from_start % 24) / 24)  # Sine wave for daily temperature fluctuation

        if season == 0:  # Spring
            temp_base = 15 + 10 * time_of_day
        elif season == 1:  # Summer
            temp_base = 25 + 10 * time_of_day
        elif season == 2:  # Fall
            temp_base = 20 + 10 * time_of_day
        else:  # Winter
            temp_base = 10 + 10 * time_of_day

        # Humidity: 40% to 90%, higher humidity in morning and lower in afternoon
        humidity_base = 60 + 20 * np.sin(2 * np.pi * (days_from_start % 24) / 24)

        # Soil moisture: More wet after rain, drier in the afternoon
        moisture_base = 50 + 30 * np.sin(2 * np.pi * (days_from_start % 24) / 24)
        moisture_base = min(max(moisture_base, 20), 80)

        # Classify moisture as binary: 1 for wet, 0 for dry
        moisture_class = 1 if moisture_base > 35 else 0

        # pH: Could range from 5.5 to 7.5 depending on soil
        ph_base = 6.5 + 0.5 * np.sin(2 * np.pi * (days_from_start % 30) / 30)

        return temp_base, humidity_base, moisture_class, ph_base

    def simulate_yellowing(self, temp, humidity, moisture, ph):
        yellowing_probability = 0
        if temp > 30:  # Heat stress
            yellowing_probability += 0.3
        if humidity < 50:  # Dry conditions
            yellowing_probability += 0.3
        if moisture == 0:  # Dry soil (binary moisture)
            yellowing_probability += 0.4
        if ph < 6 or ph > 7:  # Extreme pH conditions
            yellowing_probability += 0.2

        yellowing_probability = min(yellowing_probability, 1.0)  # Limit to 1.0
        return choices([0, 1], weights=[1 - yellowing_probability, yellowing_probability])[0]

    def generate_optimal_condition_data(self, num_points=100):
        data = []
        for i in range(num_points):
            # Extreme conditions that cause yellowing (optimal conditions for yellowing)
            temp, humidity, moisture, ph = 35, 40, 0, 6.5  # Wet soil (moisture = 1)
            yellowing = 1  # Yellowing detected
            timestamp = self.start_date + timedelta(days=i)
            data.append([timestamp, temp, humidity, moisture, ph, yellowing])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'humidity', 'moisture', 'ph', 'yellowing'])
        return df

    def generate_non_optimal_condition_data(self, num_points=100):
        data = []
        for i in range(num_points):
            # Non-optimal conditions (slightly adjusted features but yellowing occurs)
            temp, humidity, moisture, ph = 22, 70, 0, 6.5  # Dry soil (moisture = 0)
            yellowing = 1  # Yellowing detected
            timestamp = self.start_date + timedelta(days=i)
            data.append([timestamp, temp, humidity, moisture, ph, yellowing])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'humidity', 'moisture', 'ph', 'yellowing'])
        return df

    def generate_data(self):
        data = []
        current_date = self.start_date
        for record_id in range(self.num_records):
            days_from_start = record_id
            temp, humidity, moisture, ph = self.generate_seasonal_trends(days_from_start)
            yellowing = self.simulate_yellowing(temp, humidity, moisture, ph)

            # Prepare the data entry
            entry = {
                'timestamp': current_date,
                'temperature': temp,
                'humidity': humidity,
                'moisture': moisture,
                'ph': ph,
                'yellowing': yellowing
            }
            data.append(entry)

            # Increment the current date by one day
            current_date += timedelta(days=1)

        return pd.DataFrame(data)

    def test_model(self, optimal_points=100, non_optimal_points=100):
        # Generate optimal and non-optimal condition data for prediction
        optimal_data = self.generate_optimal_condition_data(num_points=optimal_points)
        non_optimal_data = self.generate_non_optimal_condition_data(num_points=non_optimal_points)

        # Concatenate optimal and non-optimal data for prediction
        full_data = pd.concat([optimal_data, non_optimal_data])

        # Feature columns (excluding 'timestamp' and 'yellowing')
        X_pred = full_data.drop(columns=['timestamp', 'yellowing'])

        # Target column (yellowing status)
        y_pred_actual = full_data['yellowing']

        # Predict on the generated data using the loaded model
        predictions = self.model.predict(X_pred)

        # Count correct predictions for optimal and non-optimal data
        correct_optimal_predictions = sum(
            pred == actual for pred, actual in zip(predictions[:optimal_points], y_pred_actual[:optimal_points]))
        correct_non_optimal_predictions = sum(
            pred == actual for pred, actual in zip(predictions[optimal_points:], y_pred_actual[optimal_points:]))

        # Print the results
        print(f"Correct Predictions for Optimal Conditions: {correct_optimal_predictions}/{optimal_points}")
        print(f"Correct Predictions for Non-Optimal Conditions: {correct_non_optimal_predictions}/{non_optimal_points}")

    def predict_disease(self, entry):
        # Convert the entry dict into a pandas DataFrame for model prediction
        df = pd.DataFrame([entry])

        print(f"DF: {df}")

        # Drop the 'timestamp' and 'yellowing' columns for prediction
        X_pred = df.drop(columns=['timestamp', 'yellowing', 'image_name'])

        # Predict yellowing using the model
        predicted_yellowing = self.model.predict(X_pred)[0]  # Get the prediction for this entry

        # If the model predicts no yellowing, but the actual yellowing value is 1,
        # and environmental conditions are optimal (we define them as non-stressful), it's likely due to disease.
        if predicted_yellowing == 0 and entry['yellowing'] == 1:
            # Check if the environmental conditions are optimal (non-stressful)
            temp, humidity, moisture, ph = entry['temperature'], entry['humidity'], entry['moisture'], entry['ph']
            if self.is_optimal_conditions(temp, humidity, moisture, ph):
                return 1  # Likely disease, as environmental conditions are optimal, but yellowing still occurs.

        return 0  # No disease, either because the model predicts yellowing or because conditions are not optimal.

    def is_optimal_conditions(self, temp, humidity, moisture, ph):
        # Optimal conditions (e.g., ranges for healthy plant conditions)
        optimal_temp_range = (20, 30)  # Temperature between 20°C and 30°C
        optimal_humidity_range = (50, 80)  # Humidity between 50% and 80%
        optimal_moisture = 1  # Moisture between 30% and 70%
        optimal_ph_range = (6.0, 7.5)  # pH between 6.0 and 7.5

        # Check if the conditions fall within the optimal ranges
        if (optimal_temp_range[0] <= temp <= optimal_temp_range[1] and
                optimal_humidity_range[0] <= humidity <= optimal_humidity_range[1] and
                optimal_moisture == 1 and optimal_ph_range[0] <= ph <= optimal_ph_range[1]):
            print("OPTIMAL")
            return True  # The conditions are optimal
        print("NOT OPTIMAL")
        return False  # The conditions are not optimal

# if __name__ == '__main__':
#     health_model = HealthModel()
#
#     optimal_entry = {
#         'timestamp': datetime.now(),
#         'temperature': 22,
#         'humidity': 70,
#         'moisture': 1,
#         'ph': 7,
#         'yellowing': 1
#     }
#
#     disease_detected = health_model.predict_disease(entry=optimal_entry)
#
#     print(disease_detected)
#     if disease_detected:
#         print("DISEASE DETECTED")
