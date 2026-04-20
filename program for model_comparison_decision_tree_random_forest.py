import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score
import numpy as np
import time

# Load data
df = pd.read_excel('updated_data.xlsx')

# Apply conditions and preprocessing 
def apply_conditions(row):
    pv_irraidace = row['PV_irradiance']
    load1 = row['Load1']
    load2 = row['Load2']
        
    # Initialize new columns
    pv_switch = 'OFF'
    central_switch = 'OFF'
    grid_switch = 'OFF'
    load1_new = load1
    load2_new = load2

    # Condition 1
    if pv_irradiance < 400 and load1 == 'OFF' and load2 == 'OFF':
        pv_switch = 'OFF'
        central_switch = 'OFF'
        grid_switch = 'ON'
        load1_new = 'ON'
        load2_new = 'ON'
    
    # Condition 2
    elif pv_irradiance > 400 and pv_irradiance < 700 and load1 == 'ON' and load2 == 'OFF':
        pv_switch = 'ON'
        central_switch = 'OFF'
        grid_switch = 'OFF'
        load1_new = load1
        load2_new = load2
    
    # Condition 3
    elif pv_irradiance > 800 and load1 == 'ON' and load2 == 'ON':
        pv_switch = 'ON'
        central_switch = 'OFF'
        grid_switch = 'OFF'
        load1_new = load1
        load2_new = load2
    
    # Condition 4
    elif pv_irradiance > 800 and load1 == 'ON' and load2 == 'OFF':
        pv_switch = 'ON'
        central_switch = 'ON'
        grid_switch = 'OFF'
        load1_new = load1
        load2_new = load2

    return pd.Series([pv_switch, central_switch, grid_switch, load1_new, load2_new])

df[['pv_switch', 'central_switch', 'grid_switch', 'load1_new', 'load2_new']] = df.apply(apply_conditions, axis=1)

# Convert categorical columns to numerical values
df['Load1'] = df['Load1'].map({'OFF': 0, 'ON': 1})
df['Load2'] = df['Load2'].map({'OFF': 0, 'ON': 1})
df['load1_new'] = df['load1_new'].map({'OFF': 0, 'ON': 1})
df['load2_new'] = df['load2_new'].map({'OFF': 0, 'ON': 1})
df['pv_switch'] = df['pv_switch'].map({'OFF': 0, 'ON': 1})
df['central_switch'] = df['central_switch'].map({'OFF': 0, 'ON': 1})
df['grid_switch'] = df['grid_switch'].map({'OFF': 0, 'ON': 1})

# Features for prediction
X = df[['PV_irradiance', 'Load1', 'Load2']]
y = df['load1_new']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize models
dt_model = DecisionTreeClassifier(random_state=42)
rf_model = RandomForestClassifier(random_state=42)

# Track runtime and metrics for Decision Tree
start_time = time.time()
dt_model.fit(X_train, y_train)
dt_runtime = time.time() - start_time

dt_predictions = dt_model.predict(X_test)

# Calculate metrics for Decision Tree
dt_mse = mean_squared_error(y_test, dt_predictions)
dt_mae = mean_absolute_error(y_test, dt_predictions)
dt_rmse = np.sqrt(dt_mse)
dt_mape = np.mean(np.abs((y_test - dt_predictions) / y_test)) * 100
dt_r2 = r2_score(y_test, dt_predictions)
dt_accuracy = accuracy_score(y_test, dt_predictions)
dt_precision = precision_score(y_test, dt_predictions)
dt_recall = recall_score(y_test, dt_predictions)

# Track runtime and metrics for Random Forest
start_time = time.time()
rf_model.fit(X_train, y_train)
rf_runtime = time.time() - start_time

rf_predictions = rf_model.predict(X_test)

# Calculate metrics for Random Forest
rf_mse = mean_squared_error(y_test, rf_predictions)
rf_mae = mean_absolute_error(y_test, rf_predictions)
rf_rmse = np.sqrt(rf_mse)
rf_mape = np.mean(np.abs((y_test - rf_predictions) / y_test)) * 100
rf_r2 = r2_score(y_test, rf_predictions)
rf_accuracy = accuracy_score(y_test, rf_predictions)
rf_precision = precision_score(y_test, rf_predictions)
rf_recall = recall_score(y_test, rf_predictions)

# Prepare results for saving into Excel
results = pd.DataFrame({
    'Model': ['Decision Tree', 'Random Forest'],
    'MSE': [dt_mse, rf_mse],
    'MAE': [dt_mae, rf_mae],
    'RMSE': [dt_rmse, rf_rmse],
    'MAPE': [dt_mape, rf_mape],
    'R² Score': [dt_r2, rf_r2],
    'Accuracy': [dt_accuracy, rf_accuracy],
    'Precision': [dt_precision, rf_precision],
    'Recall': [dt_recall, rf_recall],
    'Runtime (seconds)': [dt_runtime, rf_runtime]
})

# Save results to Excel
results.to_excel('model_performance_metrics.xlsx', index=False)

print("Excel file with model metrics saved.")
