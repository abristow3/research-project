### Breakdown of the Simulation Data Generation

In this project, we aim to simulate data that reflects the environmental conditions of a miniature fig tree, based on sensor readings, and to predict whether the tree’s leaves will exhibit yellowing due to those conditions. The simulation data mimics real-world environmental factors such as temperature, humidity, soil moisture, and pH levels, which are common variables for monitoring plant health. Below is a step-by-step breakdown of how this simulated data is generated:

#### 1. **Understanding the Key Environmental Factors**

The four main environmental factors that we simulate data for are:

* **Temperature**: How hot or cold the environment is. Extreme temperatures can stress plants, leading to leaf yellowing.
* **Humidity**: The amount of moisture in the air. Low humidity can lead to dehydration of plants, contributing to stress and yellowing.
* **Soil Moisture**: The amount of water in the soil. Too little moisture can cause the plant to dry out, leading to yellowing of leaves.
* **Soil pH**: The acidity or alkalinity of the soil. A pH outside of the optimal range for a plant can cause stress and negatively affect plant health.

#### 2. **Simulating Seasonal Trends**

The simulation includes seasonal variations, where the environmental conditions change depending on the time of year. The following seasonal patterns are used to make the simulated data more realistic:

* **Spring**: Mild temperatures with moderate swings during the day, and moderate humidity.
* **Summer**: Warmer temperatures with larger fluctuations between day and night, and lower humidity.
* **Fall**: Temperatures are cooler than summer, but still fluctuate. The humidity rises again.
* **Winter**: Cooler temperatures with less fluctuation, and higher humidity.

These seasonal changes are represented by a **sinusoidal pattern**. Sinusoidal functions mimic natural fluctuations, like how temperature or humidity rises and falls throughout the day or across the seasons.

#### 3. **Daily Fluctuations**

Within each day, environmental factors also fluctuate due to time-of-day effects:

* **Temperature**: The temperature follows a daily fluctuation, where it’s cooler during the night and warms up during the day. This pattern is simulated using a sine wave.
* **Humidity**: The humidity is higher in the early morning and lower in the afternoon, mimicking natural diurnal changes.
* **Soil Moisture**: Moisture levels fluctuate over the course of the day, being higher in the morning when the soil is still moist from overnight and lower during the afternoon as the soil dries out.

#### 4. **Calculating Environmental Factors**

Each of the four environmental factors is calculated for each day in the simulation. Here's how they are derived:

* **Temperature**: It’s based on a sine wave function where the base temperature is adjusted according to the season, and a sine wave modifies it to simulate daily fluctuation. The ranges are adjusted for each season:

  * **Spring**: 15°C average, ±10°C swing
  * **Summer**: 25°C average, ±10°C swing
  * **Fall**: 20°C average, ±10°C swing
  * **Winter**: 10°C average, ±10°C swing

* **Humidity**: The humidity follows a sinusoidal fluctuation throughout the day (higher in the morning and lower in the afternoon). The range of humidity is kept between **40% and 90%**. The values fluctuate based on the time of day.

* **Soil Moisture**: This fluctuates in a sinusoidal pattern that ranges from **20% to 80%**. Higher moisture levels occur in the morning, while lower moisture levels are seen in the afternoon.

* **Soil pH**: The soil pH is modeled to vary between **5.5 and 7.5**, reflecting normal soil conditions. Like the other variables, it follows a cyclic fluctuation based on the time of year.

#### 5. **Simulating Leaf Yellowing**

Leaf yellowing is the result of stress caused by the environmental conditions. In the simulation, the probability of leaf yellowing is calculated based on certain thresholds for each environmental factor:

* **High temperature (over 30°C)** increases the likelihood of yellowing.
* **Low humidity (under 50%)** increases the chance of yellowing.
* **Low soil moisture (under 30%)** causes stress, leading to yellowing.
* **Extreme pH values (below 6 or above 7)** contribute to yellowing.

For each data point, a "yellowing probability" is computed, and based on that probability, the model randomly decides whether the leaves will yellow (1) or remain healthy (0). The probability is calculated by summing the individual contributions from each of the above factors, which are then weighted appropriately.

#### 6. **Data Generation Over Time**

The simulation is set to run for a specific number of records (for example, 10,000 records). Each record corresponds to a unique day in the simulation. For each day, the following steps happen:

1. **Seasonal trends and daily fluctuations** for temperature, humidity, soil moisture, and pH are calculated based on the number of days passed since the start of the simulation.
2. **The yellowing probability** is determined based on the simulated environmental conditions for that day.
3. **A data entry** is created, which includes:

   * **Timestamp**: The current date.
   * **Temperature**: The calculated temperature for that day.
   * **Humidity**: The calculated humidity for that day.
   * **Soil Moisture**: The simulated soil moisture for that day.
   * **Soil pH**: The simulated pH for that day.
   * **Yellowing**: The result of whether the leaves are yellowing (1) or healthy (0) based on the yellowing probability.

This process is repeated for the desired number of records.

#### 7. **Final Output**

The generated data is stored as a pandas DataFrame and is ready for use in training machine learning models. The features include the environmental conditions, while the target variable is whether the leaves are yellowing or not.

### Conclusion

The simulated data reflects real-world trends by incorporating seasonal changes, daily fluctuations, and realistic relationships between environmental factors and plant health. By simulating data in this way, the model can be trained to predict leaf yellowing based on temperature, humidity, moisture, and pH, helping to automate the detection of plant stress in real-time systems.
