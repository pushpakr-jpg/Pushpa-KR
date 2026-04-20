from sklearn.tree import DecisionTreeClassifier
import numpy as np

def predict_switches(pv_irradiance, loadcontrol_switch):
    # Define the dataset based on the logic
    X = [
        [400, 1],  # pv_irradiance < 400, loadcontrol_switch = 0
        [400, 0],  # pv_irradiance < 400, loadcontrol_switch = 1
        [401, 1],  # pv_irradiance > 400, loadcontrol_switch = 0
        [401, 0],  # pv_irradiance > 400, loadcontrol_switch = 1
    ]

    # Each output is a tuple (pv, grid, central)
    y = [
        [0, 1, 0],  # Output for pv_irradiance < 400
        [0, 1, 0],  # Output for pv_irradiance < 400
        [1, 0, 0],  # Output for pv_irradiance > 400, loadcontrol_switch = 0
        [1, 0, 1],  # Output for pv_irradiance > 400, loadcontrol_switch = 1
    ]

    # Create and train the model using decision tree
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # model is predicting 3 switch state (output) based on pv_voltage and loadcontrol_switch (input)
    prediction = model.predict([[pv_irradiance, loadcontrol_switch]])

    pv_switch, grid_switch, central_switch = map(int, prediction[0])
    print(pv_switch, grid_switch, central_switch)

    return pv_switch, grid_switch, central_switch


# predict_switches(pv_irradince=500, loadcontrol_switch=1)
