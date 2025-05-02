import numpy as np
import pandas as pd
from random import choices
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix


class HealthModel:
    def __init__(self, num_records=1000, start_date=None):
        self.num_records = num_records
        if not start_date:
            start_date = datetime.now() - timedelta(days=self.num_records + 1)
        self.start_date = start_date

    def generate_seasonal_trends(self, days_from_start):
        """Generate trends for temperature, humidity, and moisture based on seasons and time of day."""
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

        humidity_base = 60 + 20 * np.sin(2 * np.pi * (days_from_start % 24) / 24)
        moisture_base = 50 + 30 * np.sin(2 * np.pi * (days_from_start % 24) / 24)
        moisture_base = min(max(moisture_base, 20), 80)
        ph_base = 6.5 + 0.5 * np.sin(2 * np.pi * (days_from_start % 30) / 30)

        return temp_base, humidity_base, moisture_base, ph_base

    def simulate_yellowing(self, temp, humidity, moisture, ph):
        """Simulate leaf yellowing based on sensor readings."""
        yellowing_probability = 0
        if temp > 30:
            yellowing_probability += 0.3
        if humidity < 50:
            yellowing_probability += 0.3
        if moisture < 30:
            yellowing_probability += 0.4
        if ph < 6 or ph > 7:
            yellowing_probability += 0.2

        yellowing_probability = min(yellowing_probability, 1.0)  # Limit to 1.0
        return choices([0, 1], weights=[1 - yellowing_probability, yellowing_probability])[0]

    def generate_data(self):
        """Generate synthetic data with trends for the given number of records."""
        data = []
        current_date = self.start_date
        for record_id in range(self.num_records):
            days_from_start = record_id
            temp, humidity, moisture, ph = self.generate_seasonal_trends(days_from_start)
            yellowing = self.simulate_yellowing(temp, humidity, moisture, ph)

            entry = {
                'timestamp': current_date,
                'temperature': temp,
                'humidity': humidity,
                'moisture': moisture,
                'ph': ph,
                'yellowing': yellowing
            }
            data.append(entry)

            current_date += timedelta(days=1)

        return pd.DataFrame(data)


# Model training and evaluation
if __name__ == '__main__':
    health_model = HealthModel(num_records=10000)

    # Generate data (excluding 'timestamp' column for model)
    data = health_model.generate_data()

    # Feature columns (excluding 'timestamp' and 'yellowing')
    X = data.drop(columns=['timestamp', 'yellowing'])

    # Target column (yellowing status)
    y = data['yellowing']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize XGBoost model
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

    # Evaluate the model on the test set
    y_pred = xgb_model.predict(X_test)

    # Print accuracy and classification report
    print("Test Accuracy:", xgb_model.score(X_test, y_test))
    print("Test Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
