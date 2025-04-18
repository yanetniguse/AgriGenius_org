import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables
soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
sprinkling = ctrl.Consequent(np.arange(0, 101, 1), 'sprinkling')

# Membership functions (Triangular)
soil_moisture['very_dry'] = fuzz.trimf(soil_moisture.universe, [0, 10, 20])
soil_moisture['dry'] = fuzz.trimf(soil_moisture.universe, [15, 30, 50])
soil_moisture['moist'] = fuzz.trimf(soil_moisture.universe, [40, 60, 80])
soil_moisture['wet'] = fuzz.trimf(soil_moisture.universe, [70, 90, 100])

temperature['cold'] = fuzz.trimf(temperature.universe, [0, 5, 15])
temperature['warm'] = fuzz.trimf(temperature.universe, [10, 20, 30])
temperature['hot'] = fuzz.trimf(temperature.universe, [25, 35, 50])

humidity['low'] = fuzz.trimf(humidity.universe, [0, 20, 40])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 80, 100])

sprinkling['low'] = fuzz.trimf(sprinkling.universe, [0, 20, 40])
sprinkling['medium'] = fuzz.trimf(sprinkling.universe, [30, 50, 70])
sprinkling['high'] = fuzz.trimf(sprinkling.universe, [60, 80, 100])

# Fuzzy rules
rule1 = ctrl.Rule(soil_moisture['very_dry'] & temperature['hot'], sprinkling['high'])
rule2 = ctrl.Rule(soil_moisture['dry'] & temperature['warm'], sprinkling['medium'])
rule3 = ctrl.Rule(soil_moisture['moist'] & temperature['cold'], sprinkling['low'])
rule4 = ctrl.Rule(humidity['low'] & soil_moisture['dry'], sprinkling['high'])
rule5 = ctrl.Rule(soil_moisture['wet'], sprinkling['low'])

# Control system
irrigation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
irrigation_simulation = ctrl.ControlSystemSimulation(irrigation_ctrl)

# Map user-friendly input descriptions to numeric values
soil_levels = {"Very Dry": 10, "Dry": 30, "Moist": 60, "Wet": 90}
temp_levels = {"Cold": 5, "Warm": 20, "Hot": 35}
humidity_levels = {"Low": 20, "Medium": 50, "High": 80}

def get_irrigation_recommendation(soil, temp, hum):
    try:
        # Handle both numeric & descriptive inputs
        soil_value = soil_levels.get(soil, soil if isinstance(soil, (int, float)) else None)
        temp_value = temp_levels.get(temp, temp if isinstance(temp, (int, float)) else None)
        hum_value = humidity_levels.get(hum, hum if isinstance(hum, (int, float)) else None)

        # Error handling: Check if inputs are valid
        errors = []
        if soil_value is None:
            errors.append("❌ Invalid Soil Moisture! Enter a value (0-100) or select a level.")
        if temp_value is None:
            errors.append("❌ Invalid Temperature! Enter a value (0-50°C) or select a level.")
        if hum_value is None:
            errors.append("❌ Invalid Humidity! Enter a value (0-100%) or select a level.")
        
        if errors:
            return "\n".join(errors)

        # Detect extreme conditions
        alerts = []
        if temp_value > 40:
            alerts.append("🔥 Temperature is extremely high! Consider shading your crops.")
        if soil_value < 15:
            alerts.append("⚠️ Soil is too dry! Increase watering frequency.")
        if hum_value > 90:
            alerts.append("💧 Humidity is too high! Reduce watering to prevent fungal growth.")

        # Compute recommendation
        irrigation_simulation.input['soil_moisture'] = soil_value
        irrigation_simulation.input['temperature'] = temp_value
        irrigation_simulation.input['humidity'] = hum_value
        irrigation_simulation.compute()
        
        sprinkling = round(irrigation_simulation.output['sprinkling'], 2)
        
        recommendation = f"💦 Recommended watering: {sprinkling}%."
        if sprinkling < 30:
            recommendation += " (Low watering needed.)"
        elif 30 <= sprinkling < 70:
            recommendation += " (Moderate watering required.)"
        else:
            recommendation += " (High watering necessary! Soil is too dry.)"

        # Suggest watering time for efficiency
        best_time = "🌅 Best time to water: Early morning or late afternoon to reduce evaporation."
        alerts.append(best_time)

        return recommendation + "\n" + "\n".join(alerts)

    except Exception as e:
        return f"⚠️ Error: {str(e)}. Please check your inputs and try again!"
